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
# Company ---> ARRK
# Link ------> https://arrkeurope.onlyfy.jobs/candidate/job/ajax_list?display_length=400&page=1&sort=matching&sort_dir=DESC&search=&_ps_widget_token=tMU6eTWJkBAGWF7DxNep3O83rN2owhZyjUrvVqLojQ704xeU3sRAvmKFfnnzc9WKaZKQVgh459vPDJRviAvJnA8sbU4j0j7jb9r9ZI0OBoT99CuysZwQcMyyu3uv5WrQIFzBb3TBxP-UT-zl7YZN-KMzPnzs,mHgPgtQPsr5xVNp2784JeZZ0VswqwmbAkFqDUzbyCAYV2Q0iBOQhpofKQoRsT1yHksD&parentUrl=https://engineering.arrk.com/jobs-career/current-job-offers&widgetConfig=yl6c10ku&_=1687204199282
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
    ... scrape data from ARRK scraper.
    '''
    soup = GetStaticSoup("https://arrkeurope.onlyfy.jobs/candidate/job/ajax_list?display_length=400&page=1&sort=matching&sort_dir=DESC&search=&_ps_widget_token=tMU6eTWJkBAGWF7DxNep3O83rN2owhZyjUrvVqLojQ704xeU3sRAvmKFfnnzc9WKaZKQVgh459vPDJRviAvJnA8sbU4j0j7jb9r9ZI0OBoT99CuysZwQcMyyu3uv5WrQIFzBb3TBxP-UT-zl7YZN-KMzPnzs,mHgPgtQPsr5xVNp2784JeZZ0VswqwmbAkFqDUzbyCAYV2Q0iBOQhpofKQoRsT1yHksD&parentUrl=https://engineering.arrk.com/jobs-career/current-job-offers&widgetConfig=yl6c10ku&_=1687204199282")

    job_list = []
    for job in soup.select('[class*="row-table"][class*="collapsed"]'):
        location = job.find('div', attrs={'class': 'cell-table col-sm-6 col-xs-8'}).text.strip()

        if location in ['Cluj', 'Cluj-Napoca', 'Bucharest', 'Bucuresti']:

            # get jobs items from response
            job_list.append(Item(
                job_title=job.find('a').text.strip(),
                job_link=job.find('a')['href'],
                company='ARRK',
                country='Romania',
                county=get_county(location),
                city=location,
                remote='on-site',
            ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "ARRK"
    logo_link = "https://www.arrk.com/wp/wp-content/themes/SmartPack3.0-Ver/img/logo-blue.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
