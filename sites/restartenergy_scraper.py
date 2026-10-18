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
# Company ---> RestartEnergy
# Link ------> https://restartenergy.ro/cariere/
#
#
import re

from __utils import (
    GetStaticSoup,
    GetRequestJson,
    get_county,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from RestartEnergy scraper.
    '''
    jobs_data = GetRequestJson(
        "https://restartenergy.ro/wp-json/wp/v2/cariere?per_page=100&status=publish"
    )

    job_list = []
    if not isinstance(jobs_data, list):
        return job_list

    for job in jobs_data:
        job_title = job['title']['rendered']
        job_link = job['link']

        # get job locations from job page (h2 "Locație:" followed by cities paragraph)
        soup = GetStaticSoup(job_link)
        location_node = soup.find('h2', string=re.compile(r'Locație'))

        cities = []
        if location_node:
            location_paragraph = location_node.find_next_sibling()
            if location_paragraph:
                cities = [
                    city.strip()
                    for city in location_paragraph.get_text(',', strip=True).split(',')
                    if city.strip()
                ]

        counties = []
        found_cities = []
        for city in cities:
            county, found = get_county(city)
            if found:
                found_cities.append(city)
                counties.append(county)

        job_list.append(Item(
            job_title=job_title,
            job_link=job_link,
            company='RestartEnergy',
            country='Romania',
            county=counties if counties else '',
            city=found_cities if found_cities else '',
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "RestartEnergy"
    logo_link = "https://upload.wikimedia.org/wikipedia/commons/9/91/Restart-energy-logo-yellow.jpg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
