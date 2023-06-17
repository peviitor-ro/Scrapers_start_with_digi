#
#
#
# Company - xogito
# Link -> https://www.xogito.com/careers/
#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#
from bs4 import BeautifulSoup
#
import uuid
import time
import requests
from random import randint


class ScraperXogito:
    '''
    Scrape xogito company and store all data into variable.
    After this scraper need to test, and after send it to
    Github.
    '''

    def __init__(self, link, browser):
        self.link = link
        self.browser = browser

        # for scraped data, like the simples scraper
        self.list_with_data = []

    # DRY expected conditions in one func()
    def expected_c(self, by_name, element):
        '''
        ... here define expected_conditions.
        '''

        # search items
        by_map = {
                'ID': By.ID,
                'NAME': By.NAME,
                'CLASS_NAME': By.CLASS_NAME,
                'CSS': By.CSS_SELECTOR
            }

        wait = WebDriverWait(self.browser, 10)
        by = by_map.get(by_name)
        if by is None:
            raise ValueError(f'Invalid "by_name" value: {by_name}')

        return wait.until(EC.visibility_of_element_located((by, element)))

    def find_html_data(self):
        '''
        Scrape html data of jobs.
        '''
        self.browser.get(self.link)

        # find element for jobs div!
        elements_job = self.expected_c('CLASS_NAME', 'list-view')
        data_html_jobs = elements_job.get_attribute('outerHTML')

        return data_html_jobs

    def store_in_list(self):
        '''
        Store scraped data from html in list.
        '''

        soup = BeautifulSoup(self.find_html_data(), 'lxml')
        soup_data = soup.find_all('div', class_='position')

        for dt in soup_data:
            link_title = dt.find('a')

            if link_title:
                link = link_title['href']
                title = link_title.text.strip()
                location = dt.find('ul', class_='listing-tags').find_all('li')[-1].text

                if 'europe' in location.lower():
                    self.list_with_data.append({
                            "id": str(uuid.uuid4()),
                            "job_title": title,
                            "job_link":  link,
                            "company": "xogito",
                            "country": "Romania",
                            "city": location
                            })

        return self.list_with_data


class TestScraperXogito:
    '''
    Test scraper Xogito.
    '''

    def __init__(self, browser, data_from_xogito: list):
        self.browser = browser
        self.data_from_xogito = data_from_xogito
        self.test_list = []

    def test_links_xogito(self):
        '''
        ... test links from xogito.
        '''

        for dt in self.data_from_xogito:

            # verify title
            self.browser.get(dt['job_link'])

            title = self.browser.find_element(By.TAG_NAME, 'h1').text.strip()

            if title:
                if title == dt['job_title']:
                    self.test_list.append(dt)

            time.sleep(randint(1, 2))

        return self.test_list
