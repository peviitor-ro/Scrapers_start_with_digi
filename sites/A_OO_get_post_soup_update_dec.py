#
#
#
# This Decorator will avoid duplicate for me!
# Respect DRY
# This decorator have: default headers and soup and update data on peviitor.ro!
#
import requests
#
import os  # I do not have API KEY
#
import json
import time


DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.4044.113 Safari/5370.36 Brave/9085',
    'Accept-Language': 'en-US,en;q=0.5',
    'Refer': 'https://google.com',
    'DNT': '1'
}


########### UPDATE API DECORATOR ############
def update_peviitor_api(original_function):
    """
    Decorator for update data on Peviitor.ro API
    """

    def new_function(*args, **kwargs):
        company_name, data_list = args
        #
        API_KEY = os.environ.get('API_KEY')
        CLEAN_URL = 'https://api.peviitor.ro/v4/clean/'

        clean_header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'apikey': API_KEY
            }

        clean_request = requests.post(CLEAN_URL, headers=clean_header, data={'company': company_name})

        time.sleep(0.2)

        post_header = {
            'Content-Type': 'application/json',
            'apikey': API_KEY
            }

        post_request_to_server = requests.post('https://api.peviitor.ro/v4/update/', headers=post_header, data=json.dumps(data_list))

        # don't delete this lines if you want to see the graph on scraper's page
        file = company_name.lower() + '_scraper.py'
        data = {'data': len(data_list)}
        dataset_url = f'https://dev.laurentiumarian.ro/dataset/Scrapers_start_with_digi/{file}/'
        requests.post(dataset_url, json=data)
        ########################################################
        
        print(json.dumps(data_list, indent=4))

        return original_function(*args, **kwargs)

    return new_function
