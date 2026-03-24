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
    PostRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

def prepare_post_headers():
    '''
    ... prepare headers for post request to IQVIA'''

    url = 'https://iqvia.wd1.myworkdayjobs.com/wday/cxs/iqvia/IQVIA/jobs'

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    return url, headers


def scraper():
    '''
    ... scrape data from IQVIA scraper.
    '''
    
    url, headers = prepare_post_headers()
    
    job_list = []
    offset = 0
    limit = 20
    
    while True:
        payload = {
            "appliedFacets": {},
            "limit": limit,
            "offset": offset,
            "searchText": "Romania"
        }
        
        data = PostRequestJson(url=url, custom_headers=headers, data_json=payload)
        
        if not isinstance(data, dict) or 'jobPostings' not in data:
            break
            
        jobs = data['jobPostings']
        if not jobs:
            break
            
        for job in jobs:
            title = job.get('title')
            external_path = job.get('externalPath')
            link = f"https://iqvia.wd1.myworkdayjobs.com/IQVIA{external_path}"
            location_text = job.get('locationsText', '')
            
            # Check if job is in Romania
            if 'Romania' not in location_text:
                continue

            # Default values
            country = 'Romania'
            city = 'Bucuresti'
            county = 'Bucuresti'
            remote = 'on-site'
            
            if 'Remote' in location_text or 'Home Based' in location_text:
                remote = 'remote'
            elif 'Hybrid' in location_text:
                remote = 'hybrid'
                
            # Extract city if possible
            if ',' in location_text:
                parts = location_text.split(',')
                if len(parts) >= 1:
                    city_candidate = parts[0].strip()
                    # Check if city is not Romania or Remote
                    if city_candidate and city_candidate != 'Romania' and 'Remote' not in city_candidate:
                        city = city_candidate
                        # Try to get county
                        county_data = get_county(city)
                        if county_data and county_data[0]:
                             county = county_data[0]
                        else:
                             # If get_county fails, use city as county or keep default?
                             # For Bucuresti it's fine. For others might be None.
                             # If city is valid, use it.
                             pass
            
            job_list.append(Item(
                job_title=title,
                job_link=link,
                company='IQVIA',
                country=country,
                county=county,
                city=city,
                remote=remote,
            ).to_dict())

        if len(jobs) < limit:
            break
            
        offset += limit

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
