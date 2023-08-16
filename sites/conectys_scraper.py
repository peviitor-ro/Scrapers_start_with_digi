#
#
#
# Company - conectys
# Link -> https://careers.conectys.com/careers/?paged=2&search_keywords&selected_location=bucharest
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
#
from time import sleep
from random import randint


def collect_data_from_page(num: int) -> list:
    """
    ... collect data from page to page.
    """

    response = requests.get(url=f'https://careers.conectys.com/careers/?paged={num}&search_keywords&selected_location=bucharest',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='row')

    if len(soup_data) > 0:

        hash_data = []
        lst_with_data = []
        for dt in soup_data:
            job_data = dt.find('div', class_='job-info')

            # for duplicate
            if job_data not in hash_data:
                hash_data.append(job_data)
            else:
                continue

            #
            #city = dt.find('i', class_='fa fa-map-marker')
            if job_data:
                title = dt.find('span', class_='job-title').text
                link = dt.find('a')['href']
                city = dt.find('div', class_='job-location').text.split()[0].replace(',', '')

                lst_with_data.append({
                        "id": str(uuid.uuid4()),
                        "job_title": title,
                        "job_link":  link,
                        "company": "Conectys",
                        "country": "Romania",
                        "city": city
                    })

        return lst_with_data

    else:
        return None


def get_all_data_from_site() -> list:
    """
    Get all data from the site.
    """

    global_lst_with_jobs = []
    page = 1
    flag = ''

    while flag != 'no_data':
        data = collect_data_from_page(page)

        # check data!
        if data:
            global_lst_with_jobs.extend(data)
            print(f'Page {page} done.')

        else:
            flag = 'no_data'

        # increment page
        page += 1

        # time sleep and random!
        sleep(randint(2, 4))

    return global_lst_with_jobs


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Conectys'
data_list = get_all_data_from_site()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Conectys',
                  'https://www.conectys.com/wp-content/uploads/2021/05/Conectys.svg'))
