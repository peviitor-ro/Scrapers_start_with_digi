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
# Company ---> AppGreat
# Link ------> https://www.appgr8.com/careers/
#
#
from __utils import (
    GetStaticSoup,
    HackCloudFlare,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from AppGreat scraper.
    '''
    soup = HackCloudFlare("https://www.appgr8.com/careers/")

    job_list = []
    for job in soup.find_all('a'):
        href = job.get('href', '')
        if href and '/jobs/' in href and href not in [j.get('job_link') for j in job_list]:
            # normalize url
            if href.startswith('/'):
                job_link = 'https://www.appgr8.com' + href
            elif href.startswith('http'):
                job_link = href
            else:
                job_link = 'https://www.appgr8.com/' + href

            try:
                soup_2 = HackCloudFlare(job_link)
            except Exception:
                try:
                    soup_2 = GetStaticSoup(job_link)
                except Exception:
                    continue

            # look for location info
            location_found = False
            for item in soup_2.find_all(['p', 'li', 'span', 'div']):
                text = item.text
                if 'Bucharest' in text or 'București' in text or 'Bucuresti' in text:
                    location_found = True
                    break

            # get job title
            job_title = None
            h1 = soup_2.find('h1')
            if h1 and h1.text.strip():
                job_title = h1.text.strip()
            else:
                h4 = soup_2.find('h4', attrs={'class': 'elementor-heading-title elementor-size-default'})
                if h4 and h4.text.strip():
                    job_title = h4.text.strip()
                elif job.text.strip() and job.text.strip() not in ['Read More', 'Apply']:
                    job_title = job.text.strip()

            if not job_title:
                continue

            job_list.append(Item(
                job_title=job_title,
                job_link=job_link,
                company='AppGreat',
                country='Romania',
                county='Bucuresti',
                city='Bucuresti',
                remote='remote',
            ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "AppGreat"
    logo_link = "https://clutchco-static.s3.amazonaws.com/s3fs-public/logos/52175d74be34bfe849aef98e4ed36c4a.jpeg?VersionId=n87OrsHNyLbgXOo4MoyU4abLU4uoEUaV"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
