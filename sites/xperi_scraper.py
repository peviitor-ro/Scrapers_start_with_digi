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
# Company ---> Xperi
# Link ------> https://jobs.jobvite.com/xperi/jobs
#
#
from __utils import UpdateAPI


def scraper():
    '''
    ... scrape data from Xperi scraper.
    '''
    return []


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "xperi"
    logo_link = "https://mms.businesswire.com/media/20180104005277/en/632823/23/xpe_logo_rgb_201.jpg"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
