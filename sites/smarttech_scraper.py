#
#
# Your custom scraper here ---> Last level!
#
# Company ---> smarttech
# Link ------> https://www.smarttech247.com/careers/
#
#
# Aici va invit sa va creati propriile metode de scraping cu Python,
# ... folosind:
# -> requests
# -> BeautifulSoup
# -> requests_html etc.
#
from __utils import Item, UpdateAPI
import requests
from bs4 import BeautifulSoup


def scraper():
    '''
    ... scrape data from smarttech scraper.
    Your solution!
    '''

    response = requests.get('https://www.smarttech247.com/careers/')
    soup     = BeautifulSoup(response.text, 'lxml')
    #
    blocks   = soup.select('div.numbercard') 
    
    job_list = []
    for job in blocks:
    
        title = job.select_one('p.maintitle')
        if title:
            title = title.text.strip()

        link = job.select_one('a')
        if link:
            link = link['href']

        job_list.append(Item(
            job_title=title,
            job_link=link,
            company='Smarttech',
            country='Romania',
            county='Bucharest',
            city='Bucharest',
            remote='Remote',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Smarttech"
    logo_link = "None"

    jobs = scraper()
    print(jobs)

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    # UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
