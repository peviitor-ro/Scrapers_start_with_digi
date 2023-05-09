#
#
#
# Make new Scraper for bertrandtgroup --->
# Link to this Company ---> https://bertrandtgroup.onlyfy.jobs/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
#
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import time
from random import randint


def set_headers():
    """
    Set special headers for requests to https://bertrandtgroup.onlyfy.jobs/.
    """

    headers = {
        'authority': 'bertrandtgroup.onlyfy.jobs',
        'accept': 'text/html, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'PHPSESSID=yXh2rZ8BwhY7wO2e42u92To1t7K9z8ISWDmZrz3F7eeT13i0x%2CB5pCAed1gKY-T8SKZM1RfpZT2xg1jd3RZ7xm4NmeYsNm5WmSXtbuWgLBi8ES3iHD85V09gkGbGGMu5MHKOiCsX-NEhsJEczwyhP-fKHldnRzUUh-t5mvWM5R3176Xq5wwuTVUSBknSt1RSWAVbEGrEnEE7CNtjWlnTvERCbXCgXsZy',
        'referer': 'https://bertrandtgroup.onlyfy.jobs/',
        'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
        }

    return headers


def collect_data_from_site():
    """
    ... Make requests and collect data from site.
    """

    page = 1
    flag = None

    # go through links and collect data!
    lst_with_data = []
    while flag != 'no_data':

        response = requests.get(
                f'https://bertrandtgroup.onlyfy.jobs/candidate/job/ajax_list?display_length=10&page={page}&sort=matching&sort_dir=DESC&search=&_=1683486187449',
                headers=set_headers())
        soup = BeautifulSoup(response.text, 'lxml')

        soup_data = soup.find_all('div', class_='cell-table col-sm-14 col-xs-16')

        if 'href' in str(soup_data):
            # collect data and store it in list with data!
            for sd in soup_data:
                link = sd.find('h3').find('a')['href']
                title = sd.find('h3').find('a').text

                # add data to list!
                lst_with_data.append({
                        "id": str(uuid.uuid4()),
                        "job_title": title,
                        "job_link":  'https://bertrandtgroup.onlyfy.jobs' + link,
                        "company": "bertrandtgroup",
                        "country": "Romania",
                        "city": "Romania"
                    })
        else:
            print('Page not found. Scraper end job.')
            flag = 'no_data'

        # increment page
        print(f"Page {page} scraped!")
        page += 1

        # sleep for secure
        time.sleep(randint(1, 2))

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'bertrandtgroup'
data_list = collect_data_from_site()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('bertrandtgroup', 'https://content.prescreen.io/company/logo/2zflb91e9rc4s8gskgco4g84gss0kgw.jpg'))
