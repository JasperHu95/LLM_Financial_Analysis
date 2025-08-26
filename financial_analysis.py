import os
import re
import csv
import json
import requests
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime

# DeepSeek API configuration parameters
# TODO: Please replace with your own DeepSeek API Key
DEEPSEEK_API_KEY = "your_api_key_here"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# US GAAP compliant financial metric categories for extraction
US_GAAP_FINANCIAL_METRICS = [
    "revenue_growth",           # Revenue growth projections
    "capital_expenditure",      # Capital expenditure forecasts
    "earnings_per_share",       # Earnings per share projections
    "gross_margin",             # Gross margin projections
    "operating_margin",         # Operating margin projections
    "net_margin",               # Net margin projections
    "ebitda",                   # EBITDA projections
    "return_on_equity",         # Return on equity projections
    "return_on_assets",         # Return on assets projections
    "debt_to_equity_ratio",     # Debt to equity ratio projections
    "current_ratio",            # Current ratio projections
    "quick_ratio",              # Quick ratio projections
    "interest_coverage_ratio",  # Interest coverage ratio projections
    "price_to_earnings_ratio",  # Price to earnings ratio projections
    "dividend_yield"            # Dividend yield projections
]


def extract_company_info_from_filename(filename: str) -> Dict[str, str]:

    # Parse filename to extract company information
    pattern = r"(\d{4})-(\w{3})-(\d{2})-(.+?)\.([A-Z]+)-"
    match = re.search(pattern, filename)
    
    if match:
        year = match.group(1)
        month = match.group(2)
        day = match.group(3)
        ticker = match.group(4)
        exchange = match.group(5)
        
        return {
            "year": year,
            "month": month,
            "day": day,
            "ticker": ticker,
            "exchange": exchange,
            "filename": filename
        }
    
    # Return minimal metadata if parsing fails
    return {"filename": filename, "year": "", "month": "", "day": "", 
            "ticker": "", "exchange": ""}


