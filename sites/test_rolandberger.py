#
#
#
#
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS
import requests
from bs4 import BeautifulSoup


def return_soup(page: str):

    response = requests.get(url=f'https://careers.smartrecruiters.com/RolandBerger/api/groups?page={page}',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    return soup


def return_soup_show_more(page: str):

    response = requests.get(url=f'https://careers.smartrecruiters.com/RolandBerger/api/more?type=location&value=Bucharest%2C%20RO&page={page}',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    return soup


def get_data():

    page = 1
    page_show_more = 1
    while True:

        data = return_soup(str(page))
        soup_data = data.find_all('section', attrs={'class': 'openings-section opening opening--grouped js-group'})

        if len(soup_data) > 1:
            for sd in soup_data:
                title_country = sd.find('li').find('h3', attrs={'class': 'opening-title title display--inline-block text--default'}).text

                # check for job in Ro!
                if 'Bucharest' in title_country or 'Romania' in title_country:

                    # search all jobs:
                    for ro_job in sd.find_all('li', attrs={'class': 'opening-job job column wide-7of16 medium-1of2'}):

                        link = ro_job.find('a', attrs={'class': 'link--block details'})['href']
                        title = ro_job.find('h4', attrs={'class': 'details-title job-title link--block-target'}).text

                        print(link, title)

                    if sd.find('ul', attrs={'class': 'list--dotted'}):
                        show_more_data = return_soup_show_more(str(page_show_more))

                        print('if show more')

                        for n_job in show_more_data.find_all('li', attrs={'class': 'opening-job job column wide-7of16 medium-1of2'}):


                            link = n_job.find('a', attrs={'class': 'link--block details'})['href']
                            title = n_job.find('h4', attrs={'class': 'details-title job-title link--block-target'}).text

                            print(title, link)

        else:
            break

        page += 1


get_data()
