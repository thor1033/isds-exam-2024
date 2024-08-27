# Pricing of vacation homes in Denmark

This project analyzes vacation homes transaction data alongside socioeconomic data from Danish municipalities, focusing on Sjælland, Lolland, and Falster. The primary goal is to explore the relationships between various socioeconomic factors and vacation home prices across different municipalities over a 10-year period (2014-2023).

## Project Structure

The project is organized into the following files:

### 1. `scraping.py`
This script scrapes real estate transaction data from the Boliga API. The data collected includes details such as the price per square meter (sqmPrice), property type, and location. The results are saved as JSON files for further analysis.

### 2. `data_preprocessing.py`
This script processes and cleans the socioeconomic data sourced from Danmarks Statistik (dst). It standardizes and normalizes the data, ensuring that it's ready for analysis. Additionally, this script merges the cleaned socioeconomic data with the real estate transaction data based on municipality codes and dates, creating a comprehensive dataset for further analysis.

### 3. `descriptive_analysis.ipynb`
This Jupyter Notebook performs descriptive analysis on the merged dataset. It generates two interactive HTML files that visualize:
- `municipalities_average_sqm_price.html`: The average price per square meter across municipalities.
- `municipalities_transactions.html`: The total number of real estate transactions across municipalities.

These HTML files can be viewed in your browser to explore the data visually.

### 4. `regression_analysis.ipynb`
This notebook contains the implementation of machine learning models, such as Lasso and Ridge regression, to predict real estate prices based on the processed data. It includes steps for feature selection, model training, and validation.

## Data Sources

- **Danmarks Statistik (dst)**: Socioeconomic data including crime rates, average age, employment, and education levels in each municipality.
- **Boliga**: Real estate transaction data, including the price per square meter for properties sold in Sjælland, Lolland, and Falster.

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/thor1033/isds-exam-2024.git
   cd isds-exam-2024
   ```

2. **Install Dependencies**
   Ensure you have Python 3.7+ installed, then install the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Data Scraping Script**
   Collect the real estate transaction data by running:
   ```bash
   python scraping.py
   ```
   This will save the data in JSON format in the `data/` directory.

4. **Run the Data Preprocessing Script**
   Process and clean the data, then merge the socioeconomic data with the transaction data:
   ```bash
   python data_preprocessing.py
   ```
   This will generate `merged_data.csv` in the `data/` directory.

5. **Run the Descriptive Analysis Notebook**
   Explore the descriptive statistics and generate visualizations by running `descriptive_analysis.ipynb` in Jupyter Notebook. The resulting HTML files can be viewed in your browser.

6. **Run Machine Learning Models**
   Train and validate machine learning models using the data in `regression_analysis.ipynb`. You can experiment with different models and hyperparameters to optimize the predictions.

## Analysis Highlights

- **Descriptive Analysis**: Visualization of real estate transactions and average prices per square meter across different municipalities.
- **Machine Learning**: Predictive modeling of real estate prices using socioeconomic data, with an emphasis on feature selection and model validation.

## License

This project is licensed under the GPLv3 License. See the `LICENSE` file for details.

## Collaborators

vzj697 - Rigmor G. Gavrani

flc296 - Romal G. Sadat

bxm615 - Daniel Kofoed

zvr697 - Thor Bøje Simonsen

