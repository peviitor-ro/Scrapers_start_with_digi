#
#
#  Basic for scraping data from static pages
#  ... project made by Andrei Cojocaru
#  LinkedIn: https://www.linkedin.com/in/andrei-cojocaru-985932204/
#  Github: https://github.com/andreireporter13
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
# Company ---> pmi
# Link ------> https://www.pmi.com/careers/explore-our-job-opportunities?title=&locations=Romania&departments=&contracts=&page=1
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


'''
    Daca te-ai deprins cu aceasta formula de cod,
    atunci poti sterge acest comentariu din fisierul
    __create_scraper.py, din functia -> create_static_scraper_config <-

    Deci:
    ########################################################################
    1) --->  clasa GetStaticSoup returneaza un obiect BeautifulSoup,
    direct in instanta, fara a apela alte metode.

    soup = GetStaticSoup(link) -> si gata, ai acces la obiectul soup
    si deja poti face -> for job in soup.find_all(...)

    + poti sa-i adaugi si custom_headers
    soup = GetStaticSoup(link, custom_headers)
    ... by default, custom_headers = None, dar in __utils ai un fisier
    default_headers.py unde poti sa-ti setezi headerele tale default.

    --------------IMPORTANT----------------
    La nivel de proiect, ca o variabila globala, este definit Session()!
    ... acest session inseamna ca orice clasa va putea folosi
    ... aceeasi sesiune, practic se va evita multiple requests;

    ########################################################################

    2) ---> get_county(nume_localitat) -> returneaza numele judetului;
    poti pune chiar si judetul, de exemplu, nu va fi o eroare.

    ########################################################################

    3) --->get_job_type(job_type: str) -> returneaza job_type-ul: remote,
    hybrid, on-site

    ########################################################################

    4) ---> Item -> este un struct pentru datele pe care le vom stoca in lista
    si, apoi, le vom trimite catre API.
    exemplu: job_list.append(Item(job_title="titlu_str",
                                    job_link="link",
                                    company="nume_companie",
                                    country="Romania",
                                    county="Judetul",
                                    city="Orasul",
                                    remote="remote, onsite sau hibryd"))

    ########################################################################

    5) ---> clasa UpdateAPI are doua metode:
    update_jobs(lista_dict_joburi) si update_logo(nume_companie, link_logo)

    UpdateAPI().update_jobs(company_name: str, data_jobs: list)
    UpdateAPI().update_logo(id_company: str, logo_link: str)

    ########################################################################
'''


def scraper():
    '''
    ... scrape data from pmi scraper.
    '''

    # job list for all jobs
    job_list = []
    page = 1
    while True:
        soup = GetStaticSoup(f"https://www.pmi.com/careers/explore-our-job-opportunities?title=&locations=Romania&departments=&contracts=&page={page}")
        soup_data = soup.find_all('a', attrs={'class': 'job-row'})

        link_verification = 'https://www.pmi.com' + soup.find_all('a', attrs={'class': 'job-row'})[0]['href'].strip()

        # verification for link exists in job_list json
        if job_list:
            if link_verification in [job["job_link"] for job in job_list]:
                break

        for idx, job in enumerate(soup_data):
            link_str = f"https://www.pmi.com{job['href'].strip()}"

            req_page = GetStaticSoup(link_str)

            #  search location
            location = req_page.find('p', attrs={'class': 'details--note details--positionIcon location'}).text

            # get jobs items from response
            job_list.append(Item(
                job_title=job.find('h3', attrs={'class': 'job-row--title title8'}).text.strip(),
                job_link=link_str,
                company='pmi',
                country='Romania',
                county=get_county(location.split(',')[0]),
                city=location.split(',')[0],
                remote=get_job_type('remote'),
            ).to_dict())

        page += 1

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "pmi"
    logo_link = "https://www.pmi.com/resources/images/default-source/default-album/pmi-logoaaf115bd6c7468f696e2ff0400458fff.svg?sfvrsn=37857db4_2"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
