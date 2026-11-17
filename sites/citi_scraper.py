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
# Company ---> Citi
# Link ------> https://jobs.citi.com/search-jobs/Romania/287/2/798549/46/25/50/2
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


SEARCH_URL = 'https://jobs.citi.com/search-jobs'
MAX_PAGES = 10

COUNTRIES = {
    'united states': 'United States',
    'united kingdom': 'United Kingdom',
    'united arab emirates': 'United Arab Emirates',
    'romania': 'Romania',
    'india': 'India',
    'china': 'China',
    'poland': 'Poland',
    'canada': 'Canada',
    'malaysia': 'Malaysia',
    'costa rica': 'Costa Rica',
    'philippines': 'Philippines',
    'bahrain': 'Bahrain',
    'ireland': 'Ireland',
    'taiwan': 'Taiwan',
    'singapore': 'Singapore',
    'japan': 'Japan',
    'mexico': 'Mexico',
    'france': 'France',
    'spain': 'Spain',
    'hungary': 'Hungary',
    'germany': 'Germany',
    'switzerland': 'Switzerland',
    'netherlands': 'Netherlands',
    'brazil': 'Brazil',
    'hong kong': 'Hong Kong',
    'australia': 'Australia',
    'sweden': 'Sweden',
    'italy': 'Italy',
}


def get_country(location_text):
    '''
    ... extract the country from a Citi location string.
    '''
    parts = [part.strip() for part in location_text.split(',') if part.strip()]

    for part in reversed(parts):
        if part.lower() in COUNTRIES:
            return COUNTRIES[part.lower()]

    return parts[-1] if parts else 'Romania'


def get_job_links():
    '''
    ... collect Citi job links from the current search results.
    '''
    job_links = set()

    for page in range(1, MAX_PAGES + 1):
        soup = GetStaticSoup(f"{SEARCH_URL}?p={page}")
        for job in soup.select('li.sr-job-item a.sr-job-item__link'):
            href = job.get('href')
            if href and '/job/' in href:
                job_links.add(href if href.startswith('http') else f"https://jobs.citi.com{href}")

    return job_links


def scraper():
    '''
    ... scrape data from Citi scraper.
    '''
    job_list = []

    for data in get_job_links():
        job_link = data if data.startswith('http') else f"https://jobs.citi.com{data}"
        second_soup = GetStaticSoup(job_link)

        try:
            location_div = second_soup.find('div', class_='job-description__desc-job-info job-location')
            if not location_div:
                continue

            location_detail = location_div.find('p', class_='job-description__desc-detail') \
                or location_div.find('dd', class_='job-description__desc-detail')
            location_text = location_detail.text.strip()
            location = location_text.split(',')[0].strip()
            country = get_country(location_text)

            remote_div = second_soup.find('div', class_='job-description__desc-job-info job-remote-type')
            remote = remote_div.find('p', class_='job-description__desc-detail').text.strip() if remote_div else "On-site"

            job_title = second_soup.find('h1').text.strip()
        except Exception:
            continue

        if country == 'Romania':
            if location.lower() in ['bucharest']:
                location = "Bucuresti"

            location_finish = get_county(location=location)
            county = location_finish[0] if True in location_finish else None
            city = 'all' if location.lower() == location_finish[0].lower()\
                        and True in location_finish and 'bucuresti' != location.lower()\
                            else location
        else:
            county = None
            city = location

        job_list.append(Item(
            job_title=job_title,
            job_link=job_link,
            company='Citi',
            country=country,
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

    company_name = "Citi"
    logo_link = "https://tbcdn.talentbrew.com/company/287/26508/content/logo.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
