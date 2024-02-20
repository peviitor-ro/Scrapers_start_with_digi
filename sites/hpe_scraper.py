#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> HPE
# Link ------> https://careers.hpe.com/us/en/search-results
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

    #
    GetHeadersDict,
    GetStaticSoup,
    #
    get_data_with_regex
)


def get_csrf_token():
    '''
    ... this func return a csrf token from html page
    '''
    return [element for element in 
            get_data_with_regex('"csrfToken":"([a-fA-F0-9]+)"', 
            str(GetStaticSoup('https://careers.hpe.com/us/en/search-results'))).split(':')[-1].split('"')
            if element.strip()][0]


def get_ids_from_site():
    '''
    ... get all ids from site.
    '''
    string_regex_data = str(GetHeadersDict('https://careers.hpe.com/us/en/search-results'))

    play_session = get_data_with_regex('PLAY_SESSION=([a-zA-Z0-9._-]+);', string_regex_data)
    phppe_act = get_data_with_regex('PHPPPE_ACT=([a-fA-F0-9-]+);', string_regex_data)

    return play_session, phppe_act


def prepare_post_headers():
    '''
    ... prepare post headers for new post requests
    '''
    play_session, phppe = get_ids_from_site()

    url = 'https://careers.hpe.com/widgets'

    headers = {
        'authority': 'careers.hpe.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.7',
        'content-type': 'application/json',
        'cookie': f'{play_session} {phppe} VISITED_LANG=en; VISITED_COUNTRY=us',
        'origin': 'https://careers.hpe.com',
        'referer': 'https://careers.hpe.com/us/en/search-results',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'x-csrf-token': f'{get_csrf_token()}',
    }

    payload = '{"lang":"en_us","deviceType":"desktop","country":"us","pageName":"search-results","ddoKey":"refineSearch","sortBy":"","subsearch":"","from":0,"jobs":true,"counts":true,"all_fields":["category","country","state","city","type","postalCode","remote"],"size":100,"clearAll":false,"jdsource":"facets","isSliderEnable":false,"pageId":"page11","siteType":"external","keywords":"","global":true,"selected_fields":{"country":["Romania"]},"locationData":{}}' 

    return url, headers, payload


def scraper():
    '''
    ... scrape data from HPE scraper.
    '''
    url, headers, payload = prepare_post_headers()

    post_data = PostRequestJson(url=url, custom_headers=headers, data_raw=payload)

    job_list = []
    for job in post_data.get('refineSearch').get('data').get('jobs'):

        if (location := job.get('city').lower()) == 'bucharest':
            location = 'Bucuresti'

        # get jobs items from response
        job_list.append(Item(
            job_title=job.get('title'),
            job_link=job.get('applyUrl').replace('apply', ''),
            company='HPE',
            country='Romania',
            county=get_county(location.title()),
            city=location.title(),
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo() 
    '''

    company_name = "HPE"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
