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

    url = 'https://mingle.ro/api/boards/careers-page/jobs?company=htss&location=195&location=3197&page=0&pageSize=30&sort='

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
        
        # location and type job
        location = None
        job_type = None
        if len((data_locations := job.get('locations'))) == 1:
            if (new_location := data_locations[0].get('label')) and 'remote' not in new_location.lower():
                if new_location.lower() == 'bucharest':
                    location = 'Bucuresti'
                location = new_location
                job_type = 'on-site'

        elif len(data_locations) > 1:
            if (new_location := data_locations[0].get('label')) and 'remote' not in new_location.lower():
                location = new_location
                job_type = data_locations[1].get('label').split()[0].lower()
            else:
                location = data_locations[1].get('label')
                job_type = data_locations[0].get('label').split()[0].lower()

        # Location from Bucharest to Bucuresti
        if location.lower() == 'bucharest':
            location = 'Bucuresti'

        # function from get county = 
        location_finish = get_county(location=location)

        #get jobs items from response
        job_list.append(Item(
            job_title=job.get('title'),
            job_link=f'https://htss.mingle.ro/en/embed/apply/{job.get("publicUid")}',
            company='HTSS',
            country='Romania',
            county=location_finish[0] if True in location_finish else None,
            city='all' if location.lower() == location_finish[0].lower()\
                        and True in location_finish and 'bucuresti' != location.lower()\
                            else location,
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
    logo_link = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRysC7nnegm3c49Yi7xNjgY3W5JNTxJ3gtSEiBlMQpfLA&s"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
