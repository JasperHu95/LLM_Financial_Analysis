# Usage Guide

This guide provides detailed instructions on how to use the Financial Analysis with LLM project.

## Prerequisites

Before you begin, make sure you have:
1. Python 3.6 or higher installed
2. A DeepSeek API key (sign up at https://www.deepseek.com/)
3. Git (optional, for cloning the repository)

## Installation

### Method 1: Download ZIP

1. Download the repository as ZIP from GitHub
2. Extract the ZIP file
3. Navigate to the project directory

### Method 2: Git Clone

```bash
git clone https://github.com/yourusername/financial-analysis-llm.git
cd financial-analysis-llm
```

## Setting up the Environment

1. Install the required dependencies:
   - On Windows: Double-click `install_dependencies.bat`
   - On Linux/Mac: Run `./install_dependencies.sh`
   - Or manually: Run `pip install -r requirements.txt`

## Preparing Your Data

1. Prepare your earnings call transcripts in plain text format (.txt)
2. Copy them to the `data_source` folder
3. Alternatively, try with the sample data provided in `sample_data` folder

## Using the Web Interface (Recommended)

1. Start the web application:
   ```bash
   python app.py
   ```

2. Open your browser and go to `http://127.0.0.1:5000`

3. Use the interface to:
   - Upload your transcript files
   - Enter your DeepSeek API key

4. Run the analysis from the command line:
   ```bash
   python financial_analysis.py
   python consolidate_financial_data.py
   ```

## Using Command Line Only

1. Edit `financial_analysis.py` to add your DeepSeek API key:
   ```python
   DEEPSEEK_API_KEY = "your_api_key_here"
   ```

2. Place your transcript files in the `data_source` folder

3. Run the analysis:
   ```bash
   python financial_analysis.py
   ```

4. Consolidate the data:
   ```bash
   python consolidate_financial_data.py
   ```

## Understanding the Output

The process generates two CSV files:

1. `financial_information.csv`: Contains raw extracted data with one row per financial statement
2. `consolidated_financial_information.csv`: Contains consolidated data with one row per company per date

## Troubleshooting

### Common Issues

1. **Module not found errors**: Make sure you've installed the dependencies with `pip install -r requirements.txt`

2. **API key errors**: Ensure your DeepSeek API key is correctly configured

3. **File not found errors**: Check that your transcript files are in the `data_source` folder

4. **Encoding errors**: Make sure your transcript files are saved in UTF-8 encoding

### Getting Help

If you encounter any issues not covered in this guide, please:
1. Check the GitHub Issues page
2. Create a new issue with a detailed description of the problem