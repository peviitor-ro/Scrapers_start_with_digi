#
#
#  Basic for scraping data from static pages
#  ... project made by Andrei Cojocaru
#
#
# Company ---> monefy
# Link ------> https://monefy.ro/careers/
#
#
from __utils import GetStaticSoup
from __utils import get_county
# from __utils import get_job_type
from __utils import Item
from __utils import UpdateAPI


def get_location(response: GetStaticSoup) -> str:
    locations = [
        location.split(":")[1]
        for element in response.find_all("div", {"class": "et_pb_text_inner"})
        for location in element.text.split()
        if "location" in location.lower()
    ]

    if locations:
        if locations[0] == 'Bucharest':
            return 'Bucuresti'

    return 'Bucuresti'


def scraper():
    '''
    ... scrape data from monefy scraper.
    '''
    soup = GetStaticSoup("https://monefy.ro/careers/")

    job_list = []
    for job in soup.find_all('h3', attrs={'class': 'entry-title'}):

        # get job data
        response = GetStaticSoup(job.a['href'])

        # get jobs items
        job_list.append(Item(
            job_title=job.find('a').text,
            job_link=job.a['href'],
            company='monefy',
            country='Romania',
            county=get_county(get_location(response)),
            city=get_location(response),
            remote='Remote',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "monefy"
    logo_link = "https://monefy.ro/wp-content/uploads/2021/02/Logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
