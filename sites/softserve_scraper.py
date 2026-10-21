#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> SoftServe
# Link ------> https://career.softserveinc.com/en-us/vacancies/country-romania
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
import time

import requests

from __utils import (
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

# The career site is behind Imperva/Incapsula. From time to time it answers
# with its html challenge page instead of the json payload, so every request
# is repeated until the json answer shows up.
MAX_ATTEMPTS = 6
WAIT_BETWEEN_ATTEMPTS = 3
WAIT_BETWEEN_PAGES = 1
REQUEST_TIMEOUT = 60

session = requests.Session()


def get_dynamic_headers(page: str):
    '''
    >>>>> This function make dynamic headers for SoftServe.

    params: page: str -> its mean page for referer.
    return: url, headers
    '''

    url = f'https://career.softserveinc.com/en-us/vacancy/search?country[]=romania&page={page}'

    headers = {
        'authority': 'career.softserveinc.com',
        'accept': 'application/json, text/plain, */*',
        'referer': f'https://career.softserveinc.com/en-us/vacancies/country-romania/page-{page}',
    }

    return url, headers


def get_api_data(url: str, headers: dict):
    '''
    >>>>> Request the json API and return the parsed payload.
    >>>>> None when the site keeps answering with the Incapsula challenge.
    '''

    for attempt in range(MAX_ATTEMPTS):
        json_data = None

        try:
            response = session.get(
                url,
                headers=headers,
                verify=False,
                timeout=REQUEST_TIMEOUT,
            )
            json_data = response.json()
        except (requests.RequestException, ValueError):
            json_data = None

        if isinstance(json_data, dict) and isinstance(json_data.get('data'), list):
            return json_data

        # Incapsula challenge page (or a broken answer) -> wait and try again
        time.sleep(WAIT_BETWEEN_ATTEMPTS * (attempt + 1))

    return None


def scraper():
    '''
    ... scrape data from SoftServe scraper.
    '''

    job_list = []
    page = 1
    flag = True
    while flag:

        # make dynamic headers
        url_for_API, headers_for_API = get_dynamic_headers(str(page))

        json_data = get_api_data(url_for_API, headers_for_API)

        if json_data is None:
            # the API is not answering right now -> stop with what we have
            break

        jobs_on_page = json_data.get('data', [])

        if jobs_on_page:
            for job in jobs_on_page:
                #
                job_type = job.get('remote')

                # get jobs items from response
                job_list.append(Item(
                    job_title=job.get('name'),
                    job_link=job.get('url'),
                    company='SoftServe',
                    country='Romania',
                    county='',
                    city='',
                    remote='remote' if job_type == 1 else 'on-site',
                ).to_dict())
        else:
            flag = False

        # the API tells us how many pages hold results
        meta = json_data.get('meta') or {}
        last_page = meta.get('last_page')
        if last_page and page >= last_page:
            flag = False

        page += 1
        time.sleep(WAIT_BETWEEN_PAGES)

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "SoftServe"
    logo_link = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/SoftServe_logo_new.png/1200px-SoftServe_logo_new.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
