# # Scraper for Ascentcore Company
# # Link to company career page -> https://ascentcore.com/careers/
# #
# #
# #
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests

#
import uuid

def collect_data_from_ascentcore():
    '''
    ... this function will collect and will return a list with jobs
    '''

    response = requests.get(url='https://api.eu.lever.co/v0/postings/ascentcore?group=team&mode=json', headers=DEFAULT_HEADERS).json()

    lst_with_data = []
    for job in response:
        for i in job ['postings']:
            title = i['text']
            link = 'https://jobs.eu.lever.co/ascentcore/' + i['id']
            location = i['categories']['location']

            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "Ascentcore",
                "country": "Romania",
                "city": location
            })
    return lst_with_data


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Ascentcore'
data_list = collect_data_from_ascentcore()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Ascentcore',
                  "https://rest.techbehemoths.com/storage/images/users/main/company-avatar-6426f04f259ed-x2.png"
                  ))

