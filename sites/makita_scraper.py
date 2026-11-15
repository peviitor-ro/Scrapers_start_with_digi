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
# Company ---> makita
# Link ------> https://makitajobs.ro/locuri-de-munca/
#
#
import base64
import re
import time
from shutil import which
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from __utils import (
    GetHtmlSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def get_driver():
    '''
    ... start a browser that can pass the source website's JS challenge.
    '''
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    )

    driver_path = which('chromedriver') or '/usr/bin/chromedriver'
    driver = webdriver.Chrome(service=Service(driver_path), options=options)
    driver.set_page_load_timeout(60)
    return driver


def get_soup(driver, url, marker):
    '''
    ... load a page and wait until its real content replaces the challenge page.
    '''
    driver.get(url)
    WebDriverWait(driver, 30, poll_frequency=0.5).until(
        lambda browser: marker in browser.page_source
    )
    return GetHtmlSoup(driver.page_source)


def get_location(soup):
    '''
    ... extract the job location from the base64 encoded page content.
    '''
    for text_node in soup.find_all(string=re.compile('bunch_service_single')):
        match = re.search(r'text="([^"]+)"', str(text_node))
        if not match:
            continue

        encoded = match.group(1)
        decoded = base64.b64decode(encoded + '=' * (-len(encoded) % 4)).decode('utf-8', errors='replace')
        text = re.sub(r'<[^>]+>', ' ', decoded)

        address_match = re.search(r'Locul tău de muncă stabil\s*-\s*([^<]+)', text)
        if address_match:
            return address_match.group(1).strip().split(',')[-1].strip().split()[-1]

        county_match = re.search(r'Jud\.\s*([^\s<]+)', text)
        if county_match:
            return county_match.group(1).strip()

    return None


def scraper():
    '''
    ... scrape data from makita scraper.
    '''
    driver = get_driver()
    try:
        soup = get_soup(driver, "https://makitajobs.ro/locuri-de-munca/", 'box-right')

        job_list = []
        for job in soup.find_all('div', attrs={'class': 'box-right'}):
            link = "https://makitajobs.ro" + job.find('div', attrs={'class': 'content-button'}).find('a')['href']

            location = None
            for _ in range(3):
                try:
                    location = get_location(get_soup(driver, link, 'bunch_service_single'))
                    break
                except Exception:
                    time.sleep(2)
                    continue

            if location is None:
                continue

            location_finish = get_county(location=location)

            
            # get jobs items from response
            job_list.append(Item(
                job_title=job.find('div', attrs={'class': 'content-title'}).text,
                job_link=link,
                company='makita',
                country='România',
                county=location_finish[0] if True in location_finish else None,
                city='all' if location.lower() == location_finish[0].lower()\
                            and True in location_finish and 'bucuresti' != location.lower()\
                                else location,
                remote='on-site',
            ).to_dict())
    finally:
        driver.quit()

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "makita"
    logo_link = "https://www.makita.ro/data/pam/public/makita_logo3.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
