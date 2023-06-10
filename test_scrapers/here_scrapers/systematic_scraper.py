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


def run_scraper() -> tuple:
    """
    ... return data from site.
    """

    response = requests.get('https://jobs.systematic.com/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_country=RO',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('tr', class_='data-row')

    lst_with_data = []
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

    return lst_with_data, len(lst_with_data)
