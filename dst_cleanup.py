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

if __name__ == "__main__":
    datasets = [
        ('dst_data/forbrydelser.xlsx', 'data/cleaned_forbrydelser.csv'),
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
