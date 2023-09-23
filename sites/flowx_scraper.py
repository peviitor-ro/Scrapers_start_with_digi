#
#
#
#
# Scraper with OOP!
# Company --------> Flow
# Link -----------> https://blog.flowx.ai/careers
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
#
import time
import re


# session for scraping
session = requests.Session()


class CheckScraper:
    """
    With this blueprint I will
    check if location==Bucharest
    on job pages.
    Encapsulated solution for
    my cod.
    """

    def make_soup_object(self, link: str):
        '''
        This method will be returned a soup_object.
        '''
        return BeautifulSoup(session.get(url=link, headers=DEFAULT_HEADERS).text, 'lxml')

    def check_location(self, link: str):
        '''
        This method will be check if job page have location Romania.
        '''
        loc_data = self.make_soup_object(link)
        h2 = [i.text.strip() for i in loc_data.find_all('h2')]
        h3 = [i.text.strip() for i in loc_data.find_all('h3')]
        h4 = [i.text.strip() for i in loc_data.find_all('h4')]
        total_list = h2 + h3 + h4

        #
        regex = r"\bBucharest\b"
        for element in total_list:
            if re.search(regex, element):
                return True


def return_lst_dict(title: str, link: str, city: str) -> dict:
    '''
    ... this function will return a dict to append to a list and avoid DRY
    '''
    dct = {
        "id": str(uuid.uuid4()),
        "job_title": title,
        "job_link": link,
        "company": "flowx",
        "country": "Romania",
        "city": city
    }

    return dct


def collect_links_to_jobs():
    '''
    ... for this step I will collect all links
    from all pages and check them with class:
    CheckLocation.
    '''

    # list for jobs data
    lst_with_data = []

    page = 1
    err = False
    #
    while err != True:

        soup = CheckScraper().make_soup_object(f'https://blog.flowx.ai/careers/page/{page}')
        time.sleep(1)

        soup_data = soup.find_all('article', attrs={'class': 'blog-index__post blog-index__post--small'})

        if len(soup_data) > 1:
            # try to catch links here

            for job in soup_data:
                data = job.find('a', attrs={'class': 'blog-index__post-title-link'})
                #
                title = data.text.strip()
                link = data['href'].strip()

                if CheckScraper().check_location(link):
                    lst_with_data.append(return_lst_dict(title=title, link=link, city='Bucuresti'))

        else:
            err = True  # 404

        # increment page
        page += 1

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'flowx'
data_list = collect_links_to_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('flowx',
                  'https://ami.cname.ro/_/company/flowx.ai/mediaPool/uawgRuH.png'
                  ))
