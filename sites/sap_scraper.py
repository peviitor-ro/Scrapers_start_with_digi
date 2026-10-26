#
#
#  Basic for scraping data from static pages
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
# Company ---> SAP
# Link ------> https://jobs.sap.com/search/?q=&locationsearch=Romania&startrow=0&scrollToTable=True
#
#
import re

import requests

from __utils import (
    GetStaticSoup,
    GetRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def _make_job(title, link, location, remote='on-site'):
    location = location.strip()
    if location == 'Bucharest':
        location = 'Bucuresti'

    location_finish = get_county(location=location)

    return Item(
        job_title=title,
        job_link=link,
        company='SAP',
        country='Romania',
        county=location_finish[0] if True in location_finish else None,
        city='all' if location.lower() == location_finish[0].lower()
                and True in location_finish and 'bucuresti' != location.lower()
                    else location,
        remote=remote,
    ).to_dict()


def _scrape_previous_site():
    '''
    ... scrape jobs still posted on SAP's previous careers site.
    '''
    job_list = []
    startrow = 0
    base_url = 'https://careers.sap.com'

    while True:
        try:
            soup = GetStaticSoup(f"{base_url}/search/?q=&locationsearch=Romania&startrow={startrow}&scrollToTable=True")
        except requests.exceptions.ConnectionError:
            break

        rows = soup.select('tr.data-row')
        if not rows:
            break

        for job in rows:
            title_link = job.select_one('a.jobTitle-link')
            if not title_link:
                continue

            location_elem = job.select_one('span.jobLocation')
            if not location_elem:
                continue

            location = location_elem.text.strip().split(',')[0]

            job_list.append(_make_job(
                title_link.text.strip(),
                f"{base_url}{title_link['href']}",
                location,
            ))

        startrow += 25

    return job_list


def _new_site_job_links():
    '''
    ... map new-site job ids to their canonical jobs.sap.com links.
    '''
    links = {}

    try:
        soup = GetStaticSoup('https://jobs.sap.com/en/jobs/sitemap.xml')
    except requests.exceptions.RequestException:
        return links

    for loc in soup.find_all('loc'):
        link = loc.text.strip()
        match = re.search(r'/en/jobs/(\d+)/', link)
        if match:
            links[match.group(1)] = link

    return links


def _scrape_new_site():
    '''
    ... scrape jobs published on SAP's new careers site (SmartRecruiters).
    '''
    job_list = []
    offset = 0
    limit = 100
    company_id = 'SAPITBusinessSysteme'
    links = _new_site_job_links()

    while True:
        data = GetRequestJson(
            f"https://api.smartrecruiters.com/v1/companies/{company_id}/postings"
            f"?country=ro&limit={limit}&offset={offset}"
        )
        if not isinstance(data, dict):
            break

        content = data.get('content') or []
        if not content:
            break

        for job in content:
            location_data = job.get('location') or {}
            if location_data.get('country') != 'ro':
                continue

            title = (job.get('name') or '').strip()
            job_link = links.get(str(job.get('id'))) or job.get('postingUrl')
            if not title or not job_link:
                continue

            if location_data.get('remote'):
                remote = 'remote'
            elif location_data.get('hybrid'):
                remote = 'hybrid'
            else:
                remote = 'on-site'

            job_list.append(_make_job(
                title,
                job_link,
                location_data.get('city', ''),
                remote=remote,
            ))

        offset += len(content)
        if offset >= int(data.get('totalFound', 0)) or len(content) < limit:
            break

    return job_list


def scraper():
    '''
    ... scrape data from SAP scraper.
    '''
    return _scrape_previous_site() + _scrape_new_site()


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "SAP"
    logo_link = "https://logowik.com/content/uploads/images/467_sap.jpg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
