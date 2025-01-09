#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> Capex
# Link ------> https://capex.com/en/careers
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

    # for on time use
    GetHeadersDict,

    # re
    get_data_with_regex,
)


def get_verification_tokens():
    '''
    ... get verification token site and afinity same site!
    '''

    re_data = GetHeadersDict('https://portal.dynamicsats.com/JobListing/347022b3-2e4e-48d2-9dac-9f7d78675080')

    # get data with request
    request_verification_token = get_data_with_regex('__RequestVerificationToken=([^;]+);', str(re_data))
    afinity_same_site = get_data_with_regex('ARRAffinity=([^;]+);', str(re_data))

    return request_verification_token, afinity_same_site


# ---> Get tokens once - for this time scraping
id_from_function = get_verification_tokens()


def make_headers():
    '''
    ... make headers for post requests
    '''
    url = 'https://portal.dynamicsats.com/JobListing/WebForm/JobListing_Read'

    headers = {
            'authority': 'portal.dynamicsats.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.5',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': f'{id_from_function[0]} {id_from_function[:-1]}',
            'origin': 'https://portal.dynamicsats.com',
            'referer': 'https://portal.dynamicsats.com/JobListing/347022b3-2e4e-48d2-9dac-9f7d78675080',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

    data_raw = {
            'sort': '',
            'group': '',
            'filter': '',
            'formId': '347022b3-2e4e-48d2-9dac-9f7d78675080'
        }

    return url, headers, data_raw


def scraper():
    '''
    ... scrape data from Capex scraper.
    '''

    data_uhp = make_headers()

    job_list = []
    if len(check_json := PostRequestJson(url=data_uhp[0], custom_headers=data_uhp[1], data_raw=data_uhp[2])) > 0:
        for job in check_json['Data']:

            if (location := job.get('dcrs_location').lower().split('-')[0].strip()) and 'bucharest' in location:
                location = "Bucuresti"

                location_finish = get_county(location=location)

                # get jobs items from response
                job_list.append(Item(
                    job_title=job.get('dcrs_jobtitle'),
                    job_link=job.get('JobUrl'),
                    company='Capex',
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

    company_name = "Capex"
    logo_link = "https://capex.com/assets/logo/capex-com-logo-red.svg"

    jobs = scraper()
    print(jobs)

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
