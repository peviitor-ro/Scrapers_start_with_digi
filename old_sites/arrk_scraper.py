#
#
#
#
# Company -> arrk
# Link -> https://arrkeurope.onlyfy.jobs/candidate/job/ajax_list?display_length=400&page=1&sort=matching&sort_dir=DESC&search=&_ps_widget_token=tMU6eTWJkBAGWF7DxNep3O83rN2owhZyjUrvVqLojQ704xeU3sRAvmKFfnnzc9WKaZKQVgh459vPDJRviAvJnA8sbU4j0j7jb9r9ZI0OBoT99CuysZwQcMyyu3uv5WrQIFzBb3TBxP-UT-zl7YZN-KMzPnzs,mHgPgtQPsr5xVNp2784JeZZ0VswqwmbAkFqDUzbyCAYV2Q0iBOQhpofKQoRsT1yHksD&parentUrl=https://engineering.arrk.com/jobs-career/current-job-offers&widgetConfig=yl6c10ku&_=1687204199282
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def scrape_data_from_arrk():
    '''
    Scrap all data from arrk with one requests.
    '''

    response = requests.get(url='https://arrkeurope.onlyfy.jobs/candidate/job/ajax_list?display_length=400&page=1&sort=matching&sort_dir=DESC&search=&_ps_widget_token=tMU6eTWJkBAGWF7DxNep3O83rN2owhZyjUrvVqLojQ704xeU3sRAvmKFfnnzc9WKaZKQVgh459vPDJRviAvJnA8sbU4j0j7jb9r9ZI0OBoT99CuysZwQcMyyu3uv5WrQIFzBb3TBxP-UT-zl7YZN-KMzPnzs,mHgPgtQPsr5xVNp2784JeZZ0VswqwmbAkFqDUzbyCAYV2Q0iBOQhpofKQoRsT1yHksD&parentUrl=https://engineering.arrk.com/jobs-career/current-job-offers&widgetConfig=yl6c10ku&_=1687204199282',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data_1 = soup.find_all('div', class_='row row-table row-24 collapsed row-table-condensed')
    soup_data_2 = soup.find_all('div', class_='row row-table row-24 collapsed even row-table-condensed')

    lst_with_data = []

    # first div
    for i_dt in soup_data_1:
        link = i_dt.find('a')['href']
        title = i_dt.find('a').text
        location = i_dt.find('div', class_='cell-table col-sm-6 col-xs-8').text.strip()

        if location == 'Cluj-Napoca':
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "ARRK",
                "country": "Romania",
                "city": location
                })

    # second div!
    for j_dt in soup_data_2:
        link = j_dt.find('a')['href']
        title = j_dt.find('a').text
        location = j_dt.find('div', class_='cell-table col-sm-6 col-xs-8').text.strip()

        if location == 'Cluj-Napoca':
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "ARRK",
                "country": "Romania",
                "city": location
                })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'ARRK'
data_list = scrape_data_from_arrk()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('ARRK',
                  'https://www.arrk.com/wp/wp-content/themes/SmartPack3.0-Ver/img/logo-blue.svg'
                  ))
