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
# Company ---> WPRiders
# Link ------> https://inside.wpriders.com/careers/
#
#
from __utils import Item, UpdateAPI
from bs4 import BeautifulSoup


def get_soup(url):
    '''
    ... load the careers page in a browser to pass its JS challenge.
    '''
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from shutil import which

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    )
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    driver_path = which('chromedriver') or '/usr/bin/chromedriver'
    driver = webdriver.Chrome(service=Service(driver_path), options=options)
    driver.set_page_load_timeout(60)
    try:
        driver.get(url)
        WebDriverWait(driver, 45, poll_frequency=0.5).until(
            lambda browser: 'One moment' not in browser.page_source
        )
        return BeautifulSoup(driver.page_source, 'lxml')
    finally:
        driver.quit()


def scraper():
    '''
    ... scrape data from WPRiders scraper.
    '''
    url = "https://inside.wpriders.com/careers/"
    try:
        soup = get_soup(url)
    except Exception:
        return []

    job_list = []
    seen_links = set()

    for job in soup.find_all('a', href=True):
        href = job['href']
        if '/careers/' not in href or href.rstrip('/').endswith('/careers'):
            continue
        if href in seen_links:
            continue

        title = ' '.join(job.get_text(' ', strip=True).split())
        if not title or 'view job oppening' in title.lower():
            continue

        seen_links.add(href)
        job_list.append(Item(
            job_title=title,
            job_link=href,
            company='WPRiders',
            country='Romania',
            county='Bucuresti',
            city='Bucuresti',
            remote='remote',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "WPRiders"
    logo_link = "https://wpriders.com/wp-content/themes/wpriders-theme/assets/landing_page/logo_header_black.svg"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
