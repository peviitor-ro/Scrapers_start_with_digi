#
#
# Config for Workable Account Jobs API!
#
# Company ---> FlowxAI
# Link ------> https://apply.workable.com/flowxai/
#
#
from __utils import (
    GetRequestJson,
    get_county,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from FlowXAI scraper.
    '''

    # The public account widget API is not rate-limited like the v3 jobs API.
    url = 'https://apply.workable.com/api/v1/widget/accounts/flowxai?details=true'
    post_data = GetRequestJson(url=url)
    results = post_data.get('jobs') or []

    # Romania has no jobs left, so scrape the full list from the source.
    job_list = []
    seen_shortcodes = set()

    for job in results:
        shortcode = job.get('shortcode')
        if shortcode in seen_shortcodes:
            continue
        seen_shortcodes.add(shortcode)

        location = (job.get('city') or '').strip()
        job_country = job.get('country') or ''

        if location.lower() == 'bucharest':
            location = 'Bucuresti'

        location_finish = get_county(location=location)

        # get jobs items from response
        job_list.append(Item(
            job_title=job.get('title'),
            job_link=f'https://apply.workable.com/flowxai/j/{shortcode}/',
            company='FlowXAI',
            country=job_country,
            county=location_finish[0] if True in location_finish else None,
            city='all' if location.lower() == location_finish[0].lower()\
                        and True in location_finish and 'bucuresti' != location.lower()\
                            else location,
            remote='remote' if job.get('telecommuting') else 'on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "FlowxAI"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
