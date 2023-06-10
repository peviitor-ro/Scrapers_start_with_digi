#
#
#
# Scrap emag job data.
# Link to data ---> https://lde.tbe.taleo.net/lde02/ats/careers/v2/searchResults?org=EMAG&cws=37
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
#
import requests
from bs4 import BeautifulSoup
#
import uuid
#
import time
from random import randint
#

def return_id_cookie():
    '''
    ... return id cookie for new requests.
    '''

    resp = requests.get('https://lde.tbe.taleo.net/lde02/ats/careers/v2/searchResults?org=EMAG&cws=37')

    return resp.headers['Set-Cookie'].split()[0]


def set_headers():
    """
    This func() is about set_headers for futures requests.
    ... need page_num 0..10..20 etc.
    """
    new_cookie = return_id_cookie()

    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': f'{new_cookie};' + 'CookieConsent={stamp:%27J99FH2S7j/82Ra9L4U+TlOL9EcWDDFksypv5/+OyCOgbv0vL0r/+Fg==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1684522150518%2Cregion:%27ro%27}; ak_bmsc=55A1603D58E113824390C0E333A9A7C1~000000000000000000000000000000~YAAQDpNOUoyFNQSIAQAAg0FZNROa78dxEJGhrJT1ChGW0zGiWYJXxXsGQJVx4Ggscnb6dk3hEdpxG0o6h9p3ZC6EbUe8lduEao9jf9iUTD7erS+7p89wOCCh4rW09a/zFvQsPL0H36enA32vvdpzAJbzEVQCySjF9y4OeZj0sJ0xcQvKtnsWZDzamT3/UE7pmmZML7YainlI2KPRuIG1t/JrToI3uQAac0QD6Zd4Zq3gTKyOrMHfT+u9F8o8dUsI4ntggIb7Jn7mfaA74Ot2kIyCOeqf4cAZj4DRArccvRgISLZY4muFWCCODbsgDc+cUqWk8/pY2Icn2P+JCLlakLRa3SdaBSYFfHZYW/QAb2eJL4ud/tPlkw5bCXMZxKSH; ADRUM_BTa="R:0|g:2f24ca57-3988-4668-a20e-5cc6ff8df5d1|n:customer1_cc2551bb-5a3a-4515-b658-a61e16e64999"; ADRUM_BT1="R:0|i:112|e:684"; bm_sv=A86E59E97463411939FD1E8E8E3B42D4~YAAQDpNOUgOGNQSIAQAA45tZNRMAXPsR36xXSMsjy+1PLAi55HHo2DmQhiTQd6FPhPeMidjWeA10obnGDtakWYPbkjofPTvqGSDI55k9JUkBdDOY0vHbn+5ik5DUiBhr868bkPkOlSf81B+aoBXFGSiWJ96+wGYUknz58hWLaRTUpVJoPV5jsHGYQqGRxHPYEFYCs5WxtCt3v4YUvROOP/zyat/L4Sh2uNp7iOj3bYQoZiha+6Yu9Xf4yjJMZtnJEmrF~1',
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


def run_scraper():
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

    # print jobs num
    print(f'Total jobs num from Emag ---> {len(lst_for_json_data)}')
    return lst_for_json_data, len(lst_for_json_data)
