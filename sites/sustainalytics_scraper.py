#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> Sustainalytics
# Link ------> https://careers.morningstar.com/sustainalytics/us/en/home
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
    #
    GetRequestJson, # for another locations need to make GetRequestJson
    #
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
    #
    GetHeadersDict,
    #
    counties,
)
#
import re
from typing import Union


def make_dict_jobs_dict(title: str,
                        job_link: str,
                        county: Union[str | list],
                        city: Union[str | list]):
    '''
    >>> >>> >>> this function make dict for SustainAnalytics API --->

    params: title: str, job_link: str, county: str, city: str
    return: dict[str, str]
    '''

    # get jobs items from response
    return  Item(
                job_title=title,
                job_link=job_link,
                company='Sustainalytics',
                country='Romania',
                county=county,
                city=city,
                remote=['on-site', 'remote'],
            ).to_dict()


def get_special_keys():
    '''
    >>> >>> >>> Get special keys from MyWorkDayJobs ---> Sustainanalytics <---

    params: None
    return: play_session: str,
            wday_vps_cookie: str,
            __cflb: str,
            wd_browser_id: str,
            calypso_csrf_token: str,
    '''

    str_headers = str(GetHeadersDict('https://morningstar.wd5.myworkdayjobs.com/en-US/Sustainalytics/jobs?locations=0e19b52288b5019ff735e44eda00fe40&locations=0e19b52288b501a1c52ad54eda00f640'))

    new_dict = dict(wday_vps_cookie=r'wday_vps_cookie=([^;]+)',
                    PLAY_SESSION='PLAY_SESSION=([^;]+)',
                    wd_broser_id='wd-browser-id=([^;]+)',
                    CALYPSO_CSRF_TOKEN='CALYPSO_CSRF_TOKEN=([^;]+)')

    # catch data from requests and store it in new dict
    regex_dict = dict()
    for key, value in new_dict.items():
        match = re.search(value, str_headers)
        if match:
            regex_form = match.group(1)
            regex_dict[key] = regex_form

    return regex_dict


# all of this keys need to store in one Session # # # SESION KEYS FOR COOKIES # # # 
keys_dict_ids = get_special_keys()


def get_dynamic_headers(all_jobs: str=None, one_job_info: str=None):
    '''
    >>> >>> >>> get dynamic headers to scrape MyWorkDayJobs API ---> 
    >>> >>> >>> But, params need to be one True and one False, not both True

    params: all_jobs: str=None, one_job_info: str=None
    return: url: str, headers: dict, payload: json
    '''

    # check if params not both True
    url = None
    if all_jobs is not None:
        url = f'https://morningstar.wd5.myworkdayjobs.com/wday/cxs/morningstar/Sustainalytics{all_jobs}'
    elif one_job_info is not None:
        url = f'https://morningstar.wd5.myworkdayjobs.com/wday/cxs/morningstar/Sustainalytics{one_job_info}'
    else:
        raise ValueError("'all_jobs' and 'one_job_info' can not be True both.")

    headers = {
        'authority': 'morningstar.wd5.myworkdayjobs.com',
        'accept': 'application/json',
        'accept-language': 'en-US',
        'content-type': 'application/json',
        'cookie': f"PLAY_SESSION={keys_dict_ids.get('PLAY_SESSION')}; wday_vps_cookie={keys_dict_ids.get('wday_vps_cookie')}; timezoneOffset=-120; wd-browser-id={keys_dict_ids.get('wd_broser_id')}; CALYPSO_CSRF_TOKEN={keys_dict_ids.get('CALYPSO_CSRF_TOKEN')};",
        'origin': 'https://morningstar.wd5.myworkdayjobs.com',
        'referer': f'https://morningstar.wd5.myworkdayjobs.com/en-US/Sustainalytics{"/jobs?locations=0e19b52288b5019ff735e44eda00fe40&locations=0e19b52288b501a1c52ad54eda00f640" if all_jobs is not None else one_job_info }',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'x-calypso-csrf-token': f"{keys_dict_ids.get('CALYPSO_CSRF_TOKEN')}",
    }

    json_data = {
        'appliedFacets': {
            'locations': [
                '0e19b52288b5019ff735e44eda00fe40',
                '0e19b52288b501a1c52ad54eda00f640',
            ],
        },
        'limit': 20,
        'offset': 0,
        'searchText': '',
    }

    #
    if all_jobs is not None:
        return url, headers, json_data
    else:
        return url, headers


def scraper():
    '''
    ... scrape data from Sustainalytics scraper.
    '''
    
    url, headers, json_data = get_dynamic_headers(all_jobs='/jobs') # need scrape all_jobs

    post_data = PostRequestJson(url=url, custom_headers=headers, data_json=json_data)

    job_list = []
    for job in post_data.get('jobPostings'):

        location: Union[str, list] = None
        if (location := job.get('locationsText').lower()) == 'bucharest':
            location = 'bucuresti'
        elif '2 locations' == location:
            
            # # # # # HERE MAKE ANOTHER REQUEST TO JOB PAGE INFO AND SCRAPE ACCURATE LOCATION # # # # # #
            # Make headers for 
            url_get, headers_get = get_dynamic_headers(one_job_info=job.get('externalPath'))
            json_get_data = GetRequestJson(url=url_get, custom_headers=headers_get)

            #
            location = list()
            loc = None
            if (loc := json_get_data.get('jobPostingInfo').get('location').lower()) == 'bucharest' or loc == 'timisoara':
                if loc == 'bucharest':
                    loc = 'bucuresti'
                
                # to lower()
                loc = loc.lower()
                #
                location.append(loc)

            # additional locations
            for job_sec in json_get_data.get('jobPostingInfo').get('additionalLocations'):
                new_loc = None
                for search_city in counties:
                    for v in search_city.values():
                        for ccity in v:
                            if re.search(r'\b{}\b'.format(re.escape(ccity.split()[-1].lower())), job_sec.lower()):
                                new_loc = ccity.lower()
                                break

                if new_loc:
                    location.append(new_loc)
            
        #
        if type(location).__name__ == 'str':
            #
            location_finish = get_county(location=location)
            #
            job_list.append(make_dict_jobs_dict(title=job.get('title'),
                                                job_link=f"https://morningstar.wd5.myworkdayjobs.com/en-US/Sustainalytics{job.get('externalPath')}",
                                                county=location_finish[0] if True in location_finish else None,
                                                city=location.title()))
        #
        elif type(location).__name__ == 'list' and len(location) == 1:
            #
            location_finish = get_county(location=location[0])
            #
            job_list.append(make_dict_jobs_dict(title=job.get('title'),
                                                job_link=f"https://morningstar.wd5.myworkdayjobs.com/en-US/Sustainalytics{job.get('externalPath')}",
                                                county=location_finish[0] if True in location_finish else None,
                                                city=location[0].title()))
        #
        elif type(location).__name__ == 'list' and len(location) > 1:
            #
            location_finish = [get_county(location=city_jud) for city_jud in location]
            get_locations_with_none = [location_finish[0] if True in location_finish else None for location_finish in location_finish]
            #
            job_list.append(make_dict_jobs_dict(title=job.get('title'),
                                                job_link=f"https://morningstar.wd5.myworkdayjobs.com/en-US/Sustainalytics{job.get('externalPath')}",
                                                county=None if None in get_locations_with_none else get_locations_with_none,
                                                city=[xx.title() for xx in location]))
    #
    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Sustainalytics"
    logo_link = "https://www.sgs.com/-/media/sgscorp/images/infographics-and-charts/sustainalytics-logo.cdn.en-US.1.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
