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
# Company ---> Fabric
# Link ------> https://blog-qa.fabricdata.com/corporate/careers
#
#
from urllib.parse import urljoin

from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from Fabric scraper.
    '''
    careers_url = "https://blog-qa.fabricdata.com/corporate/careers"
    soup = GetStaticSoup(careers_url)

    job_list = []

    # while no position is open, the careers page replaces
    # the job cards with a "not hiring" message
    no_jobs_text = [
        h3.get_text(' ', strip=True).lower()
        for h3 in soup.find_all('h3')
    ]
    if any('not hiring' in text for text in no_jobs_text):
        return job_list

    for card in soup.find_all('div', attrs={'class': 'card__content'}):

        # job title from the card header
        title_tag = card.find('h3')
        if title_tag is None:
            continue
        job_title = title_tag.get_text(strip=True)

        # location from the card description (e.g. "Bucharest, Romania");
        # keep only the jobs from Romania
        description = card.find('div', attrs={'class': 'card__description'})
        location_text = description.get_text(' ', strip=True) if description else ''
        if 'romania' not in location_text.lower():
            continue
        city = location_text.split(',')[0].strip()
        if city.lower() == 'bucharest':
            city = 'Bucuresti'

        # job page link: anchor inside the card or the slug
        # taken from the card image (careers page style)
        link_tag = card.find('a', href=True)
        if link_tag is not None:
            job_link = urljoin(careers_url, link_tag['href'].strip())
        else:
            image = card.find('img')
            image_name = image.get('src', '').rstrip('/').split('/')[-1].split('.')[0] if image else ''
            job_link = f'{careers_url}/{image_name}' if image_name else careers_url

        # get county by city
        location_finish = get_county(city)

        # get jobs items from response
        job_list.append(Item(
            job_title=job_title,
            job_link=job_link,
            company='Fabric',
            country='Romania',
            county=location_finish[0] if True in location_finish else None,
            city=city if city else 'all',
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Fabric"
    logo_link = "https://mma.prnewswire.com/media/1701193/Fabric2_Logo.jpg?p=twitter"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
