from __utils import (
    Item,
    get_county,
    remove_diacritics,
    UpdateAPI
)

import time

import requests


GREENHOUSE_URL = 'https://boards-api.greenhouse.io/v1/boards/orioninnovation/jobs?content=true'
CAREERS_URL = 'https://www.orioninnovation.com/careers/job/'


def normalize_location(location_name):
    '''
    ... normalize a location for matching, including Romanian diacritics.
    '''
    location_name = remove_diacritics(location_name or '')
    return ' '.join(location_name.lower().split())


def is_romania_location(location_name):
    '''
    ... check whether a source location refers to Romania.
    '''
    location_lower = normalize_location(location_name)
    return (
        'romania' in location_lower
        or 'bucharest' in location_lower
        or 'bucuresti' in location_lower
    )


def get_location_data(location_name):
    '''
    ... normalize county and city from a job location.
    '''
    location_name = ' '.join(location_name.split())
    location_lower = normalize_location(location_name)

    if 'bucharest' in location_lower or 'bucuresti' in location_lower:
        city = 'Bucuresti'
    else:
        city = location_name.title()

    location_finish = get_county(location=city)
    county = location_finish[0] if True in location_finish else ''

    return county, city


def build_job(job_title, job_link, location_name):
    '''
    ... build a job item from source data.
    '''
    job_type = 'remote' if 'remote' in job_title.lower() else 'hybrid'
    county, city = get_location_data(location_name)

    return Item(
        job_title=job_title,
        job_link=job_link,
        company='OrionInnovation',
        country='Romania',
        county=county,
        city=city,
        remote=job_type,
    ).to_dict()


def scrape_greenhouse():
    '''
    ... scrape Romania jobs from the Greenhouse API.
    '''
    try:
        response = requests.get(
            GREENHOUSE_URL,
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=30,
        )
        all_jobs = response.json().get('jobs', [])
    except (requests.RequestException, ValueError):
        return []

    job_list = []
    for job in all_jobs:
        location_name = job.get('location', {}).get('name', '')
        if not is_romania_location(location_name):
            continue

        job_list.append(build_job(
            job.get('title', ''),
            job.get('absolute_url', ''),
            location_name,
        ))

    return job_list


def get_careers_html():
    '''
    ... return the careers page HTML, which is protected by Cloudflare.
    '''
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException, WebDriverException
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--window-size=1280,2000')
    options.add_argument(
        '--user-agent=Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.execute_cdp_cmd(
            'Page.addScriptToEvaluateOnNewDocument',
            {'source': "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
        )

        for attempt in range(3):
            driver.get(CAREERS_URL)
            try:
                WebDriverWait(driver, 45).until(
                    lambda current_driver: current_driver.find_elements(
                        By.CSS_SELECTOR, '#jobList .job-card'
                    )
                )
                return driver.page_source
            except (TimeoutException, WebDriverException):
                if attempt == 2:
                    return ''
                time.sleep(3)
    except WebDriverException:
        return ''
    finally:
        if driver is not None:
            driver.quit()

    return ''


def scrape_careers_page():
    '''
    ... scrape Romania jobs from the Orion careers page.
    '''
    from bs4 import BeautifulSoup

    html = get_careers_html()
    if not html:
        return []

    soup = BeautifulSoup(html, 'lxml')
    job_list = []
    for card in soup.select('#jobList .job-card'):
        title_tag = card.find('h3')
        location_tag = card.select_one('.job-meta strong')
        if title_tag is None or location_tag is None:
            continue

        title = title_tag.get_text(' ', strip=True)
        location_name = location_tag.get_text(' ', strip=True)
        if not is_romania_location(location_name):
            continue

        job_list.append(build_job(title, card.get('href', ''), location_name))

    return job_list


def scraper():
    '''
    ... scrape data from OrionInnovation using Greenhouse and the careers page.
    '''
    job_list = []
    seen_titles = set()

    for job in scrape_greenhouse() + scrape_careers_page():
        title_key = job['job_title'].strip().lower()
        if title_key in seen_titles:
            continue

        seen_titles.add(title_key)
        job_list.append(job)

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "OrionInnovation"
    logo_link = "https://www.orioninnovation.com/wp-content/uploads/2022/08/Orion-Innovation-Logo-1.png"

    jobs = scraper()
    print(f"Found {len(jobs)} jobs in Romania")

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