def call_deepseek_api(text: str) -> Dict[str, Any]:
    """
    Invoke DeepSeek LLM API to extract forward-looking financial statements from earnings call transcripts.
    Implements structured prompting for financial information extraction with specific formatting requirements.
    """
    
    prompt = f"""Act as a financial analysis engine specialized in extracting forward-looking statements from earnings call transcripts.
Ensure all extracted financial metrics conform to US GAAP standards and terminology.

Target financial categories for extraction:
1. Revenue growth projections (absolute values and percentages)
2. Capital expenditure forecasts
3. Earnings per share projections
4. Gross margin projections
5. Operating margin projections
6. Net margin projections
7. EBITDA projections
8. Return on equity projections
9. Return on assets projections
10. Debt to equity ratio projections
11. Current ratio projections
12. Quick ratio projections
13. Interest coverage ratio projections
14. Price to earnings ratio projections
15. Dividend yield projections

Extraction specifications:
1. Extract only future period statements (e.g., for 2023 transcript, extract 2024+, not historical data)
2. Perform full context analysis of the transcript
3. Numerical value extraction requirements:
   - Extract ONLY pure numerical values, removing ALL text modifiers like "approximately", "over", "about", "around"
   - For percentage ranges (e.g., "2%-5%"), calculate midpoint with correct sign (-3.5% for decline range)
   - For "over X%" or "above X", record as X%
   - For "under X%" or "below X", record as X%
   - Remove ALL currency symbols and comma separators ("$1,000" → "1000")
   - Standardize monetary units to pure numbers:
     * "X million" → X * 1,000,000 (e.g., "150 million" → "150000000")
     * "X billion" → X * 1,000,000,000 (e.g., "2.5 billion" → "2500000000")
     * "X thousand" → X * 1,000 (e.g., "500 thousand" → "500000")
   - Preserve sign semantics:
     * Growth/increase/positive outlook: positive values (e.g., "increase by 5%" → "5%")
     * Decline/decrease/negative outlook: negative values (e.g., "decrease by 8%" → "-8%")
     * For ranges with decline semantics, ensure correct negative sign (e.g., "decrease by 2%-5%" → "-3.5%")
   - For percentages, ALWAYS include the % symbol (e.g., "28%" not "28")
   - For ratio metrics, record ONLY the numerical value (e.g., "1.5 to 1" → "1.5")
   - When no specific numerical value is provided, leave the field empty

Response format specification:
{{
  "forward_looking_statements": [
    {{
      "category": "revenue_growth|capital_expenditure|earnings_per_share|gross_margin|operating_margin|net_margin|ebitda|return_on_equity|return_on_assets|debt_to_equity_ratio|current_ratio|quick_ratio|interest_coverage_ratio|price_to_earnings_ratio|dividend_yield",
      "sentence": "complete sentence containing forward-looking information",
      "revenue_growth": "numerical value if revenue growth mentioned (include % for percentages with correct sign)",
      "capital_expenditure": "numerical value if capex mentioned (no currency symbols)",
      "earnings_per_share": "numerical value if EPS mentioned",
      "gross_margin": "numerical value if gross margin mentioned (include % for percentages with correct sign)",
      "operating_margin": "numerical value if operating margin mentioned (include % for percentages with correct sign)",
      "net_margin": "numerical value if net margin mentioned (include % for percentages with correct sign)",
      "ebitda": "numerical value if EBITDA mentioned (no currency symbols)",
      "return_on_equity": "numerical value if ROE mentioned (include % for percentages with correct sign)",
      "return_on_assets": "numerical value if ROA mentioned (include % for percentages with correct sign)",
      "debt_to_equity_ratio": "numerical value if debt to equity ratio mentioned",
      "current_ratio": "numerical value if current ratio mentioned",
      "quick_ratio": "numerical value if quick ratio mentioned",
      "interest_coverage_ratio": "numerical value if interest coverage ratio mentioned",
      "price_to_earnings_ratio": "numerical value if P/E ratio mentioned",
      "dividend_yield": "numerical value if dividend yield mentioned (include % for percentages with correct sign)",
      "speaker": "identified speaker if available"
    }}
  ]
}}

Transcript content for analysis:
{text[:20000]}
"""

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a specialized financial analysis engine. Return only valid JSON in the specified format. For percentage values, ALWAYS include the % symbol and correct sign. For ranges, calculate the midpoint with correct sign. Use only US GAAP compliant financial metric names."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 2000
    }
    
    try:
        # Execute API request with 60-second timeout
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            # Extract JSON from response using regex
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {"forward_looking_statements": []}
        
    except requests.exceptions.RequestException as e:
        print(f"API request failure: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
    
    return {"forward_looking_statements": []}


def process_transcript_file(file_path: str, output_csv_path: str):
    """
    Process individual transcript file and extract forward-looking financial statements.
    
    Args:
        file_path (str): Path to transcript file
        output_csv_path (str): Path to output CSV file
    """
    
    # Extract metadata from filename
    filename = os.path.basename(file_path)
    company_info = extract_company_info_from_filename(filename)
    
    print(f"Processing transcript: {filename}")
    
    try:
        # Load transcript content
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            transcript_text = file.read()
        
        # Extract forward-looking statements via API
        api_result = call_deepseek_api(transcript_text)
        
        # Prepare CSV output data
        csv_data = []
        for statement in api_result.get("forward_looking_statements", []):
            row = {
                **company_info,
                "financial_category": statement.get("category", ""),
                "forward_looking_sentence": statement.get("sentence", ""),
                "revenue_growth": statement.get("revenue_growth", ""),
                "capital_expenditure": statement.get("capital_expenditure", ""),
                "earnings_per_share": statement.get("earnings_per_share", ""),
                "gross_margin": statement.get("gross_margin", ""),
                "operating_margin": statement.get("operating_margin", ""),
                "net_margin": statement.get("net_margin", ""),
                "ebitda": statement.get("ebitda", ""),
                "return_on_equity": statement.get("return_on_equity", ""),
                "return_on_assets": statement.get("return_on_assets", ""),
                "debt_to_equity_ratio": statement.get("debt_to_equity_ratio", ""),
                "current_ratio": statement.get("current_ratio", ""),
                "quick_ratio": statement.get("quick_ratio", ""),
                "interest_coverage_ratio": statement.get("interest_coverage_ratio", ""),
                "price_to_earnings_ratio": statement.get("price_to_earnings_ratio", ""),
                "dividend_yield": statement.get("dividend_yield", ""),
                "speaker": statement.get("speaker", ""),
                "extraction_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            csv_data.append(row)
        
        # Append results to CSV output
        file_exists = os.path.exists(output_csv_path)
        
        with open(output_csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'year', 'month', 'day', 'ticker', 'exchange', 'filename',
                'financial_category', 'forward_looking_sentence',
                'revenue_growth', 'capital_expenditure', 'earnings_per_share',
                'gross_margin', 'operating_margin', 'net_margin', 'ebitda',
                'return_on_equity', 'return_on_assets', 'debt_to_equity_ratio',
                'current_ratio', 'quick_ratio', 'interest_coverage_ratio',
                'price_to_earnings_ratio', 'dividend_yield',
                'speaker', 'extraction_date'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header for new files
            if not file_exists:
                writer.writeheader()
            
            writer.writerows(csv_data)
        
        print(f"Completed {filename}: Extracted {len(csv_data)} statements")
        
    except Exception as e:
        print(f"Error processing {filename}: {e}")


def process_all_transcripts(directory_path: str, output_csv_path: str):
    """
    Batch process all transcript files in specified directory.
    
    Args:
        directory_path (str): Directory containing transcript files
        output_csv_path (str): Path to output CSV file
    """
    
    # Validate directory existence
    if not os.path.exists(directory_path):
        print(f"Directory not found: {directory_path}")
        return
    
    # Enumerate transcript files
    transcript_files = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt') and 'Transcript' in filename:
            transcript_files.append(os.path.join(directory_path, filename))
    
    print(f"Located {len(transcript_files)} transcript files for processing")
    
    # Process files sequentially
    for i, file_path in enumerate(transcript_files, 1):
        print(f"\nProcessing file {i}/{len(transcript_files)}")
        process_transcript_file(file_path, output_csv_path)
        
        # Rate limiting delay
        import time
        time.sleep(5)


if __name__ == "__main__":
    # Configuration parameters
    TRANSCRIPT_DIR = r"data_source"
    OUTPUT_CSV = r"financial_information.csv"
    
    # Execute batch processing pipeline
    process_all_transcripts(TRANSCRIPT_DIR, OUTPUT_CSV)
    
    print(f"\nProcessing pipeline complete. Results saved to: {OUTPUT_CSV}")