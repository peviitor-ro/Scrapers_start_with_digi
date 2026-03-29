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
# Company ---> WWF
# Link ------> https://wwf.ro/despre-wwf/wwf-romania/cariere/
#
#
from __utils import Item, GetStaticSoup, UpdateAPI


def scraper():
    '''
    ... scrape data from WWF scraper.
    '''
    soup = GetStaticSoup("https://wwf.ro/despre-wwf/wwf-romania/cariere/")

    job_list = []
    for job in soup.find_all('div', attrs={'class': 'elementor-image-box-content'}):
        link_tag = job.find('a', href=True)
        if link_tag is None:
            continue

        title = link_tag.get_text(strip=True)
        link = link_tag['href']

        if 'wwfeu' in link or title.lower().startswith('raport anual'):
            continue

        if not link.startswith('https://wwf.ro'):
            link = 'https://wwf.ro' + link

        job_list.append(Item(
            job_title=title,
            job_link=link,
            company='WWF',
            country='Romania',
            county='Bucuresti',
            city='Bucuresti',
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "WWF"
    logo_link = "https://cdn.wwf.ro/uploads/2021/04/13154419/wwf-logo-250x281-1.jpg"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
