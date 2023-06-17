#
#
#
#
# SEND DATA TO API SCRIPT!
#
#
import requests
#
import os  # I do not have API KEY
#
import json


class UpdateAPI:
    '''
    class for update API
    '''

    def update_data(self, company_name: str, data_jobs: list):
        '''
        ... update data on peviitor.
        '''

        API_KEY = os.environ.get('API_KEY')
        CLEAN_URL = 'https://api.peviitor.ro/v4/clean/'

        # clean headers
        clean_header = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'apikey': API_KEY
                }

        # clean data
        clean_request = requests.post(CLEAN_URL, headers=clean_header, data={'company': company_name})
        print(f"{company_name} clean -> {clean_request.status_code}")

        # post headers
        post_header = {
            'Content-Type': 'application/json',
            'apikey': API_KEY
            }

        # update data
        post_request_to_server = requests.post('https://api.peviitor.ro/v4/update/', headers=post_header, data=json.dumps(data_jobs))
        print(f"{company_name} post -> {post_request_to_server}")

    def update_logo(self, id_company: str, logo_link: str):
        '''
        ... update logo on pe viitor.
        '''

        headers = {
            "Content-Type": "application/json"
        }

        url = "https://api.peviitor.ro/v1/logo/add/"
        data = json.dumps([{"id": id_company, "logo": logo_link}])

        response = requests.post(url, headers=headers, data=data)

        return f'Logo update ---> succesfuly {response.text}'
