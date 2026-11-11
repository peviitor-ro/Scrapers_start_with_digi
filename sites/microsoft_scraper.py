#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> Microsoft
# Link ------> https://apply.careers.microsoft.com/careers?domain=microsoft.com&location=Romania
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
import time

from __utils import (
    GetRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def prepare_get_headers(page: str):
    '''
    ... prepare get headers dict for microsoft company API'''

    page_size = 10
    start = (int(page) - 1) * page_size
    url = f'https://apply.careers.microsoft.com/api/pcsx/search?domain=microsoft.com&query=&location=Romania&start={start}'

    headers = {
        'authority': 'apply.careers.microsoft.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.5',
        'origin': 'https://apply.careers.microsoft.com',
        'referer': 'https://apply.careers.microsoft.com/careers',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    return url, headers


def get_json_with_retries(url: str, headers: dict, attempts: int = 5):
    '''
    ... retry API calls that are temporarily rate limited.
    '''

    for attempt in range(attempts):
        json_data = GetRequestJson(url=url, custom_headers=headers)
        if isinstance(json_data, dict):
            return json_data

        if attempt < attempts - 1:
            time.sleep(min(5 * (2 ** attempt), 60))

    return None


def scraper():
    '''
    ... scrape data from Microsoft scraper.
    '''

    job_list = list()
    seen_jobs = set()
    page = 1
    page_size = 10
    total_jobs = None
    flag = True
    while flag:
        url, headers = prepare_get_headers(str(page))

        json_data = get_json_with_retries(url=url, headers=headers)

        # Check if response is valid JSON and contains expected data
        if not isinstance(json_data, dict) or json_data.get('status') != 200:
            flag = False
            continue

        data = json_data.get('data') or {}
        jobs = data.get('positions') or []
        if total_jobs is None:
            total_jobs = data.get('count') or 0

        if jobs:
            for job in jobs:
                job_id = job.get('id')
                if job_id in seen_jobs:
                    continue
                seen_jobs.add(job_id)

                locations = job.get('locations') or []
                romania_locations = [
                    loc for loc in locations
                    if 'romania' in loc.lower()
                ]
                if not romania_locations:
                    continue

                # logic to catch City and All ---> Start
                set_data_loc = set()
                for loc in romania_locations:
                    if 'multiple locations' in loc.lower():
                        set_data_loc.add('multiple locations')
                    elif 'bucharest' in loc.lower():
                        set_data_loc.add('bucuresti')
                #
                new_loc = ''
                if 'bucuresti' in set_data_loc:
                    new_loc = 'Bucuresti'
                else:
                    new_loc = 'All'
                # logic to catch City and All ---> End

                # here the logic for JobType
                work_option = (job.get('workLocationOption') or '').lower()
                flexibility = (job.get('locationFlexibility') or '').lower()
                if 'remote' in work_option or '100%' in flexibility:
                    job_type = 'remote'
                elif 'hybrid' in work_option or '50%' in flexibility:
                    job_type = 'hybrid'
                else:
                    job_type = 'on-site'
                # here the logic for jobType -------> END

                job_title = (job.get('name') or '').strip()
                position_url = job.get('positionUrl') or f"/careers/job/{job_id}"
                if position_url.startswith('/'):
                    job_link = f'https://apply.careers.microsoft.com{position_url}'
                else:
                    job_link = position_url

                # get jobs items from response
                job_list.append(Item(
                    job_title=job_title,
                    job_link=job_link,
                    company='Microsoft',
                    country='Romania',
                    county='Bucuresti' if new_loc == 'Bucuresti' else 'All',
                    city=new_loc,
                    remote=job_type,
                ).to_dict())
        else:
            flag = False

        if len(jobs) < page_size or (total_jobs is not None and page * page_size >= total_jobs):
            flag = False

        # increment page
        page += 1

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Microsoft"
    logo_link = "https://img-prod-cms-rt-microsoft-com.akamaized.net/cms/api/am/imageFileData/RE1Mu3b?ver=5c31"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()