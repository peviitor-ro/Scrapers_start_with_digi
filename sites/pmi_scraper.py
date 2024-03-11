#
#
#  Basic for scraping data from static pages
#  ... project made by Andrei Cojocaru
#  LinkedIn: https://www.linkedin.com/in/andrei-cojocaru-985932204/
#  Github: https://github.com/andreireporter13
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
# Company ---> pmi
# Link ------> https://www.pmi.com/careers/explore-our-job-opportunities?title=&locations=Romania&departments=&contracts=&page=1
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
    ... scrape data from pmi scraper.
    '''

    # job list for all jobs
    job_list = []
    page = 1
    while True:
        soup = GetStaticSoup(f"https://www.pmi.com/careers/explore-our-job-opportunities?title=&locations=Romania&departments=&contracts=&page={page}")
        soup_data = soup.find_all('a', attrs={'class': 'job-row'})

        link_verification = 'https://www.pmi.com' + soup.find_all('a', attrs={'class': 'job-row'})[0]['href'].strip()

        # verification for link exists in job_list json
        if job_list:
            if link_verification in [job["job_link"] for job in job_list]:
                break

        for idx, job in enumerate(soup_data):
            link_str = f"https://www.pmi.com{job['href'].strip()}"

            req_page = GetStaticSoup(link_str)

            #  search location
            new_loc = list()
            if len((location := req_page.find('p', attrs={'class': 'details--note details--positionIcon location'}).text.strip().split(',')[0].split())) > 1:
                new_loc = '-'.join(location)
            else:
                new_loc = location[0]

            if new_loc.lower() == 'bucharest':
                new_loc = 'Bucuresti'

            location_finish = get_county(location=new_loc)

            # get jobs items from response
            job_list.append(Item(
                job_title=job.find('h3', attrs={'class': 'job-row--title title8'}).text.strip(),
                job_link=link_str,
                company='pmi',
                country='Romania',
                county=location_finish[0] if True in location_finish else None,
                city='all' if new_loc.lower() == location_finish[0].lower()\
                        and True in location_finish and 'bucuresti' != new_loc.lower()\
                            else new_loc,
                remote='on-site',
            ).to_dict())

        page += 1

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "pmi"
    logo_link = "https://www.pmi.com/resources/images/default-source/default-album/pmi-logoaaf115bd6c7468f696e2ff0400458fff.svg?sfvrsn=37857db4_2"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
