#
#
#
# Company -> Bittnet
# link -> https://www.bittnet.jobs/1048/lista-posturi
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_all_data() -> list:
    '''
    Get all data with one requests.
    '''

    url = 'https://www.bittnet.jobs/api/dataexchange'

    headers = {
          'authority': 'www.bittnet.jobs',
          'accept': '*/*',
          'accept-language': 'en-US,en;q=0.9',
          'content-type': 'application/x-www-form-urlencoded',
          'cookie': 'ASP.NET_SessionId=3cvagebpnxti2t45gaeeuljk',
          'origin': 'https://www.bittnet.jobs',
          'referer': 'https://www.bittnet.jobs/1048/lista-posturi',
          'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Linux"',
          'sec-fetch-dest': 'empty',
          'sec-fetch-mode': 'cors',
          'sec-fetch-site': 'same-origin',
          'sec-gpc': '1',
          'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        }

    data = {
        'transport': 'fIh90vbStQIALVzhryTM9x36QRnts/ePtYlI87cxS0cXz19ykXlxbmAJ1k7B0ZDAjCVuZLJPXOGvl42IJKBKDFzMDFBnFyczbKnMCBUWY9Y6+PE3vJcHEA4ilpm3RcGcpaJbyMOhThOc2OZxj8WuogjgJZf1glGs07nPpuj04bjgzGFMsx0ZLQ1m4hNV8VckIywX09XfIa8ift0H0nIUF/aMlw6ui9gnTWtfUrZ65Kk=',
        'cykey': 'GPDZ7aKmCgjKD1PPGfoZi3zmwID/9biWpa/qBAwwwwwwwwAAAAAA123456789AAAAAAAAwwwwwwww5gJ0XHRvpQlTO41uwwwwwwwwAAAAAA123456789AAAAAAAAwwwwwwwwzJkeoul8ABZYOSty5ceMZGZUb26pRZt54LPzpHuRDygjqoG4XKdTVvPtxIzOcnOzDHFEwfezePNR4RAlSD36jJaGMYb6/wwwwwwwwAAAAAA123456789AAAAAAAAwwwwwwwwEjFtg40mqqJkCg13E03yC51ktGelZx/qOoycjuwwwwwwwwAAAAAA123456789AAAAAAAAwwwwwwwwO2T5wwwwwwwwAAAAAA123456789AAAAAAAAwwwwwwwwraJSnyHpi7hnavdtWHPw=='
        }

    return url, headers, data


def make_post_request():
    """
    Here make a post request.
    """

    data = get_all_data()
    response = requests.post(url=data[0], headers=data[1], data=data[2])

    lst_with_data = []
    for dt in response.text.split('|'):
        split_dt = dt.split('¦')

        title = split_dt[2]
        link = 'https://www.bittnet.jobs/' + split_dt[-1].replace('┼8', '')
        city = split_dt[4]

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "bittnet",
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


company_name = 'bittnet'
data_list = make_post_request()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('bittnet',
                  'https://www.bittnet.jobs/img/logo_ro.png'))
