#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> Siemens
# Link ------> https://jobs.siemens.com/careers\?location\=Romania\&pid\=563156119178765\&domain\=siemens.com\&sort_by\=relevance\&triggerGoButton\=true
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
    remove_diacritics,
    Item,
    UpdateAPI,
    #
    GetHeadersDict,
)


def get_ids():
    '''
    ... Get ids from site: _vs, traceID

    params: None
    return: _vs: str, traceID: str
    '''

    keys_data = GetHeadersDict('https://jobs.siemens.com/careers?location=bucharest%2B&pid=563156118434737&domain=siemens.com&sort_by=relevance&triggerGoButton=false')

    _vsID = keys_data.get('Set-Cookie').split()[0]
    traceID = keys_data.get('X-EF-Trace-ID')

    return _vsID, traceID


# get ids on time, for one session
_vsID, traceID = get_ids()


def make_headers(star_page: str):
    '''
    ... make headers ---> for get Siemens's API.

    params: start_page: str
    return: url, headers
    '''

    url = f'https://jobs.siemens.com/api/apply/v2/jobs?domain=siemens.com&start={star_page}&num=10&exclude_pid=563156119178765&location=Romania&pid=563156119178765&domain=siemens.com&sort_by=relevance&triggerGoButton=true'

    headers = {
        'authority': 'jobs.siemens.com',
        'accept': '*/*',
        'content-type': 'application/json',
        'cookie': f's_cc=true; {_vsID} _vscid=1',
        'referer': 'https://jobs.siemens.com/careers?location=Romania&pid=563156119178765&domain=siemens.com&sort_by=relevance&triggerGoButton=true',
        'sentry-trace': f'{traceID}',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    return url, headers


def scraper():
    '''
    ... scrape data from Siemens scraper.
    '''

    count = 0

    job_list = []
    page = 0 # increment +10 and send str type to function make_headers
    flag = True
    while flag:
        url, headers = make_headers(str(page))
        if len(json_job_data := GetRequestJson(url=url, custom_headers=headers).get('positions')) > 0:
            for job in json_job_data:

                # collect all data about locations
                location_towns = list()
                #location_counties = list()
                if (location := job.get('location').lower().split(',')) and 'romania' in location:
                    if 'bucharest' in location:
                        location_towns.append('Bucuresti')
                        #location_counties.append('Bucuresti')

                    # add it to default
                    location_towns.append(location[0].title())
                    #location_counties.append(location_counties[1].title())

                # data - search data in locations - list with locations from API
                else:
                    locations_else = ['cluj', 'bucharest', 'timis', 'iasi', 'sibiu', 'brasov', 'bucuresti', 'craiova',]
                    for another_loc in job.get('locations'):
                        for city_ro in locations_else:
                            if (city_ro := remove_diacritics(city_ro)) and city_ro in another_loc.lower():
                                # ...
                                city_ro = remove_diacritics(another_loc.split(',')[0])
                                if city_ro.lower() == 'bucharest':
                                    city_ro = 'Bucuresti'
                                location_towns.append(city_ro)

                # logic to catch towns ---> !
                if location_towns:

                    # get locations --->
                    location_towns = list(set(location_towns))
                    job_counties = [get_county(city_ro) for city_ro in location_towns]
                    get_locations_with_none = [location_finish[0] if True in location_finish else None for location_finish in job_counties]

                    # get jobs items from response
                    job_list.append(Item(
                        job_title=job.get('name'),
                        job_link=f"https://jobs.siemens.com/careers?location=Romania&pid={job.get('id')}&domain=siemens.com&sort_by=relevance&triggerGoButton=true",
                        company='Siemens',
                        country='Romania',
                        county=None if any(x is None for x in get_locations_with_none) else (get_locations_with_none[0] if len(get_locations_with_none) == 1 else get_locations_with_none),
                        city=location_towns[0] if len(location_towns) == 1 else location_towns,
                        remote=job.get('work_location_option').split('_')[0],
                    ).to_dict())

        else:
            flag = False

        page += 10



    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Siemens"
    logo_link = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRy4X0h4JCY_Ex39Rq7sl1kIf4yXaF6In_BxJjl24CHFg&s"

    jobs = scraper()
    print(len(jobs))

    # uncomment if your scraper done
    # UpdateAPI().update_jobs(company_name, jobs)
    # UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
