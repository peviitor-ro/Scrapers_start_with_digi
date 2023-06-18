#
#
#
# Company -> LeasePlan
# Link -> https://www.leaseplan.com/en-lh/lpsc/overview/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_updated_data():
    """
    ... prepare headers for requests.
    """

    response = requests.get('https://www.leaseplan.com/api2/lh/vacancies/',
                             headers=DEFAULT_HEADERS).json()

    lst_with_data = []
    for dt in response:
        try:
            if dt['locationCountry'] in ['Romania']:
                link = dt['referenceID']
                title = dt['jobPostingTitle']
                city = dt['locationCity']
                if '-' in city:
                    city = city.split('-')[-1]

                lst_with_data.append({
                        "id": str(uuid.uuid4()),
                        "job_title": title,
                        "job_link": f'https://www.leaseplan.com/en-lh/lpsc/overview/{link}/',
                        "company": "leaseplan",
                        "country": "Romania",
                        "city": city
                        })
        except:
            pass

    return lst_with_data


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'leaseplan'
data_list = get_updated_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('leaseplan',
                  'https://www.leaseplan.com/-/media/leaseplan-digital/shared/images/other/site-logo/leaseplan/leaseplanlogoheader2x.png?rev=-1&mw=1300'
                  ))
