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
# Company ---> AECOM
# Link ------> https://aecom.jobs/rom/jobs/
#
mport (
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
    ... scrape data from AECOM scraper.
    '''

    job_list = []
    flag = True
    offset = 0
    while flag:
        soup = GetStaticSoup(f"https://aecom.jobs/rom/jobs/ajax/joblisting/?num_items=15&offset={offset}")
        soup_data = soup.find_all('li', class_='direct_joblisting with_description')

        if len(soup_data) < 1:
            flag = False

        for job in soup_data:
            loc = job.find('div', class_='direct_joblocation').text.strip()

            if 'romania' not in loc.lower():
                break

            # get jobs items from response
            job_list.append(Item(
                job_title=job.find('h4').text.strip(),
                job_link='https://aecom.jobs/' + job.find('a').get('href').strip(),
                company='AECOM',
                country='Romania',
                county=get_county(loc.split('\n')[0]),
                city=loc.split('\n')[0],
                remote=get_job_type('hybrid'),
            ).to_dict())

        # don't forget this details in loops
        offset += 15

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "AECOM"
    logo_link = "https://1000logos.net/wp-content/uploads/2021/12/AECOM-logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
