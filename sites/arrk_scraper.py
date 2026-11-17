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
# Company ---> ARRK
# Link ------> https://engineering.arrk.com/jobs-career/current-job-offers
#
#
from urllib.parse import urljoin
from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)

JOBS_URL = (
    "https://arrkeurope.onlyfy.jobs/candidate/job/ajax_list"
    "?widgetConfig=z8xcghls&display_length=400&page=1"
    "&sort=date&sort_dir=DESC&search="
)

COUNTRIES = {
    'munich': 'Germany',
    'madrid': 'Spain',
    'kuala lumpur': 'Malaysia',
    'petaling jaya': 'Malaysia',
    'hefei': 'China',
}


def scraper():
    '''
    ... scrape data from ARRK scraper.
    '''
    soup = GetStaticSoup(JOBS_URL)

    job_list = []
    for job in soup.select('[class*="row-table"][class*="collapsed"]'):
        title_tag = job.find('a')
        location = job.find('div', attrs={'class': 'cell-table col-sm-6 col-xs-8'}).text.strip()
        call_get_county = get_county(location=location)

        # get jobs items from response
        job_list.append(Item(
            job_title=title_tag.text.strip(),
            job_link=urljoin('https://arrkeurope.onlyfy.jobs/', title_tag['href']),
            company='ARRK',
            country=COUNTRIES.get(location.lower(), 'Romania'),
            county=call_get_county[0] if True in call_get_county else None,
            city='all' if location.lower() == call_get_county[0].lower()\
                and True in call_get_county and 'bucuresti' != location.lower()\
                    else location,
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "ARRK"
    logo_link = "https://www.arrk.com/wp/wp-content/themes/SmartPack3.0-Ver/img/logo-blue.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
