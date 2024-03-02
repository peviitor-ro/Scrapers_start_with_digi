#
#
# Your custom scraper here ---> Last level!
#
# Company ---> OrionInnovation
# Link ------> https://www.orioninc.com/careers/jobs/\?_job_location\=romania
#
#
# Aici va invit sa va creati propriile metode de scraping cu Python,
# ... folosind:
# -> requests
# -> BeautifulSoup
# -> requests_html etc.
#
from __utils import (
    Item, 
    GetHtmlSoup, 
    get_county,
    UpdateAPI
)

import requests
# from requests_html import HTMLSession


def prepare_headers():
    '''
    ... prepare post requests headers, cookies and paramas for OrionInnovation
    '''
    cookies = {
        '_icl_visitor_lang_js': 'en_us',
        'wp-wpml_current_language': 'en',
        'wpml_browser_redirect_test': '0',
    }

    headers = {
        'authority': 'www.orioninc.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.8',
        'content-type': 'application/json',
        # 'cookie': '_icl_visitor_lang_js=en_us; wp-wpml_current_language=en; wpml_browser_redirect_test=0',
        'origin': 'https://www.orioninc.com',
        'referer': 'https://www.orioninc.com/careers/jobs/?_job_location=romania',
        'sec-ch-ua': '"Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    params = {
        '_job_location': 'romania',
    }

    json_data = {
        'action': 'facetwp_refresh',
        'data': {
            'facets': {
                'job_category': [],
                'job_location': [
                    'romania',
                ],
                'job_work_type': [],
            },
            'frozen_facets': {},
            'http_params': {
                'get': {
                    '_job_location': 'romania',
                },
                'uri': 'careers/jobs',
                'url_vars': {
                    'job_location': [
                        'romania',
                    ],
                },
                'lang': 'en',
            },
            'template': 'wp',
            'extras': {
                'sort': 'default',
            },
            'soft_refresh': 0,
            'is_bfcache': 1,
            'first_load': 0,
            'paged': 1,
        },
    }

    return cookies, headers, params, json_data


def scraper():
    '''
    ... scrape data from OrionInnovation scraper.
    Your solution!
    '''
    cookies, headers, params, json_data = prepare_headers()
    response = GetHtmlSoup(requests.post('https://www.orioninc.com/careers/jobs/',\
                                         params=params, cookies=cookies, headers=headers,\
                                            json=json_data).json().get('template'))
    job_list = []
    for job in response.select('article.teaser.teaser-search.col-12'):
        title_link = job.select_one('a.article-title')
        
        # get location
        if (location := [element.strip() for element in\
                                   job.select_one('div.location').text.split('\n')\
                                    if element.strip()][-1].lower()) == 'bucharest':
            location = 'Bucuresti'

        # get job type
        job_type = [element.strip() for element in job.select_one('div.work-type').text.split(':')\
                    if element.strip()][-1]
                                
        location_finish = get_county(location=location)

        # get jobs items from response
        job_list.append(Item(
            job_title=title_link.text,
            job_link=f"https://www.orioninc.com{title_link['href']}",
            company='OrionInnovation',
            country='Romania',
            county=location_finish[0] if True in location_finish else None,
            city='all' if location.lower() == location_finish[0].lower()\
                        and True in location_finish and 'bucuresti' != location.lower()\
                            else location,
            remote=job_type.lower(),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "OrionInnovation"
    logo_link = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2YqNIJOYvfWussTm2Nc-aWi7wOXTCNXvhX48cNWMhRA&s"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
