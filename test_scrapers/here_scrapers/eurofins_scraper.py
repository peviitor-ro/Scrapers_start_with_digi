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
company = 'eurofins'


def run_scraper():
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

    return payload, len(payload)
