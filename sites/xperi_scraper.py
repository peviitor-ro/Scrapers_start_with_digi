#
#
#
#
# Company -> xperi
# Link ----> https://xperi.com/careers/open-positions/?p=jobs%2Falljobs
# Second link -> https://jobs.jobvite.com/xperi/jobs
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
#
import re
from time import sleep


def return_lst_dict(title: str, link: str, city: str) -> dict:
    '''
    ... this function will return a dict to append to a list and avoid DRY
    '''
    dct = {
        "id": str(uuid.uuid4()),
        "job_title": title,
        "job_link": link,
        "company": "xperi",
        "country": "Romania",
        "city": city
    }

    return dct


def return_soup(url: str):
    '''
    ... return soup. Except DRY.
    '''

    response = requests.get(url=url, headers=DEFAULT_HEADERS, timeout=2)

    return BeautifulSoup(response.text, 'lxml')


def parse_jobs(data: BeautifulSoup) -> dict:
    '''
    ... parse data and return jobs.
    '''

    cities = ['bucharest', 'brasov', 'iasi']

    link = 'https://jobs.jobvite.com' + data.find('a', attrs={'class': 'flex-row'})['href']
    title = data.find('div', attrs={'class': 'jv-job-list-name'}).text.strip()
    location = data.find('div', attrs={'class': 'ml-auto jv-job-list-location'}).text.strip().lower()
    location_2 = data.find('div', attrs={'class': 'jv-meta'})

    if location_2 is not None:
        loc = return_soup(link)
        sleep(1)
        loc_object = loc.find('p', class_='jv-job-detail-meta')

        if loc_object:
            for ct in cities:
                if ct.capitalize() in str(loc_object).split():
                    return return_lst_dict(title=title, link=link, city=ct.capitalize())
    else:
        # for cities
        for cc in cities:
            if cc in location:
                return return_lst_dict(title=title, link=link, city=cc.capitalize())


def collect_data_from_xperi() -> list[dict]:
    '''
    ... return all data from one request.
    '''

    soup = return_soup('https://jobs.jobvite.com/xperi/jobs')

    soup_data = soup.select('ul.list-unstyled.jv-job-list')
    all_categories_titles = soup.select('h3.h2')

    lst_with_data = []
    for idx, sd in enumerate(soup_data):

        # try to catch available jobs
        for aka_job in sd.select('li.row'):
            lst_with_data.append(parse_jobs(aka_job))

        # if category have show more, need to make another requests
        if sd.find('a', class_='show-more'):

            page = 0
            flag = True
            while flag != False:

                # it for showmore page:
                page_sufix = all_categories_titles[idx].text
                result_page_sufix = re.split(r"/|\s", page_sufix)
                #
                show_more_jobs = return_soup(f'https://jobs.jobvite.com/xperi/search/?p={page}&c={"-".join(result_page_sufix)}')

                if show_more_jobs.select('li.row'):
                    for job in show_more_jobs.select('li.row'):
                        lst_with_data.append(parse_jobs(job))
                else:
                    flag = False
                    break

                page += 1
                sleep(1)

    # refresh list
    new_lst_jobs = []
    for dr in lst_with_data:
        if dr is not None:
            new_lst_jobs.append(dr)

    return new_lst_jobs, len(new_lst_jobs)


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'xperi'
data_list = collect_data_from_xperi()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('xperi',
                  'https://mms.businesswire.com/media/20180104005277/en/632823/23/xpe_logo_rgb_201.jpg'
                  ))
