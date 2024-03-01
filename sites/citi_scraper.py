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


def scraper():
    '''
    ... scrape data from Citi scraper.
    '''
    soup = GetStaticSoup("https://jobs.citi.com/search-jobs/Romania/287/2/798549/46/25/50/2")

    job_list = []
    lst_jobs_links = list()

    for job in soup.find_all('a'):
        try:
            if '/job/' in job['href']:
                lst_jobs_links.append(job['href'])
        except:
            pass
    
    # second for - scrape data from collected links
    for data in set(lst_jobs_links):
        second_soup = GetStaticSoup(f"https://jobs.citi.com{data}")
        job_info = second_soup.find_all('span', attrs={'class': 'job-info__item'})
        #
        location = job_info[1].text.split()[1].replace(',', '').strip()
        if location.lower() in ['bucharest']:
            location = "Bucuresti"

        location_finish = get_county(location=location)

        # get jobs items from response
        job_list.append(Item(
            job_title=second_soup.find('h1').text,
            job_link=f"https://jobs.citi.com{data}",
            company='Citi',
            country='Romania',
            county=location_finish[0] if True in location_finish else None,
            city='all' if location.lower() == location_finish[0].lower()\
                        and True in location_finish and 'bucuresti' != location.lower()\
                            else location,
            remote=job_info[2].text.split()[-1].strip(),
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
