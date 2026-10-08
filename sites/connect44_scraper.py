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
# Company ---> Connect44
# Link ------> https://www.connect44.com/careers/jobs\?search\=
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
    '''
    ... scrape data from Connect44 scraper.
    '''
    job_list = []
    page = 1

    # jobs are listed with Livewire pagination (?page=N);
    # country=3 (Romania) has no jobs left, so scrape the full list
    while page <= 50:
        soup = GetStaticSoup(f"https://www.connect44.com/careers/jobs?search=&page={page}")

        # walrus - best option
        if len((data_soup := soup.find_all('div', attrs={'class': 'col-md-6'}))) == 0:
            break

        for job in data_soup:
            location_span = job.find('span', attrs={'class': 'me-3 d-flex align-items-center'})
            title_div = job.find('div', attrs={'class': 'mb-4 d-flex align-items-center'})
            link_tag = job.find('a', attrs={'class': 'stretched-link'})

            if location_span is None or title_div is None or link_tag is None:
                continue

            # location format on site -> "Country, City[, Region]"
            location_parts = [' '.join(part.split()) for part in location_span.text.split(',')]
            job_country = location_parts[0] if location_parts else ''
            location = location_parts[1] if len(location_parts) > 1 else job_country

            if location.lower() == "bucharest":
                location = "Bucuresti"

            location_finish = get_county(location=location)

            # get jobs items from response
            job_list.append(Item(
                job_title=title_div.text.strip(),
                job_link=link_tag['href'].strip(),
                company='Connect44',
                country=job_country,
                county=location_finish[0] if True in location_finish else None,
                city='all' if location.lower() == location_finish[0].lower()\
                            and True in location_finish and 'bucuresti' != location.lower()\
                                else location,
                remote='on-site',
            ).to_dict())

        page += 1

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Connect44"
    logo_link = "https://www.totaljobs.com/CompanyLogos/32ec644942c1486e89eb54318d6eed92.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
