#
#
# Your custom scraper here ---> Last level!
#
# Company ---> OSFDigital
# Link ------> https://osf.digital/careers/jobs?location=romania
#
#
# Aici va invit sa va creati propriile metode de scraping cu Python,
# ... folosind:
# -> requests
# -> BeautifulSoup
# -> requests_html etc.
#
from __utils import (
    Item,
    GetHtmlSoup,
    get_county,
    UpdateAPI,
)
import requests
# from requests_html import HTMLSession


def prepare_post_request_headers():
    '''
    ... prepare post requests headers for OSFDigital company.
    '''

    cookies = {
            '__RequestVerificationToken': 'grLon0gehq2vJD1akIYBLDAYQjZQPDHb3pbkaey-RMVBQCajp4LQ4gCD8r8TuDD5EmJeRIDUK_WkjSYp48LP7CinLAI1',
        }

    headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://osf.digital',
            'Referer': 'https://osf.digital/careers/jobs?location=romania',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
    }

    params = {
            'location': 'romania',
        }

    data = {
        'scController': 'OsfCommerceJob',
        'scAction': 'GetItems',
        'parameter': 'request',
        '__RequestVerificationToken': 'n5wlTj0ZO_KUdQAbO7xpolMiBny2fH0UOaRkbjGfwUYfe5Qv3WZeNnHuHaPcldg_g_ByjygGvgATyKQw8DVirM7PREA1',
    }

    return cookies, headers, params, data

def scraper():
    '''
    ... scrape data from OSFDigital scraper.
    Your solution!
    '''
    cookies, headers, params, data = prepare_post_request_headers()

    response = GetHtmlSoup(requests.post('https://osf.digital/careers/jobs',\
                                         params=params, cookies=cookies, headers=headers, data=data).text)

    job_list = []
    for job in response.select('div.section-positions.section-border'):
        if (location := [element.text for element in\
                    job.select('p.blue-title-jobs.job-title')][1].lower()) and 'romania' in location:
            location = 'Bucuresti'

        location_finish = get_county(location=location)

        # get jobs items from response
        job_list.append(Item(
            job_title=job.select_one('a.blue-link > h4').text,
            job_link=f"https://osf.digital{job.select_one('a.blue-link')['href']}",
            company='OSFDigital',
            country='Romania',
            county=location_finish[0] if True in location_finish else None,
            city='all' if location.lower() == location_finish[0].lower()\
                        and True in location_finish and 'bucuresti' != location.lower()\
                            else location,
            remote='remote',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "OSFDigital"
    logo_link = "https://osf.digital/library/media/osf/digital/common/header/osf-digital-20-years-logo.svg?h=35&la=en&w=240&hash=E5BC4C8E1EEF3EB1CFE110D0E1910DE415634B2D"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
