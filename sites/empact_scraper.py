#
#
#
# New scraper for Empact company!
# Link ---> https://empact.app/careers
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_site() -> list:
    '''
    Collect data from site and store it in list.
    '''

    response = requests.get(url='https://empact.app/careers',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    #
    soup_data = soup.find('table', attrs={'class': 'table table-align-middle'}).find_all('tr')

    lst_with_data = []
    for job in soup_data:

        # save data to dict
        data_dict = {'title': None, 'location': None, 'link': None}

        for idx, under_job in enumerate(job.find_all('td')):

            match idx:
                case 0:
                    title = data_dict['title'] = \
                                under_job.find('p').text.strip()
                case 2:
                    location = data_dict['location'] \
                                = under_job.find('p').text.strip().split()[-1]
                case 3:
                    link = data_dict['link'] = \
                                'https://empact.app' + under_job.find('a')['href'].strip()

        if data_dict['title'] is not None and data_dict['location'] is not None and data_dict['link'] is not None:
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": data_dict['title'],
                "job_link": data_dict['link'],
                "company": 'Empact',
                "country": 'Romania',
                "city": data_dict['location'],
                })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Empact'
data_list = collect_data_from_site()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Empact',
                  'https://empact.app/hubfs/raw_assets/public/Empact_May_2022/images/EmpactPowerdBy.svg'
                  ))
