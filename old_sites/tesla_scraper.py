#
#
#
# This is script for Tesla!
# Link to tesla ---> https://www.tesla.com/ro_ro/careers
#
# https://www.tesla.com/ro_RO/careers/search/job
# (mai departe titlul prin - - - concatenat + id)
#
# Example - Title - Open Tech Day Bucharest - 27th April 2023
# ---------> link - https://www.tesla.com/ro_RO/careers/search/job/open-tech-day-bucharest-27th-april-2023-179440
# ---------> link - https://www.tesla.com/cua-api/apps/careers/state
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
#
import uuid


def return_response_from_api(url: str, headers: dict):
    """
    This func make a full request to tesla api.
    """

    response = requests.get(url=url, headers=DEFAULT_HEADERS).json()

    return response


def return_all_dict_data_jobs():
    """
    This func() return all nums from api, Romania.
    """

    data = return_response_from_api('https://www.tesla.com/cua-api/apps/careers/state', DEFAULT_HEADERS)

    data_lst = []
    ###
    try:
        all_l_nums = data['geo'][1]['sites'][22]['cities']
        for dl in all_l_nums:
            data_lst.extend(all_l_nums[dl])
    except:
        all_l_nums = data['geo'][1]['sites'][23]['cities']
        for dl in all_l_nums:
            data_lst.extend(all_l_nums[dl])
    ###

    lst_with_dict_data = []
    for data in data['listings']:
        cod = data['l']

        if cod in data_lst:
            lst_with_dict_data.append(data)

    return lst_with_dict_data


def return_links_with_jobs():
    """
    This func() return all jobs from this nums...
    """
    list_dict = return_all_dict_data_jobs()

    list_for_pe_viitor = []
    for ide in list_dict:
        link_1 = ide['t'].lower().replace('- ', '').split()
        link_2 = str(ide['id'])

        title = ide['t']
        link_final = 'https://www.tesla.com/ro_RO/careers/search/job/' + '-'.join(link_1) + '-' + link_2

        list_for_pe_viitor.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  link_final,
            "company": "Tesla",
            "country": "Romania",
            "city": "Romania"
            })

    return list_for_pe_viitor


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Tesla'
data_list = return_links_with_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Tesla',
                  'https://autostickere.ro/image/cache/catalog/Stickere/Stickere%20Auto/Stickere%20Marci/Tesla/sticker-tesla-text-1000x1000.jpg'
                  ))
