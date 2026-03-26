#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> TrustYou
# Link ------> https://www.trustyou.com/careers/
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
    Item,
    UpdateAPI,
)


def get_location_data(location_text):
    '''
    ... normalize TrustYou Romania location.
    '''
    if 'cluj' in location_text.lower():
        county_data = get_county(location='Cluj')
        return county_data[0] if True in county_data else 'Cluj', 'Cluj', 'on-site'

    if 'romania' in location_text.lower() and 'remote' in location_text.lower():
        return '', 'Romania', 'remote'

    return '', 'Romania', 'on-site'


def scraper():
    '''
    ... scrape data from TrustYou scraper.
    '''
    jobs_data = GetRequestJson('https://api.lever.co/v0/postings/trustyou?mode=json&skip=0&limit=50')

    job_list = []
    for job in jobs_data:
        categories = job.get('categories') or {}
        location = categories.get('location', '')

        if 'romania' not in location.lower() and 'cluj' not in location.lower():
            continue

        county, city, remote = get_location_data(location)

        job_list.append(Item(
            job_title=job.get('text'),
            job_link=job.get('hostedUrl'),
            company='TrustYou',
            country='Romania',
            county=county,
            city=city,
            remote=remote,
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "TrustYou"
    logo_link = "https://play-lh.googleusercontent.com/SzbVFK34kqMq1IbRFf5FhlNW0APelGW17Elb0aaBEdlRk_zHgbm7YYp9rEnN9kFBK0k"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
