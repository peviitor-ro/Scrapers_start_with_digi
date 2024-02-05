#
#
#
#
# Company -> capex
# Link ----> https://capex.com/en/careers
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid


def prepare_post_requests() -> tuple:
    '''
    ... prepare post requests for new requests data.
    '''

    url = 'https://portal.dynamicsats.com/JobListing/WebForm/JobListing_Read'

    headers = {
        'authority': 'portal.dynamicsats.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': '__RequestVerificationToken=1ikI1JXu0sPXI2iq1UP_KGhf2M0PIdM9hHNrg0dy0_0-ivkhW7L0MplAoHBHrKT1GgjQSFlDlSYUstpwf_fNRmdgqZIcDDReNVHisjgbQz41; ARRAffinitySameSite=5be4f6076895b28fe7622c56a3f9d12283381141aea24a194955ebb0cccaaba9',
        'origin': 'https://portal.dynamicsats.com',
        'referer': 'https://portal.dynamicsats.com/JobListing/347022b3-2e4e-48d2-9dac-9f7d78675080',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
        }

    data = 'sort=&group=&filter=&formId=347022b3-2e4e-48d2-9dac-9f7d78675080'

    return url, headers, data


def collect_data_from_capex():
    '''
    ... collect data with prepared post requests.
    '''

    url, headers, data = prepare_post_requests()

    response = requests.post(url=url, headers=headers, data=data).json()

    lst_with_data = []
    for job in response['Data']:
        title = job['dcrs_jobtitle']
        link = 'https://portal.dynamicsats.com/JobListing/Details/347022b3-2e4e-48d2-9dac-9f7d78675080/' + job['Id']
        city = job['dcrs_location'].strip()

        if city in ['Bucharest']:
            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link":  link,
                    "company": "CAPEX",
                    "country": "Romania",
                    "city": "Bucuresti"
                })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'CAPEX'
data_list = collect_data_from_capex()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('CAPEX',
                  'https://capex.com/assets/logo/capex-com-logo-red.svg'))
