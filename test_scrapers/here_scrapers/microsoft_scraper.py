#
#
#
# Company -> Microsoft
# https://jobs.careers.microsoft.com/global/en/search?lc=Romania&l=en_us&pg=1&pgSz=20&o=Relevance&flt=True
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid


def run_scraper() -> tuple:
    """
    Collect data from microsoft with one requests.
    """
    # https://jobs.careers.microsoft.com/global/en/job/1557338/Support-Engineering-Manager

    response = requests.get('https://gcsservices.careers.microsoft.com/search/api/v1/search?lc=Romania&l=en_us&pg=1&pgSz=20&o=Relevance&flt=true',
                           headers=DEFAULT_HEADERS).json()

    lst_with_data = []
    for dt in response['operationResult']['result']['jobs']:
        title = dt['title']
        id_link = dt['jobId']
        city = dt['properties']['locations'][0].split()[0].replace(',', '')

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": f"https://jobs.careers.microsoft.com/global/en/job/{id_link}/{'-'.join(title.split())}",
            "company": "microsoft",
            "country": "Romania",
            "city": city
            })

    return lst_with_data, len(lst_with_data)
