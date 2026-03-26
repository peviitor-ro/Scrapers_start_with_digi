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
# Company ---> Wirtek
# Link ------> https://www.wirtek.com/company/careers
#
#
from __utils import GetStaticSoup, Item, UpdateAPI


def scraper():
    '''
    ... scrape data from Wirtek scraper.
    '''
    soup = GetStaticSoup("https://www.wirtek.com/company/careers")

    job_list = []
    for job in soup.find_all('div', class_='single_article manual'):
        link_tag = job.find('a', href=True)
        title_tag = job.find('h2')
        meta_tag = job.find('h5', class_='body-sm')

        if link_tag is None or title_tag is None or meta_tag is None:
            continue

        meta_text = ' '.join(meta_tag.get_text(' ', strip=True).split())
        if 'romania' not in meta_text.lower():
            continue

        city = 'Romania'
        if 'cluj' in meta_text.lower():
            city = 'Cluj-Napoca'

        remote = 'remote' if 'remote' in meta_text.lower() else 'hybrid' if 'hybrid' in meta_text.lower() else 'on-site'

        job_list.append(Item(
            job_title=title_tag.get_text(strip=True),
            job_link=link_tag['href'],
            company='Wirtek',
            country='Romania',
            county='Cluj' if city == 'Cluj-Napoca' else '',
            city=city,
            remote=remote,
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Wirtek"
    logo_link = "https://www.wirtek.com/hs-fs/hubfs/Wirtek_logo_22_years_v01_132x52px.gif?width=132&height=52&name=Wirtek_logo_22_years_v01_132x52px.gif"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
