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
# Company ---> Serrala
# Link ------> https://careers.serrala.com/search/\?searchby\=distance\&createNewAlert\=false\&q\=\&geolocation\=\&d\=10\&lat\=\&lon\=\&optionsFacetsDD_dept\=\&optionsFacetsDD_location\=\&optionsFacetsDD_country\=RO
#
# Note ---> careers.serrala.com has no jobs in Romania at the moment, so the
#           country RO search is tried first and, while it returns nothing, the
#           full job list is scraped and every job keeps the country reported
#           by the site.
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

SEARCH_URL = (
    "https://careers.serrala.com/search/"
    "?searchby=distance&createNewAlert=false&q=&geolocation=&d=10&lat=&lon="
    "&optionsFacetsDD_dept=&optionsFacetsDD_location=&optionsFacetsDD_country={country}"
    "&startrow={startrow}"
)

# the search results show the country as a two letters code (DE, ES, IN, US...)
COUNTRY_NAMES = {
    'AT': 'Austria',
    'BE': 'Belgium',
    'BG': 'Bulgaria',
    'CA': 'Canada',
    'CH': 'Switzerland',
    'CZ': 'Czechia',
    'DE': 'Germany',
    'DK': 'Denmark',
    'ES': 'Spain',
    'FI': 'Finland',
    'FR': 'France',
    'GB': 'United Kingdom',
    'GR': 'Greece',
    'HR': 'Croatia',
    'HU': 'Hungary',
    'IE': 'Ireland',
    'IN': 'India',
    'IT': 'Italy',
    'NL': 'Netherlands',
    'NO': 'Norway',
    'PL': 'Poland',
    'PT': 'Portugal',
    'RO': 'Romania',
    'RS': 'Serbia',
    'SE': 'Sweden',
    'SI': 'Slovenia',
    'SK': 'Slovakia',
    'TR': 'Turkey',
    'US': 'United States',
}


def get_jobs_rows(country):
    '''
    ... job rows from the search results, following the site pagination
    '''
    job_rows = []
    start_row = 0

    while True:
        soup = GetStaticSoup(SEARCH_URL.format(country=country, startrow=start_row))
        rows = soup.find_all('tr', class_='data-row')
        if not rows:
            break

        job_rows.extend(rows)
        start_row += len(rows)

        pagination = soup.find('span', class_='paginationLabel')
        try:
            jobs_num = int(pagination.text.split()[-1])
        except (AttributeError, ValueError):
            break

        if start_row >= jobs_num:
            break

    return job_rows


def scraper():
    '''
    ... scrape data from serrala scraper.
    '''
    job_rows = get_jobs_rows('RO')

    # the careers site has no jobs left in Romania -> take the full list
    if not job_rows:
        job_rows = get_jobs_rows('')

    job_list = []
    for job in job_rows:

        link = job.find('a')
        location = job.find('span', class_='jobLocation').text.strip().split(',')[0]
        location = COUNTRY_NAMES.get(location.upper(), location)
        if location.lower() == 'bucharest':
            location = 'Bucuresti'

        location_finish = get_county(location=location)

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find('a').text.strip(),
            job_link="https://careers.serrala.com" + link['href'],
            company='serrala',
            country='Romania' if True in location_finish else location,
            county=location_finish[0] if True in location_finish else None,
            city='all' if location.lower() == location_finish[0].lower\
                        and True in location_finish and 'bucuresti' != location.lower\
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

    company_name = "serrala"
    logo_link = r"https://cookie-cdn.cookiepro.com/logos/c260fbd9-3298-48e4-8478-41e8a0cb0ab7/24f7e702-f5ef-4966-a29c-cd2ea3fab97b/de6ed974-29cf-418d-ad05-21dd545142de/serrala-vector-logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
