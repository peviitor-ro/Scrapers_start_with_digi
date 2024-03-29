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
# Company ---> TotalSoft
# Link ------> https://totalsoft.applytojob.com/apply/
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

    2) ---> get_county(nume_localitate) -> returneaza numele judetului;
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
    ... scrape data from TotalSoft scraper.
    '''
    soup = GetStaticSoup("https://totalsoft.applytojob.com/apply/")

    job_list = []
    for job in soup.find_all('li', attrs={'class': 'list-group-item'}):
        nume_link = job.find('h4', attrs={'class': 'list-group-item-heading'})
        city = job.find('ul', attrs={'class': 'list-inline list-group-item-text'}).find('li').text.strip().split(',')[0].strip()
        if city == 'Bucharest' or city == 'București':
            city='Bucuresti'
        if city == "Remote":
            city = ''
            type = 'remote'
        else:
            type = 'on-site'

        location_finish = get_county(city)

        # get jobs items from response
        job_list.append(Item(
            job_title=nume_link.find('a').text.strip(),
            job_link=nume_link.find('a')['href'].strip(),
            company='TotalSoft',
            country='Romania',
            county=location_finish[0] if True in location_finish else None,
            city='all' if city.lower() == location_finish[0].lower()\
                        and True in location_finish and 'bucuresti' != city.lower()\
                            else city,
            remote=type,
        ).to_dict())
    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "TotalSoft"
    logo_link = "https://s3.amazonaws.com/resumator/customer_20210709140908_K4QGZKBVFQVKWUDT/logos/20211008120729_TotalSoft_220_50px.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
