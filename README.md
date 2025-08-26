# Financial Analysis with LLM

This project uses Large Language Models (LLM) to extract forward-looking financial information from earnings call transcripts. It processes financial documents to identify and extract key financial metrics and projections based on US GAAP standards.

## Project Structure

- `financial_analysis.py` - Main script to extract financial data from transcripts
- `consolidate_financial_data.py` - Script to consolidate extracted data into a unified format
- `data_source/` - Directory containing earnings call transcript files
- `sample_data/` - Directory containing sample transcript for testing
- `app.py` - Web interface for easy file upload and API key configuration
- `templates/` - HTML templates for the web interface
- `install_dependencies.bat` - One-click script to install dependencies (Windows)
- `install_dependencies.sh` - One-click script to install dependencies (Linux/Mac)

## Getting Started

### Prerequisites

- Python 3.x installed on your system
- A DeepSeek API key (get it from [DeepSeek](https://www.deepseek.com/))

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/financial-analysis-llm.git
   ```

2. Navigate to the project directory:
   ```bash
   cd financial-analysis-llm
   ```

3. Install required packages using one of these methods:
   
   Windows:
   ```
   install_dependencies.bat
   ```
   
   Linux/Mac:
   ```
   ./install_dependencies.sh
   ```
   
   Or manually:
   ```
   pip install -r requirements.txt
   ```

4. Copy sample data to test the project:
   ```
   cp sample_data/* data_source/
   ```

## How to Use

### Option 1: Using the Web Interface (Recommended)

1. Start the web interface:
   ```
   python app.py
   ```

2. Open your browser and go to `http://127.0.0.1:5000`

3. Use the web interface to:
   - Upload transcript files via file selection
   - Configure your DeepSeek API key

4. Run the analysis scripts in your terminal:
   ```
   python financial_analysis.py
   python consolidate_financial_data.py
   ```

### Option 2: Command Line Usage

1. Place your earnings call transcript files (.txt format) in the `data_source` folder
2. Run `financial_analysis.py` first to extract financial information:
   ```
   python financial_analysis.py
   ```
   This generates `financial_information.csv` with raw extracted data.

3. Run `consolidate_financial_data.py` to process and consolidate the data:
   ```
   python consolidate_financial_data.py
   ```
   This generates `consolidated_financial_information.csv` with organized financial data.

## Output Files

- `financial_information.csv` - Raw extracted financial data from transcripts
- `consolidated_financial_information.csv` - Cleaned and consolidated financial data

## Requirements

- Python 3.x
- pandas
- requests
- flask

## API Key Configuration

Before running the analysis, you need to configure your DeepSeek API key. You can do this either:
1. Using the web interface (recommended)
2. By manually editing the `financial_analysis.py` file

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to DeepSeek for providing the LLM API
- Thanks to all contributors who have helped to improve this project