#
#
#
#
import requests
import os


def clean_data(company_name: str) -> None:

    API_KEY = os.environ.get('API_KEY')
    CLEAN_URL = 'https://api.peviitor.ro/v4/clean/'

    print('API_KEY = ', API_KEY)

    clean_header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'apikey': API_KEY
        }

    clean_request = requests.post(CLEAN_URL, headers=clean_header, data={'company': company_name})
    print(f"{company_name} clean -> {clean_request.status_code}")


print(clean_data('bandainamco'))
