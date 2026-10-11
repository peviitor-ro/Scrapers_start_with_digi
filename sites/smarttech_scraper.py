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
    soup = BeautifulSoup(response.text, 'lxml')
    blocks = soup.select('div.w-dyn-item')

    job_list = []
    for job in blocks:
        title = None
        title_elem = job.select_one('h2')
        if title_elem:
            title = title_elem.text.strip()

        link = None
        link_elem = job.select_one('a[href*="/careers/"]')
        if not link_elem:
            link_elem = job.find('a', href=True)
        if link_elem and link_elem.has_attr('href'):
            href = link_elem['href']
            if href.startswith('http'):
                link = href
            elif href.startswith('/'):
                link = 'https://www.smarttech247.com' + href
            else:
                link = 'https://www.smarttech247.com/careers/' + href

        # Try to extract location
        country = 'Romania'
        county = 'Bucharest'
        city = 'Bucharest'

        # Look for location in body-sm elements
        loc_elems = job.select('.body-sm')
        if loc_elems:
            loc_text = ' '.join(e.text.strip() for e in loc_elems)
            loc_lower = loc_text.lower()
            if 'ireland' in loc_lower or 'cork' in loc_lower or 'dublin' in loc_lower or 'belfast' in loc_lower:
                country = 'Ireland'
            elif 'romania' in loc_lower or 'bucharest' in loc_lower:
                country = 'Romania'
            elif 'uk' in loc_lower or 'united kingdom' in loc_lower or 'england' in loc_lower:
                country = 'United Kingdom'

        job_list.append(Item(
            job_title=title,
            job_link=link,
            company='Smarttech',
            country=country,
            county=county,
            city=city,
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
