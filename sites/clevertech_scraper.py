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


def collect_data_from_clevertech() -> list[dict]:
    '''
    ... get data from clever tech with one request to json data.
    Need more attention, because may be cause errros.
    '''

    response = requests.get(url='https://clevertech.biz/_next/data/zQTYSNLXDx0R_Taw0AR4v/jobs/apply.json',
                            headers=DEFAULT_HEADERS).json()

    lst_with_data = []
    for job in response['pageProps']['activeJobs']:
        slug = job['slug']
        title = job['name']

        lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link":  f'https://clevertech.biz/remote-jobs/{slug}',
                    "company": "clevertech",
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


company_name = 'clevertech'
data_list = collect_data_from_clevertech()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('clevertech',
                  "https://clevertech.biz/_next/static/media/ct-logo-greyred.cc64d432.svg"
                  ))
