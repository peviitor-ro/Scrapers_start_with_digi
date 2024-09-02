#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> Spyrosoft
# Link ------> https://spyro-soft.com/career?area=all&skills=all&location=romania&experience=all
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
    counties,
)
#
import re


def get_static_headers():
    '''
    >>>>>>>> Make Post Request for Ajax ---> retrun HTML

    params: None
    return: url: str, headers: dict, payload:
    '''

    url = 'https://spyro-soft.com/wp-admin/admin-ajax.php'

    headers = {
        'authority': 'spyro-soft.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://spyro-soft.com',
        'referer': 'https://spyro-soft.com/career?area=all&skills=all&location=romania&experience=all',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'action': 'career_listing',
        'location[]': 'romania',
        'search': '',
        'group': '',
        'paged': '1',
    }

    return url, headers, data


def scraper():
    '''
    ... scrape data from Spyrosoft scraper.
    '''

    url, headers, data_raw = get_static_headers()

    post_data = PostRequestJson(url=url,
                                custom_headers=headers,
                                data_raw=data_raw)

    job_list = []
    for job in post_data.select('div.col-sm-6.col-lg-4.CareerThumbnail-col'):

        # get location ----> and filter for location
        location = job.select_one('p.CareerThumbnail__city').text.strip().lower()

        # get location with regex
        new_loc = None
        for search_city in counties:
            for v in search_city.values():
                for ccity in v:
                    if re.search(r'\b{}\b'.format(re.escape(ccity.split()[-1].lower())), location.lower()):
                        new_loc = ccity
                        break

        # get correct location
        if new_loc != None:
            location_finish = get_county(location=new_loc)
        else:
            location_finish = 'all'

        # get jobs items from response
        job_list.append(Item(
            job_title=job.select_one('p.CareerThumbnail__title').text.strip(),
            job_link=job.select_one('a.CareerThumbnail').get('href'),
            company='Spyrosoft',
            country='Romania',
            county='all' if location_finish == 'all' else (location_finish[0] if True in location_finish else None),
            city='all' if location_finish == 'all' else (location_finish[0] if location_finish != 'all'\
                                                         and True not in location_finish else new_loc),
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Spyrosoft"
    logo_link = "https://spyro-soft.com/wp-content/uploads/2022/06/spyrosoft_color_rgb.png"

    jobs = scraper()
    # # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
