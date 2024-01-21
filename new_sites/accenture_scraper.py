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
# Company ---> Accenture
# Link ------> https://www.accenture.com/ro-en/jobpostings-sitemap.xml
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

# single, because it used once
from __utils import GetXMLObject


def scraper():
    '''
    ... scrape data from Accenture scraper.
    '''
    soup = GetXMLObject("https://www.accenture.com/ro-en/jobpostings-sitemap.xml")
    
    for url_element in soup.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        loc_element = url_element.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')

        if loc_element is not None and loc_element.text:
            
            # parse data from links
            xml_link = GetStaticSoup(link=loc_element.text)
            print(xml_link.title.text)

    return None


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Accenture"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
