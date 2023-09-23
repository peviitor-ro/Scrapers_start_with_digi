#
#
#
#
# Company -> Gradle
# Linl ----> https://gradle.com/careers/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def crawl_data_from_gradle():
    '''
    ... get all data from site with one requests.
    '''

    response = requests.get(url='https://gradle.com/careers/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('li', attrs={'class': 'careers__jobs-list'})

    lst_with_data = []
    for job in soup_data:
        data = job.find('a', attrs={'class': 'careers__job-link'})
        location = job.find('div', attrs={'class': 'careers__job-location'})

        if data and location:
            title = data.text
            link = data['href']
            loc = location.text

            check_loc = loc.lower()
            if 'anywhere' in check_loc or 'emea' in check_loc or 'europe' in check_loc:
                lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": link,
                    "company": "gradle",
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


company_name = 'gradle'
data_list = crawl_data_from_gradle()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('gradle',
                  'https://cdn.freebiesupply.com/logos/thumbs/2x/gradle-1-logo.png'
                  ))
