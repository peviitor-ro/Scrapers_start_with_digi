#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> Morningstar
# Link ------> https://careers.morningstar.com/widgets
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
)

import json

def get_headers():
    url = "https://careers.morningstar.com/widgets"

    payload = json.dumps({
    "lang": "en_us",
    "deviceType": "desktop",
    "country": "us",
    "pageName": "search-results",
    "ddoKey": "refineSearch",
    "sortBy": "",
    "subsearch": "",
    "from": 0,
    "jobs": True,
    "counts": True,
    "all_fields": [
        "category",
        "country",
        "state",
        "city",
        "type",
        "visibilityType",
        "brand"
    ],
    "size": 100,
    "clearAll": False,
    "jdsource": "facets",
    "isSliderEnable": False,
    "pageId": "page14",
    "siteType": "external",
    "keywords": "Romania",
    "global": True,
    "selected_fields": {
        "country": [
        "Romania"
        ]
    }
    })
    headers = {
    'accept': '*/*',
    'content-type': 'application/json',
    'referer': 'https://careers.morningstar.com/us/en/search-results?keywords=Romania',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'Cookie': 'PHPPPE_ACT=82c6ec1c-ee53-4020-b536-a9fb682647b3; PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7IkpTRVNTSU9OSUQiOiI4MmM2ZWMxYy1lZTUzLTQwMjAtYjUzNi1hOWZiNjgyNjQ3YjMifSwibmJmIjoxNzQzMjczODYwLCJpYXQiOjE3NDMyNzM4NjB9.QrI4DK3nAM9ZWNtZLl-BdL_dayI3KLS430Ky_x2Rh-0'
    }
    

    return url, payload, headers

def scraper():

    url, payload, headers = get_headers()
    post_data = PostRequestJson(url , custom_headers=headers, data_raw=payload)
    jobs = post_data.get("refineSearch").get("data").get("jobs")


    job_list = []

        
    for job in jobs:
        location= "Bucuresti" if job.get('cityState')=="Bucharest" else job.get('cityState')


        # get jobs items from response
        job_list.append(Item(
            job_title=job.get('title'),
            job_link= 'https://careers.morningstar.com/us/en/job/'+ job['jobId']+'/'+ '-'.join(job['title'].split()),
            company='Morningstar',
            country='Romania',
            county= location,
            city="all" if not job["city"] else job["city"],
            remote=job.get('type', '').lower() if job.get('type','') else None,
        ).to_dict())

    # for i in job_list:
    #     print (i)
    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Morningstar"
    logo_link = "https://upload.wikimedia.org/wikipedia/commons/6/67/Morningstar_Logo.svg"

    jobs = scraper()
    # print(len(jobs), jobs)

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
