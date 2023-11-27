#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> GiGroup
# Link ------> https://ro.gigroup.com/oferta-noastra-de-locuri-de-munca
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
    Item,
    UpdateAPI,
)


def prepare_post_request() -> tuple:
    '''
    ... prepare post request for giGroup.
    '''
    url = 'https://ro.gigroup.com/wp-content/themes/gi-group-child/job-search-infinite-scroll_ALL.php?'

    headers = {
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://ro.gigroup.com',
        'Referer': 'https://ro.gigroup.com/oferta-noastra-de-locuri-de-munca',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    return url, headers


def scraper():
    '''
    ... scrape data from GiGroup scraper.
    '''

    url, headers = prepare_post_request()

    # list with data
    job_list = []

    offset = 0
    flag = True

    while flag:
        json_data = PostRequestJson(url=url, custom_headers=headers, data_raw={
                "X_GUMM_REQUESTED_WITH": "XMLHttpRequest",
                "action": "scrollpagination",
                "numberLimit": 30,
                "offset": offset
            })

        # get data and ad to offset
        data = len(json_data.find_all('article'))
        if data > 0:
            offset += 30
        else:
            flag = False
        # end

        for job in json_data.find_all('article', attrs={'class': 'workRow job-item-s'}):
            location_clear = ''
            location_divs = job.find('div', attrs={'class': 'span8'}).find_all('div', attrs={'class': 'workCol2'})[1].find('h3').text.split(',')[0].strip()
            if '-' in location_divs:
                location_clear = location_divs.split('-')[0].strip()
            else:
                location_clear = location_divs

            # get jobs items from response
            job_list.append(Item(
                job_title=job.find('div', attrs={'class': 'titleBlock'}).find('h2').text,
                job_link=job.find('div', attrs={'class': 'titleBlock'}).find('a').get('href'),
                company='GiGroup',
                country='Romania',
                county=get_county(location_clear),
                city=location_clear,
                remote='on-site',
            ).to_dict())

    return job_list, len(job_list)


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "GiGroup"
    logo_link = "logo_link"

    jobs = scraper()
    print(jobs)

    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
