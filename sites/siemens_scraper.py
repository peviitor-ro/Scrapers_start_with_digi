#
#
#
#new scraper for -> SIEMENS
#URL -> https://jobs.siemens.com/api/apply/v2/jobs?domain=siemens.com&start=0&num=10&location=Romania&domain=siemens.com&sort_by=relevance



company = 'siemens'
url = 'https://jobs.siemens.com/api/apply/v2/jobs?domain=siemens.com&start=0&num=10&location=Romania&domain=siemens.com&sort_by=relevance'

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo

import requests
import uuid


def siemens():
    response = requests.get(url, headers=DEFAULT_HEADERS).json()
    count=response.get('count')//10+1
    payload = [] 
    for i in range(0,count+1):
        y=i*10
        url_x='https://jobs.siemens.com/api/apply/v2/jobs?domain=siemens.com&start='+str(y)+'&num=10&location=Romania&domain=siemens.com&sort_by=relevance'
        responsejob = requests.get(url_x, headers=DEFAULT_HEADERS).json()['positions']
        
        for job in responsejob:
            title = job.get('name')
            link = 'https://jobs.siemens.com/careers/job?domain=siemens.com&pid='+str(job.get('id'))
            city = job.get('locations')
            country = job.get('location').split(',')[-1]
            payload.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": link,
                    "company": company,
                    "country": country,
                    "city": city
                    }
                )

    return payload


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = company
data_list = siemens()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo(company,
                  'https://1000logos.net/wp-content/uploads/2021/11/Siemens-logo-500x281.png'
                  ))
