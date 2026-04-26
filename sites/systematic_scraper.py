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
# Company ---> Systematic
# Link ------> https://jobs.systematic.com/search/\?createNewAlert\=false\&q\=\&locationsearch\=\&optionsFacetsDD_country\=RO
#


from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)
from __utils.req_bs4_shorts import session
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def scraper():
    '''
    ... scrape data from Systematic scraper.
    try jobs.systematic.com first, fall back to hipo.ro if unavailable.
    '''
    job_list: list = list()
    location = 'Bucuresti'
    location_finish = get_county(location=location)

    try:
        soup: GetStaticSoup = GetStaticSoup("https://jobs.systematic.com/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_country=RO", verify=False)
        jobs_num: int = int(soup.select_one('span.paginationLabel').text.split()[-1])

        start_row_page: int = 0
        while start_row_page < jobs_num:
            soup_jobs: GetStaticSoup = GetStaticSoup(url=f'https://jobs.systematic.com/search/?q=&sortColumn=referencedate&sortDirection=desc&optionsFacetsDD_country=RO&startrow={str(start_row_page)}', verify=False)

            for job in soup_jobs.select('tr.data-row'):
                if (loc := job.select_one('span.jobLocation').text.strip().split(',')[0]) and loc.lower() == 'bucharest':
                    loc = 'Bucuresti'
                location_finish = get_county(location=loc)

                job_list.append(Item(
                    job_title=job.select_one('a.jobTitle-link').text,
                    job_link=f"https://jobs.systematic.com{job.select_one('a.jobTitle-link').get('href')}",
                    company='Systematic',
                    country='Romania',
                    county=location_finish[0] if True in location_finish else None,
                    city='all' if loc.lower() == location_finish[0].lower()\
                            and True in location_finish and 'bucuresti' != loc.lower()\
                                else loc,
                    remote='on-site',
                ).to_dict())

            start_row_page += 10

    except Exception:
        soup = GetStaticSoup("https://www.hipo.ro/locuri-de-munca/vizualizareFirma/2240/Systematic/", verify=False)
        base_url = "https://www.hipo.ro"
        seen_links = set()

        for job in soup.select('a[href*="/locuri-de-munca/locuri_de_munca/"]'):
            job_title = job.get_text(strip=True)
            job_link = base_url + job.get('href')
            if job_title and job_title != 'Vezi detalii' and '/Systematic/' in job_link and job_link not in seen_links:
                seen_links.add(job_link)
                job_list.append(Item(
                    job_title=job_title,
                    job_link=job_link,
                    company='Systematic',
                    country='Romania',
                    county=location_finish[0] if True in location_finish else None,
                    city='Bucuresti',
                    remote='hybrid',
                ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Systematic"
    logo_link = "https://stemo.bg/uploads/media/stemo_partners/0001/01/033c7005869e36d01af59bf2f777b3c9bf14569c.jpeg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()