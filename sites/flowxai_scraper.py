#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> FlowxAI
# Link ------> https://apply.workable.com/flowxai/
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
import json

from __utils import (
    PostRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,

    # for this time
    GetHeadersDict,

    get_data_with_regex,
)


def get_cookie_ids():
    '''
        ... get unic ids for cookie, headers
    '''
    string_regex_data = str(GetHeadersDict('https://apply.workable.com/flowxai/'))

    return get_data_with_regex('__cf_bm=([^;]+);', string_regex_data), get_data_with_regex('wmc=([^;]+);', string_regex_data)


def prepare_headers():
    '''
        ... prepare post personalized post requests
    '''
    data_ids = get_cookie_ids()
    #
    url = 'https://apply.workable.com/api/v3/accounts/flowxai/jobs'
    headers = {
        'authority': 'apply.workable.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en',
        'content-type': 'application/json',
        'cookie': f'{data_ids[1]} {data_ids[0]} _dd_s=rum=0&expire=1708242969216',
        'origin': 'https://apply.workable.com',
        'referer': 'https://apply.workable.com/flowxai/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    payload = {
        'query': '',
        'location': [],
        'department': [],
        'worktype': [],
        'remote': [],
        'workplace': [],
    }

    return url, headers, payload


def scraper():
    '''
    ... scrape data from FlowXAI scraper.
    '''

    data_prepare_headers = prepare_headers()
    url, headers, payload = data_prepare_headers

    # Romania has no jobs left, so scrape the full list from the source.
    job_list = []
    seen_shortcodes = set()
    next_page = None

    while True:
        request_payload = dict(payload)
        if next_page:
            request_payload['token'] = next_page

        post_data = PostRequestJson(url=url, custom_headers=headers, data_raw=json.dumps(request_payload))
        results = post_data.get('results') or []

        for job in results:
            shortcode = job.get('shortcode')
            if shortcode in seen_shortcodes:
                continue
            seen_shortcodes.add(shortcode)

            job_location = job.get('location') or {}
            location = (job_location.get('city') or '').strip()
            job_country = job_location.get('country') or ''

            if location.lower() == 'bucharest':
                location = 'Bucuresti'

            location_finish = get_county(location=location)

            # get jobs items from response
            job_list.append(Item(
                job_title=job.get('title'),
                job_link=f'https://apply.workable.com/flowxai/j/{shortcode}/',
                company='FlowXAI',
                country=job_country,
                county=location_finish[0] if True in location_finish else None,
                city='all' if location.lower() == location_finish[0].lower()\
                            and True in location_finish and 'bucuresti' != location.lower()\
                                else location,
                remote=job.get('workplace'),
            ).to_dict())

        next_page = post_data.get('nextPage')
        if not next_page:
            break

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "FlowxAI"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
