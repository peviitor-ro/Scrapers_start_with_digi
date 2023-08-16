#
#
#
# New scraper for -> Eurofins
# Acronis job page -> https://careers.eurofins.com/ro/
# Acronis API call -> https://atsintegration.eurofins.com/ATSWebService.asmx/GetJobs?language=ro
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
import uuid


url ='https://atsintegration.eurofins.com/ATSWebService.asmx/GetJobs?language=ro'
company = 'Eurofins'


def eurofins():
    response = requests.get(url, headers=DEFAULT_HEADERS).json()

    payload = []
    for job in response:
        title = job.get('title')
        link = job.get('applyUrl')
        city = job.get('locationCity')
        country = job.get('countryName')
        payload.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": link,
                    "company": company,
                    "country": country,
                    "city": city
                    })

    return payload


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = company
data_list = eurofins()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo(company,
                  'https://cdnmedia.eurofins.com/corporate-eurofins/media/1004/logo.png'
                  ))
