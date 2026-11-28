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
# Company ---> Neptun
# Link ------> https://www.neptun-gears.ro/ro/cariere/
#
#
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from __utils import (
    GetStaticSoup,
    DEFAULT_HEADERS,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

CAREERS_URL = "https://www.neptun-gears.ro/cariere/"
EJOBS_URL = "https://www.ejobs.ro/company/s-c-neptun-s-a/73778"


def _extract_jobs_from_soup(soup):
    '''
    ... build job items from the careers page soup.
    '''
    job_list = []
    jobs_container = soup.select_one('.fusion-text-2 ul')
    if jobs_container:
        for job in jobs_container.select('li'):
            title = job.get_text(' ', strip=True)
            if not title:
                continue

            job_list.append(Item(
                job_title=title,
                job_link=CAREERS_URL,
                company='Neptun',
                country='Romania',
                county='Prahova',
                city='Campina',
                remote='on-site',
            ).to_dict())

    return job_list


def _get_careers_soup_with_browser():
    '''
    ... load the careers page in a browser when Cloudflare blocks requests.
    '''
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--window-size=1366,900')
    options.add_argument(f"--user-agent={DEFAULT_HEADERS['User-Agent']}")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=options)
    try:
        driver.execute_cdp_cmd(
            'Page.addScriptToEvaluateOnNewDocument',
            {'source': "Object.defineProperty(navigator,'webdriver',{get:()=>undefined});"},
        )
        driver.get(CAREERS_URL)

        for _ in range(15):
            if driver.find_elements(By.CSS_SELECTOR, '.fusion-text-2 ul li'):
                break
            time.sleep(2)

        return BeautifulSoup(driver.page_source, 'lxml')
    finally:
        driver.quit()


def _get_jobs_from_careers_page():
    '''
    ... get jobs from the company careers page.
    '''
    job_list = _extract_jobs_from_soup(GetStaticSoup(CAREERS_URL))
    if not job_list:
        job_list = _extract_jobs_from_soup(_get_careers_soup_with_browser())

    return job_list


def _get_jobs_from_ejobs():
    '''
    ... fallback to the company page on eJobs when the careers site is down.
    '''
    response = requests.get(EJOBS_URL, headers=DEFAULT_HEADERS, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    job_list = []
    seen_links = set()
    for link in soup.select('a[href*="/user/locuri-de-munca/"]'):
        title = link.get_text(' ', strip=True)
        href = link.get('href', '')

        if not title or href in seen_links:
            continue

        seen_links.add(href)
        job_list.append(Item(
            job_title=title,
            job_link=f"https://www.ejobs.ro{href}",
            company='Neptun',
            country='Romania',
            county='Prahova',
            city='Campina',
            remote='on-site',
        ).to_dict())

    return job_list


def scraper():
    '''
    ... scrape data from Neptun scraper.
    '''
    try:
        job_list = _get_jobs_from_careers_page()
    except Exception:
        job_list = []

    if not job_list:
        try:
            job_list = _get_jobs_from_ejobs()
        except (requests.RequestException, ValueError):
            job_list = []

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Neptun"
    logo_link = "https://www.neptun-gears.ro/images/logo.jpg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
