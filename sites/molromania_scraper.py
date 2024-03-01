#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> MOLRomania
# Link ------> https://molgroup.taleo.net/careersection/external/jobsearch.ftl\?lang\=en\&location\=4505100397
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
)

def prepare_post_headers():
    '''
    ... make headers for post request
    '''

    url = 'https://molgroup.taleo.net/careersection/rest/jobboard/searchjobs?lang=en&portal=8205100397'

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/json',
        'Origin': 'https://molgroup.taleo.net',
        'Referer': 'https://molgroup.taleo.net/careersection/external/jobsearch.ftl?lang=en&location=4505100397',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'tz': 'GMT+02:00',
        'tzname': 'Europe/Bucharest',
    }

    data_raw = {"multilineEnabled":"false","sortingSelection":{"sortBySelectionParam":"3","ascendingSortingOrder":"false"},"fieldData":{"fields":{"KEYWORD":"","LOCATION":"4505100397","ORGANIZATION":""},"valid":"true"},"filterSelectionParam":{"searchFilterSelections":[{"id":"LOCATION","selectedValues":[]},{"id":"JOB_FIELD","selectedValues":[]},{"id":"JOB_SCHEDULE","selectedValues":[]},{"id":"ORGANIZATION","selectedValues":[]}]},"advancedSearchFiltersSelectionParam":{"searchFilterSelections":[{"id":"LOCATION","selectedValues":[]},{"id":"JOB_FIELD","selectedValues":[]},{"id":"JOB_LEVEL","selectedValues":[]},{"id":"JOB_TYPE","selectedValues":[]},{"id":"JOB_NUMBER","selectedValues":[]}]},"pageNo":1}

    return url, headers, data_raw


def scraper():
    '''
    ... scrape data from MOLRomania scraper.
    '''

    url, headers, data_raw = prepare_post_headers()
    post_data = PostRequestJson(url=url, custom_headers=headers, data_json=data_raw)

    job_list = []
    for job in post_data.get('requisitionList'):

        new_city = ''
        if (location := job.get('column')[1].lower().split('"')):
            
            if len((new_location := location[1].split('-'))) == 2:
                if 'romania' in new_location:
                    new_city = new_location[-1]
            elif len(new_location) == 3:
                new_city = '-'.join([element.title() for element in new_location[1:]])
            elif len(new_location) == 1:
                    if 'romania' in new_location:
                        new_city = 'all'
                    elif 'multiple locations' in new_location:
                        new_city = 'all'

        location_finish = get_county(location=new_city)

        # get jobs items from response
        job_list.append(Item(
            job_title=job.get('column')[0],
            job_link=f"https://molgroup.taleo.net/careersection/external/jobdetail.ftl?job={job.get('jobId')}&tz=GMT%2B02%3A00&tzname=Europe%2FBucharest",
            company='MOLRomania',
            country='Romania',
            county=(
                    'all' if 'all' in location_finish else
                    location_finish[0] if location_finish and isinstance(location_finish[0], str) else
                    None
                ),
            city='all' if new_city.lower() == 'all' else new_city.title(),
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "MOLRomania"
    logo_link = "https://molromania.ro/img/logo-mol-colorful.88751645.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
