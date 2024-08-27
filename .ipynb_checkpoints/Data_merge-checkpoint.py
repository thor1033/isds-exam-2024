# Auto-generated Python script from Jupyter Notebook

if __name__ == '__main__':

    import pandas as pd
    import numpy as np 

    import pandas as pd
    
    # Path to the folder containing the files
    folder_path = 'dst_data/'
    
    # File names and their respective dataframe names in English
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
    
    # Dictionary to hold the dataframes
    dataframes = {}
    
    # Load each file into a dataframe and store it in the dictionary with the appropriate name
    for file, df_name in files.items():
        file_path = f"{folder_path}{file}"
        try:
            dataframes[df_name] = pd.read_excel(file_path)
            print(f"Loaded {df_name} successfully.")
        except Exception as e:
            print(f"Failed to load {df_name}: {e}")
    
    # Check which dataframes were loaded successfully
    dataframes.keys()

    import pandas as pd
    import numpy as np
    
    def process_and_standardize_dataframes(dataframes):
        """
        Process all dataframes in the given dictionary:
        1. Rename 'Column1' to 'Municipality'
        2. Set 'Municipality' as the index
        3. Ensure all dataframes have columns for years 2014-2023
        4. For 'crimes' dataframe, convert quarterly data to yearly data and handle special cases
        """
        processed_dataframes = {}
        years = range(2014, 2024)  # 2014 to 2023
        
        for key, df in dataframes.items():
            # Rename 'Column1' to 'Municipality' and set as index
            df = df.rename(columns={'Column1': 'Municipality'})
            df = df.set_index('Municipality')
            
            # Special processing for 'crimes' dataframe
            if key == 'crimes':
                # Identify all year columns (assuming they start with '20')
                year_columns = [col for col in df.columns if str(col).startswith('20')]
                
                # Group columns by year and sum to convert quarterly to yearly data
                df = df[year_columns].groupby(lambda x: str(x)[:4], axis=1).sum()
                
                # Drop the 'Uoplyst kommune' index
                df = df.drop('Uoplyst kommune', errors='ignore')
            
    
            if key == 'area_of_sports_facilities': 
                df = df.drop('Hele landet')
            # Ensure dataframe has columns for years 2014-2023
            for year in years:
                if str(year) not in df.columns:
                    df[str(year)] = np.nan  # Add missing year columns with NaN values
            
            # Keep only the columns for years 2014-2023
            df = df[[str(year) for year in years]]
            
            processed_dataframes[key] = df
    
    
        return processed_dataframes
    
    
    dataframes = process_and_standardize_dataframes(dataframes)



    dataframes['population'] = dataframes['danish_origin']+dataframes['descendants']+ dataframes['immigrants']

    import pandas as pd
    import numpy as np
    
    def normalize_specified_dataframes(dataframes, variables_to_normalize):
        """
        Normalize specified dataframes by dividing their values by the population for each municipality.
        Keep all other dataframes unchanged.
        
        Args:
        dataframes (dict): Dictionary of dataframes
        variables_to_normalize (list): List of dataframe keys to normalize
        
        Returns:
        dict: Updated dictionary of dataframes with specified ones normalized
        """
        # Ensure population dataframe exists
        if 'population' not in dataframes:
            raise KeyError("Population dataframe not found. Please ensure it exists in the dataframes dictionary.")
    
        population_df = dataframes['population']
        updated_dataframes = dataframes.copy()
    
        for var in variables_to_normalize:
            if var not in dataframes:
                print(f"Warning: {var} not found in dataframes. Skipping.")
                continue
    
            df = dataframes[var]
            
            # Ensure the dataframe has the same index as population_df
            df = df.reindex(population_df.index)
            
            # Normalize the dataframe
            normalized_df = df.div(population_df)
            
            # Handle division by zero: replace inf and -inf with NaN
            normalized_df = normalized_df.replace([np.inf, -np.inf], np.nan)
            
            updated_dataframes[var] = normalized_df
            
            print(f"Normalized {var}")
    
        return updated_dataframes
    
    # Example usage:
    variables_to_normalize = [
        'danish_origin', 'descendants', 'crimes', 'full_time_unemployed',
        'immigrants', 'primaryschool', 'kvu', 'lvu', 'job'
    ]
    
    # normalized_dataframes = normalize_specified_dataframes(dataframes, variables_to_normalize)

    dataframes = normalize_specified_dataframes(dataframes, variables_to_normalize)

    # Load the transaction data
    df_falster = pd.read_json('./data/boliga_transaction_history_vacation_homes_lolland_falster.json')
    df_sjaelland = pd.read_json('./data/boliga_transaction_history_vacation_homes_sjaelland.json')
    # Concatenate the two DataFrames
    df = pd.concat([df_falster, df_sjaelland], ignore_index=True)

    import pandas as pd
    
    def map_municipality_codes(transaction_df, municipality_codes_path):
        """
        Map municipality codes in the transaction data to municipality names.
        
        Args:
        transaction_df (pd.DataFrame): DataFrame containing transaction data
        municipality_codes_path (str): Path to the CSV file with municipality codes
        
        Returns:
        pd.DataFrame: Updated DataFrame with new 'municipality' column
        """
        
        # Read the municipality codes CSV file
        municipality_codes = pd.read_csv(municipality_codes_path)
        
        # Create a dictionary for mapping
        municipality_map = dict(zip(municipality_codes['Code'], municipality_codes['Municipality']))
        print("Error is not here")
        # Add a new column 'municipality' based on the mapping
        transaction_df['Municipality'] = transaction_df['municipalityCode'].map(municipality_map)
        
        # Check for any unmapped codes
        unmapped_codes = transaction_df[transaction_df['Municipality'].isna()]['municipalityCode'].unique()
        if len(unmapped_codes) > 0:
            print(f"Warning: The following municipality codes were not mapped: {unmapped_codes}")
        
        return transaction_df

    municipality_codes = pd.read_csv('dst_data/municipality_codes.csv')
    municipality_codes

    municipality_codes = pd.read_csv('dst_data/municipality_codes.csv')
    print(municipality_codes.columns)
    # Create a dictionary for mapping: Code -> Municipality
    municipality_map = dict(zip(municipality_codes['Code'], municipality_codes['Municipality']))

    
    df = map_municipality_codes(df, 'dst_data/municipality_codes.csv')

    # Convert soldDate to datetime and filter for 2014-2023
    df['soldDate'] = pd.to_datetime(df['soldDate'])
    df =df[(df['soldDate'].dt.year >= 2014) & (df['soldDate'].dt.year <= 2023)]
    
    # Extract year from soldDate
    df['year'] = df['soldDate'].dt.year
    
    # Start with the vacation data
    merged_data = df.copy()
    
    # Merge with each social dataframe
    for key, df in dataframes.items():
        # Melt the dataframe to convert years to a single column
        df_melted = df.reset_index().melt(id_vars='Municipality', var_name='year', value_name=key)
        df_melted['year'] = df_melted['year'].astype(int)
        
        # Merge with the vacation data
        merged_data = pd.merge(merged_data, df_melted, on=['Municipality', 'year'], how='left')

    merged_data
