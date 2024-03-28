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
from __utils import (
    GetRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
    #
    GetHeadersDict,
)
import re


def get_dynamic_ids():
    '''
    >>>>>>> This function return dynamic ids for SoftServe.

    params: None
    return: tuple[str] -> XSRF_token, softserve_session, vis_incap_id
    '''

    headers_string = str(GetHeadersDict('https://career.softserveinc.com/en-us/vacancies/country-romania'))

    XSRF_token = re.search(r'XSRF-TOKEN=([^;]+)', headers_string).group(1)
    softserve_session = re.search(r'softserve_session=([^;]+)', headers_string).group(1)
    vis_incap_id = re.search(r'2401886=([^;]+)', headers_string).group(1)

    return XSRF_token, softserve_session, vis_incap_id


# call keys one time
XSRF_token, softserve_session, vis_incap_id = get_dynamic_ids()


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
        'cookie': f'incap_ses_1083_2401886={vis_incap_id}; XSRF-TOKEN={XSRF_token}; softserve_session={softserve_session}',
        'referer': f'https://career.softserveinc.com/en-us/vacancies/country-romania/page-{page}',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    return url, headers


def scraper():
    '''
    ... scrape data from SoftServe scraper.
    '''

    job_list = [] # stored data jobs
    page = 1
    flag = True
    while flag:

        # make dynamic headers
        url_for_API, headers_for_API = get_dynamic_headers(str(page))
        
        # make req with new headers
        if len(json_data := GetRequestJson(url=url_for_API, custom_headers=headers_for_API).get('data')) > 0:

            for job in json_data:
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

        page += 1

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
