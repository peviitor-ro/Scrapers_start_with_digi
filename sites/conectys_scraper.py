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
# Company ---> Conectys
# Link ------> https://careers.conectys.com/careers/\?search_keywords\=\&selected_location\=
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
    ... scrape data from Conectys scraper.
    '''

    cities_for_requests = ['bucharest', 'sibiu']

    job_list = []
    for city_search in cities_for_requests:
        soup = GetStaticSoup(f"https://careers.conectys.com/careers/?search_keywords=&selected_location={city_search}")

        if len(check_soup := soup.find_all('div', attrs={'class': 'col-md-4 col-sm-6 grid-item'})) > 0:
            for job in check_soup:
                location = job.find('div', attrs={'class': 'job-location'}).text.strip().split(',')[0].strip()

                if location.lower() == 'bucharest':
                    location = 'Bucuresti'

                location_finish = get_county(location=location)

                # get jobs items from response
                job_list.append(Item(
                    job_title=job.find('span', attrs={'class': 'job-title'}).text.strip(),
                    job_link=job.find('div', attrs={'class': 'job-info'}).find('a')['href'].strip(),
                    company='Conectys',
                    country='Romania',
                    county=location_finish[0] if True in location_finish else None,
                    city='all' if location.lower() == location_finish[0].lower()\
                            and True in location_finish and 'bucuresti' != location.lower()\
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

    company_name = "Conectys"
    logo_link = "https://www.conectys.com/wp-content/uploads/2021/05/Conectys.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
