#
#
#
# Company - CITI !
# Link -> https://jobs.citi.com/search-jobs/Romania/287/2/798549/46/25/50/2
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_data_from_citi() -> list:
    """
    Get data from websites.
    """

    response = requests.get(url='https://jobs.citi.com/search-jobs/Romania/287/2/798549/46/25/50/2',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('a')

    lst_with_data = []
    for dt in soup_data:
        if 'job' in dt['href'] and dt.find('h2'):
            link = dt['href']
            title = dt.find('h2').text.strip()
            city = dt.find('span', class_='job-location').text.split(',')[0]

            # collect data
            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link":  'https://jobs.citi.com/' + link,
                    "company": "Citi",
                    "country": "Romania",
                    "city": city
                })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Citi'
data_list = get_data_from_citi()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Citi',
                  'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMDQiIGhlaWdodD0iMTE4IiB2aWV3Qm94PSIwIDAgMjA0IDExOCIgZmlsbD0ibm9uZSI+CjxwYXRoIGQ9Ik0wLjk0Nzc1NCA3OS45NjY4QzAuOTQ3NzU0IDU4Ljk3MzIgMTguMTA5NiA0Mi42MjkyIDQwLjQ3NjMgNDIuNjI5MkM1My40MTggNDIuNjI5MiA2NS4yMzQ0IDQ4LjQwNTkgNzEuOTg2NiA1Ny4xNDE1TDYyLjI4MDMgNjYuODYzNEM1OS43MDU3IDYzLjU2MTggNTYuNDIwOCA2MC44ODQzIDUyLjY3MDEgNTkuMDMwM0M0OC45MTkzIDU3LjE3NjMgNDQuNzk5NCA1Ni4xOTM2IDQwLjYxNjkgNTYuMTU1M0MyNy4yNTMyIDU2LjE1NTMgMTYuNTYyMiA2Ni4xNTg5IDE2LjU2MjIgNzkuOTY2OEMxNi41NjIyIDkzLjkxNTUgMjcuMjUzMiAxMDMuOTE5IDQwLjYxNjkgMTAzLjkxOUM0NC45NDkgMTAzLjkxNCA0OS4yMjE0IDEwMi45MDcgNTMuMTAxIDEwMC45NzZDNTYuOTgwNiA5OS4wNDUyIDYwLjM2MjcgOTYuMjQzMiA2Mi45ODM2IDkyLjc4ODRMNzIuNTQ5MiAxMDIuMjI4QzY2LjA3ODQgMTExLjM4NyA1My42OTkzIDExNy40NDUgNDAuNDc2MyAxMTcuNDQ1QzE4LjEwOTYgMTE3LjQ0NSAwLjk0Nzc1NCAxMDEuMTAxIDAuOTQ3NzU0IDc5Ljk2NjhaIiBmaWxsPSIjMjU1QkUzIi8+CjxwYXRoIGQ9Ik04NS4yMDk1IDQ1LjE2NTNIMTAwLjU0M1YxMTQuOTA5SDg1LjIwOTVWNDUuMTY1M1oiIGZpbGw9IiMyNTVCRTMiLz4KPHBhdGggZD0iTTEyOS4wOTkgOTYuMTY5OFY1OC4xMjc4SDExMi4zNTlWNDUuMTY1M0gxMjkuODAzVjMwLjIzMDJMMTQ0LjE1MSAyMy4xODU0VjQ1LjE2NTNIMTY2Ljk0VjU4LjEyNzhIMTQ0LjE1MVY5My42MzM3QzE0NC4xNTEgMTAwLjY3OSAxNDguMDkgMTAzLjc3OCAxNTUuNTQ1IDEwMy43NzhDMTU5LjQyNSAxMDMuNzk4IDE2My4yNjMgMTAyLjk4MSAxNjYuNzk5IDEwMS4zODNWMTE0LjYyN0MxNjIuMzY5IDExNi41NzQgMTU3LjU2OSAxMTcuNTM2IDE1Mi43MzIgMTE3LjQ0NUMxMzkuMDg3IDExNy40NDUgMTI5LjA5OSAxMDkuOTc4IDEyOS4wOTkgOTYuMTY5OFoiIGZpbGw9IiMyNTVCRTMiLz4KPHBhdGggZD0iTTE3OS4wMzcgNDUuMTY1M0gxOTQuMzdWMTE0LjkwOUgxNzkuMDM3VjQ1LjE2NTNaIiBmaWxsPSIjMjU1QkUzIi8+CjxwYXRoIGQ9Ik0xMzkuNjQ4IDAuNzgyODMyQzE1Mi4yNDEgMC43NTI3MyAxNjQuNjU3IDMuNzU4MzEgMTc1Ljg0NiA5LjU0NTc1QzE4Ny4wMzUgMTUuMzMzMiAxOTYuNjY5IDIzLjczMjUgMjAzLjkzNSAzNC4wMzQ0SDE4Ni4wN0MxODAuMjE0IDI3LjUxNTQgMTczLjA1NSAyMi4zMDI2IDE2NS4wNTggMTguNzM0M0MxNTcuMDYxIDE1LjE2NiAxNDguNDAzIDEzLjMyMjEgMTM5LjY0OCAxMy4zMjIxQzEzMC44OTMgMTMuMzIyMSAxMjIuMjM2IDE1LjE2NiAxMTQuMjM5IDE4LjczNDNDMTA2LjI0MiAyMi4zMDI2IDk5LjA4MjcgMjcuNTE1NCA5My4yMjcgMzQuMDM0NEg3NS4zNjE4QzgyLjYyNzcgMjMuNzMyNSA5Mi4yNjIxIDE1LjMzMzIgMTAzLjQ1MSA5LjU0NTc1QzExNC42NCAzLjc1ODMxIDEyNy4wNTUgMC43NTI3MyAxMzkuNjQ4IDAuNzgyODMyVjAuNzgyODMyWiIgZmlsbD0iI0ZGM0MyOCIvPgo8L3N2Zz4='))
