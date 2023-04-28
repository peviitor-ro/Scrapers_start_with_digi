#
#
#
#
import requests
import json


def update_jti():
    """
    Update data on api peviitor.
    """

    API_KEY = '3686bc-c0b-7f5c-e152-c1718c25867'
    CLEAN_URL = 'https://api.peviitor.ro/v4/clean/'

    clean_header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'apikey': API_KEY
        }

    clean_request = requests.post(CLEAN_URL, headers=clean_header, data={'company': 'jti'})
    print(clean_request.status_code)

    post_header = {
        'Content-Type': 'appliction/json',
        'apikey': API_KEY
        }

    with open('scrapers_forzza/data_jti.json', 'r') as file:
        data = json.load(file)

    post_request_to_server = requests.post('https://api.peviitor.ro/v4/update/', headers=post_header, data=json.dumps(data))
    print(post_request_to_server)
