#
#
#
# Scrape new website - DelgazGrid
# here link ---> https://careers.eon.com/romania/go/Toate-joburile-din-Romania/3727401/?q=&sortColumn=referencedate&sortDirection=desc
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import json
#
from math import ceil
import time


def set_global_headers():
    """
    This func() is about setting global headers for all requests.
    """

    headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json; charset=utf-8',
            'Cookie': 'JSESSIONID=AAF269AA89A8A450240C292FD0D04BA9; CookieConsent={stamp:%27q9oRCI730pMVBXyjzJozvyzLXlN/NiLtwTgKrmwaFNVqcGtyzk9BxA==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1682358188456%2Cregion:%27ro%27}; ak_bmsc=218CD526E93B665ECCACFD0DAEB6F7A4~000000000000000000000000000000~YAAQDpNOUmGu/6CHAQAAFBOOzhOnDaWkkyXVeTJ2zhtVB7/aPi9N+n7oU5TWoEidnu5AgeOHmriJITvPCvdYMTWp2CCYUw/IATsG+D4iZS4IjQa2EbeVd3hvegqbfFg/tVDTvO5hipOF3JMN6KcevXVGJfpiqoklvkqx/dugCaS5O6fkMGIx5z5VIMMkWsq9Y+EWPUC6l5JQc5rjk2bqgIv1ofyDhaQ1aob0HpfnGYhoSy+G5cFkBFmgTSJ2EQTCxHUyB+7gzRElHsZbNnLUYdZgItM0LB0L7mVWDayLxTkMXS6jAtDnIinjuqYDbwf4iz5Vdgp/qf9M0gN0+uaR7nxffjGb+Pjffmd78+FyTII1qsILhSBJwx5MfFV76Hpd9w==; bm_sv=93579EB54DA0B94079041FF50B6B4312~YAAQDpNOUim3/6CHAQAAjMuQzhOoKOHOdxuPcVnLzRRixy64Y+kc2E/4qTJsZy0RjjN+KBkpoLsKoruqyU1rZn0P7Ac/adK/U07zre8teWVTw/A9XFx6bbNkRPtViYDAi5jJX9nVmGIYJISTDD7yENv0eu7KNsvKqQH8wwWEDCWGfLVh0V7kIMB17xe7VaNIt2VyFPcZxeNK5yfZtmrTEmjRThagYRjyVFYe9A7O6KGnycxG/JU+JKTm6+6tOuBvEgUh~1',
            'Referer': 'https://rmk-map-12.jobs2web.com/map/?esid=TSQFfJb%2BCCFBth%2BRcwDxFw%3D%3D&locale=ro_RO&uselcl=false&watercolor=%23ffffff&jobdomain=careers.eon.com&maplbljob=Post&maplbljobs=posturi&mapbtnsearchjobs=C%C4%83utare&centerpoint=46,25&mapzoom=6&keyword=&regionCode=RO&mapbrand=romania&limittobrand=true&parentURL=http%3A%2F%2Fcareers.eon.com%2Fromania%2Fgo%2FToate-joburile-din-Romania%2F3727401%2F25%2F%3Fq%3D%26sortColumn%3Dreferencedate%26sortDirection%3Ddesc',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"'
        }

    return headers


def get_all_jobs_num() -> int:
    """
    ... this func return nums of jobs from current site.
    """

    response = requests.get(
            'https://lde.tbe.taleo.net/lde02/ats/careers/v2/searchResults?next&rowFrom=80&act=null&sortColumn=null&sortOrder=null&currentTime=1682797821746',
            headers=set_global_headers()
        )
    soup = BeautifulSoup(response.text, 'lxml')

    num_jobs = soup.find('span', class_="paginationLabel").text.split()

    return int(num_jobs[-1]), int(num_jobs[-3])


def get_data_from_website() -> list:
    """
    This func() return data from one page in list for extend it in final list.
    """

    func_num_jobs = get_all_jobs_num()
    num_iterations = ceil(func_num_jobs[0] / func_num_jobs[1])

    # create new list for jobs
    jobs_data = []
    count = 0  # it need to increment with 25
    for it in range(1, num_iterations + 1):
        response = requests.get(
                f'https://careers.eon.com/romania/go/Toate-joburile-din-Romania/3727401/{count}/?q=&sortColumn=referencedate&sortDirection=desc',
                headers=set_global_headers())
        soup_data = BeautifulSoup(response.text, 'lxml')

        data = soup_data.find_all('span', class_='jobTitle hidden-phone')

        for zt in data:
            link = zt.find('a')['href']
            title = zt.find('a').get_text()

            jobs_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  'https://careers.eon.com' + link,
                "company": "delgazgrid",
                "country": "Romania",
                "city": "Romania"
                })

        print(f'Page {it} ---> Done!')

        # increment for new page
        count += 25

        # it is time for sleep
        time.sleep(1)

    return jobs_data


def scrape_delgazgrid():
    """
    This function is last func() for this sections of script.
    ... all logic stored here.
    """

    lst_with_data = get_data_from_website()

    # store data in json file
    with open('scrapers_forzza/data_delgazgrid.json', 'w') as new_file:
        json.dump(lst_with_data, new_file)

    print('DelgazGrid ---> Done!')
