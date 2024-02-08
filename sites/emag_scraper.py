#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> eMAG
# Link ------> https://lde.tbe.taleo.net/lde02/ats/careers/v2/searchResults\?org\=EMAG\&cws\=37
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

    # only this time
    GetHeadersDict,
    #
    get_data_with_regex,
    counties,
)
from time import sleep
from random import randint


def get_only_jsession_id():
    '''
    ... get session id for get requests.
    '''
    dict_response = GetHeadersDict('https://lde.tbe.taleo.net/lde02/ats/careers/v2/searchResults?org=EMAG&cws=37')
    match_data_re = get_data_with_regex('JSESSIONID=([a-zA-Z0-9]+);', str(dict_response))

    return match_data_re


# get ID on time for scraping in session
jsession_id_for_session = get_only_jsession_id()


def make_headers(page_count: str):
    '''
        ... this function make headers for get requests to API
        In this function I have parameter "page_count" - it increment with + 10 from 0 -> for pages
    '''

    url = f'https://lde.tbe.taleo.net/lde02/ats/careers/v2/searchResults?next&rowFrom={page_count}&act=null&sortColumn=null&sortOrder=null&currentTime=1707341012108'

    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.6',
        'Connection': 'keep-alive',
        'Cookie': f'{jsession_id_for_session}',
        'Referer': 'https://lde.tbe.taleo.net/lde02/ats/careers/v2/searchResults?org=EMAG&cws=37',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        }
    
    return url, headers


def scraper():
    '''
    ... scrape data from eMAG scraper.
    '''

    job_list = []
    page = 0
    flag = True
    while flag:
        url_header = make_headers(str(page))
        html_data = GetRequestJson(url=url_header[0], custom_headers=url_header[1])

        if len(all_job_elements := html_data.find_all('div', attrs={'class': 'oracletaleocwsv2-accordion oracletaleocwsv2-accordion-expandable clearfix'})) > 0:
            
            for job_data in all_job_elements:
                new_loc = ''
                location = job_data.find('div', attrs={'class': 'oracletaleocwsv2-accordion-head-info'}).find_all('div')[1].text
                for search_city in counties:
                    for k, v in search_city.items():
                        for ccity in v:
                            if ccity.split()[-1].lower(0) in location.lower():
                                new_loc = ccity
                                break

                # find one error
                if new_loc == 'Bucu':
                    new_loc = 'Bucurestiss'

                # find type job
                job_type_f = ''
                if 'remote' in location.lower():
                    job_type_f = 'remote'
                elif 'hybrid' in location.lower():
                    job_type_f = 'hybrid'
                else:
                    job_type_f = 'on-site'
                
                link_title = job_data.find('h4', attrs={'class', 'oracletaleocwsv2-head-title'}).find('a')
                # get jobs items from response
                job_list.append(Item(
                    job_title=link_title.text,
                    job_link=link_title['href'],
                    company='eMAG',
                    country='Romania',
                    county=get_county(new_loc),
                    city=new_loc,
                    remote=job_type_f,
                ).to_dict())
            
        else:
            flag = False

        # increment for new page request
        page += 10

        # sleep for better work
        sleep(randint(1,3))

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "eMAG"
    logo_link = "https://s13emagst.akamaized.net/layout/ro/images/logo//59/88362.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
