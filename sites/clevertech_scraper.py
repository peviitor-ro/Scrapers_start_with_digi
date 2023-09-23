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
from bs4 import BeautifulSoup
#
import uuid


def get_id() -> str:
    '''
    ... get id from site.
    '''

    response = requests.get(url='https://clevertech.biz/jobs',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    # search scr script
    scr_script_id = str(soup.find_all("script", src=True)[-1]).split('/')[-3]

    return scr_script_id


def collect_data_from_clevertech():
    '''
    ... get data from clever tech with one request to json data.
    Need more attention, because may be cause errros.
    '''

    idx = get_id()
    response = requests.get(url=f'https://clevertech.biz/_next/data/{idx}/jobs/apply.json',
                            headers=DEFAULT_HEADERS).json()

    lst_with_data = []
    for job in response['pageProps']['activeJobs']:
        slug = job['slug']
        title = job['name']

        lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link":  f'https://clevertech.biz/remote-jobs/{slug}',
                    "company": "Clevertech",
                    "country": "Romania",
                    "city": "Remote"
                })

    return lst_with_data


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Clevertech'
data_list = collect_data_from_clevertech()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Clevertech',
                  "https://clevertech.biz/_next/static/media/ct-logo-greyred.cc64d432.svg"
                  ))
