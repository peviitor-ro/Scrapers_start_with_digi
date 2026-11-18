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
# Company ---> RedBeeSoftware
# Link ------> https://redbeesoftware.com/career
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from RedBeeSoftware scraper.
    """
    base_url = "https://redbeesoftware.com"
    career_url = f"{base_url}/career"
    soup = GetStaticSoup(career_url)

    job_list = []
    seen = set()

    for anchor in soup.select('a[href*="/career/"]'):
        href = (anchor.get("href") or "").strip()
        if not href or href in {"/career", "/career/"}:
            continue
        if href.startswith(base_url):
            href = href[len(base_url):]
        if not href.startswith("/career/"):
            continue
        if href.rstrip("/").endswith("/career"):
            continue
        if href.startswith("/_next") or href.endswith(".js") or href.endswith(".css"):
            continue

        job_link = href if href.startswith("http") else f"{base_url}{href}"
        if job_link in seen:
            continue
        seen.add(job_link)

        title_tag = anchor.select_one("h3") or anchor.select_one("h2") or anchor
        job_title = title_tag.get_text(" ", strip=True)
        if not job_title:
            continue

        soup_job = GetStaticSoup(job_link)
        job_text = soup_job.get_text(" ", strip=True).lower() if soup_job else ""
        remote = "remote" if "regim de lucru: remote" in job_text else "on-site"

        job_list.append(
            Item(
                job_title=job_title,
                job_link=job_link,
                company="RedBeeSoftware",
                country="Romania",
                county="Cluj",
                city="Cluj-Napoca",
                remote=remote,
            ).to_dict()
        )

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "RedBeeSoftware"
    logo_link = "https://redbeesoftware.com/wp-content/uploads/2022/07/Redbee-vertical-red@2x-1.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
