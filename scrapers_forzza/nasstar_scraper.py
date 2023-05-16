#
#
#
# Start scrape Nasstar
# link -> https://nasstar.teamtailor.com/jobs?location=Bucharest&query=
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_nasstar() -> list:
    """
    Collect data from one requests.
    """

    response = requests.get(
            url='https://nasstar.teamtailor.com/jobs?location=Bucharest&query=',
            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('a', class_='flex flex-col py-6 text-center sm:px-6 hover:bg-gradient-block-base-bg focus-visible-company focus-visible:rounded')

    lst_with_data = []
    for sd in soup_data:
        link = sd['href']
        title = sd.find('span', class_='text-block-base-link sm:min-w-[25%] sm:truncate company-link-style').text

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "nasstar",
                "country": "Romania",
                "city": "Romania"
            })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'nasstar'
data_list = collect_data_nasstar()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('nasstar',
                  'https://images.teamtailor-cdn.com/images/s3/teamtailor-production/logotype-v3/image_uploads/d7dd57ca-b67c-4c32-82fa-548d166e6142/original.png'
                  ))
