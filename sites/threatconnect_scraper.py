#
#
#  Config for Dynamic Get Method -> For Json format!
#
# Company ---> ThreatConnect
# Link ------> https://dataminr.wd12.myworkdayjobs.com/Dataminr
#  ... ThreatConnect a fost preluat de Dataminr, iar joburile companiei se publica
#  pe boardul de joburi al Dataminr (cel linkat din pagina de cariere a firmei).
#  Joburile din Romania se iau de pe acelasi board.
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
import html
import re

import requests

from __utils import (
    get_county,
    Item,
    UpdateAPI,
)


session = requests.Session()

WORKDAY_HOST = "https://dataminr.wd12.myworkdayjobs.com"
BOARD_URL = f"{WORKDAY_HOST}/Dataminr"
API_URL = f"{WORKDAY_HOST}/wday/cxs/dataminr/Dataminr/jobs"
JOB_URL = f"{WORKDAY_HOST}/en-US/Dataminr"

# locatiile din Romania de pe board (ex: "Cluj-Napoca, RO", "Romania - Remote")
ROMANIA_MARKERS = ("romania", ", ro")


def get_headers():
    '''
    ... initialize session and build Workday headers.
    '''
    session.get(BOARD_URL, timeout=30, headers={'User-Agent': 'Mozilla/5.0'})
    csrf_token = session.cookies.get('CALYPSO_CSRF_TOKEN', '')

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Origin': WORKDAY_HOST,
        'Referer': BOARD_URL,
        'User-Agent': 'Mozilla/5.0',
    }
    if csrf_token:
        headers['X-CALYPSO-CSRF-TOKEN'] = csrf_token

    return headers


def get_postings(headers, location_ids=None, offset=0):
    '''
    ... returns the postings of the board, optionally filtered by locations.
    '''
    payload = {
        'appliedFacets': {'locations': location_ids} if location_ids else {},
        'limit': 20,
        'offset': offset,
        'searchText': '',
    }

    response = session.post(API_URL, headers=headers, json=payload, timeout=30).json()

    return response.get('jobPostings') or [], response.get('total') or 0


def get_job_info(external_path):
    '''
    ... returns the details of a job posting.
    '''
    response = session.get(
        f"{WORKDAY_HOST}/wday/cxs/dataminr/Dataminr{external_path}",
        headers={'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        timeout=30,
    ).json()

    return response.get('jobPostingInfo') or {}


def get_all_postings(headers):
    '''
    ... returns all postings of the board.
    '''
    postings, total = get_postings(headers)
    offset = len(postings)

    while offset < total:
        more_postings, _ = get_postings(headers, offset=offset)
        if not more_postings:
            break

        postings.extend(more_postings)
        offset += len(more_postings)

    return postings


def get_job_text(job_info):
    '''
    ... returns a plain-text version of the job description.
    '''
    description = job_info.get('jobDescription') or ''
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', description))).strip()


def is_romania_remote_job(job_info):
    '''
    ... returns True if the posting can be performed remotely from Romania.
    '''
    job_text = get_job_text(job_info)
    if 'romania' not in job_text.lower():
        return False

    locations = [job_info.get('location') or ''] + list(job_info.get('additionalLocations') or [])
    if not any('remote' in location.lower() for location in locations):
        return False

    patterns = [
        r'based remotely in[^.]*romania',
        r'remotely in[^.]*romania',
        r'remote in[^.]*romania',
        r'romania[^\S\r\n-]*[-–,]?[^\S\r\n]*remote',
        r'remote[^\S\r\n-]*[-–,]?[^\S\r\n]*romania',
    ]
    return any(re.search(pattern, job_text, re.IGNORECASE) for pattern in patterns)


def get_romanian_locations(job_info):
    '''
    ... returns the Romanian locations of a job posting.
    '''
    locations = [job_info.get('location') or '']
    locations.extend(job_info.get('additionalLocations') or [])

    romanian_locations = [
        location for location in locations
        if any(marker in location.lower() for marker in ROMANIA_MARKERS)
    ]

    if romanian_locations:
        return romanian_locations

    if is_romania_remote_job(job_info):
        return ['Romania - Remote']

    return []


def get_romanian_location(romanian_locations):
    '''
    ... returns the location used for the city of a job posting.
    '''
    # prefer locations with a city (ex: "Cluj-Napoca, RO")
    for location in romanian_locations:
        if ', ro' in location.lower():
            return location

    return romanian_locations[0] if romanian_locations else ''


def get_location_data(location):
    '''
    ... normalize the Romanian location of a job posting.
    '''
    if ', ro' in location.lower():
        city = location.split(',')[0].strip()
    else:
        city = location.split('-')[0].strip() or 'Romania'

    county_data = get_county(location=city)
    county = county_data[0] if True in county_data else ''

    return county, city


def scraper():
    '''
    ... scrape data from ThreatConnect scraper.
    '''
    headers = get_headers()
    postings = get_all_postings(headers)

    job_list = []
    for job in postings:
        external_path = job.get('externalPath') or ''
        job_info = get_job_info(external_path)

        romanian_locations = get_romanian_locations(job_info)
        location = get_romanian_location(romanian_locations)
        if not location:
            continue

        county, city = get_location_data(location)

        is_remote = any('remote' in item.lower() for item in romanian_locations)

        job_list.append(Item(
            job_title=job.get('title'),
            job_link=JOB_URL + external_path,
            company='ThreatConnect',
            country='Romania',
            county=county,
            city=city,
            remote='remote' if is_remote else 'on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "ThreatConnect"
    logo_link = "https://lever-client-logos.s3.us-west-2.amazonaws.com/38d6dcb4-a016-4ba9-8ef1-6d5d80c6688c-1766163095536.png"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
