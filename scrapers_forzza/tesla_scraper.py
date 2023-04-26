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
import requests
#
import uuid
import json


def set_headers():
    """
    This function is about setting headers for Tesla.
    """
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }

    return HEADERS


def return_response_from_api(url: str, headers: dict):
    """
    This func make a full request to tesla api.
    """

    response = requests.get(url=url, headers=headers).json()

    return response


def return_all_dict_data_jobs():
    """
    This func() return all nums from api, Romania.
    """

    data = return_response_from_api('https://www.tesla.com/cua-api/apps/careers/state', set_headers())
    all_l_nums = data['geo'][1]['sites'][24]['cities']['București']

    lst_with_dict_data = []
    for data in data['listings']:
        cod = data['l']

        if cod in all_l_nums:
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
            "company": "tesla",
            "country": "Romania",
            "city": "Romania"
            })

    return list_for_pe_viitor


def scrape_tesla():
    """
    Last part of script. Store here all logic of code. Tesla!
    """

    lst_final = return_links_with_jobs()

    print(lst_final)

    # save to json()
    with open('scrapers_forzza/data_tesla.json', 'w') as new_file:
        json.dump(lst_final, new_file)

    print("Tesla ---> Done!")
