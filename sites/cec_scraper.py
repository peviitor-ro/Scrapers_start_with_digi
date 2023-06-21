#
#
#
# New Scraper for CEC Bank
# ... link for this site: https://www.cec.ro/cariere
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from bs4 import BeautifulSoup
import requests
#
import json
#
import uuid


def set_global_headers():
    """
    Set global headers for new requests. Important for scraping.
    """

    url = 'https://www.cec.ro/views/ajax?_wrapper_format=drupal_ajax'

    headers = {
            'authority': 'www.cec.ro',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.5',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': 'cookiebot-consent--necessary=1; CookieConsent={stamp:%27SmbeUifP0rpvpb0j/n3KggU/3jhfCMcA4PX4iE1WRm1WSPZrUbn1Eg==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1682722318133%2Cregion:%27ro%27}; cookiebot-consent--preferences=1; cookiebot-consent--statistics=1; cookiebot-consent--marketing=1',
            'origin': 'https://www.cec.ro',
            'referer': 'https://www.cec.ro/cariere',
            'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

    data = {
            "field_cariere_judet": "All",
            "field_cariere_tip": "All",
            "search": "",
            "view_name": "cariere",
            "view_display_id": "block_1",
            "view_args": "",
            "view_path": "/node/110",
            "view_base_path": "",
            "view_dom_id": "342061481f43ca917a334b9ad5b1cba87342e830f02949144bcc72d7ec3fc8c9",
            "pager_element": "0",
            "_drupal_ajax": "1",
            "ajax_page_state[theme]": "cec",
            "ajax_page_state[theme_token]": "",
            "ajax_page_state[libraries]": "cec/bootstrap-grid,cec/cecbot,cec/form,cec/global,cec/paragraph_header,cec/paragraph_html,cec/paragraph_views,cec/styleguide,cec/tailwind,cheeseburger_menu/cheeseburger_menu.js,ckeditor_responsive_table/responsive_table,classy/base,classy/messages,cookiebot/cookiebot,core/normalize,core/picturefill,google_analytics/google_analytics,paragraphs/drupal.paragraphs.unpublished,system/base,views/views.ajax,views/views.module",
    }

    return url, headers, data


def collect_data_post_requests():
    """
    This func() make full post requests to CEC bank. Return json with data.
    """

    post_data = set_global_headers()

    response = requests.post(url=post_data[0], headers=post_data[1], data=post_data[2])
    soup_json_data = BeautifulSoup(response.json()[4]['data'], 'lxml')
    new_data = soup_json_data.find_all('h2', class_='h4')

    lst_with_data = []
    for nd in new_data:
        link = nd.find('a')['href'].strip()
        title = nd.find('a').text.strip()

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  'https://www.cec.ro' + link,
            "company": "cec",
            "country": "Romania",
            "city": "Romania"
        })

    print(lst_with_data)
    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'cec'
data_list = collect_data_post_requests()
scrape_and_update_peviitor(company_name, data_list)
