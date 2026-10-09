#
#
# Your custom scraper here ---> Last level!
#
# Company ---> OSFDigital
# Link ------> https://osf.digital/careers/jobs?location=romania
#
#
# Aici va invit sa va creati propriile metode de scraping cu Python,
# ... folosind:
# -> requests
# -> BeautifulSoup
# -> requests_html etc.
#
from __utils import (
    Item,
    get_county,
    UpdateAPI,
)
import json
import re
import requests


def get_embedded_jobs(html):
    '''
    ... extract the jobs list embedded in the Next.js flight data.
    The careers page no longer exposes the old "OsfCommerceJob/GetItems"
    endpoint, the jobs are rendered from the RSC payload instead.
    '''

    flight_data = ''
    for chunk in re.findall(r'self\.__next_f\.push\((\[.*?\])\)</script>', html, re.S):
        try:
            data = json.loads(chunk)
        except json.JSONDecodeError:
            continue
        if len(data) > 1 and isinstance(data[1], str):
            flight_data += data[1]

    marker = '"jobsBoxes":'
    index = flight_data.find(marker)
    if index == -1:
        return []

    array_start = flight_data.find('[', index + len(marker))
    jobs, _ = json.JSONDecoder().raw_decode(flight_data[array_start:])
    return jobs


def is_romanian_job(job):
    '''
    ... check if a job is available in Romania.
    '''

    if 'romania' in (job.get('location') or '').lower():
        return True

    return any(
        'romania' in (job_location.get('label') or '').lower()
        for job_location in (job.get('jobLocation') or [])
    )


def scraper():
    '''
    ... scrape data from OSFDigital scraper.
    Your solution!
    '''

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    response = requests.get('https://osf.digital/careers/jobs',
                            params={'location': 'romania'}, headers=headers)

    job_list = []
    for job in get_embedded_jobs(response.text):
        if not is_romanian_job(job):
            continue

        location = 'Bucuresti'
        location_finish = get_county(location=location)

        # get jobs items from response
        job_list.append(Item(
            job_title=job['title'],
            job_link=f"https://osf.digital{job['jobUrl']['href']}",
            company='OSFDigital',
            country='Romania',
            county=location_finish[0] if True in location_finish else None,
            city='all' if location.lower() == location_finish[0].lower()\
                        and True in location_finish and 'bucuresti' != location.lower()\
                            else location,
            remote='remote',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "OSFDigital"
    logo_link = "https://osf.digital/library/media/osf/digital/common/header/osf-digital-20-years-logo.svg?h=35&la=en&w=240&hash=E5BC4C8E1EEF3EB1CFE110D0E1910DE415634B2D"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
