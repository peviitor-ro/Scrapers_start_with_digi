#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> FIS
# Link ------> https://careers.fisglobal.com/us/en/search-results?s=1
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
import json
from __utils import (
    PostRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,

    # for regex
    get_data_with_regex,

    # import StatiClass for get csrf
    GetStaticSoup,
)
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_csrf_token():
    '''
    ... this func return a csrf token from html page
    '''
    response = requests.get('https://careers.fisglobal.com/us/en/search-results?s=1', verify=False)
    soup = BeautifulSoup(response.text, 'lxml')
    return [element for element in
            get_data_with_regex('"csrfToken":"([a-fA-F0-9]+)"',
            str(soup)).split(':')[-1].split('"')
            if element.strip()][0]


def get_ids_from_site():
    '''
        ... get all needed ids for cod
    '''
    string_regex_data = str(requests.head('https://careers.fisglobal.com/us/en/search-results?s=1', verify=False).headers)

    play_session = get_data_with_regex('PLAY_SESSION=([a-zA-Z0-9._-]+);', string_regex_data)
    phppe_act = get_data_with_regex('PHPPPE_ACT=([a-fA-F0-9-]+);', string_regex_data)

    return play_session, phppe_act


def build_payload(selected_fields=None):
    '''
        ... json body for the widgets search request
        (size is capped at 500 by the site; the "from" offset is ignored,
         so this is the biggest slice of the result list we can get)
    '''
    payload = {
        "lang": "en_us",
        "deviceType": "desktop",
        "country": "us",
        "pageName": "search-results",
        "ddoKey": "eagerLoadRefineSearch",
        "sortBy": "",
        "subsearch": "",
        "from": 0,
        "jobs": True,
        "counts": True,
        "all_fields": ["category", "country", "state", "city", "jobType", "companyValue", "phLocSlider"],
        "size": 500,
        "clearAll": False,
        "jdsource": "facets",
        "isSliderEnable": True,
        "pageId": "page13",
        "siteType": "external",
        "keywords": "",
        "global": True,
        "selected_fields": selected_fields or {},
        "locationData": {"sliderRadius": 25, "aboveMaxRadius": True, "LocationUnit": "miles"},
        "s": "1",
    }

    return json.dumps(payload)


def prepare_headers():
    '''
        ... prepare post headers for post requests
    '''
    # get ids
    ids_from_site = get_ids_from_site()

    url = 'https://careers.fisglobal.com/widgets'

    headers = {
        'authority': 'careers.fisglobal.com',
        'content-type': 'application/json',
        'cookie': f'{ids_from_site[0]} VISITED_LANG=en; VISITED_COUNTRY=us; {ids_from_site[1]}',
        'origin': 'https://careers.fisglobal.com',
        'referer': 'https://careers.fisglobal.com/us/en/search-results?s=1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'x-csrf-token': f'{get_csrf_token()}',
    }

    payload = build_payload({"country": ["Romania"]})

    return url, headers, payload


def get_jobs(url, headers, payload):
    '''
        ... post the search request and return the jobs list
    '''
    post_data = requests.post(url, headers=headers, data=payload, verify=False).json()

    return ((post_data.get('eagerLoadRefineSearch') or {}).get('data') or {}).get('jobs') or []


def scraper():
    '''
    ... scrape data from FIS scraper.
    '''
    # __call__ here the hedears
    data_with_headers = prepare_headers()

    job_list_with_headers = get_jobs(data_with_headers[0], data_with_headers[1], data_with_headers[2])

    # the careers site has no jobs left in Romania -> take the full list
    if not job_list_with_headers:
        job_list_with_headers = get_jobs(
            data_with_headers[0], data_with_headers[1], build_payload())

    job_list = []
    for job in job_list_with_headers:

        location = (job.get('city') or job.get('state') or job.get('country') or '').strip()

        if location.lower() == 'bucharest':
            location = 'Bucuresti'

        location_finish = get_county(location=location)

        # get jobs items from response
        job_list.append(Item(
            job_title=job.get('title'),
            job_link=job.get('applyUrl').replace('apply', ''),
            company='FIS',
            country=job.get('country') or 'Romania',
            county=location_finish[0] if True in location_finish else None,
            city='all' if location.lower() == location_finish[0].lower()\
                        and True in location_finish and 'bucuresti' != location.lower()\
                            else location,
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "FIS"
    logo_link = "https://cdn.phenompeople.com/CareerConnectResources/FIGLUS/images/SmallLogoBIv2-1668201955570.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
