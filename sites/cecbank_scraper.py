#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> CECBank
# Link ------> https://www.cec.ro/cariere
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
from __utils import (
    GetRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,

    # for this reason
    GetStaticSoup,
    GetHtmlSoup,
)
#
import re
from time import sleep
import html


def get_id_from_site():
    '''
    ... get id from site.
    '''
    return re.search(r'"view_dom_id":"([^"]+)"', str(GetStaticSoup('https://www.cec.ro/cariere'))).group(1)


# one time requests
id_dom = get_id_from_site()


def prepare_headers(page: str):
    '''
    ... prepare headers for post req.
    '''

    url = f"https://www.cec.ro/views/ajax?field_cariere_judet=All&field_cariere_tip=All&search=&viewsreference%5Bdata%5D%5Btitle%5D=0&viewsreference%5Bdata%5D%5Bargument%5D=&viewsreference%5Benabled_settings%5D%5Bargument%5D=argument&viewsreference%5Benabled_settings%5D%5Btitle%5D=title&viewsreference%5Bparent_entity_type%5D=paragraph&viewsreference%5Bparent_entity_id%5D=500&viewsreference%5Bparent_field_name%5D=field_view_ref&page={page}&_wrapper_format=drupal_ajax&field_cariere_judet=All&field_cariere_tip=All&search=&view_name=cariere&view_display_id=block_1&view_args=&view_path=%2Fnode%2F110&view_base_path=&view_dom_id={id_dom}&pager_element=0&viewsreference%5Bdata%5D%5Btitle%5D=0&viewsreference%5Bdata%5D%5Bargument%5D=&viewsreference%5Benabled_settings%5D%5Bargument%5D=argument&viewsreference%5Benabled_settings%5D%5Btitle%5D=title&viewsreference%5Bparent_entity_type%5D=paragraph&viewsreference%5Bparent_entity_id%5D=500&viewsreference%5Bparent_field_name%5D=field_view_ref&_drupal_ajax=1&ajax_page_state%5Btheme%5D=cec&ajax_page_state%5Btheme_token%5D=&ajax_page_state%5Blibraries%5D=blazy%2Fbio.ajax%2Ccec%2Fbootstrap-grid%2Ccec%2Fcecbot%2Ccec%2Fform%2Ccec%2Fglobal%2Ccec%2Fparagraph_header%2Ccec%2Fparagraph_html%2Ccec%2Fparagraph_views%2Ccec%2Fstyleguide%2Ccec%2Ftailwind%2Ccheeseburger_menu%2Fcheeseburger_menu.js%2Cckeditor_responsive_table%2Fresponsive_table%2Cclassy%2Fbase%2Cclassy%2Fmessages%2Ccookiebot%2Fcookiebot%2Ccore%2Fnormalize%2Cgoogle_analytics%2Fgoogle_analytics%2Cparagraphs%2Fdrupal.paragraphs.unpublished%2Csystem%2Fbase%2Cviews%2Fviews.ajax%2Cviews%2Fviews.module"

    headers = {
        'authority': 'www.cec.ro',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.6',
        'referer': f'https://www.cec.ro/cariere?field_cariere_judet=All&field_cariere_tip=All&search=&viewsreference%5Bdata%5D%5Btitle%5D=0&viewsreference%5Bdata%5D%5Bargument%5D=&viewsreference%5Benabled_settings%5D%5Bargument%5D=argument&viewsreference%5Benabled_settings%5D%5Btitle%5D=title&viewsreference%5Bparent_entity_type%5D=paragraph&viewsreference%5Bparent_entity_id%5D=500&viewsreference%5Bparent_field_name%5D=field_view_ref&page={page}',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    return url, headers


def scraper():
    '''
    ... scrape data from CECBank scraper.
    '''

    page = 0
    flag = True
    job_list = []

    # no duplicates links
    no_duplicates_links = []

    while flag:
        data = prepare_headers(str(page))
        json_data = GetRequestJson(url=data[0], custom_headers=data[1])

        soup = GetHtmlSoup(json_data[2]['data']).find_all('div', attrs={'class': 'mb-4 views-row'})
        if len(soup) > 0:
            for job_b in soup:
                link = 'https://www.cec.ro' + job_b.find('a')['href']

                if link not in no_duplicates_links:
                    no_duplicates_links.append(link)

                    # second soup for scraping
                    second_soup = html.unescape(GetStaticSoup(link))
                    location = second_soup.find('div', attrs={'class': 'col-12 col-sm-12 col-md-12 col-lg-3 col-xl-3'}).find('p').text.split()[-1].strip()

                    location_finish = get_county(location=location)

                    # get jobs items from response
                    job_list.append(Item(
                        job_title=second_soup.title.text,
                        job_link=link,
                        company='CECBank',
                        country='Romania',
                        county=location_finish[0] if True in location_finish else None,
                        city='all' if location.lower() == location_finish[0].lower()\
                                    and True in location_finish and 'bucuresti' != location.lower()\
                                        else location,
                        remote='on-site',
                    ).to_dict())

        else:
            flag = False
        
        # increment
        page += 1

        # sleep for better functionality
        sleep(1)

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "CECBank"
    logo_link = "https://www.cec.ro/themes/custom/cec/logo.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
