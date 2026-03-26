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
# Company ---> TotalSoft
# Link ------> https://totalsoft.applytojob.com/apply/
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)


def get_location_data(location_text):
    '''
    ... normalize TotalSoft location text.
    '''
    if location_text == 'Romania':
        return '', 'Romania', 'on-site'

    first_location = location_text.split(',')[0].strip()
    if first_location == 'Bucharest':
        first_location = 'Bucuresti'

    location_finish = get_county(location=first_location)

    return (
        location_finish[0] if True in location_finish else '',
        first_location,
        'on-site',
    )


def scraper():
    '''
    ... scrape data from TotalSoft scraper.
    '''
    soup = GetStaticSoup("https://totalsoft.applytojob.com/apply/")

    job_list = []
    for job in soup.find_all('li', attrs={'class': 'list-group-item'}):
        link_tag = job.find('a')
        location_tag = job.find('ul', attrs={'class': 'list-inline list-group-item-text'})

        if link_tag is None or location_tag is None:
            continue

        location_text = location_tag.get_text(' ', strip=True)
        county, city, remote = get_location_data(location_text)

        job_list.append(Item(
            job_title=link_tag.get_text(strip=True),
            job_link=link_tag['href'].strip(),
            company='TotalSoft',
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

    company_name = "TotalSoft"
    logo_link = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/TotalSoft_logo.png/1200px-TotalSoft_logo.png"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
