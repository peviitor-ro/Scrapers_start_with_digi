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
# Company ---> AECOM
# Link ------> https://aecom.jobs/rom/jobs/
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
    ... scrape data from AECOM scraper.
    '''

    job_list = []
    flag = True
    offset = 0
    while flag:
        soup = GetStaticSoup(f"https://aecom.jobs/rom/jobs/ajax/joblisting/?num_items=15&offset={offset}")
        soup_data = soup.find_all('li', class_='direct_joblisting with_description')

        if len(soup_data) < 1:
            flag = False

        for job in soup_data:
            if (loc := job.find('div', class_='direct_joblocation').text.strip().split('\n')) and 'romania' in [element.strip().lower() for element in loc]:
                loc_f = loc[0].strip().split(',')[0]
                if loc_f.lower() == 'bucharest':
                    loc_f = 'Bucuresti'

                # make one call for locations
                location_finish = get_county(location=loc_f)

                # get jobs items from response
                job_list.append(Item(
                    job_title=job.find('h4').text.strip(),
                    job_link='https://aecom.jobs' + job.find('a').get('href').strip(),
                    company='AECOM',
                    country='Romania',
                    county=location_finish[0] if True in location_finish else None,
                    city='all' if loc_f.lower() == location_finish[0].lower() and\
                        True in location_finish and 'bucuresti' != loc_f.lower()\
                            else loc_f,
                    remote=get_job_type('hybrid'),
                ).to_dict())

        # don't forget this details in loops
        offset += 15

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "AECOM"
    logo_link = "https://1000logos.net/wp-content/uploads/2021/12/AECOM-logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()