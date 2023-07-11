#
#
#
#
# Company -> iqvia
# Link ----> https://jobs.iqvia.com/search-jobs/Romania/24443/2/798549/46/25/50/2
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
#
from time import sleep


def return_dict(url: str, title: str, city='Romania') -> dict:
    '''
    ... return dict for scraping data.
    '''

    dct = ({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  'https://jobs.iqvia.com' + url,
            "company": "iqvia",
            "country": "Romania",
            "city": city
        })

    return dct


def return_soup_object(url: str) -> BeautifulSoup:
    '''
    ... return html data from json format.
    '''

    response = requests.get(url=url, headers=DEFAULT_HEADERS).json()

    #
    return BeautifulSoup(response['results'], 'lxml')


def collect_data_from_iqvia() -> list[dict]:
    '''
    ... collect data from site with get requests.
    '''

    lst_with_data = []
    page = 1
    #
    while True:

        # here return data from one url!
        data = return_soup_object(f'https://jobs.iqvia.com/search-jobs/results?ActiveFacetID=0&CurrentPage={page}&RecordsPerPage=12&Distance=50&RadiusUnitType=0&Keywords=&Location=Romania&Latitude=46.00000&Longitude=25.00000&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=1&SearchType=1&LocationType=2&LocationPath=798549&OrganizationIds=24443&PostalCode=&ResultsType=0&fc=&fl=&fcf=&afc=&afl=&afcf=')

        # sleep time
        sleep(0.7)

        print(f'Scrape page = {page}')

        soup_data = data.find_all('a')
        #
        if len(soup_data) > 1 and data.find('h2', class_='job-info'):

            # print all data from this site!
            for sd in soup_data:
                link = sd['href']
                title = sd.find('h2', class_='job-info')
                city = sd.find('span', class_='job-info job-location')

                if title is not None and link is not None and city is not None:
                    new_title = title.text

                    # clean city
                    if 'Various' not in city.text:
                        lst_with_data.append(return_dict(url=link,
                                                         title=new_title,
                                                         city=city.text.split()[0]))
                    else:
                        lst_with_data.append(return_dict(url=link,
                                                         title=new_title))
        else:
            break

        # increment pages
        page += 1

    return lst_with_data


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'iqvia'
data_list = collect_data_from_iqvia()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('iqvia',
                  'https://tbcdn.talentbrew.com/company/24443/22617/content/iqvia-logo-color.svg'
                  ))
