#
#
#
#
# Company -> funcom
# Link ----> https://www.funcom.com/funcom-bucharest/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid


def collect_data_from_funcom():
    '''
    ... collect data from funcom, request to API with get.
    '''

    response = requests.get(url='https://api.teamtailor.com/v1/jobs?include=department,locations&page[size]=30&filter[feed]=public&page[number]=1&filter[locations]=178583&api_version=20161108&api_key=nCvUhI8oZU8a22OS8tNPoJltCnk0IUTRY90ADtLp',
                            headers=DEFAULT_HEADERS).json()

    lst_with_data = []
    for job in response['data']:
        link = job['links']['careersite-job-url']
        title = job['attributes']['title']

        lst_with_data.append({
                        "id": str(uuid.uuid4()),
                        "job_title": title,
                        "job_link": link,
                        "company": "funcom",
                        "country": "Romania",
                        "city": "Bucharest"
                    })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'funcom'
data_list = collect_data_from_funcom()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('funcom',
                  'https://upload.wikimedia.org/wikipedia/en/7/7c/Funcom_Logo_as_of_August_2017.png'
                  ))
