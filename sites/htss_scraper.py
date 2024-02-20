#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> HTSS
# Link ------> https://ro.htssgroup.eu/cariere/
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
)


def prepare_get_headers():
    '''
    ... prepare headers for get request'''

    url = 'https://mingle.ro/api/boards/mingle/jobs?q=companyUid~eq~%22htss%22&page=0&pageSize=30&sort=modifiedDate~DESC'

    headers = {
        'authority': 'mingle.ro',
        'accept': 'application/json',
        'content-type': 'application/json',
        'origin': 'https://htss.mingle.ro',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'x-utc-offset': '120',
        'x-zone-id': 'Europe/Bucharest',
    }

    return url, headers


def scraper():
    '''
    ... scrape data from HTSS scraper.
    '''

    url, headers = prepare_get_headers()
    json_data = GetRequestJson(url=url, custom_headers=headers)

    job_list = []
    for job in json_data.get('data').get('results'):

        job_type = ''
        location_city = ''
        if (data_locations := job.get('locations')) != None:          
            if len(data_locations) > 1:
                job_type = 'remote' if 'remote' in data_locations[0].get('name').lower() else data_locations[1].get('name').split()[0].lower()
                location_city = data_locations[0].get('name').lower() if 'remote' not in data_locations[0].get('name').lower() else data_locations[1].get('name')
            else:
                job_type = 'on-site'
                location_city = data_locations[0].get('name')

        if job_type == '' and location_city == '':
            job_type = 'on-site'
            location_city = 'Bucuresti'

        if location_city.lower() == 'bucharest':
            location_city = 'Bucuresti'

        # get jobs items from response
        job_list.append(Item(
            job_title=job.get('jobTitle'),
            job_link=f'https://htss.mingle.ro/en/embed/apply/{job.get("publicUid")}',
            company='HTSS',
            country='Romania',
            county=get_county(location_city.title()),
            city=location_city.title(),
            remote=job_type,
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "HTSS"
    logo_link = "logo_link"

    jobs = scraper()
    print(jobs, len(jobs))

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
