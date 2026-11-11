#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> Funcom
# Link ------> https://www.funcom.com/funcom-bucharest/
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
    Item,
    UpdateAPI,
)


API_URL = 'https://api.teamtailor.com/v1/jobs'
API_KEY = 'nCvUhI8oZU8a22OS8tNPoJltCnk0IUTRY90ADtLp'
API_VERSION = '20210218'


def prepare_get_headers():
    '''
    ... prepare get headers for request funcom's API
    '''

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://www.funcom.com',
        'Referer': 'https://www.funcom.com/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    return headers


def build_jobs_url(page_number: int):
    '''
    ... build the jobs API url for a page
    '''

    return (
        f'{API_URL}?include=department,locations&page[size]=30&filter[feed]=public'
        f'&page[number]={page_number}&api_version={API_VERSION}&api_key={API_KEY}'
    )


def is_romania_job(job, locations):
    '''
    ... check if a job is located in Romania
    '''

    job_locations = job.get('relationships', {}).get('locations', {}).get('data') or []

    for job_location in job_locations:
        location = locations.get(job_location.get('id'), {})
        location_data = ' '.join(
            str(location.get(field) or '')
            for field in ('name', 'city', 'country')
        ).lower()

        if 'romania' in location_data or 'bucure' in location_data:
            return True

    return False


# use function for better resposnse
def get_job_type_data(remote_status: str):
    '''
    ... convert teamtailor remote status to peviitor job type
    '''

    remote_status = (remote_status or '').strip().lower()

    if remote_status == 'temporary':
        return 'hybrid'
    elif remote_status == 'hybrid':
        return ['remote', 'hybrid']
    elif remote_status == 'fully':
        return 'remote'
    else:
        return 'on-site'


def scraper():
    '''
    ... scrape data from Funcom scraper.
    '''

    headers = prepare_get_headers()

    job_list = []
    page_number = 1
    page_count = 1

    while page_number <= page_count:
        json_data = GetRequestJson(url=build_jobs_url(page_number), custom_headers=headers)

        if not isinstance(json_data, dict):
            break

        page_count = int(json_data.get('meta', {}).get('page-count') or 0)
        included = json_data.get('included') or []

        locations = {
            location.get('id'): location.get('attributes', {})
            for location in included
            if location.get('type') == 'locations'
        }

        for job in json_data.get('data') or []:
            if not is_romania_job(job, locations):
                continue

            attributes = job.get('attributes') or {}
            job_url = job.get('links', {}).get('careersite-job-url')

            # get jobs items from response
            job_list.append(Item(
                job_title=attributes.get('title'),
                job_link=job_url,
                company='Funcom',
                country='Romania',
                county='Bucuresti',
                city='Bucuresti',
                remote=get_job_type_data(attributes.get('remote-status')),
            ).to_dict())

        page_number += 1

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Funcom"
    logo_link = "https://pr.funcom.com/Content/Themes/Funcom/img/Funcom_R_logo_Horz_med.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
