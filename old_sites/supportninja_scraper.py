#
#
#
#
# Company -> supportninja
# Link ----> https://jobs.lever.co/supportninja?location=Work%20From%20Home%2C%20Romania
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_site():
    '''
    Return list with dict from one requests...
    -> with default headers.
    '''

    response = requests.get(url='https://jobs.lever.co/supportninja?location=Work%20From%20Home%2C%20Romania',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('a', attrs={'class': 'posting-title'})

    lst_with_data = []
    for sd in soup_data:
        link = sd['href']
        title = sd.find('h5').text

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  link,
            "company": "supportninja",
            "country": "Romania",
            "city": "Remote"
            })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'supportninja'
data_list = collect_data_from_site()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('supportninja',
                  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcScT6uVfDSUz9ligU2zZ2SDNLo_mQY8KcpkTdpLoSwLqIGLtcugPlOeXtViRLIgW5jMFcY'
                  ))
