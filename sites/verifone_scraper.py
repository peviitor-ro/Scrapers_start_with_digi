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
# Company ---> Verifone
# Link ------> https://connect.verifone.com/en/global/careers/jobs?title=&departments=All&locations=686
#
#
from __utils import (
    get_county,
    GetStaticSoup,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from Verifone scraper.
    '''
    soup = GetStaticSoup("https://connect.verifone.com/en/global/careers/jobs?title=&departments=All&locations=686")

    job_list = []
    for job in soup.find_all('tr'):
        link_tag = job.find('a', href=True)
        location_tag = job.find('td', attrs={'class': 'views-field views-field-field-offices'})

        if link_tag is None or location_tag is None:
            continue

        city = location_tag.get_text(strip=True)
        normalized_city = 'Bucuresti' if city == 'Bucharest' else city
        county_data = get_county(location=normalized_city)

        job_list.append(Item(
            job_title=link_tag.get_text(strip=True),
            job_link=link_tag['href'].strip(),
            company='Verifone',
            country='Romania',
            county=county_data[0] if True in county_data else '',
            city=normalized_city,
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Verifone"
    logo_link = "https://datasym.co.uk/wp-content/uploads/2017/09/verifone-logo-300x120.png"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
