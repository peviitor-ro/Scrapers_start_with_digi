#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> Morningstar
# Link ------> https://morningstar.wd5.myworkdayjobs.com/en-US/Morningstar
#
from __utils import (
    PostRequestJson,
    get_county,
    Item,
    UpdateAPI,
)

import re


def get_headers():
    url = "https://morningstar.wd5.myworkdayjobs.com/wday/cxs/morningstar/Morningstar/jobs"

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    }

    return url, headers


def scraper():
    url, headers = get_headers()

    job_list = []

    payload = {
        "appliedFacets": {"locationCountry": ["f2e609fe92974a55a05fc1cdc2852122"]},
        "limit": 20,
        "offset": 0,
        "searchText": "",
    }

    data = PostRequestJson(url=url, custom_headers=headers, data_json=payload)

    if not isinstance(data, dict) or "jobPostings" not in data:
        return job_list

    jobs = data["jobPostings"]

    for job in jobs:
        title = job.get("title")
        external_path = job.get("externalPath")
        if not title or not external_path:
            continue

        link = f"https://morningstar.wd5.myworkdayjobs.com/en-US/Morningstar{external_path}"

        city = "Bucuresti"
        county = "Bucuresti"
        remote = "on-site"

        city_match = re.search(r"/job/([^/]+)/", external_path)
        if city_match:
            city_name = city_match.group(1).replace("-", " ")
            if city_name.lower() == "bucharest":
                city_name = "Bucuresti"
            city = city_name
            county_data = get_county(city)
            if county_data and county_data[0]:
                county = county_data[0]

        job_list.append(Item(
            job_title=title,
            job_link=link,
            company="Morningstar",
            country="Romania",
            county=county,
            city=city,
            remote=remote,
        ).to_dict())

    return job_list


def main():
    company_name = "Morningstar"
    logo_link = "https://upload.wikimedia.org/wikipedia/commons/6/67/Morningstar_Logo.svg"

    jobs = scraper()
    print(jobs)
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == "__main__":
    main()
