#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> BlackLine
# Link ------> https://careers.blackline.com/careers-home/jobs\?page\=2\&location\=Romania\&woe\=12\&stretchUnit\=MILES\&stretch\=10
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

    # get headers
    GetHeadersDict,
)
import re


def get_keys():
    '''
    ... get keys from site
    '''
    data_headers = GetHeadersDict('https://careers.blackline.com/careers-home/jobs?page=2&location=Romania&woe=12&stretchUnit=MILES&stretch=10')
    n_data = str(data_headers)

    jrasession = re.search('jrasession=([a-fA-F0-9\\-]+);', n_data).group(1)
    jassesion = re.search('jasession=([a-zA-Z0-9%._-]+);', n_data).group(1)

    return jrasession, jassesion


# define here and call one time
data_keys = get_keys()


def get_headers(page: str):
    '''
    ... get headers from site.
    '''


    url = f'https://careers.blackline.com/api/jobs?page={page}&location=Romania&woe=12&stretchUnit=MILES&stretch=10&sortBy=relevance&descending=false&internal=false'
    headers = {
        'authority': 'careers.blackline.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.5',
        'cookie': f'i18n=en-US; searchSource=external; jrasession={data_keys[0]}; jasession={data_keys[1]}; _janalytics_ses.79de=*; _janalytics_id.79de=84147b7a-cd35-4f96-9c73-9c81c95a8df9.1706736342.1.1706736367.1706736342.95d2b4b9-e905-41de-a790-4c2226fd0e10',
        'referer': f'https://careers.blackline.com/careers-home/jobs?page={page}&location=Romania&woe=12&stretchUnit=MILES&stretch=10',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    return url, headers


def scraper():
    '''
    ... scrape data from BlackLine scraper.
    '''

    job_list = list()
    count = 1
    flag = True

    while flag:

        data_h = get_headers(str(count))
        json_data = GetRequestJson(data_h[0], custom_headers=data_h[1])

        if len(json_data['jobs']) > 0:
            for job in json_data['jobs']:
                if job['data']['country'] == "Romania":
                    location = job['data']['location_name']

                    # change Bucharest
                    if location.lower() in ['bucharest']:
                        location = "Bucuresti"

                    job_type = 'on-site'
                    if 'remote' in location.lower():
                        location = 'Bucuresti'
                        job_type = 'remote'
                    elif 'hybrid' in location.lower():
                        job_type = 'hybrid'
                    else:
                        job_type = 'on-site'

                    # location
                    location_finish = get_county(location=location)

                    job_list.append(Item(
                        job_title=job['data']['title'],
                        job_link=f"https://careers.blackline.com/careers-home/jobs/{job['data']['slug']}?lang=en-us",
                        company='BlackLine',
                        country='Romania',
                        county=location_finish[0] if True in location_finish else None,
                        city='all' if location.lower() == location_finish[0].lower()\
                                    and True in location_finish and 'bucuresti' != location.lower()\
                                        else location,
                        remote=job_type,
                    ).to_dict())

        else:
            flag = False

        count += 1

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "BlackLine"
    logo_link = "https://cms.jibecdn.com/prod/blackline/assets/HEADER-NAV_LOGO-en-us-1640926577769.svg"

    jobs = scraper()
    print(jobs, len(jobs))
    # uncomment if your scraper done
    # UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
