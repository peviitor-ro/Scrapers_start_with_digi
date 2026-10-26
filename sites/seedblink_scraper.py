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
# Company ---> SeedBlink
# Link ------> https://seedblink.com/careers
#
#
import re

from __utils import (
    GetStaticSoup,
    GetXMLObject,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

BASE_URL = "https://seedblink.com"
CAREERS_URL = f"{BASE_URL}/careers"
SITEMAP_URL = f"{BASE_URL}/sitemap.xml"

# careers page runs on Webflow now; open positions live in the #open-positions
# section and each job links to /careers/<job-slug>
JOB_LINK_SELECTOR = 'a[href^="/careers/"]'
HEADING_SELECTOR = 'h1, h2, h3, h4, h5, h6'


def normalize_job_href(href):
    '''
    ... normalize a careers link to its job path.
    '''
    href = (href or '').split('#')[0].split('?')[0].strip()

    if href.startswith(BASE_URL):
        href = href[len(BASE_URL):]

    if href.endswith('/'):
        href = href.rstrip('/')

    if not href.startswith('/careers/') or href == '/careers':
        return None

    return href


def get_sitemap_job_links():
    '''
    ... get job paths from the sitemap (some jobs are not linked on /careers).
    '''
    root = GetXMLObject(SITEMAP_URL)
    if root is None:
        return []

    job_links = []
    for node in root.iter():
        if node.tag.rsplit('}', 1)[-1] != 'loc':
            continue

        href = normalize_job_href(node.text)
        if href and href not in job_links:
            job_links.append(href)

    return job_links


def count_job_links(card):
    '''
    ... job links found in card (the card itself counts if it is the link).
    '''
    count = len(card.select(JOB_LINK_SELECTOR))

    if card.name == 'a' and (card.get('href') or '').startswith('/careers/'):
        count += 1

    return count


def get_job_card(link):
    '''
    ... get the wrapper holding this single job link and its title;
    ... None when the card could not be isolated (use the link itself then).
    '''
    card = link

    for _ in range(5):
        if card.select_one(HEADING_SELECTOR) and count_job_links(card) == 1:
            return card

        parent = card.parent
        if parent is None or parent.name in ('body', 'html'):
            return None

        card = parent

    return None


def get_location(card, job_title):
    '''
    ... get the job location from the open position card text;
    ... default to the country when the card has no location details.
    '''
    for tag in card.select('p, span'):
        text = tag.get_text(' ', strip=True)
        if not text or text == job_title or len(text) > 60:
            continue

        location = text.split(',')[0].strip()

        # remote / hybrid are work place types, not locations
        if location.lower() in ('remote', 'hybrid'):
            continue

        if ',' in text or get_county(location=location)[1]:
            return location

    return 'Romania'


def get_remote(card):
    '''
    ... get the work place type from the open position card.
    '''
    words = set(re.findall(r'[a-z]+', card.get_text(' ', strip=True).lower()))

    for place in ('remote', 'hybrid'):
        if place in words:
            return get_job_type(place)

    return get_job_type('')


def scraper():
    '''
    ... scrape data from SeedBlink scraper.
    '''
    soup = GetStaticSoup(CAREERS_URL)

    # when SeedBlink has no openings, this section only shows an empty state
    section = soup.select_one('#open-positions') or soup

    page_links = {}
    for link in section.select(JOB_LINK_SELECTOR):
        href = normalize_job_href(link.get('href'))
        if href and href not in page_links:
            page_links[href] = link

    for href in get_sitemap_job_links():
        page_links.setdefault(href, None)

    job_list = []
    for href, link in page_links.items():
        slug = href.rsplit('/', 1)[-1]
        if not slug:
            continue

        if link is not None:
            card = get_job_card(link) or link
            title_tag = card.select_one(HEADING_SELECTOR)
        else:
            job_soup = GetStaticSoup(f"{BASE_URL}{href}")
            card = job_soup.select_one('.wrapper-careers-left') or job_soup
            title_tag = card.select_one(HEADING_SELECTOR)

        job_title = title_tag.get_text(' ', strip=True) if title_tag \
                        else link.get_text(' ', strip=True) if link else ''
        if not job_title:
            job_title = slug.replace('-', ' ').title()

        location = get_location(card, job_title)

        if location.lower() == 'bucharest':
            location = 'Bucuresti'

        location_finish = get_county(location=location)

        # get jobs items from response
        job_list.append(Item(
            job_title=job_title,
            job_link=f"{BASE_URL}{href}",
            company='SeedBlink',
            country='Romania',
            county=location_finish[0] if True in location_finish else None,
            city='all' if location.lower() == location_finish[0].lower()\
                        and True in location_finish and 'bucuresti' != location.lower()\
                            else location,
            remote=get_remote(card),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "SeedBlink"
    logo_link = "https://seedblink.com/_next/static/images/seedblink-logo-f8978e8317c9a57dca40e52a53247d6e.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
