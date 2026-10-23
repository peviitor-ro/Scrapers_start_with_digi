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


def get_job_links():
    '''
    ... collect Citi job links for Romania.
    '''
    sitemap_soup = GetStaticSoup("https://jobs.citi.com/sitemap.xml")
    sitemap_urls = [loc.text.strip() for loc in sitemap_soup.find_all('loc')]

    romanian_locations = set()
    for url in sitemap_urls:
        if '/location/' not in url:
            continue
        location_slug = url.split('/location/', 1)[1].split('/', 1)[0]
        if location_slug.endswith('-romania-jobs'):
            romanian_locations.add(location_slug[:-len('-romania-jobs')])

    romanian_locations.update({'romania', 'bucharest', 'bucuresti'})

    def is_romanian_location(city_slug):
        for location_slug in romanian_locations:
            if city_slug == location_slug or location_slug.startswith(f'{city_slug}-') \
                    or location_slug.endswith(f'-{city_slug}') or f'-{city_slug}-' in location_slug:
                return True
        return False

    job_links = set()
    for url in sitemap_urls:
        if '/job/' not in url:
            continue
        path = url.split('/job/', 1)[1].split('/')
        if len(path) > 1 and is_romanian_location(path[0]):
            job_links.add(url)

    if not job_links:
        soup = GetStaticSoup("https://jobs.citi.com/search-jobs/Romania/287/2/798549/46/25/50/2")
        for job in soup.find_all('a'):
            href = job.get('href')
            if href and '/job/' in href:
                job_links.add(href)

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

            location_text = location_div.find('p', class_='job-description__desc-detail').text.strip()
            if 'romania' not in location_text.lower():
                continue

            location = location_text.split(',')[0].strip()

            remote_div = second_soup.find('div', class_='job-description__desc-job-info job-remote-type')
            remote = remote_div.find('p', class_='job-description__desc-detail').text.strip() if remote_div else "On-site"

            job_title = second_soup.find('h1').text.strip()
        except Exception:
            continue

        if location.lower() in ['bucharest']:
            location = "Bucuresti"

        location_finish = get_county(location=location)

        job_list.append(Item(
            job_title=job_title,
            job_link=job_link,
            company='Citi',
            country='Romania',
            county=location_finish[0] if True in location_finish else None,
            city='all' if location.lower() == location_finish[0].lower()\
                        and True in location_finish and 'bucuresti' != location.lower()\
                            else location,
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
