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
# Company ---> ARRK
# Link ------> https://arrkeurope.onlyfy.jobs/candidate/job/ajax_list?display_length=400&page=1&sort=matching&sort_dir=DESC&search=&_ps_widget_token=tMU6eTWJkBAGWF7DxNep3O83rN2owhZyjUrvVqLojQ704xeU3sRAvmKFfnnzc9WKaZKQVgh459vPDJRviAvJnA8sbU4j0j7jb9r9ZI0OBoT99CuysZwQcMyyu3uv5WrQIFzBb3TBxP-UT-zl7YZN-KMzPnzs,mHgPgtQPsr5xVNp2784JeZZ0VswqwmbAkFqDUzbyCAYV2Q0iBOQhpofKQoRsT1yHksD&parentUrl=https://engineering.arrk.com/jobs-career/current-job-offers&widgetConfig=yl6c10ku&_=1687204199282
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
    ... scrape data from ARRK scraper.
    '''
    soup = GetStaticSoup("https://arrkeurope.onlyfy.jobs/candidate/job/ajax_list?display_length=400&page=1&sort=matching&sort_dir=DESC&search=&_ps_widget_token=tMU6eTWJkBAGWF7DxNep3O83rN2owhZyjUrvVqLojQ704xeU3sRAvmKFfnnzc9WKaZKQVgh459vPDJRviAvJnA8sbU4j0j7jb9r9ZI0OBoT99CuysZwQcMyyu3uv5WrQIFzBb3TBxP-UT-zl7YZN-KMzPnzs,mHgPgtQPsr5xVNp2784JeZZ0VswqwmbAkFqDUzbyCAYV2Q0iBOQhpofKQoRsT1yHksD&parentUrl=https://engineering.arrk.com/jobs-career/current-job-offers&widgetConfig=yl6c10ku&_=1687204199282")

    job_list = []
    for job in soup.select('[class*="row-table"][class*="collapsed"]'):
        location = job.find('div', attrs={'class': 'cell-table col-sm-6 col-xs-8'}).text.strip()

        if location in ['Cluj', 'Cluj-Napoca', 'Bucharest', 'Bucuresti']:

            # get jobs items from response
            job_list.append(Item(
                job_title=job.find('a').text.strip(),
                job_link=job.find('a')['href'],
                company='ARRK',
                country='Romania',
                county=get_county(location),
                city=location,
                remote='on-site',
            ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "ARRK"
    logo_link = "https://www.arrk.com/wp/wp-content/themes/SmartPack3.0-Ver/img/logo-blue.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
