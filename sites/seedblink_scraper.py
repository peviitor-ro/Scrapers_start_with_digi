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
from bs4 import BeautifulSoup
#
import uuid


def search_link_ID():
    '''
    ... search link ID.
    '''
    response = requests.get(url='https://seedblink.com/careers', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    # search scr script
    scr_script_id = str(soup.find_all("script", src=True)[-1]).split('/')[-3]

    return scr_script_id


def get_data_seedblink():
    '''
    ... path for requests. Path is new code for
    new succesful requests.
    '''

    resp = requests.get(f'https://seedblink.com/_next/data/{search_link_ID()}/en/careers.json',
                         headers=DEFAULT_HEADERS).json()

    lst_with_data = []
    for job in resp['pageProps']['allJobs']:
        title = job['data']['title']

        if 'fake' not in title.lower():
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  f'https://seedblink.com/en/careers/{job["jobSlug"]}',
                "company": "SeedBlink",
                "country": "Romania",
                "city": job['data']['location']
            })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'SeedBlink'
data_list = get_data_seedblink()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('SeedBlink',
                  'https://seedblink.com/_next/static/images/seedblink-logo-f8978e8317c9a57dca40e52a53247d6e.png'
                  ))
