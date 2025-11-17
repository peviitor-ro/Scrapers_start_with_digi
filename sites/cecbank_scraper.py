#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> CECBank
# Link ------> https://www.cec.ro/cariere
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
from __utils import (
    GetRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,

)
#
import re
from time import sleep
import html
from typing import Union


def get_headers() -> tuple:
    '''
    ... This function returns a tuple (url: str, headers: dict) with url and headers
    '''

    url = 'https://mingle.ro/api/boards/careers-page/jobs?company=cec&page=0&pageSize=1000&sort='

    headers = {
        'accept': 'application/json',
        'accept-language': 'ro',
        'content-type': 'application/json',
        'origin': 'https://cec.mingle.ro',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-utc-offset': '180',
        'x-zone-id': 'Europe/Bucharest',
    }

    return url, headers


def scraper():
    '''
    ... scrape data from CECBank scraper.
    '''

    url, headers = get_headers()

    job_list    = []

    jobs_from_api = GetRequestJson(url=url, custom_headers=headers)
    
    for job in jobs_from_api.get('data').get('results'):
        title       = job.get('title')
        if title:
            title   = html.unescape(title)
            title   = title.strip()

        link_uid    = job.get('uid')
        #
        location        = None
        try:
            location_brut   = job.get('locations')[0].get('label')
            if location_brut:
                location = location_brut
                if ';' in location:
                    location = location.replace(';', '')
        except (IndexError, TypeError, AttributeError):
            location = None
        
        # # # Get correct location
        if location is not None:
            if location == 'Bucharest':
                location = 'Bucuresti'

        # GET correct county and city
        location_finish = get_county(location=location)

        county  = ''
        city    = ''

        try:
            county_brut     = location_finish[0] if location_finish else None
            if county_brut:
                county      = county_brut.strip()
        except (IndexError, TypeError, AttributeError):
            county = ''
        #
        try:
            city_brut       = 'all' if location and location_finish and location.lower() == location_finish[0].lower()\
                                and 'bucuresti' != location.lower()\
                                    else location
            if city_brut:
                city        = city_brut.strip()
        except (IndexError, TypeError, AttributeError):
            city = ''

        # get jobs items from response
        job_list.append(Item(
            job_title=title,
            job_link=f"https://cec.mingle.ro/en/apply/{link_uid}",
            company='CECBank',
            country='Romania',
            county=county,
            city=city,
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "CECBank"
    logo_link = "https://cdn.mingle.ro/media/cec/img/93007091589.png?response-content-disposition=inline%3B+filename%3D%22logo_cec.png%22&Expires=1725694631&Signature=ZHKhaBUyEpB9GppMCNDNWg5rkHXrXlCtaiLRuzrbKu58SEnOBt0susjkGDEA1eltto4DWqLoz~S2hvpOmYvuyq4PdX1yF3lm-nBU8RX1jpJ5JuVoQr7v1y1ZITrYN8CM9VmAb4kMsfRCAz3dy9p5nDJLSk~tWeu-s06eosBjrpX000-QqP8JQHbEehhlB9MO1MRbHgJ5xQd6xjrf7u2cehFT7y7XC8dGOLO6FhTyrfJq9t8BxiIP26LR1S6cABcGd4geMdE5Uq~u5rjc4gJEMr6zBZ2OF0x-Wj8lYJo8OlUzp5n4AVQOBHrSjE6U0XZGo7wlNVfMvuiiU8KNB8SQvg__&Key-Pair-Id=K2ZGK0W1NCXI8F"

    jobs = scraper()
    print(jobs)
    
    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
