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
# Company ---> WPRiders
# Link ------> https://inside.wpriders.com/careers/
#
#
from __utils import Item, GetStaticSoup, UpdateAPI


def scraper():
    '''
    ... scrape data from WPRiders scraper.
    '''
    soup = GetStaticSoup("https://inside.wpriders.com/careers/")

    job_list = []
    seen_links = set()

    for job in soup.find_all('a', href=True):
        href = job['href']
        if '/careers/' not in href or href.rstrip('/').endswith('/careers'):
            continue
        if href in seen_links:
            continue

        title = ' '.join(job.get_text(' ', strip=True).split())
        if not title or 'view job oppening' in title.lower():
            continue

        seen_links.add(href)
        job_list.append(Item(
            job_title=title,
            job_link=href,
            company='WPRiders',
            country='Romania',
            county='Bucuresti',
            city='Bucuresti',
            remote='remote',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "WPRiders"
    logo_link = "https://wpriders.com/wp-content/themes/wpriders-theme/assets/landing_page/logo_header_black.svg"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
