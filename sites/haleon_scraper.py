#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> Haleon
# Link ------> https://www.haleon.com/careers
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
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


def get_ids_from_api():
    '''
        ... get all ids from external API
    '''
    response_headers = GetHeadersDict('https://gsknch.wd3.myworkdayjobs.com/GSKCareers')
    string_headers_cookie = str(response_headers.get('Set-Cookie', ''))

    def get_cookie(cookie_name):
        '''
            ... return the full "name=value" pair from Set-Cookie header
        '''
        return get_data_with_regex(f'{cookie_name}=([^;,\\s]+)', string_headers_cookie)

    wd_browser_ID = get_cookie('wd-browser-id')
    calypso_csrf = get_cookie('CALYPSO_CSRF_TOKEN')
    play_session = get_cookie('PLAY_SESSION')
    wday_vps_cookie = get_cookie('wday_vps_cookie')
    __cf_bm = get_cookie('__cf_bm')
    __cflb = get_cookie('__cflb')

    # csrf token is also returned as dedicated header by workday
    if not calypso_csrf:
        calypso_csrf = str(response_headers.get('X-CALYPSO-CSRF-TOKEN', ''))

    return wd_browser_ID, calypso_csrf, play_session, wday_vps_cookie, __cf_bm, __cflb


def prepare_post_headers():
    '''
        ... prepare post requests.
    '''

    all_ids = get_ids_from_api()

    cookies = '; '.join(part for part in (
        all_ids[3],
        'timezoneOffset=-120',
        all_ids[0],
        all_ids[1],
        all_ids[2],
        all_ids[4],
        all_ids[5],
    ) if part)

    url = 'https://gsknch.wd3.myworkdayjobs.com/wday/cxs/gsknch/GSKCareers/jobs'
    headers = {
        'authority': 'gsknch.wd3.myworkdayjobs.com',
        'accept': 'application/json',
        'accept-language': 'en-US',
        'content-type': 'application/json',
        'cookie': cookies,
        'origin': 'https://gsknch.wd3.myworkdayjobs.com',
        'referer': 'https://gsknch.wd3.myworkdayjobs.com/GSKCareers?locations=03fe97f04c9a017ec1d4d4e8a757dd50',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'x-calypso-csrf-token': all_ids[1].split('=', 1)[-1],
    }

    payload = {
            'appliedFacets': {
                'locationCountry': [
                    'f2e609fe92974a55a05fc1cdc2852122',
                ],
            },
            'searchText': '',
        }
        
    return url, headers, payload


def scraper():
    '''
    ... scrape data from Haleon scraper.
    '''
    headers_data = prepare_post_headers()
    post_data = PostRequestJson(url=headers_data[0], custom_headers=headers_data[1], data_json=headers_data[2])

    job_list = []
    for job in post_data.get('jobPostings'):

        # get jobs items from response
        job_list.append(Item(
            job_title=job.get('title'),
            job_link=f"https://gsknch.wd3.myworkdayjobs.com/en-US/GSKCareers{job.get('externalPath')}?locations=03fe97f04c9a017ec1d4d4e8a757dd50",
            company='Haleon',
            country='Romania',
            county='Bucuresti',
            city='Bucuresti',
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Haleon"
    logo_link = "https://centaur-wp.s3.eu-central-1.amazonaws.com/marketingweek/prod/content/uploads/2022/02/22163936/haleon-full-size.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
