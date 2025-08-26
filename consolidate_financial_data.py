import pandas as pd
import os
from collections import defaultdict

def consolidate_financial_data(input_file, output_file):
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Cannot find input file {input_file}")
        return
    
    # Read CSV file, handling encoding issues
    try:
        df = pd.read_csv(input_file, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(input_file, encoding='gbk')
        except UnicodeDecodeError:
            df = pd.read_csv(input_file, encoding='latin1')
    
    # Display basic information
    print(f"Original data shape: {df.shape}")
    print(f"Number of unique companies: {df['ticker'].nunique()}")
    
    # Create a dictionary to store records for each company-date combination
    consolidated_data = defaultdict(dict)
    
    # Iterate through each row of data
    for index, row in df.iterrows():
        # Create a unique key (based on company identifier and date)
        company_key = (
            str(row['ticker']) if pd.notna(row['ticker']) else '',
            str(row['year']) if pd.notna(row['year']) else '',
            str(row['month']) if pd.notna(row['month']) else '',
            str(row['day']) if pd.notna(row['day']) else '',
            str(row['exchange']) if pd.notna(row['exchange']) else ''
        )
        
        # If this key doesn't exist, initialize basic information
        if company_key not in consolidated_data:
            consolidated_data[company_key] = {
                'year': row['year'] if pd.notna(row['year']) else '',
                'month': row['month'] if pd.notna(row['month']) else '',
                'day': row['day'] if pd.notna(row['day']) else '',
                'ticker': row['ticker'] if pd.notna(row['ticker']) else '',
                'exchange': row['exchange'] if pd.notna(row['exchange']) else '',
                'filename': row['filename'] if pd.notna(row['filename']) else ''
            }
        
        # Get the financial category of the current row
        category = row['financial_category']
        
        # Add the financial indicator values of this row to the corresponding company-date record
        financial_fields = [
            'revenue_growth', 'capital_expenditure', 'earnings_per_share',
            'gross_margin', 'operating_margin', 'net_margin', 'ebitda',
            'return_on_equity', 'return_on_assets', 'debt_to_equity_ratio',
            'current_ratio', 'quick_ratio', 'interest_coverage_ratio',
            'price_to_earnings_ratio', 'dividend_yield'
        ]
        
        for field in financial_fields:
            if pd.notna(row[field]) and row[field] != '':
                consolidated_data[company_key][field] = row[field]
    
    # Convert dictionary to list
    consolidated_list = list(consolidated_data.values())
    
    # Create a new DataFrame
    consolidated_df = pd.DataFrame(consolidated_list)
    
    # Reorder columns to put basic information first and financial indicators last
    column_order = [
        'year', 'month', 'day', 'ticker', 'exchange', 'filename',
        'revenue_growth', 'capital_expenditure', 'earnings_per_share',
        'gross_margin', 'operating_margin', 'net_margin', 'ebitda',
        'return_on_equity', 'return_on_assets', 'debt_to_equity_ratio',
        'current_ratio', 'quick_ratio', 'interest_coverage_ratio',
        'price_to_earnings_ratio', 'dividend_yield'
    ]
    
    # Keep only existing columns
    existing_columns = [col for col in column_order if col in consolidated_df.columns]
    consolidated_df = consolidated_df[existing_columns]
    
    # Save to new CSV file
    consolidated_df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"Consolidated data shape: {consolidated_df.shape}")
    print(f"Data saved to: {output_file}")
    print(f"Records before consolidation: {len(df)}")
    print(f"Records after consolidation: {len(consolidated_df)}")

if __name__ == "__main__":
    # Set input and output file paths
    input_csv = r"financial_information.csv"
    output_csv = r"consolidated_financial_information.csv"
    
    # Execute data consolidation
    consolidate_financial_data(input_csv, output_csv)