#
#
#
# New scraper for company - playtika
# Link to this company - https://www.playtika.com/careers/all/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid


def collect_all_data_from_playtika() -> list:
    """
    ... collect data from playtika. Search only
    romanian jobs.
    """

    response = requests.get(
            url='https://www.comeet.co/careers-api/2.0/company/01.001/positions?token=101404202909505303909202606606&details=true',
            headers=DEFAULT_HEADERS)

    lst_with_data = []
    for dt in response.json():

        # try except!
        try:
            data = dt['location']['name']
            if data == "Romania":

                # here collect data --->
                link = dt['url_active_page']
                title = dt['name']

                lst_with_data.append({
                        "id": str(uuid.uuid4()),
                        "job_title": title,
                        "job_link":  link,
                        "company": "playtika",
                        "country": "Romania",
                        "city": "Romania"
                    })

        except:
            pass

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'playtika'
data_list = collect_all_data_from_playtika()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('playtika',
                  'https://www.playtika.com/img/logo-playtika.png'
                  ))
