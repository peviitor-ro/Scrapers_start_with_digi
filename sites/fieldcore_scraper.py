#
#
#
#
#
#
#
#
#
# New Scraper for FieldCore!
# Link for this job page ---> https://www.fieldcore.com/careers/jobs/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_fieldcore() -> list[dict]:
    '''
    ... collect data from dynamic site.
    '''

    response = requests.get(url='https://jobs.jobvite.com/fieldcore/search?nl=1&nl=1&r=&l=Remote%20-%20Romania%20(LR18)&c=&q=&fr=true',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('td', attrs={'class': 'jv-job-list-name'})

    lst_with_data = []
    for job in soup_data:
        link = job.find('a')['href']
        title = job.find('div', attrs={'class': 'title'}).text
        location = job.find('div', attrs={'class': 'jv-job-list-location'}).text.strip()

        if 'romania' in location.lower():
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  f'https://www.fieldcore.com/careers/jobs/?p=job%2F{link.split("/")[-1]}&r=&l=Remote+-+Romania+%28LR18%29&c=&q=&nl=1',
                "company": "FieldCore",
                "country": "Romania",
                "city": location.split(',')[-1].strip(),
                })

    return lst_with_data


# update date pe viitor
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'FieldCore'
data_list = collect_data_from_fieldcore()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('FieldCore',
                  'https://www.fieldcore.com/wp-content/uploads/2022/09/logo-new.png'
                  ))
