#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> AUTOTOTAL
# Link ------> https://www.autototal.ro/cariere/
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
    PostRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


'''
    Daca deja te-ai deprins cu aceasta formula de cod,
    atunci poti sterge acest comentariu din fisierul
    __create_scraper.py, din functia - create_static_scraper_config -.

    Deci:
    ########################################################################

    1) --->  clasa PostRequestJson returneaza un obiect Json in urma unui
    post request direct in instanta.

    json_data = PostRequestJson(link, custom_headers, data)
    -> si returneaza datele din acel fisier json dupa un post request,
    direct in instanta.
    Uneori e nevoie de headere mai deosebite pentru post requests,
    ceea ce inseamna ca trebuie o logica mai avansata. Dar nu e nimic greu.

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
    exemplu: list_jobs.append(Item(job_title="titlu_str",
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
    ... scrape data from AUTOTOTAL scraper.
    '''
    post_data = PostRequestJson("https://www.autototal.ro/cariere/", custom_headers=headers, data_raw=data_raw)

    job_list = []
    for job in post_data:
        pass

        # get jobs items from response
        job_list.append(Item(
            job_title='',
            job_link='',
            company='AUTOTOTAL',
            country='',
            county='',
            city='',
            remote='',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "AUTOTOTAL"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
