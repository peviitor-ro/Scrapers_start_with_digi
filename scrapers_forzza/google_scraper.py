#
#
#
# Company Google
# link to Google -> https://careers.google.com/jobs/results/?distance=50&has_remote=false&hl=en_US&jlo=en_US&location=Romania&q=
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid


def get_data_from_google():
    """
    Get data from Google with one requests.
    """

    response = requests.get('https://careers.google.com/api/v3/search/?distance=50&has_remote=false&hl=en_US&jlo=en_US&location=Romania&q=',
                            headers=DEFAULT_HEADERS).json()['jobs']

    lst_with_data = []
    for dt in response:
        title = dt['title']
        id_link = dt['id'][5:]
        city = dt['locations'][0]['city']

        # prepare link here
        new_title = title.replace(',', '').replace('(', '').replace(')', '').lower().split()

        lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": f"https://careers.google.com/jobs/results/{id_link}-{'-'.join(new_title)}/?location=Romania",
                    "company": "google",
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


company_name = 'google'
data_list = get_data_from_google()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('google',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google_2015_logo.svg/250px-Google_2015_logo.svg.png'
                  ))
