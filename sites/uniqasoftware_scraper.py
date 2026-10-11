#
#
#  Basic for scraping data from static pages
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
# Company ---> UNIQA Software Services
# Link ------> https://www.uniqasoftware.ro/join-uss/
#
#
from __utils import (
    GetRequestJson,
    get_county,
    Item,
    UpdateAPI,
)


def prepare_get_headers():
    '''
    ... prepare url and headers for the mingle careers API
    '''

    url = 'https://mingle.ro/api/boards/careers-page/jobs?company=uniqasoftware&page=0&pageSize=100&sort='

    headers = {
        'authority': 'mingle.ro',
        'accept': 'application/json',
        'content-type': 'application/json',
        'origin': 'https://uniqasoftware.mingle.ro',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'x-utc-offset': '120',
        'x-zone-id': 'Europe/Bucharest',
    }

    return url, headers


def scraper():
    '''
    ... scrape data from UNIQA Software Services scraper.
    '''

    url, headers = prepare_get_headers()
    json_data = GetRequestJson(url=url, custom_headers=headers)

    job_list = []
    for job in json_data.get('data', {}).get('results', []):
        title = job.get('title')
        if not title:
            continue
        title = title.strip()

        # location and type job
        location = None
        locations = job.get('locations') or []
        if locations:
            location = locations[0].get('label')

        remote = 'on-site'
        if location and 'remote' in location.lower():
            remote = 'remote'

        # clean location suffix -> keep the pure location for county lookup
        if location:
            location = location.replace('(Remote)', '').replace('(remote)', '').strip()

        location_finish = get_county(location=location)

        # get jobs items from response
        job_list.append(Item(
            job_title=title,
            job_link=f'https://uniqasoftware.mingle.ro/en/apply/{job.get("uid")}',
            company='UNIQA Software Services',
            country='Romania',
            county=location_finish[0] if location_finish and location_finish[0] else None,
            city='all' if location and location_finish and location.lower() == str(location_finish[0]).lower()\
                        and True in location_finish and 'bucuresti' != location.lower()\
                            else location,
            remote=remote,
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "UNIQA Software Services"
    logo_link = "https://www.uniqasoftware.ro/wp-content/uploads/2021/04/120x60.jpeg"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
