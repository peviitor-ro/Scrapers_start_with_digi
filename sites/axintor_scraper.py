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
# Company ---> Axintor
# Link ------> https://www.axintor.be/ro/locuri-de-munca\?sector\=\&jobtitle\=\&sortorder\=asc\&searchterm\=
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
    ... scrape data from Axintor scraper.
    '''
    soup = GetStaticSoup("https://www.axintor.be/ro/locuri-de-munca?sector=&jobtitle=&sortorder=asc&searchterm=")

    job_list = []
    for job in soup.find_all('div', attrs={'class': 'col-12 col-md-6 col-xl-4'}):
        
        # second requst for category
        second_soup = GetStaticSoup(f"https://www.axintor.be{job.find('a')['href'].strip()}")

        # scrape data
        for last_job in second_soup.find_all('a', attrs={'class': 'listing listing--callout'}):
            title = last_job.find('h3', attrs={'class': 'listing__title'}).text.strip()
            location = last_job.find('div', attrs={'class': 'listing__intro'}).find('p', attrs={'class': 'wage'}).text.strip()

            # get jobs items from response
            job_list.append(Item(
                job_title=f"{title} {location}",
                job_link=f"https://www.axintor.be{last_job['href']}",
                company='Axintor',
                country="Romania",
                county='',
                city='',
                remote='on-site',
            ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Axintor"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
