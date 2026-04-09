#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> eMAG
# Link ------> https://boards-api.greenhouse.io/v1/boards/emag/jobs
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
    Item,
    UpdateAPI,
    counties,
)
from time import sleep
from random import randint
import re


def extract_city(location_name: str) -> str:
    if not location_name:
        return 'all'
    
    if location_name.lower() == 'romania':
        return 'all'
    
    parts = [p.strip() for p in location_name.split(',')]
    if parts:
        return parts[0]
    return location_name


def get_city_county(location_name: str):
    city = extract_city(location_name)
    
    if city == 'all':
        return 'all', None
    
    county_result = get_county(location=city)
    county = county_result[0] if True in county_result else None
    
    return city, county


def scraper():
    '''
    ... scrape data from eMAG scraper using Greenhouse API.
    '''
    job_list = []
    page = 1
    flag = True
    
    while flag:
        url = f'https://boards-api.greenhouse.io/v1/boards/emag/jobs?page={page}'
        json_data = GetRequestJson(url=url)
        
        if not json_data or 'jobs' not in json_data or len(json_data['jobs']) == 0:
            flag = False
            break
            
        for job in json_data['jobs']:
            job_title = job.get('title', '')
            job_link = job.get('absolute_url', '')
            location_name = job.get('location', {}).get('name', '')
            
            way_of_working = 'on-site'
            for meta in job.get('metadata', []):
                if meta.get('name') == 'Way of working':
                    way_val = meta.get('value', '').lower()
                    if 'remote' in way_val:
                        way_of_working = 'remote'
                    elif 'hybrid' in way_val:
                        way_of_working = 'hybrid'
                    elif 'site' in way_val:
                        way_of_working = 'on-site'
                    break
            
            city, county = get_city_county(location_name)
            
            job_list.append(Item(
                job_title=job_title,
                job_link=job_link,
                company='eMAG',
                country='Romania',
                county=county,
                city=city,
                remote=way_of_working,
            ).to_dict())
        
        total = json_data.get('meta', {}).get('total', 0)
        if page * 100 >= total:
            flag = False
        
        page += 1
        sleep(randint(1, 3))
    
    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''
    
    company_name = "eMAG"
    logo_link = "https://s13emagst.akamaized.net/layout/ro/images/logo//59/88362.svg"
    
    jobs = scraper()
    
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
