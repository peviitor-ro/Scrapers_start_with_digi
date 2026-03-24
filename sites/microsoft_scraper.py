#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> Microsoft
# Link ------> https://gcsservices.careers.microsoft.com/search/api/v1/search?lc=Romania&l=en_us&pg=1&pgSz=20&o=Relevance&flt=true
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


def prepare_get_headers(page: str):
    '''
    ... prepare get headers dict for microsoft company API'''

    url = f'https://gcsservices.careers.microsoft.com/search/api/v1/search?lc=Romania&l=en_us&pg={page}&pgSz=20&o=Relevance&flt=true'

    headers = {
        'authority': 'gcsservices.careers.microsoft.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.5',
        'authorization': 'Bearer undefined',
        'origin': 'https://jobs.careers.microsoft.com',
        'referer': 'https://jobs.careers.microsoft.com/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    return url, headers


def scraper():
    '''
    ... scrape data from Microsoft scraper.
    '''

    job_list = list()
    page = 1
    flag = True
    while flag:
        url, headers = prepare_get_headers(str(page))

        json_data = GetRequestJson(url=url, custom_headers=headers)
        
        # Check if response is valid JSON and contains expected data
        if not isinstance(json_data, dict) or 'operationResult' not in json_data:
            flag = False
            continue
        
        operation_result = json_data.get('operationResult')
        if not operation_result or 'result' not in operation_result:
            flag = False
            continue

        result = operation_result.get('result')
        if not result or 'jobs' not in result:
            flag = False
            continue

        jobs = result.get('jobs')
        if jobs and len(jobs) > 0:
            for job in jobs:
                
                # logic to catch City and All ---> Start
                set_data_loc = set()
                if len(locations := job.get('properties').get('locations')) > 0:
                    for loc in locations:
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

                # here the logic for JobType 0% mean on-site, 50% mean hybrid, 100% mean remote
                job_type = ''
                if (job_type_procent := job.get('properties').get('workSiteFlexibility').lower()):
                    if '100%' in job_type_procent:
                        job_type = 'remote'
                    elif '50%' in job_type_procent:
                        job_type = 'hybrid'
                    elif 'on-site' in job_type_procent:
                        job_type = 'on-site'
                    else:
                        job_type = 'on-site'
                # here the logic for jobType -------> END

                # get jobs items from response
                job_list.append(Item(
                    job_title=job.get('title'),
                    job_link=f"https://jobs.careers.microsoft.com/global/en/job/{job.get('jobId')}/{'-'.join(job.get('title').split())}",
                    company='Microsoft',
                    country='Romania',
                    county='Bucuresti' if new_loc == 'Bucuresti' else 'All',
                    city=new_loc,
                    remote=job_type,
                ).to_dict())
        else:
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