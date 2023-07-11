#
#
#
#
# Company -> dowjones
# Link ----> https://dowjones.jobs/opis/new-jobs/#2
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


def make_req(offset: str) -> BeautifulSoup:
    '''
    ... return BeautifulSoup object from offset.
    '''

    response = requests.get(url=f'https://dowjones.jobs/opis/new-jobs/ajax/joblisting/?num_items=20&offset={offset}',
                            headers=DEFAULT_HEADERS)

    return BeautifulSoup(response.text, 'lxml')


def collect_data_from_dowjones() -> list[dict]:
    '''
    ... collect data with one requests.
    '''

    lst_with_data = []

    str_offset = 0
    while True:
        data_jobs = make_req(str(str_offset))
        soup_data = data_jobs.find_all('li', attrs={'class': 'direct_joblisting with_description'})

        if len(soup_data) > 1:
            for jobs in soup_data:
                link = jobs.find('h4').find('a')['href']
                title = jobs.find('h4').find('a').text.strip()
                city = jobs.find_all('span')[1].text.split()[0]

                if 'Romania' in city:
                    lst_with_data.append({
                            "id": str(uuid.uuid4()),
                            "job_title": title,
                            "job_link":  'https://dowjones.jobs' + link,
                            "company": "dowjones",
                            "country": "Romania",
                            "city": "Romania"
                        })
        else:
            break

        str_offset += 20
        sleep(0.7)

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'dowjones'
data_list = collect_data_from_dowjones()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('dowjones',
                  'https://dn9tckvz2rpxv.cloudfront.net/dow-jones/img/logo2.jpg'))
