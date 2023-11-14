#
#
#  You can create new files for scrapers from ->
#  ... your terminal. For example:
#  python3 __create_scraper.py "name_scraper" "link" "type_scraper"
#  Its really useful when you have a lot of scrapers
#
#  You can create your own scraper:
#  ... static
#  ... dynamic_json_get
#  ... dynamic_json_post
#  ... dynamic_render
#  ... custom
#
import sys
import os


#  ---------------------> STATIC SCRAPER <---------------------
def create_static_scraper_config(nume_scraper, link):
    config_content = f"""#
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
# Company ---> {nume_scraper}
# Link ------> {link}
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
    In interiorul clasei GetStaticSoup este definit Session() ->
    deci requesturile se fac in aceeasi sesiune!

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
    ... scrape data from {nume_scraper} scraper.
    '''
    soup = GetStaticSoup("{link}")

    job_list = []
    for job in soup.find_all(...):
        pass

        # get jobs items from response
        job_list.append(Item(
            job_title='',
            job_link='',
            company='{nume_scraper}',
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

    company_name = "{nume_scraper}"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
"""

    with open(f'{nume_scraper.lower()}_scraper.py', 'w') as f:
        f.write(config_content)
    print(f'Static scraper {nume_scraper.lower()}_scraper.py was succesfully created!')


#  ---------------------> DYNAMIC JSON GET <---------------------
def create_dynamic_json_get_scraper_config(nume_scraper, link):
    config_content = f"""#
#
# Config for Dynamic Get Method -> For Json format!
#  ... project made by Andrei Cojocaru
#  LinkedIn: https://www.linkedin.com/in/andrei-cojocaru-985932204/
#  Github: https://github.com/andreireporter13
#
# Company ---> {nume_scraper}
# Link ------> {link}
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
)

'''
    Daca deja te-ai deprins cu aceasta formula de cod,
    atunci poti sterge acest comentariu din fisierul
    __create_scraper.py, din functia -> create_static_scraper_config <-

    Deci:
    ########################################################################

    1) --->  clasa GetRequestJson returneaza un obiect Json in urma unui
    GetRequest, direct in instanta.
    json_data = GetRequestJson(link) -> returneaza direct jsonul.
    Are default headers,

    dar daca vrei sa-i dai headers speciale, poti sa-i setezi cu
    json_data = GetRequestJson(link, custom_headers=headers -> new headers)

    --------------IMPORTANT----------------
    In interiorul clasei GetRequestJson este definit Session() ->
    deci requesturile se fac in aceeasi sesiune!

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
    ... scrape data from {nume_scraper} scraper.
    '''
    json_data = GetRequestJson("{link}")

    job_list = []
    for job in json_data['key']:
        pass

        # get jobs items from response
        job_list.append(Item(
            job_title='',
            job_link='',
            company='{nume_scraper}',
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

    company_name = "{nume_scraper}"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
"""

    with open(f'{nume_scraper.lower()}_scraper.py', 'w') as f:
        f.write(config_content)
    print(f'Scraper type: dynamic_json_get {nume_scraper.lower()}_scraper.py was successfully created!')


#  ---------------------> DYNAMIC JSON POST <---------------------
def create_dynamic_json_post_scraper_config(nume_scraper, link):
    config_content = f"""#
#
# Config for Dynamic Post Method -> For Json format!
#  ... project made by Andrei Cojocaru
#  LinkedIn: https://www.linkedin.com/in/andrei-cojocaru-985932204/
#  Github: https://github.com/andreireporter13
#
# Company ---> {nume_scraper}
# Link ------> {link}
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
    In interiorul clasei PostRequestJson este definit Session() ->
    deci requesturile se fac in aceeasi sesiune!

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
    ... scrape data from {nume_scraper} scraper.
    '''
    json_data = PostRequestJson("{link}", custom_headers=headers, data=data_row)

    job_list = []
    for job in json_data['key']:
        pass

        # get jobs items from response
        job_list.append(Item(
            job_title='',
            job_link='',
            company='{nume_scraper}',
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

    company_name = "{nume_scraper}"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
"""

    with open(f'{nume_scraper.lower()}_scraper.py', 'w') as f:
        f.write(config_content)
    print(f'Scraper type: dynamic_json_post {nume_scraper.lower()}_scraper.py was successfully created!')


