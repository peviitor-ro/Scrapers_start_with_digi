#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> IQVIA
# Link ------> https://jobs.iqvia.com/search-jobs
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
    GetHtmlSoup,
)


def prepare_get_headers(page_req: str):
    '''
    ... prepare headers for get request to IQVIA'''

    url = f'https://jobs.iqvia.com/search-jobs/results?ActiveFacetID=798549&CurrentPage={page_req}&RecordsPerPage=12&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=798549&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=35&FacetFilters%5B0%5D.Display=Romania&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=1&SearchType=5&PostalCode=&ResultsType=0&fc=&fl=&fcf=&afc=&afl=&afcf='

    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/json; charset=utf-8',
        'Referer': 'https://jobs.iqvia.com/search-jobs',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    return url, headers


def scraper():
    '''
    ... scrape data from IQVIA scraper.
    '''
    json_data = GetRequestJson("https://jobs.iqvia.com/search-jobs")

    job_list = []
    page = 1
    flag = True
    while flag:

        url, headers = prepare_get_headers(page_req=str(page))
        json_data = GetRequestJson(url=url, custom_headers=headers)

        if len(soup_data := GetHtmlSoup(json_data.get('results')).select('a.job-result-list')) > 0:
            for job in soup_data:

                # get jobs items from response
                job_list.append(Item(
                    job_title=job.select_one('h2.job-result-list-heading').text.strip(),
                    job_link=f"https://jobs.iqvia.com{job['href']}",
                    company='IQVIA',
                    country='Romania',
                    county='Bucuresti',
                    city='Bucuresti',
                    remote='on-site',
                ).to_dict())
        else:
            flag = False

        page += 1

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "IQVIA"
    logo_link = "https://tukuz.com/wp-content/uploads/2019/08/iqvia-logo-vector.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
