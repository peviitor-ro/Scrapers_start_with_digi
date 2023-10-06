#
#
#
# Company -> systematic!
# Link -> https://jobs.systematic.com/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_country=RO!
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


# init Session
session = requests.Session()


def get_soup_object(url: str) -> BeautifulSoup:
    """
    ... return soup object.
    """
    response = session.get(url=url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    return soup


def get_data_from_systematic() -> str:
    """
    ... return data from site.
    """
    get_jobs_soup = get_soup_object('https://jobs.systematic.com/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_country=RO')
    get_jobs_num = get_jobs_soup.find('div', attrs={'class': 'pagination-label-row'}).text.strip().split('\n')[0].split(' ')[-1]

    lst_with_data = []
    for i in range(0, int(get_jobs_num), 10):

        # get response from site
        url_systematic = f'https://jobs.systematic.com/search/?q=&sortColumn=referencedate&sortDirection=desc&optionsFacetsDD_country=RO&startrow={i}'
        data = get_soup_object(url=url_systematic)
        soup_data = data.find_all('tr', class_='data-row')

        for dt in soup_data:
            title = dt.find('a').text
            link = dt.find('a')['href']
            city = dt.find('span', class_='jobLocation').text.split()[0].replace(',', '')

            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link":  "https://jobs.systematic.com/" + link,
                    "company": "systematic",
                    "country": "Romania",
                    "city": city
                    })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'systematic'
data_list = get_data_from_systematic()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('systematic',
                  'https://seekvectorlogo.com/wp-content/uploads/2020/02/systematic-inc-vector-logo.png'
                  ))
