#
#
#
#
# Company -> clevertech
# Link ----> https://clevertech.biz/jobs
# Api link - https://clevertech.biz/_next/data/zQTYSNLXDx0R_Taw0AR4v/jobs/apply.json
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid


def get_id() -> str:
    '''
    ... get id from site.
    '''

    response = requests.head(url='https://clevertech.biz/jobs',
                            headers=DEFAULT_HEADERS)

    return response.headers


print(get_id())
