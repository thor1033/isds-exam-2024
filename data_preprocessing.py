import pandas as pd
import numpy as np

def load_dataframes(folder_path, files):
    """
    Load all files from a specified folder into dataframes and store them in a dictionary.
    
    Args:
    folder_path (str): Path to the folder containing the files.
    files (dict): Dictionary mapping file names to dataframe names.
    
    Returns:
    dict: Dictionary of dataframes loaded from the files.
    """
    dataframes = {}
    for file, df_name in files.items():
        file_path = f"{folder_path}{file}"
        try:
            dataframes[df_name] = pd.read_excel(file_path)
            print(f"Loaded {df_name} successfully.")
        except Exception as e:
            print(f"Failed to load {df_name}: {e}")
    return dataframes

def process_and_standardize_dataframes(dataframes):
    """
    Process and standardize dataframes in the given dictionary.
    
    Args:
    dataframes (dict): Dictionary of dataframes to process.
    
    Returns:
    dict: Dictionary of processed dataframes.
    """
    processed_dataframes = {}
    years = range(2014, 2024)  # 2014 to 2023
    
    for key, df in dataframes.items():
        df = df.rename(columns={'Column1': 'Municipality'})
        df = df.set_index('Municipality')
        
        if key == 'crimes':
            year_columns = [col for col in df.columns if str(col).startswith('20')]
            df = df[year_columns].groupby(lambda x: str(x)[:4], axis=1).sum()
            df = df.drop('Uoplyst kommune', errors='ignore')
        
        if key == 'area_of_sports_facilities':
            df = df.drop('Hele landet')
        
        for year in years:
            if str(year) not in df.columns:
                df[str(year)] = np.nan
                
        df = df[[str(year) for year in years]]
        processed_dataframes[key] = df

    return processed_dataframes

def normalize_specified_dataframes(dataframes, variables_to_normalize):
    """
    Normalize specified dataframes by dividing their values by the population for each municipality.
    
    Args:
    dataframes (dict): Dictionary of dataframes to normalize.
    variables_to_normalize (list): List of dataframe keys to normalize.
    
    Returns:
    dict: Updated dictionary of dataframes with specified ones normalized.
    """
    if 'population' not in dataframes:
        raise KeyError("Population dataframe not found. Please ensure it exists in the dataframes dictionary.")

    population_df = dataframes['population']
    updated_dataframes = dataframes.copy()

    for var in variables_to_normalize:
        if var not in dataframes:
            print(f"Warning: {var} not found in dataframes. Skipping.")
            continue

        df = dataframes[var]
        df = df.reindex(population_df.index)
        normalized_df = df.div(population_df)
        normalized_df = normalized_df.replace([np.inf, -np.inf], np.nan)
        updated_dataframes[var] = normalized_df

    return updated_dataframes

def map_municipality_codes(transaction_df, municipality_codes_path):
    """
    Map municipality codes in the transaction data to municipality names.
    
    Args:
    transaction_df (pd.DataFrame): DataFrame containing transaction data.
    municipality_codes_path (str): Path to the CSV file with municipality codes.
    
    Returns:
    pd.DataFrame: Updated DataFrame with new 'municipality' column.
    """
    municipality_codes = pd.read_csv(municipality_codes_path)
    municipality_map = dict(zip(municipality_codes['Code'], municipality_codes['Municipality']))
    transaction_df['Municipality'] = transaction_df['municipalityCode'].map(municipality_map)
    
    unmapped_codes = transaction_df[transaction_df['Municipality'].isna()]['municipalityCode'].unique()
    if len(unmapped_codes) > 0:
        print(f"Warning: The following municipality codes were not mapped: {unmapped_codes}")
    
    return transaction_df

def main():
    # Paths and file names
    folder_path = 'dst_data/'
    files = {
        'areal af sportsanlæg.xlsx': 'area_of_sports_facilities',
        'Dansk oprindelse.xlsx': 'danish_origin',
        'efterkommere.xlsx': 'descendants',
        'forbrydelser.xlsx': 'crimes',
        'fuldtidsledige.xlsx': 'full_time_unemployed',
        'ginikoeff.xlsx': 'gini_coefficient',
        'gnms_alder.xlsx': 'average_age',
        'indvandrere.xlsx': 'immigrants',
        'kommuneskat.xlsx': 'municipal_tax',
        'grundskole.xlsx': 'primaryschool',
        'KVU.xlsx': 'kvu',
        'LVU.xlsx': 'lvu',
        'job.xlsx': 'job'
    }
    
    # Load dataframes
    dataframes = load_dataframes(folder_path, files)
    
    # Process and standardize dataframes
    dataframes = process_and_standardize_dataframes(dataframes)
    
    # Compute population dataframe
    dataframes['population'] = dataframes['danish_origin'] + dataframes['descendants'] + dataframes['immigrants']
    
    # Normalize specified dataframes
    variables_to_normalize = [
        'danish_origin', 'descendants', 'crimes', 'full_time_unemployed',
        'immigrants', 'primaryschool', 'kvu', 'lvu', 'job'
    ]
    dataframes = normalize_specified_dataframes(dataframes, variables_to_normalize)
    
    # Load and process transaction data
    df_falster = pd.read_json('./data/boliga_transaction_history_vacation_homes_lolland_falster.json')
    df_sjaelland = pd.read_json('./data/boliga_transaction_history_vacation_homes_sjaelland.json')
    df = pd.concat([df_falster, df_sjaelland], ignore_index=True)
    
    # Map municipality codes
    df = map_municipality_codes(df, 'dst_data/municipality_codes.csv')
    
    # Filter transaction data for years 2014-2023
    df['soldDate'] = pd.to_datetime(df['soldDate'])
    df = df[(df['soldDate'].dt.year >= 2014) & (df['soldDate'].dt.year <= 2023)]
    df['year'] = df['soldDate'].dt.year
    
    # Merge vacation data with social dataframes
    merged_data = df.copy()
    for key, df in dataframes.items():
        df_melted = df.reset_index().melt(id_vars='Municipality', var_name='year', value_name=key)
        df_melted['year'] = df_melted['year'].astype(int)
        merged_data = pd.merge(merged_data, df_melted, on=['Municipality', 'year'], how='left')
    

    merged_data.to_csv('data/merged_data.csv', index=False)
    print("Done with merging and cleaning of dataframes. Data saved to 'data/merged_data.csv'.")

if __name__ == '__main__':
    main()
