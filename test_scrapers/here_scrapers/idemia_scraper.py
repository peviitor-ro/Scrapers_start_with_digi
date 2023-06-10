#
#
#
# New company to scrape ---> Idemia
# Link to this company ---> https://careers.idemia.com/
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
    Collect all data from idemia.
    """

    response = requests.get(url='https://careers.idemia.com/search/?createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_city=&optionsFacetsDD_customfield2=&optionsFacetsDD_customfield3=',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('tr', class_='data-row')

    lst_with_data = []
    for sd in soup_data:
        link = sd.find('a', class_='jobTitle-link')['href']
        title = sd.find('a', class_='jobTitle-link').text

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  'https://careers.idemia.com/' + link,
            "company": "idemia",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_with_data, len(lst_with_data)
