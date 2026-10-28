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
# Company ---> Farmexim
# Link ------> https://careers.phoenixgroup.eu/Farmexim/
#
#
from __utils import (
    get_county,
    Item,
    UpdateAPI,
)
from __utils.req_bs4_shorts import session


JOBS_API_URL = "https://careers.phoenixgroup.eu/services/recruiting/v1/jobs"


def get_jobs_from_api():
    '''
    ... return all job postings from the Phoenix Group careers API.
    '''
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://careers.phoenixgroup.eu/Farmexim/search/?locale=ro_RO",
    }

    jobs = []
    page = 0
    while True:
        payload = {
            "keywords": "",
            "locale": "ro_RO",
            "location": "",
            "pageNumber": page,
            "sortBy": "recent",
        }
        response = session.post(
            JOBS_API_URL,
            headers=headers,
            json=payload,
            verify=False,
            timeout=30,
        )
        try:
            page_jobs = response.json().get("jobSearchResult", [])
        except ValueError:
            print(
                "Farmexim jobs API did not return JSON "
                f"(HTTP {response.status_code}); returning no jobs."
            )
            break

        if not page_jobs:
            break

        jobs.extend(page_jobs)
        page += 1

    return jobs


def scraper():
    '''
    ... scrape data from Farmexim scraper.
    '''
    job_list = []
    for job in get_jobs_from_api():
        job_data = job.get("response", {})

        if "Farmexim" not in job_data.get("sfstd_marketingBrand_obj", []):
            continue

        location_finish = get_county(
            location=(job_data.get("jobLocationState") or [None])[0]
        )
        cities = [
            location.removeprefix("Romania-").strip()
            for location in job_data.get("jobLocationShort", [])
        ]

        # get jobs items from response
        job_list.append(Item(
            job_title=job_data.get("unifiedStandardTitle"),
            job_link=(f"https://careers.phoenixgroup.eu/Farmexim/job/"
                      f"{job_data.get('unifiedUrlTitle')}/{job_data.get('id')}-ro_RO"),
            company='Farmexim',
            country='Romania',
            county=location_finish[0] if True in location_finish else None,
            city=cities[0] if len(cities) == 1 else cities,
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Farmexim"
    logo_link = "https://farmexim.ro/templates/default/assets/img/Logo-farmexm-135x77.png"

    jobs = scraper()

    # uncomment if your scraper done
    try:
        UpdateAPI().update_jobs(company_name, jobs)
        UpdateAPI().update_logo(company_name, logo_link)
    except Exception as e:
        print(f"UpdateAPI Error: {e}")


if __name__ == '__main__':
    main()
