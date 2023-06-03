#
#
#
# New Company - Haleon
# Link to jobs - https://careers.haleon.com/en-gb/jobs?location=Romania&stretch=10&stretchUnit=MILES&page=1
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid


def collect_data_from_haleon():
    """
    Collect data with one requests,
    ... all from haleon.
    """

    response = requests.get('https://careers.haleon.com/api/jobs?page=1&location=Romania&stretch=10&stretchUnit=MILES&sortBy=relevance&descending=false&internal=false',
                           headers=DEFAULT_HEADERS).json()

    lst_with_data = []
    for dt in response['jobs']:
        link = dt['data']['apply_url']
        title = dt['data']['title']
        location = dt['data']['country_code']

        # check country code!
        if location != 'RO':
            location = 'Multiple'

        lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link":  link,
                    "company": "haleon",
                    "country": "Romania",
                    "city": location
                    })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'haleon'
data_list = collect_data_from_haleon()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('haleon',
                  'https://cms.jibecdn.com/prod/haleon/assets/HEADER-NAV_LOGO-en-us-1653650925897.png'
                  ))
