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


def get_csrf_token():
    '''
    ... this func return a csrf token from html page
    '''
    return [element for element in 
            get_data_with_regex('"csrfToken":"([a-fA-F0-9]+)"', 
            str(GetStaticSoup('https://careers.fisglobal.com/us/en/search-results?s=1'))).split(':')[-1].split('"')
            if element.strip()][0]


def get_ids_from_site():
    '''
        ... get all needed ids for cod
    '''
    string_regex_data = str(requests.head('https://careers.fisglobal.com/us/en/search-results?s=1').headers)

    play_session = get_data_with_regex('PLAY_SESSION=([a-zA-Z0-9._-]+);', string_regex_data)
    phppe_act = get_data_with_regex('PHPPPE_ACT=([a-fA-F0-9-]+);', string_regex_data)

    return play_session, phppe_act


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

    payload = '{"lang":"en_us","deviceType":"desktop","country":"us","pageName":"search-results","ddoKey":"eagerLoadRefineSearch","sortBy":"","subsearch":"","from":0,"jobs":true,"counts":true,"all_fields":["category","country","state","city","jobType","companyValue","phLocSlider"],"size":100,"clearAll":false,"jdsource":"facets","isSliderEnable":true,"pageId":"page13","siteType":"external","keywords":"","global":true,"selected_fields":{"country":["Romania"]},"locationData":{"sliderRadius":25,"aboveMaxRadius":true,"LocationUnit":"miles"},"s":"1"}'

    return url, headers, payload


def scraper():
    '''
    ... scrape data from FIS scraper.
    '''
    # __call__ here the hedears
    data_with_headers = prepare_headers()

    post_data = PostRequestJson(url=data_with_headers[0], custom_headers=data_with_headers[1], data_raw=data_with_headers[2])
    
    job_list = []
    for job in post_data.get('eagerLoadRefineSearch').get('data').get('jobs'):

        if (location := job.get('city').lower()) == 'bucharest':
            location = 'Bucuresti'

        location_finish = get_county(location=location)

        # get jobs items from response
        job_list.append(Item(
            job_title=job.get('title'),
            job_link=job.get('applyUrl').replace('apply', ''),
            company='FIS',
            country='Romania',
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
