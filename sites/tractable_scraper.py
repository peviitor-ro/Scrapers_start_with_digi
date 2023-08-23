#
#
#
#
#
# Scrape new Company - Tractable
# links ---> https://tractable.ai/en/jobs
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid


def get_data() -> list[dict]:

    response = requests.get('https://tractable.ai/api/joblist?board=tractable',
                            headers=DEFAULT_HEADERS)

    lst_with_data = []
    for job in response.json()['jobs']:
        location = job['location']

        if 'romania' in location.lower():
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": job['title'],
                "job_link": 'https://tractable.ai/' + job['href'],
                "company": "Tractable",
                "country": "Romania",
                "city": location.split(',')[0]
                })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Tractable'
data_list = get_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Tractable',
                  'https://media.graphassets.com/resize=w:1616,h:535,fit:crop/auto_image/compress/Q1HdbVpoSdnYkE3bf03V'
                  ))
