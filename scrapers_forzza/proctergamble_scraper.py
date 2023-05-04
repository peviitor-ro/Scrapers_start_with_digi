#
#
#
# Scrape new site - Procter & Gamble
# Link to this site ---> https://www.pgcareers.com/search-jobs?ascf=[{%27key%27:%27custom_fields.Language%27,%27value%27:%27English%27},]&alp=798549&alt=2
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
#
import requests
from bs4 import BeautifulSoup
#
import uuid
#
import re
from math import ceil
import time


def set_global_headers(page_num: int):
    """
    Set global headers for multiple requests.
    """

    url = f'https://www.pgcareers.com/search-jobs/results?ActiveFacetID=0&CurrentPage={page_num}&RecordsPerPage=20&Distance=50&RadiusUnitType=0&Keywords=&Location=Romania&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=798549&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=37&FacetFilters%5B0%5D.Display=Romania&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&FacetFilters%5B1%5D.ID=English&FacetFilters%5B1%5D.FacetType=5&FacetFilters%5B1%5D.Count=37&FacetFilters%5B1%5D.Display=English&FacetFilters%5B1%5D.IsApplied=true&FacetFilters%5B1%5D.FieldName=custom_fields.Language&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=6&PostalCode=&ResultsType=0&fc=&fl=&fcf=&afc=&afl=&afcf='

    headers = {
        'authority': 'www.pgcareers.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json; charset=utf-8',

        'cookie': 'SearchVisitorId=ab8664a5-80fa-d326-89ea-498d445d6633; SearchSessionId={%22SearchSessionId%22:%22e83e134a-fee5-cdcd-8705-93659bf79646%22%2C%22ImpressionParentId%22:%22%22%2C%22ViewParentId%22:%22%22%2C%22GoogleSearchRequestId%22:%22%22%2C%22GoogleJobId%22:%22%22%2C%22Created%22:%221682624859506%22}; BannerDisplayed=true; SearchSelCountry=798549; SearchSelLanguage=English; ConsentCapture=2023-04-27T19:48:02.930Z; apstr=tPFL1p9fjSRmcQJwOaOgpw%253d%253d; PersonalizationCookie=[{%22Locations%22:[{%22Path%22:%22798549-680962-8334667-680963%22%2C%22FacetType%22:4%2C%22GeolocationLatitude%22:44.1598%2C%22GeolocationLongitude%22:28.6348%2C%22LocationName%22:%22Constan%25C8%259Ba%252C%2520Romania%22%2C%22GeoType%22:%22ipambientonly%22%2C%22SetByHtml5%22:false}]%2C%22Categories%22:[]%2C%22PersonalizationType%22:0%2C%22DateCreated%22:%222023-04-27T19:47:39.987Z%22%2C%22CustomFacets%22:[]%2C%22TenantId%22:936%2C%22OnetCode%22:null%2C%22Served%22:true}%2C{%22Locations%22:[{%22Path%22:%22798549%22%2C%22FacetType%22:1}]%2C%22Categories%22:[%221641%22]%2C%22PersonalizationType%22:1%2C%22DateCreated%22:%222023-04-27T19:59:14.522Z%22%2C%22CustomFacets%22:[{%22CustomFacetValue%22:%22English%22%2C%22CustomFacetTerm%22:%22custom_fields.Language%22}]%2C%22TenantId%22:936}%2C{%22Locations%22:[{%22Path%22:%22798549%22%2C%22FacetType%22:2}]%2C%22Categories%22:[]%2C%22PersonalizationType%22:1%2C%22DateCreated%22:%222023-04-27T20:07:48.932Z%22%2C%22CustomFacets%22:[{%22CustomFacetValue%22:%22English%22%2C%22CustomFacetTerm%22:%22custom_fields.Language%22}]%2C%22TenantId%22:936}]',

        'referer': 'https://www.pgcareers.com/search-jobs?ascf=[{%27key%27:%27custom_fields.Language%27,%27value%27:%27English%27},]&alp=798549&alt=2',
        'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    return url, headers


def get_all_num_jobs():
    """
    This func return all jobs from website.
    """

    response_for_num = requests.get(
            url='https://www.pgcareers.com/search-jobs?ascf=[{%27key%27:%27custom_fields.Language%27,%27value%27:%27English%27},]&alp=798549&alt=2',
            headers = { 
                       'authority': 'www.pgcareers.com',
                       'accept': '*/*',
                       'accept-language': 'en-US,en;q=0.9',
                       'content-type': 'application/json; charset=utf-8',
                       'cookie': 'SearchVisitorId=ab8664a5-80fa-d326-89ea-498d445d6633; SearchSessionId={%22SearchSessionId%22:%22e83e134a-fee5-cdcd-8705-93659bf79646%22%2C%22ImpressionParentId%22:%22%22%2C%22ViewParentId%22:%22%22%2C%22GoogleSearchRequestId%22:%22%22%2C%22GoogleJobId%22:%22%22%2C%22Created%22:%221682624859506%22}; BannerDisplayed=true; SearchSelCountry=798549; SearchSelLanguage=English; ConsentCapture=2023-04-27T19:48:02.930Z; apstr=AZ9fTIYe8CMFh792PJefhA%253d%253d; viewedJobs=icdmEj8J7PEBCFZgs4lFp05I14GzvS1Z3WdpgDdF8UbWBFlc8SFgXHpmM1RB4rpROt2xQBwOqrYHYvIAC4ON6Uz2PQ0GUrdaw0mJqWqALX8%253d; PersonalizationCookie=[{%22Locations%22:[{%22Path%22:%22798549-680962-8334667-680963%22%2C%22FacetType%22:4%2C%22GeolocationLatitude%22:44.1598%2C%22GeolocationLongitude%22:28.6348%2C%22LocationName%22:%22Constan%25C8%259Ba%252C%2520Romania%22%2C%22GeoType%22:%22ipambientonly%22%2C%22SetByHtml5%22:false}]%2C%22Categories%22:[]%2C%22PersonalizationType%22:0%2C%22DateCreated%22:%222023-04-27T19:47:39.987Z%22%2C%22CustomFacets%22:[]%2C%22TenantId%22:936%2C%22OnetCode%22:null%2C%22Served%22:true}%2C{%22Locations%22:[{%22Path%22:%22798549-683504-8335003-683506%22%2C%22FacetType%22:4}]%2C%22Categories%22:[%223605%22]%2C%22PersonalizationType%22:1%2C%22DateCreated%22:%222023-04-28T17:24:07.827Z%22%2C%22CustomFacets%22:[{%22CustomFacetValue%22:%22Experienced%20Professionals%22%2C%22CustomFacetTerm%22:%22job_level%22}]%2C%22TenantId%22:936}%2C{%22Locations%22:[{%22Path%22:%22798549%22%2C%22FacetType%22:2}]%2C%22Categories%22:[]%2C%22PersonalizationType%22:1%2C%22DateCreated%22:%222023-04-28T17:29:31.810Z%22%2C%22CustomFacets%22:[{%22CustomFacetValue%22:%22English%22%2C%22CustomFacetTerm%22:%22custom_fields.Language%22}]%2C%22TenantId%22:936}]',
                       'referer': 'https://www.pgcareers.com/search-jobs?ascf=[{%27key%27:%27custom_fields.Language%27,%27value%27:%27English%27},]&alp=798549&alt=2',
                       'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
                       'sec-ch-ua-mobile': '?0',
                       'sec-ch-ua-platform': '"Linux"',
                       'sec-fetch-dest': 'empty',
                       'sec-fetch-mode': 'cors',
                       'sec-fetch-site': 'same-origin',
                       'sec-gpc': '1',
                       'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
                       'x-requested-with': 'XMLHttpRequest'
                    })

    soup = BeautifulSoup(response_for_num.text, 'lxml')
    jobs_num = soup.find('h1', class_='results__heading').text.split()[0]

    return int(jobs_num)


def get_jobs_dict():
    """
    Return number of jobs on site Procter & Gamble.
    """
    total_num_jobs = get_all_num_jobs()

    job_list = []
    for i in range(1, ceil(total_num_jobs/20) + 1):

        heady = set_global_headers(i)
        response = requests.get(url=heady[0], headers=heady[1])

        str_response = str(response.json())

        title = re.compile(r'<h2\s+class=\"results__item-heading\">([^<]+)<\/h2>')
        link = re.compile(r'<a\s+href=(?:"|\\")(\/job\/[^"\']+)(?:"|\\\')')

        title_jobs = re.findall(title, str_response)
        link_jobs = re.findall(link, str_response)

        for data in range(len(link_jobs)):

            # save data direct to list
            job_list.append({
                "id": str(uuid.uuid4()),
                "job_title": title_jobs[data],
                "job_link":  'https://www.pgcareers.com' + link_jobs[data],
                "company": "proctergamble",
                "country": "Romania",
                "city": "Romania"
            })

        time.sleep(1)

    return job_list


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'proctergamble'
data_list = get_jobs_dict()
scrape_and_update_peviitor(company_name, data_list)
