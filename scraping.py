import requests
import os
import json
import time
from datetime import datetime

def get_transaction_history(filename=None):
    url = "https://api.boliga.dk/api/v2/sold/search/results"
    results = []
    #You can change the amount of pages it can search
    pageCount = 1
    totalpageCounts = 1
    parameters = {
        'sort': 'date-d',
        'zipcodeFrom': 3000,
        'zipcodeTo': 4999,
        'street': '',
        'propertyType': 4,
        'salesDateMin':2014
    }
    
    while pageCount <= totalpageCounts:
        time.sleep(1)
        parameters['page'] = pageCount
        response = requests.get(url, params=parameters)
        if response.status_code != 200:
            #Sometimes boliga's API responds with an error if too many request sequentially
            print(f"pageCount {pageCount}: status_code {response.status_code} - waiting and trying again!")
            time.sleep(5)
        else:
            totalpageCounts = response.json()['meta']['totalpageCounts']
            print(f"pageCount {pageCount} of {totalpageCounts}")
            
            results.extend(response.json()['results'])
            pageCount += 1

        dir = os.path.dirname(os.path.abspath(__file__))
        folder = os.path.join(dir, 'data')
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)
        print(path)
        with open(path, 'w') as file:
            file.write(json.dumps(results))
    
    return results

if __name__ == "__main__":
    get_transaction_history(filename='boliga_transaction_history_vacation_homes.json')
