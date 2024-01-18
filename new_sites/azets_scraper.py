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
# Company ---> azets
# Link ------> https://www.azets.ro/talentlink/
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from azets scraper.
    '''
    soup = GetStaticSoup("https://www.azets.ro/talentlink/")

    job_list = []
    for job in soup.find_all('div', attrs={'class': 'talentlink-expandable-item-header'}):
        id_ = job.find('a', attrs={'class': 'panel-heading ps-2 py-2 pe-4 pe-lg-6 px-lg-5'})['href'].split('_')[-1]

        # go to pages and collect else data!
        second_soup = GetStaticSoup(f"https://www.azets.ro/talentlink/advertpage/?advertid={id_}")
        location = second_soup.find('div', attrs={'class': 'job-location-value'}).text.strip()

        # get jobs items from response
        job_list.append(Item(
            job_title=second_soup.find('h1', attrs={'class': 'py-3'}).text.strip(),
            job_link=f"https://www.azets.ro/talentlink/advertpage/?advertid={id_}",
            company='azets',
            country='Romania',
            county=get_county(location),
            city=location,
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "azets"
    logo_link = "https://www.azets.no/globalassets/global/graphics/logos/azets_logo.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