#  ---------------------> DYNAMIC RENDER <---------------------
def create_dynamic_render_scraper_config(nume_scraper, link):
    config_content = f"""#
#
# Configurare pentru Scraperul Dynamic Render!
#  ... project made by Andrei Cojocaru
#  LinkedIn: https://www.linkedin.com/in/andrei-cojocaru-985932204/
#  Github: https://github.com/andreireporter13
#
# Company ---> {nume_scraper}
# Link ------> {link}
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
    GetDynamicSoup,
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

    1) --->  clasa GetDynamicSoup returneaza un obiect HTML in urma unui
    request pe un site dinamic, car se incarca cu javascript.

    De obicei unele site-uri nu pot fi scrapuite cu get request sau cu post request.
    Motive sunt diferite. Dar, folosind GetDynamicSoup, putem sa returnam un html
    care sta in spatele unui cod de JS.

    get_dynamic_soup = GetDynamicSoup(link) -> si primim html intr-un obiect BeautifulSoup.

    Putem sa-i dam si headere:
    GetDynamicSoup(link, custom_headers=headers)

    --------------IMPORTANT----------------
    In interiorul clasei GetDynamicSoup este definit Session() ->
    deci requesturile se fac in aceeasi sesiune!

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
    ... scrape data from {nume_scraper} scraper.
    '''
    soup = GetDynamicSoup("{link}")

    job_list = []
    for job in soup.find_all(...):
        pass

        # get jobs items from response
        job_list.append(Item(
            job_title='',
            job_link='',
            company='{nume_scraper}',
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

    company_name = "{nume_scraper}"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
"""

    with open(f'{nume_scraper.lower()}_scraper.py', 'w') as f:
        f.write(config_content)
    print(f'Scraper type: dynamic_render {nume_scraper.lower()}_scraper.py was successfully created!')


#  ---------------------> CUSTOM SCRAPER <---------------------
def create_custom_scraper_config(nume_scraper, link):
    config_content = f"""#
#
# Your custom scraper here ---> Last level!
#
# Company ---> {nume_scraper}
# Link ------> {link}
#
#
# Aici va invit sa va creati propriile metode de scraping cu Python,
# ... folosind:
# -> requests
# -> BeautifulSoup
# -> requests_html etc.
#
from __utils import Item
import requests
from bs4 import BeautifulSoup
# from requests_html import HTMLSession


def scraper():
    '''
    ... scrape data from {nume_scraper} scraper.
    Your solution!
    '''

    job_list = []
    for job in []:

        # get jobs items from response
        job_list.append(Item(
            job_title='',
            job_link='',
            company='{nume_scraper}',
            country='',
            county='',
            city='',
            remote='',
        ).to_dict())


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "{nume_scraper}"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
"""

    with open(f'{nume_scraper.lower()}_scraper.py', 'w') as f:
        f.write(config_content)
    print(f'Custom scraper {nume_scraper.lower()}_scraper.py was successfully created!')


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 create_scraper.py \"nume_scraper\" \"link\" \"static/dynamic_json_get/dynamic_json_post/dynamic_render/custom\"")
    else:
        nume_scraper = sys.argv[1]
        link = sys.argv[2]
        scraper_type = sys.argv[3]

        # Verificați dacă fișierul scraper există deja sau nu
        if os.path.exists(f'{nume_scraper.lower()}_scraper.py'):
            print(f"File {nume_scraper.lower()}_scraper.py already exists!")
        else:
            if scraper_type == 'static':
                create_static_scraper_config(nume_scraper, link)
            elif scraper_type == 'dynamic_json_get':
                create_dynamic_json_get_scraper_config(nume_scraper, link)
            elif scraper_type == 'dynamic_json_post':
                create_dynamic_json_post_scraper_config(nume_scraper, link)
            elif scraper_type == 'dynamic_render':
                create_dynamic_render_scraper_config(nume_scraper, link)
            elif scraper_type == 'custom':
                create_custom_scraper_config(nume_scraper, link)
            else:
                print("Type of scraper needs to be 'static', 'dynamic_json_get', 'dynamic_json_post', 'dynamic_render' or 'custom'.")
