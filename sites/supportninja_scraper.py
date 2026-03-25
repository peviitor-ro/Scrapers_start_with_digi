#
#
# Config for Dynamic Get Method -> For JSON format.
#
# Company ---> SupportNinja
# Link ------> https://www.supportninja.com/careers
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


CAREERS_URL = "https://www.supportninja.com/careers"
ADP_BASE_URL = "https://workforcenow.adp.com"
CLIENT_ID = "41a778b2-3a5e-42c7-9770-87f62458fb3e"
CAREER_CENTER_ID = "9200871461420_2"
LOCALE = "en_US"


def get_adp_headers():
    return {
        'Accept-Language': LOCALE,
        'locale': LOCALE,
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json',
        'x-forwarded-host': 'www.supportninja.com',
        'Referer': (
            'https://workforcenow.adp.com/mascsr/default/mdf/recruitment/'
            f'recruitment.html?cid={CLIENT_ID}&ccId={CAREER_CENTER_ID}&lang={LOCALE}'
        ),
    }


def get_adp_query_params():
    return {
        'client': '',
        'lang': LOCALE,
        'cid': CLIENT_ID,
        'ccId': CAREER_CENTER_ID,
        'locale': LOCALE,
        'timeStamp': '123',
    }


def get_jobs_data():
    '''
    ... get SupportNinja Romania jobs from ADP endpoint.
    '''
    return GetRequestJson(
        url=(
            f'{ADP_BASE_URL}/mascsr/default/careercenter/public/events/'
            'staffing/v1/job-requisitions?'
            f'client=&lang={LOCALE}&cid={CLIENT_ID}&ccId={CAREER_CENTER_ID}'
            f'&locale={LOCALE}&timeStamp=123'
        ),
        custom_headers=get_adp_headers(),
    )


def get_job_link(job_id):
    return (
        f'{ADP_BASE_URL}/mascsr/default/mdf/recruitment/recruitment.html?'
        f'cid={CLIENT_ID}&ccId={CAREER_CENTER_ID}&jobId={job_id}&lang={LOCALE}'
    )


def scraper():
    '''
    ... scrape data from SupportNinja scraper.
    '''
    jobs_data = get_jobs_data()
    job_requisitions = jobs_data.get('jobRequisitions') or []

    job_list = []
    for job in job_requisitions:
        locations = job.get('requisitionLocations') or []
        if not locations:
            continue

        location_name = locations[0].get('nameCode', {}).get('shortName', '')
        if 'romania' not in location_name.lower():
            continue

        job_list.append(Item(
            job_title=job.get('requisitionTitle'),
            job_link=get_job_link(job.get('itemID')),
            company='SupportNinja',
            country='Romania',
            county='',
            city='Remote',
            remote='remote',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "SupportNinja"
    logo_link = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcScT6uVfDSUz9ligU2zZ2SDNLo_mQY8KcpkTdpLoSwLqIGLtcugPlOeXtViRLIgW5jMFcY"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
