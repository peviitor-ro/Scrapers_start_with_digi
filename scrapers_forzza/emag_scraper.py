#
#
#
# Scrap emag job data.
# Link to data ---> https://lde.tbe.taleo.net/lde02/ats/careers/v2/searchResults?org=EMAG&cws=37
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
#
import requests
from bs4 import BeautifulSoup
#
import uuid
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
        'Accept-Language': 'en-US,en;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID=AAF269AA89A8A450240C292FD0D04BA9; CookieConsent={stamp:%27q9oRCI730pMVBXyjzJozvyzLXlN/NiLtwTgKrmwaFNVqcGtyzk9BxA==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1682358188456%2Cregion:%27ro%27}; ak_bmsc=218CD526E93B665ECCACFD0DAEB6F7A4~000000000000000000000000000000~YAAQDpNOUmGu/6CHAQAAFBOOzhOnDaWkkyXVeTJ2zhtVB7/aPi9N+n7oU5TWoEidnu5AgeOHmriJITvPCvdYMTWp2CCYUw/IATsG+D4iZS4IjQa2EbeVd3hvegqbfFg/tVDTvO5hipOF3JMN6KcevXVGJfpiqoklvkqx/dugCaS5O6fkMGIx5z5VIMMkWsq9Y+EWPUC6l5JQc5rjk2bqgIv1ofyDhaQ1aob0HpfnGYhoSy+G5cFkBFmgTSJ2EQTCxHUyB+7gzRElHsZbNnLUYdZgItM0LB0L7mVWDayLxTkMXS6jAtDnIinjuqYDbwf4iz5Vdgp/qf9M0gN0+uaR7nxffjGb+Pjffmd78+FyTII1qsILhSBJwx5MfFV76Hpd9w==; bm_sv=93579EB54DA0B94079041FF50B6B4312~YAAQDpNOUim3/6CHAQAAjMuQzhOoKOHOdxuPcVnLzRRixy64Y+kc2E/4qTJsZy0RjjN+KBkpoLsKoruqyU1rZn0P7Ac/adK/U07zre8teWVTw/A9XFx6bbNkRPtViYDAi5jJX9nVmGIYJISTDD7yENv0eu7KNsvKqQH8wwWEDCWGfLVh0V7kIMB17xe7VaNIt2VyFPcZxeNK5yfZtmrTEmjRThagYRjyVFYe9A7O6KGnycxG/JU+JKTm6+6tOuBvEgUh~1',
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


def get_data_from_emag(page_num: int) -> None:
    """
    This func() return num of pages for scrap. Tjis func() neew a page_num
    ... for scraping data. 0..10..20
    """

    url = f'https://lde.tbe.taleo.net/lde02/ats/careers/v2/searchResults?next&rowFrom={page_num}&act=null&sortColumn=null&sortOrder=null&currentTime=1682362037768'

    response = requests.get(url, headers=set_headers())

    # check if it return something
    soup = BeautifulSoup(response.content, 'lxml')

    # make with morj operator
    if (soup_data := soup.find_all('h4', class_='oracletaleocwsv2-head-title')):

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

    else:
        return 'Error_err'


def emag_scrape():
    """
    This func() is about scrape dat on emag. Store it to json and
    ... push to peviitor.ro server.
    """

    lst_for_json_data = []

    count = 0
    flag = ''
    while flag != 'Error_err':
        all_data = get_data_from_emag(count)

        # check data ####################
        if all_data == 'Error_err':
            flag = all_data
        #################################
        else:
            lst_for_json_data.extend(all_data)

            print(f'Scraping pe pagina {count}')

            time.sleep(randint(2, 3))

            count += 10

    return lst_for_json_data


# update date pe viitor
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'emag'
data_list = emag_scrape()
scrape_and_update_peviitor(company_name, data_list)
