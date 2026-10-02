#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> Spyrosoft
# Link ------> https://spyro-soft.com/career?area=all&skills=all&location=romania&experience=all
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
    #
    counties,
)
import requests
import re


def get_static_headers():
    '''
    >>>>>>>> Make GET request for JSON

    return: url: str, headers: dict, payload:
    '''
    # params are in the url
    url = 'https://spyro-soft.com/wp-json/teamtailor/v1/get-jobs?skills=all&locations=1206845&experience=all&page=1&per_page=50'

    headers = {
        'authority': 'spyro-soft.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.5',
        'origin': 'https://spyro-soft.com',
        'referer': 'https://spyro-soft.com/career?area=all&skills=all&location=romania&experience=all',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    return url, headers


def scraper():
    '''
    ... scrape data from Spyrosoft scraper.
    '''

    url, headers = get_static_headers()

    job_list = []
    for job in GetRequestJson(url=url, custom_headers=headers).get("jobs", []):

        # get location ----> and filter for location
        location = job['loc'][0]['name_raw'].lower().strip()
        new_loc = None
        for search_city in counties:
            for v in search_city.values():
                for ccity in v:
                    if re.search(r'\b{}\b'.format(re.escape(ccity.split()[-1].lower())), location.lower()):
                        new_loc = ccity
                        break

        # get correct location
        if new_loc != None:
            location_finish = get_county(location=new_loc)
        else:
            location_finish = 'all'

        # parse employment type
        match job['remote_status']:
                case 'fully':
                    remoteStat = 'remote'
                case 'hybrid':
                    remoteStat = 'hybrid'
                case 'on-site':
                    remoteStat = 'on-site'
                case _:
                    remoteStat = '-'
                    
        # get jobs items from response
        job_list.append(Item(
            job_title = job['title'],
            job_link = job['url'],
            company = 'Spyrosoft',
            country = 'Romania',
            county = 'all' if location_finish == 'all' else (location_finish[0] if True in location_finish else None),
            city = 'all' if location_finish == 'all' else (location_finish[0] if location_finish != 'all'\
                                                        and True not in location_finish else new_loc),
            remote = remoteStat,
        ).to_dict())
    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Spyrosoft"
    logo_link = "https://spyro-soft.com/wp-content/uploads/2022/06/spyrosoft_color_rgb.png"

    jobs = scraper()

    # # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
