#
#
#
#
# Company -> Raben
# Link ----> https://romania.raben-group.com/cariere
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS
#
import requests
#
import uuid


def make_get_req(url: str = '') -> tuple:
    '''
    ... Here prepare get requests to the site.
    '''

    url = f'https://romania.raben-group.com/headless/cariere{url}'

    headers = {
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://romania.raben-group.com/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            }

    return url, headers


def collect_data_from_site() -> list[dict]:
    '''
    ... here collect all data from site.
    '''

    lst = []
    for page in requests.get(url=make_get_req('')[0], headers=make_get_req('')[1]).json()['content']['colPos0'][1]['content']['tiles']:
        url = page['content']['link']['url']

        if 'cariere' in url:
            new_url = '/' + url.split('/')[-1]
            link, headers = make_get_req(new_url)
            print(link)
            for job in requests.get(url=link, headers=headers).json()['content']['colPos0'][1]['content']['offers']:
                title = job['title']
                link = job['link']['url']
                city = job['city']

                lst.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link":  link,
                    "company": "raben",
                    "country": "Romania",
                    "city": city,
                    })

    return lst, len(lst)


print(collect_data_from_site())
