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
# Company ---> Wirtek
# Link ------> https://wirtek.bamboohr.com/careers
#
#
from __utils import GetRequestJson, Item, UpdateAPI, get_county


def scraper():
    '''
    ... scrape data from Wirtek scraper.
    '''
    data = GetRequestJson("https://wirtek.bamboohr.com/careers/list")

    job_list = []
    for job in data.get('result', []):
        ats_location = job.get('atsLocation') or {}
        country = (ats_location.get('country') or '').strip()
        if country.lower() != 'romania':
            continue

        city = (ats_location.get('city') or '').strip()
        if city.lower() == 'cluj':
            city = 'Cluj-Napoca'

        county, _ = get_county(city) if city else (None, None)

        location_type = str(job.get('locationType'))
        remote = {
            '0': 'on-site',
            '1': 'remote',
            '2': 'hybrid',
        }.get(location_type, 'on-site')

        job_list.append(Item(
            job_title=job.get('jobOpeningName'),
            job_link=f"https://wirtek.bamboohr.com/careers/{job.get('id')}",
            company='Wirtek',
            country='Romania',
            county=county or '',
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

    company_name = "Wirtek"
    logo_link = "https://www.wirtek.com/hs-fs/hubfs/Wirtek_logo_22_years_v01_132x52px.gif?width=132&height=52&name=Wirtek_logo_22_years_v01_132x52px.gif"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
