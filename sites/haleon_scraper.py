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
    string_headers_cookie = str(GetHeadersDict('https://gsknch.wd3.myworkdayjobs.com/GSKCareers'))

    wd_browser_ID = get_data_with_regex('wd-browser-id=([a-fA-F0-9-]+);',  string_headers_cookie)
    calypso_csrf = get_data_with_regex('CALYPSO_CSRF_TOKEN=([a-fA-F0-9-]+);', string_headers_cookie)
    play_session = get_data_with_regex('PLAY_SESSION=([a-fA-F0-9-]+-[a-zA-Z0-9&;=_]+);', string_headers_cookie)
    wday_vps_cookie = get_data_with_regex('wday_vps_cookie=([0-9]+\.[0-9]+\.[0-9]+);', string_headers_cookie)
    __cf_bm = get_data_with_regex('__cf_bm=([^;]+);', string_headers_cookie)
    __cflb = get_data_with_regex('__cflb=([A-Za-z0-9+/=]+);', string_headers_cookie)

    return wd_browser_ID, calypso_csrf, play_session, wday_vps_cookie, __cf_bm, __cflb


def prepare_post_headers():
    '''
        ... prepare post requests.
    '''

    all_ids = get_ids_from_api()

    url = 'https://gsknch.wd3.myworkdayjobs.com/wday/cxs/gsknch/GSKCareers/jobs'
    headers = {
        'authority': 'gsknch.wd3.myworkdayjobs.com',
        'accept': 'application/json',
        'accept-language': 'en-US',
        'content-type': 'application/json',
        'cookie': f'{all_ids[3]} timezoneOffset=-120; {all_ids[0]} {all_ids[1]} {all_ids[2]}; {all_ids[4]} {all_ids[5]}',
        'origin': 'https://gsknch.wd3.myworkdayjobs.com',
        'referer': 'https://gsknch.wd3.myworkdayjobs.com/GSKCareers?locations=03fe97f04c9a017ec1d4d4e8a757dd50',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'x-calypso-csrf-token': '5db977b7-c44a-431e-b2cd-a2c8117b93b7', 
    }

    payload =  '{"appliedFacets":{"locations":["03fe97f04c9a017ec1d4d4e8a757dd50"]},"limit":20,"offset":0,"searchText":""}'
  
    return url, headers, payload


def scraper():
    '''
    ... scrape data from Haleon scraper.
    '''
    headers_data = prepare_post_headers()
    post_data = PostRequestJson(url=headers_data[0], custom_headers=headers_data[1], data_raw=headers_data[2])

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
