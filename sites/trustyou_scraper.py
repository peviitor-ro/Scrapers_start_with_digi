#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> TrustYou
# Link ------> https://www.trustyou.com/careers/
#
#
from __utils import (
    GetRequestJson,
    get_county,
    Item,
    UpdateAPI,
)

import requests


def get_location_data(location_text):
    '''
    ... normalize TrustYou Romania location.
    '''
    if not location_text:
        return '', 'Romania', 'on-site'

    location_text_lower = location_text.lower()
    if 'cluj' in location_text_lower:
        try:
            county_data = get_county(location='Cluj')
            if isinstance(county_data, list) and len(county_data) > 1 and county_data[1]:
                county = county_data[0] if True in county_data else county_data[1]
                return county, 'Cluj', 'on-site'
        except Exception:
            pass
        return 'Cluj', 'Cluj', 'on-site'

    if 'romania' in location_text_lower and 'remote' in location_text_lower:
        return '', 'Romania', 'remote'

    if 'romania' in location_text_lower:
        return '', 'Romania', 'on-site'

    if 'remote' in location_text_lower:
        return '', location_text, 'remote'

    return '', location_text, 'on-site'


def scraper():
    '''
    ... scrape data from TrustYou scraper.
    '''
    job_list = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Origin": "https://www.trustyou.com",
            "Referer": "https://www.trustyou.com/careers/",
            "access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXR0aW5ncyI6eyJzaG93Q2F0ZWdvcnlGaWx0ZXIiOnRydWUsInNob3dMb2NhdGlvbkZpbHRlciI6dHJ1ZSwic2hvd0VtcGxveW1lbnRUeXBlRmlsdGVyIjp0cnVlLCJsYW5ndWFnZSI6ImVuIiwiam9ic1BlclBhZ2UiOjI1fSwiam9icyI6e30sImRlc2lnbiI6eyJzaG93TG9nbyI6dHJ1ZSwic2hvd0xvY2F0aW9uIjp0cnVlLCJzaG93RW1wbG95bWVudFR5cGUiOnRydWUsInNob3dDYXRlZ29yeSI6dHJ1ZSwiY29sb3JzIjp7IndpZGdldCI6eyJiYWNrZ3JvdW5kIjoiI0ZGRkZGRiIsImZpbHRlckJvcmRlciI6IiNENEQ0RDgiLCJwYWdpbmF0aW9uIjoiIzI1NjNFQiJ9LCJqb2JDYXJkIjp7InNoYWRvdyI6IiNENEQ0RDgiLCJiYWNrZ3JvdW5kIjoiI0ZGRkZGRiIsInByaW1hcnlUZXh0IjoiIzNGM0Y0NiIsInNlY29uZGFyeVRleHQiOiIjNTI1MjVCIn19fSwidmVyc2lvbiI6MiwiY29tcGFueVB1YmxpY0lkIjoiM2UyOTczODc5ZDFhMzg5MGI1ZjdhY2UxOTc1YWI5NGUiLCJpYXQiOjE3ODExMDI1NTEsImp0aSI6ImEyYTJlZGQ0LTJhZTgtNDQ3NC1iZGJkLWIzMDUzNmY2NWRlZSJ9.BA3-0A-zYV9-CgfQ19SFoahIsg-F4s752NG0XlVQte4"
        }
        response = requests.get('https://join.com/api/widget/jobs', headers=headers, verify=False)
        jobs_data = response.json()
    except Exception:
        jobs_data = GetRequestJson('https://api.lever.co/v0/postings/trustyou?mode=json&skip=0&limit=50')

    if isinstance(jobs_data, dict):
        jobs_list = jobs_data.get('jobs') or []
    elif isinstance(jobs_data, list):
        jobs_list = jobs_data
    else:
        return []

    for job in jobs_list:
        job_title = job.get('title') or job.get('text') or ''
        job_link = job.get('url') or job.get('hostedUrl') or job.get('applyUrl') or job.get('link') or ''
        if job_link and not job_link.startswith('http'):
            job_link = 'https://join.com' + job_link

        location = job.get('location') or ''
        if isinstance(location, dict):
            city_name = location.get('cityName') or location.get('city') or ''
            country_name = location.get('countryName') or location.get('country') or ''
            location = f"{city_name} {country_name}".strip() or location.get('name', '')

        city = job.get('city') or (location.get('cityName') if isinstance(location, dict) else '')
        if isinstance(city, dict):
            city = city.get('name') or city.get('cityName') or ''

        if not city and isinstance(location, str) and ',' in location:
            parts = location.split(',')
            city = parts[0].strip()

        country = 'Romania'
        if isinstance(location, str):
            if 'romania' not in location.lower() and 'cluj' not in location.lower() and 'japan' not in location.lower() and 'germany' not in location.lower() and 'spain' not in location.lower():
                # Still include if it's not obvious? but better to follow existing logic pattern - original only took Romania/Cluj
                pass
        if isinstance(location, str) and 'japan' in location.lower() and 'romania' not in location.lower():
            continue
        if isinstance(location, str) and 'germany' in location.lower() and 'romania' not in location.lower() and 'cluj' not in location.lower():
            # may still include? check - but safer to be inclusive if Romanian location mentioned
            pass

        location_text = location if isinstance(location, str) else (city or '')
        county, city_res, remote = get_location_data(location_text)
        if not city_res and city:
            city_res = city
        if 'romania' in str(location).lower() or city_res.lower() == 'cluj' or (isinstance(location_text, str) and 'romania' in location_text.lower()):
            country = 'Romania'

        job_list.append(Item(
            job_title=job_title,
            job_link=job_link,
            company='TrustYou',
            country=country,
            county=county,
            city=city_res or '',
            remote=remote,
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "TrustYou"
    logo_link = "https://play-lh.googleusercontent.com/SzbVFK34kqMq1IbRFf5FhlNW0APelGW17Elb0aaBEdlRk_zHgbm7YYp9rEnN9kFBK0k"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
