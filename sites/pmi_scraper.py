#
#
#  Basic for scraping data from static pages
#  ... project made by Andrei Cojocaru
#  LinkedIn: https://www.linkedin.com/in/andrei-cojocaru-985932204/
#  Github: https://github.com/andreireporter13
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
# Company ---> pmi
# Link ------> https://join.pmicareers.com/gb/en/search-results?location=Romania
#
#
import re
#
from __utils import (
    PostRequestJson,
    get_county,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from pmi scraper.
    '''

    # job list for all jobs
    job_list = []
    seen_links = set()

    api_url = "https://join.pmicareers.com/widgets"
    custom_headers = {
        "Content-Type": "application/json",
        "Referer": "https://join.pmicareers.com/gb/en/search-results",
    }

    page_size = 100
    offset = 0
    flag = True
    while flag:
        payload = {
            "lang": "en_gb",
            "deviceType": "desktop",
            "country": "gb",
            "pageName": "search-results",
            "ddoKey": "refineSearch",
            "sortBy": "",
            "subsearch": "",
            "from": offset,
            "jobs": True,
            "counts": True,
            "all_fields": ["category", "country", "state", "city", "type"],
            "size": page_size,
            "clicks": 0,
            "isSliderEnable": False,
            "pageId": "page15",
            "siteType": "external",
            "keywords": "",
            "global": True,
            "selected_fields": {"country": ["Romania"]},
            "sort": {},
            "locationData": {},
            "refNum": "PMIPMIGB",
            "search": "",
        }

        response = PostRequestJson(
            api_url,
            custom_headers=custom_headers,
            data_json=payload,
        )

        if not isinstance(response, dict):
            flag = False
            break

        soup_data = response.get("refineSearch", {}).get("data", {}).get("jobs") or []

        # stop when the API has no more jobs for the requested page
        if not soup_data:
            flag = False
            break

        for job in soup_data:
            job_id = job.get("jobId")
            job_title = (job.get("title") or "").strip()

            # build the canonical job link from the job id + title slug
            title_slug = re.sub(r'[^A-Za-z0-9]+', '-', job_title).strip('-')
            link_str = f"https://join.pmicareers.com/gb/en/job/{job_id}/{title_slug}"

            # avoid duplicates between pages
            if link_str in seen_links:
                continue
            seen_links.add(link_str)

            # search location
            raw_location = (job.get("city") or job.get("location") or "").split(',')[0].strip()
            if len(raw_location.split()) > 1:
                new_loc = '-'.join(raw_location.split())
            else:
                new_loc = raw_location

            if new_loc.lower() == 'bucharest':
                new_loc = 'Bucuresti'

            location_finish = get_county(location=new_loc)

            # get jobs items from response
            job_list.append(Item(
                job_title=job_title,
                job_link=link_str,
                company='pmi',
                country='Romania',
                county=location_finish[0] if True in location_finish else None,
                city='all' if new_loc.lower() == location_finish[0].lower()\
                        and True in location_finish and 'bucuresti' != new_loc.lower()\
                            else new_loc,
                remote='on-site',
            ).to_dict())

        offset += page_size
        if len(soup_data) < page_size:
            flag = False

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "pmi"
    logo_link = "https://www.pmi.com/resources/images/default-source/default-album/pmi-logoaaf115bd6c7468f696e2ff0400458fff.svg?sfvrsn=37857db4_2"

    jobs = scraper()
    print(jobs)

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
