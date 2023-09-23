#
#
#
#
# Company -> fabricdata
# Link ----> https://www.fabricdata.com/corporate/careers
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
#
import itertools


def return_lst_dict(title: str, link: str, city: str) -> dict:
    '''
    ... this function will return a dict to append to a list and avoid DRY
    '''
    dct = {
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "Fabric",
                "country": "Romania",
                "city": city
            }

    return dct


def get_soup_object(url: str) -> BeautifulSoup:
    '''
    ... at first time need to get soup object.
    '''

    respone = requests.get(url=url,
                           headers=DEFAULT_HEADERS)

    return BeautifulSoup(respone.text, 'lxml')


def get_all_titles_and_images_tags() -> tuple:
    '''
    Here we will get all images links and titles.
    '''

    titles = []
    images_src = []
    cities = []

    soup = get_soup_object('https://www.fabricdata.com/corporate/careers')

    for data_job in soup.find_all('div', attrs={'class': 'card__content'}):
        titles.append(data_job.find('h3').text)
        images_src.append(data_job.find('img', attrs={'class': 'image'})['src'])
        cities.append(data_job.find('div', attrs={'class': 'card__description'}).find('p').text)

    return titles, images_src, cities


def get_link_from_title(title: str) -> list[str]:
    '''
    ... make valid link from title.
    '''

    special_chars = [',', '(', ')', '&', ',', '|', '.']
    split_words = title.lower().split()
    without_special_char = []
    for dd in split_words:
        for sc in special_chars:
            dd = dd.replace(sc, '')

        without_special_char.append(dd)

    # here combination for links
    combinations = []
    for r in range(1, len(without_special_char) + 1):
        combinations.extend(list(itertools.combinations(without_special_char, r)))

    links = ['-'.join(combination).lower() for combination in combinations]

    return links


def get_valid_link_for_job(title: str) -> str:
    '''
    ... get valid job for new.
    '''

    # https://www.fabricdata.com/corporate/careers/senior-backend

    for i_url in get_link_from_title(title):
        link = f'https://www.fabricdata.com/corporate/careers/{i_url}'
        #
        dd_local = requests.head(url=link, headers=DEFAULT_HEADERS).status_code
        if dd_local == 200:
            return link


def get_data_and_test_it():
    '''
    ... here get links and get data from it.
    '''
    titles, src, cities = get_all_titles_and_images_tags()

    lst_with_data = []
    if len(titles) == len(src):

        for i in range(len(titles)):
            if 'romania' in cities[i].lower():
                # here extract data!
                split_link_img = src[i].split('/')[-1].split('.')[0].strip()
                # make head requests
                link = f'https://www.fabricdata.com/corporate/careers/{split_link_img}'
                #
                dd_data = requests.head(url=link, headers=DEFAULT_HEADERS).status_code
                if dd_data == 200:
                    data_test_check = get_soup_object(link)
                    if (h2_1 := data_test_check.find('h2').text):
                        lst_with_data.append(return_lst_dict(title=h2_1, link=link, city=cities[i].split()[0].replace(',', '')))

                else:
                    link = get_valid_link_for_job(titles[i].strip())
                    if link:
                        data_test_check2 = get_soup_object(link)
                        if (h2_2 := data_test_check2.find('h2').text):
                            lst_with_data.append(return_lst_dict(title=h2_2, link=link, city=cities[i].split()[0].replace(',', '')))
    print(lst_with_data)
    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Fabric'
data_list = get_data_and_test_it()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Fabric',
                  'https://mma.prnewswire.com/media/1701193/Fabric2_Logo.jpg?p=twitter'
                  ))
