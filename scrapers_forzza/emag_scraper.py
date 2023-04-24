#
#
#
# Scrap emag job data.
# Link to data ---> https://lde.tbe.taleo.net/lde02/ats/careers/v2/searchResults?org=EMAG&cws=37
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import json
#
import re
#
import time
from random import randint
#


def set_headers():
    """
    This func() is about set_headers for futures requests.
    ... need page_num 0..10..20 etc.
    """

    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.6',
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID=A20086F84DF0456922BDEC3CDDC02AC0; CookieConsent={stamp:%27q9oRCI730pMVBXyjzJozvyzLXlN/NiLtwTgKrmwaFNVqcGtyzk9BxA==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1682358188456%2Cregion:%27ro%27}; ak_bmsc=425A0036809D3401D7FA1BB346BE3550~000000000000000000000000000000~YAAQDpNOUpk10KCHAQAAb0lktBMfPshgdX7wquz1tRa993E7nKLN4mZRIEF8pgN1shEt2lGa/KgpRTZU2uwEGaTnmlnHckErf1+uls363nmppVMRU/gBdT2dXs0v1UbZ9ahij+H9ycuq7mOqTPU8nrIyH6s7DnXfgNpXQo6pKZY73I1+gv5FOwiZJFvq1e9TVR0/URG/78OGgTOB3tp7+TezhAIPL2gQPOdSRrwZbzqgbVff82kZIjZLqhXquzedmGGl52+bchyJKnBGJ/uHU9Pm7dMTu1EdgKnYSm++ocP9EkV25veGl2gLTR5MRA3v84POylIzJzLWGVNSBWDuPNKr4MgrRTzr/xBACUYBXLULh7CxR5iWtVk26CQrgKb9qA==; ADRUM_BTa="R:0|g:247cbab2-6c23-4d56-9851-7c4019c6e012|n:customer1_cc2551bb-5a3a-4515-b658-a61e16e64999"; ADRUM_BT1="R:0|i:112|e:123"; bm_sv=42175CF5B5847D78296D882670FE4DFB~YAAQDpNOUsew0KCHAQAAo3eXtBP/WBBdNW+GuOPZ4cd+35YlLuEgehkGuz3kda9eDRAC8Ogwt2VUtWhmUmmJHlLWc/kdGTrwc14WvLRGvrELMrXde4c/AWQz1Levya+4yGTt7QccDa0YBh7mq5V5qLz6urzAjplf8kjZrLrQsV2uBZggrhnX2in4rHvhKf01lJw8utTc2WQ4FA8VzusFL23f8yTzxHzbljUqVVeUUhEQ2CcYzZEtQaDmKf3aUr/t762LYA==~1',
        'Referer': 'https://lde.tbe.taleo.net/lde02/ats/careers/v2/searchResults?org=EMAG&cws=37',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }

    return headers


def return_num_of_pages():
    """
    ... this func is about return a nums of pages.
    """
    response_pages = requests.get('https://lde.tbe.taleo.net/lde02/ats/careers/v2/viewRequisition?org=EMAG&cws=37&rid=3303', headers=set_headers())
    soup_pages = BeautifulSoup(response_pages.content, 'lxml')

    values = soup_pages.find('input', class_='form-control')
    page_num = values['value'].split()[-1]

    return page_num


def get_data_from_emag(page_num: int) -> None:
    """
    This func() return num of pages for scrap. Tjis func() neew a page_num
    ... for scraping data. 0..10..20
    """

    url = f'https://lde.tbe.taleo.net/lde02/ats/careers/v2/searchResults?next&rowFrom={page_num}&act=null&sortColumn=null&sortOrder=null&currentTime=1682362037768'

    response = requests.get(url, headers=set_headers())
    soup = BeautifulSoup(response.content, 'lxml')

    soup_data = soup.find_all('h4', class_='oracletaleocwsv2-head-title')

    lst_clean_data = []
    for dirty_data in soup_data:
        dirty_link = dirty_data.a['href']
        clean_title = dirty_data.text

        # clean link
        easy_clean_link = dirty_link.replace('amp;', '').replace('amp;', '')

        lst_clean_data.append({
            "id": str(uuid.uuid4()),
            "job_title": clean_title,
            "job_link":  easy_clean_link,
            "company": "emag",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_clean_data


def emag_scrape():
    """
    This func() is about scrape dat on emag. Store it to json and
    ... push to peviitor.ro server.
    """

    # start scrape all data from this server emag
    pages = int(return_num_of_pages())
    time.sleep(0.7)

    lst_for_json_data = []
    for req in range(0, pages, 10):
        all_data = get_data_from_emag(req)
        lst_for_json_data.extend(all_data)

        print(f'Scraping pe pagina {req}')

        time.sleep(randint(2, 5))

    # save data to json file
    with open('scrapers_forzza/data_emag.json', 'w') as json_file:
        json.dump(lst_for_json_data, json_file)


emag_scrape()


# https://lde.tbe.taleo.net/lde02/ats/careers/v2/viewRequisition?org=EMAG&cws=37&rid=3303
# https://lde.tbe.taleo.net/lde02/ats/careers/v2/viewRequisition?org=EMAG&amp;cws=37&amp;rid=3303
