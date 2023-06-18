#
#
#
# New Scraper for SeedBlink Company
# Link ---> https://seedblink.com/careers
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid


def get_path_for_request():
    '''
    ... path for requests. Path is new code for
    new succesful requests.
    '''

    resp = requests.get('https://seedblink.com/careers',
                         headers=DEFAULT_HEADERS)

    return resp.headers


print(get_path_for_request())
