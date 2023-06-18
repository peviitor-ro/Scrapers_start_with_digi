#
#
#
# Scrap new company ---> thecoders
# link to jobs ---> https://adrya.ro/en/joburi/all/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_page(url: str) -> tuple:
    """
     Collect data ---> from the coders.
     --- in this code we have 1 flag. If flag is True,
     function continue collect data, if false, stopped.
     """

    response = requests.get(
            url=url,
            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='inner')

    flag = True
    lst_with_data = []
    for sd in soup_data:
        title = sd.find('a', class_='fancy red').text
        link = sd.find('a', class_='button bg-blue white iblock fs-12 mb-30 fancy')['data-href']

        # check if job is closed!
        closed_job = sd.find('li', class_='tags no-wrap pb-30').find('a', class_='red').text.strip()
        if closed_job == 'Closed':
            flag = False

            # stop collect data!
            continue

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "thecoders",
                "country": "Romania",
                "city": "Romania"
                })

    return lst_with_data, flag


def collect_fresh_data_from_thecoders() -> list:
    """
    Here, collect all data from site.
    Collect fresh data.
    """

    page = 1
    jobs_list_data = []

    while True:

        data = collect_data_from_page(
                url=f'https://adrya.ro/en/joburi/all/?page={page}')

        if len(data[0]) > 0:
            jobs_list_data.extend(data[0])
        elif data[1] == False:
            break

        page += 1

    # total jobs num
    print(f'---> Thecoders - Numarul total de joburi -> {len(jobs_list_data)}')
    return jobs_list_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'thecoders'
data_list = collect_fresh_data_from_thecoders()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('thecoders',
                  'https://adrya.ro/images/logo.png'
                  ))
