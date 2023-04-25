#
#
#
# New scraper for MOL site...!
# Link here ---> https://molgroup.taleo.net/careersection/external/jobsearch.ftl?lang=en&location=4505100397
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import json
#
#


def set_headers():
    """
    This func() set new headers for this new script... MOL SCRAPER.
    """

    url = "https://molgroup.taleo.net/careersection/rest/jobboard/searchjobs?lang=en&portal=8205100397"

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'locale=en',
        'Origin': 'https://molgroup.taleo.net',
        'Referer': 'https://molgroup.taleo.net/careersection/external/jobsearch.ftl?lang=en&location=4505100397',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'tz': 'GMT+03:00',
        'tzname': 'Europe/Bucharest'
    }

    payload = '{"multilineEnabled":false,"sortingSelection":{"sortBySelectionParam":"3","ascendingSortingOrder":"false"},"fieldData":{"fields":{"KEYWORD":"","LOCATION":"4505100397","ORGANIZATION":""},"valid":true},"filterSelectionParam":{"searchFilterSelections":[{"id":"LOCATION","selectedValues":[]},{"id":"JOB_FIELD","selectedValues":[]},{"id":"JOB_SCHEDULE","selectedValues":[]},{"id":"ORGANIZATION","selectedValues":[]}]},"advancedSearchFiltersSelectionParam":{"searchFilterSelections":[{"id":"LOCATION","selectedValues":[]},{"id":"JOB_FIELD","selectedValues":[]},{"id":"JOB_LEVEL","selectedValues":[]},{"id":"JOB_TYPE","selectedValues":[]},{"id":"JOB_NUMBER","selectedValues":[]}]},"pageNo":1}'

    return url, headers, payload


def colect_data_from_mol_json():
    """
    This func() is about collect data from MOL site. Interesting method.
    """
    zota = set_headers()
    response = requests.post(zota[0].strip(), headers=zota[1], data=zota[2])

    json_data = response.json()["requisitionList"]

    lst_with_jobs_data = []
    for data in json_data:
        id_link = data['jobId']
        title_job = data['column'][0]

        new_link = f"https://molgroup.taleo.net/careersection/external/jobdetail.ftl?job={id_link}&tz=GMT%2B03%3A00&tzname=Europe%2FBucharest"

        lst_with_jobs_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title_job,
            "job_link":  new_link,
            "company": "MOL",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_with_jobs_data


def scrape_molTALEO():
    """
    This general func() is about scraping MolTaleo group.
    """

    json_list_with_jobs = colect_data_from_mol_json()

    # save it to json
    with open('scrapers_forzza/data_mol.json', 'w') as data_file:
        json.dump(json_list_with_jobs, data_file)

    print(json_list_with_jobs)
