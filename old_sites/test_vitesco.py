#
#
#
#
#
#
# Link -> https://jobs.vitesco-technologies.com/search/?q=&locationsearch=Romania&startrow=
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS
import requests
from bs4 import BeautifulSoup
#
from time import sleep
import uuid


# make session with requests
session = requests.Session()


def get_soup_object(url: str) -> BeautifulSoup:
    '''
    ... No DRY! Return bs4 object.
    '''

    response = session.get(url=url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    return soup


def get_num_jobs() -> int:
    '''
    Get num jobs from site.
    '''

    soup_object = get_soup_object(url='https://jobs.vitesco-technologies.com/search/?q=&locationsearch=Romania')
    total_num = soup_object.find('div', attrs={'class': 'pagination-label-row'}).text.strip().split('\n')[0].split()[-1]

    return total_num


def get_jobs_from_vitesco() -> list[dict]:
    '''
    ... get all jobs
    '''

    num_for = int(get_num_jobs())

    lst_with_data = []
    for page in range(0, num_for, 25):
        page_data = get_soup_object(url=f"https://jobs.vitesco-technologies.com/search/?q=&locationsearch=Romania&startrow={page}")

        print(f"Hei, we are on page {int(page/25) + 1}")

        for job in page_data.find_all('tr', attrs={'class': 'data-row'}):
            title_link = job.find('a', attrs={'class': 'jobTitle-link'})

            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title_link.text,
                "job_link": 'https://jobs.vitesco-technologies.com' + title_link['href'],
                "company": "Vitesco",
                "country": "Romania",
                "city": job.find('td', attrs={'class': 'colLocation hidden-phone'}).text.strip().split(',')[0]
                })

        # sweet sleep!
        sleep(1)

    return lst_with_data, len(lst_with_data)


print(get_jobs_from_vitesco())
