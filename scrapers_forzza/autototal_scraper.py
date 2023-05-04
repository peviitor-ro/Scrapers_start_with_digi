#
#
#
# Scrape new website ---> Autototal
# ----> Link to this website ----------> https://www.autototal.ro/cariere/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
#
from bs4 import BeautifulSoup
#
import uuid
import json
#
import subprocess
import os


def get_data_from_bash():
    """
    This func() return all data from Autototal with bash script.
    """

    # declare a variabile with bash script
    bash_requests = ['./curl_for_autototal.sh']

    # make it executable
    os.chmod(bash_requests[0], 0o755)

    # run it
    result = subprocess.run(bash_requests, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # write file to data
    with open('autototal.html', 'w') as file_from_bash:
        file_from_bash.write(result.stdout.decode('utf-8'))

    # open autototal
    with open('autototal.html', 'r') as new_file:
        bash_data = json.load(new_file)

    soup_data = BeautifulSoup(bash_data['html'], 'lxml')

    # out data ->
    lt_data = soup_data.find_all('div', class_='entry-title title-h4')

    lst_with_data = []
    for ltd in lt_data:
        link = ltd.find('a')['href'].strip()
        title = ltd.find('span', class_='light').text.strip()

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  link,
            "company": "autototal",
            "country": "Romania",
            "city": "Romania"
        })

    return lst_with_data


# update data on peviitor
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'autototal'
data_list = get_data_from_bash()
scrape_and_update_peviitor(company_name, data_list)