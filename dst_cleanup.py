import pandas as pd


def clean_and_save_data(input_file, output_file):
    # Load the Excel file
    df = pd.read_excel(input_file, skiprows=1)  # Adjust skiprows if needed based on the header position
    
    # Specific adjustments based on the input file
    if input_file == 'dst_data/forbrydelser.xlsx':
        df.set_index(df.columns[1], inplace=True)
    elif input_file in ['dst_data/fuldtidsledige.xlsx', 'dst_data/befolkning og indvandre.xlsx']:
        df.set_index(df.columns[4], inplace=True)
    elif input_file == 'dst_data/uddannelse.xlsx':
        df.set_index(df.columns[3], inplace=True)
    elif input_file == 'dst_data/job.xlsx':
        df.set_index(df.columns[2], inplace=True)
    else:  # Default case for other files like 'gnms_alder.xlsx', 'ginikoeff.xlsx', 'kommuneskat.xlsx'
        df.set_index(df.columns[1], inplace=True)
    
    # Drop any rows or columns that are not needed (e.g., rows/columns with NaN in the header)
    df.dropna(axis=0, how='all', inplace=True)  # Drop rows where all elements are NaN
    df.dropna(axis=1, how='all', inplace=True)  # Drop columns where all elements are NaN
    
    # Rename columns to reflect the correct years (if necessary)
    df.columns = df.iloc[0]  # Use the first row as header
    df = df[1:]  # Drop the first row now that it is used as the header
    
    # Ensure that the index and columns are correctly set
    df.index.name = 'Municipality'
    df.columns.name = 'Year'
    
    # Drop the first column that contains NaN values
    df.drop(columns=[df.columns[0]], inplace=True)
    
    # Special handling for 'forbrydelser.xlsx' (renaming columns to represent quarters)
    if input_file == 'forbrydelser.xlsx':
        new_columns = []
        for years in range(0, len(df.columns+1), 4):  # Adjust the range as necessary
            year = 2007 + years // 4
            if year == 2024:
                new_columns.extend([f"{year}-Q1", f"{year}-Q2"])
            else:
                new_columns.extend([f"{year}-Q1", f"{year}-Q2", f"{year}-Q3", f"{year}-Q4"])
        df.columns = new_columns
    
    # Save the cleaned DataFrame to a CSV file
    df.to_csv(output_file)
    print(f"Saved {output_file} successfully.")

def merge_normalize_dst():
    # List of CSV files to load
    csv_files = [
        'data/cleaned_fuldtidsledige.csv',
        'data/cleaned_indbyggertal.csv',
        'data/cleaned_gnms_alder.csv',
        'data/cleaned_job.csv',
        'data/cleaned_kommuneskat.csv',
        'data/cleaned_befolkning_og_indvandre.csv',
        'data/cleaned_uddannelse.csv'
    ]

    # Dictionary to hold the reshaped DataFrames
    reshaped_dfs = {}

    # Load, transpose, and reshape each DataFrame
    for file in csv_files:
        df = pd.read_csv(file)
        # Transpose and reshape the DataFrame
        df = df.melt(id_vars=['Municipality'], var_name='Year', value_name=file.split('/')[-1].replace('.csv', ''))
        reshaped_dfs[file] = df
        
    # Function to normalize the Year column to integers
    def normalize_year_column(df):
        df['Year'] = df['Year'].astype(float).astype(int).astype(str)
        return df

    # Apply the normalization to each reshaped DataFrame
    normalized_dfs = {file: normalize_year_column(df) for file, df in reshaped_dfs.items()}
    # Start with the first reshaped DataFrame
    merged_df = reshaped_dfs['data/cleaned_fuldtidsledige.csv']

    # Merge with each subsequent reshaped DataFrame
    for file in csv_files[1:]:
        merged_df = pd.merge(merged_df, reshaped_dfs[file], on=['Municipality', 'Year'], how='outer')

    # Remove rows where 'Municipality' is NaN
    cleaned_merged_df = merged_df.dropna(subset=['Municipality'])

    # Ensure the 'Year' column is treated as an integer using .loc to avoid the warning
    cleaned_merged_df.loc[:, 'Year'] = cleaned_merged_df['Year'].astype(int)

    # Remove rows where the 'Year' is 2013 or 2024
    cleaned_merged_df = cleaned_merged_df[~cleaned_merged_df['Year'].isin([2013, 2024])]

    # Display the cleaned DataFrame
    cleaned_merged_df.reset_index()
    # Normalizing the specified columns by 'cleaned_indbyggertal'
    columns_to_normalize = ['cleaned_job', 'cleaned_fuldtidsledige', 'cleaned_befolkning_og_indvandre', 'cleaned_uddannelse']
    for column in columns_to_normalize:
        cleaned_merged_df[f'{column}_normalized'] = cleaned_merged_df[column] / cleaned_merged_df['cleaned_indbyggertal']

    # Rename the columns to English
    cleaned_merged_df.rename(columns={
        'Municipality': 'municipality',
        'Year': 'year',
        'unemployed': 'unemployed',
        'population': 'population',
        'cleaned_gnms_alder': 'average_age',
        'jobs': 'jobs',
        'cleaned_kommuneskat': 'municipal_tax',
        'population_and_immigrants': 'population_and_immigrants',
        'education': 'education',
        'cleaned_job_normalized': 'jobs_normalized',
        'cleaned_fuldtidsledige_normalized': 'unemployed_normalized',
        'cleaned_befolkning_og_indvandre_normalized': 'population_and_immigrants_normalized',
        'cleaned_uddannelse_normalized': 'education_normalized'
    }, inplace=True)

    # Specify the filename
    output_file = 'data/merged_dst_data.csv'

    # Save the DataFrame to a CSV file
    cleaned_merged_df.to_csv(output_file, index=False)

    # Confirmation message
    print(f"DataFrame saved as {output_file}")

if __name__ == "__main__":
    datasets = [
        ('dst_data/forbrydelser.xlsx', 'data/cleaned_forbrydelser.csv'),
        ('dst_data/indbyggertal.xlsx', 'data/cleaned_indbyggertal.csv'),
        ('dst_data/fuldtidsledige.xlsx', 'data/cleaned_fuldtidsledige.csv'),
        ('dst_data/gnms_alder.xlsx', 'data/cleaned_gnms_alder.csv'),
        ('dst_data/job.xlsx', 'data/cleaned_job.csv'),
        ('dst_data/ginikoeff.xlsx', 'data/cleaned_ginikoeff.csv'),
        ('dst_data/kommuneskat.xlsx', 'data/cleaned_kommuneskat.csv'),
        ('dst_data/befolkning og indvandre.xlsx', 'data/cleaned_befolkning_og_indvandre.csv'),
        ('dst_data/uddannelse.xlsx', 'data/cleaned_uddannelse.csv')
    ]
    # Process and save each dataset
    for input_file, output_file in datasets:
        clean_and_save_data(input_file, output_file)

    merge_normalize_dst();
