#
#
#
# New company to scrape ---> Globallogic
# Link to this company ---> https://www.globallogic.com/ro/careers/
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
from random import randint


def get_soup_object(url: str):
    """
    Get soup object for scraping.
    """

    response = requests.get(url=url,
                            headers=DEFAULT_HEADERS)

    return BeautifulSoup(response.text, 'lxml')


def get_jobs_num(url: str) -> int:
    """
    Get jobs num from this site.
    ... logic is -> site have something tricky method to scrap.
    I will scrap num jobs, and page after page I will increment
    ... the number of jobs.
    While count_jobs != get_jobs_num... atunci next.
    """

    soup = get_soup_object(url=url)

    numero = soup.find('div', class_='filter-main').find('h5').text.split()[0]

    return int(numero)


def collect_data_from_globalLogic() -> list:
    """
    Here, we scrap all data from ---> GlobalLogic.
    """

    # jobs num from site
    num_jobs = get_jobs_num('https://www.globallogic.com/ro/career-search-page/?keywords=&experience=&locations=romania&c=')
    print(num_jobs)

    page = 1
    jobs_count = 0

    # StopIteration
    stop_page = int(num_jobs / 10)

    lst_with_data = []
    while page <= stop_page + 1:

        soup = get_soup_object("https://www.globallogic.com/ro/career-search-page/?keywords=&experience=&locations=romania&c=")

        # get data from site
        soup_data = soup.find_all('div', class_='col-12 col-lg-6')

        # get all data!
        for sd in soup_data:
            link = sd.find('a')['href']
            title = sd.find('a').text

            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link":  link,
                    "company": "globallogic",
                    "country": "Romania",
                    "city": "Romania"
                    })

            # increment jobs
            jobs_count += 1

            # check jobs count!
            if jobs_count == num_jobs:
                break

        # increment page, go in depth
        print(page)
        page += 1

        # sleep time between requests
        time.sleep(randint(1, 3))

    print(len(lst_with_data))

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'globallogic'
data_list = collect_data_from_globalLogic()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('globallogic',
                  'https://www.globallogic.com/wp-content/uploads/2021/07/Logo_GL-Hitachi_White-web.svg'
                  ))
