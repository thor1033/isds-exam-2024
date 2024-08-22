import requests
import os
import json
import time
from datetime import datetime

def get_transaction_history(zipcode_F=3000, zipcode_T=4999, propertyType=4, minyear=2014, filename=None):
    apiurl = "https://api.boliga.dk/api/v2/sold/search/results"
    results = []
    page = 1
    totalpages = 1
    parameters = {
        'sort': 'date-d',
        'zipcodeFrom': zipcode_F,
        'zipcodeTo': zipcode_T,
        'street': '',
        'propertyType': propertyType
    }
    
    if minyear is not None:
        parameters['salesDateMin'] = minyear

    while page <= totalpages:
        time.sleep(1)
        parameters['page'] = page
        response = requests.get(apiurl, params=parameters)
        if response.status_code != 200:
            print(f"Page {page}: status_code {response.status_code} - aborting!")
            time.sleep(5)
        else:
            totalpages = response.json()['meta']['totalPages']
            print(f"Page {page} of {totalpages}")
            
            results.extend(response.json()['results'])
            page += 1
            #time.sleep(1)

        if filename is not None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_folder = os.path.join(current_dir, 'data')

            # Ensure the data directory exists
            os.makedirs(data_folder, exist_ok=True)
            
            # Construct the full path to the data file
            data_file_path = os.path.join(data_folder, filename)
            print(data_file_path)
            with open(data_file_path, 'w') as file:
                file.write(json.dumps(results))
    
    return results

if __name__ == "__main__":
    get_transaction_history(filename='boliga_transaction_history_vacation_homes.json')
