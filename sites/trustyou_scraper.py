#
#
#
#
# Company -> trustyou
# Link ----> https://www.trustyou.com/careers#openings
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_trustyou() -> list[dict]:
    '''
    ... collect data from trustYOU with one requests and default headers.
    '''

    response = requests.get(url='https://www.trustyou.com/careers#openings',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('ul', attrs={'class': 'careers-listing careers-listing-archive'})

    lst_with_data = []
    for ul in soup_data:
        for li_job in ul:
            data = li_job.find('a')

            # search for locations
            location_h4 = li_job.find_all('p')

            if data and ('Romania' in str(location_h4) or 'Cluj' in str(location_h4)):
                title = data.text
                link = data['href']

                lst_with_data.append({
                        "id": str(uuid.uuid4()),
                        "job_title": title,
                        "job_link":  link,
                        "company": "trustyou",
                        "country": "Romania",
                        "city": "Cluj"
                    })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'trustyou'
data_list = collect_data_from_trustyou()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('trustyou',
                  'https://play-lh.googleusercontent.com/SzbVFK34kqMq1IbRFf5FhlNW0APelGW17Elb0aaBEdlRk_zHgbm7YYp9rEnN9kFBK0k'
                  ))
