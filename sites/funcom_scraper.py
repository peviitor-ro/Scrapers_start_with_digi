#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> Funcom
# Link ------> https://www.funcom.com/funcom-bucharest/
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
    GetRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,

    #
    GetHeadersDict,

    # for second request
    GetStaticSoup,
)


def get_w_tag_id():
    '''
    ... get w /tag id
    '''
    headers_string = GetHeadersDict('https://api.teamtailor.com/v1/jobs?include=department,locations&page\[size\]=30&filter\[feed\]=public&filter\[locations\]=178583&api_version=20161108&api_key=nCvUhI8oZU8a22OS8tNPoJltCnk0IUTRY90ADtLp').get('Etag')

    return headers_string


def prepare_get_headers():
    '''
    ... prepare get headers for request funcom's API
    '''

    url = 'https://api.teamtailor.com/v1/jobs?include=department,locations&page[size]=30&filter[feed]=public&page[number]=1&filter[locations]=178583&api_version=20161108&api_key=nCvUhI8oZU8a22OS8tNPoJltCnk0IUTRY90ADtLp'

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.7',
        'Connection': 'keep-alive',
        'If-None-Match': f'{get_w_tag_id()}',
        'Origin': 'https://www.funcom.com',
        'Referer': 'https://www.funcom.com/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    return url, headers


# use function for better resposnse
def get_job_type_data(data_string_with_job_type: str):
    '''
    ... get only job type
    '''
    job_type = '' 
    if 'temporarily remote' in data_string_with_job_type:
        return 'hybrid'
    elif 'remote' in data_string_with_job_type and 'hybrid' in data_string_with_job_type:
        return ['remote', 'hybrid']
    elif 'remote' in data_string_with_job_type:
        return 'remote'
    else:
        return 'on-site'



def scraper():
    '''
    ... scrape data from Funcom scraper.
    '''

    url, headers = prepare_get_headers()
    json_data = GetRequestJson(url=url, custom_headers=headers)

    job_list = []
    for job in json_data.get('data'):

        # got to the next page and scrape data with BeautifulSoup
        soup_data = GetStaticSoup(job.get('links').get('careersite-job-url'))

        # get jobs items from response
        job_list.append(Item(
            job_title=soup_data.title.text,
            job_link=job.get('links').get('careersite-job-url'),
            company='Funcom',
            country='Romania',
            county='Bucuresti',
            city='Bucuresti',
            remote=get_job_type_data(
                data_string_with_job_type=str(soup_data.find('section', attrs={'class': 'pb-20 block-px'}).find_all('dd')).lower()),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Funcom"
    logo_link = "https://pr.funcom.com/Content/Themes/Funcom/img/Funcom_R_logo_Horz_med.png"

    jobs = scraper()
    print(jobs, len(jobs))

    # # uncomment if your scraper done
    # UpdateAPI().update_jobs(company_name, jobs)
    # UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
