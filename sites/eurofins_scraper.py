#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> Eurofins
# Link ------> https://atsintegration.eurofins.com/ATSWebService.asmx/GetJobs?language=ro
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

    #
    counties,
)
import unicodedata


#
def has_diacritics(char):
    return any(unicodedata.combining(c) for c in char)


def remove_diacritics(input_string):
    normalized_string = unicodedata.normalize('NFD', input_string)
    return ''.join(char for char in normalized_string if not has_diacritics(char))


def scraper():
    '''
    ... scrape data from Eurofins scraper.
    '''
    json_data = GetRequestJson("https://atsintegration.eurofins.com/ATSWebService.asmx/GetJobs?language=ro")

    job_list = []
    for job in json_data:

        if 'ro' == job.get('countryCode'):

            if (location := job.get('locationCity')).lower() == 'bucharest':
                location = 'București'
            
            #
            location = remove_diacritics(location)

            county_general = ''
            for county_i in counties:
                for key, value in county_i.items():

                    # check this point
                    check_location = value[0]
                    for i in value:
                        if location == i and location == check_location:
                            county_general = i

            # get jobs items from response
            job_list.append(Item(
                job_title=job.get('title'),
                job_link=job.get('applyUrl'),
                company='Eurofins',
                country='Romania',
                county=county_general,
                city=location,
                remote='remote' if job.get('remoteJob') == "True" else 'on-site'
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Eurofins"
    logo_link = "https://c.smartrecruiters.com/sr-company-logo-prod-aws-dc5/59a68830e4b02f57443071f7/huge?r=s3-eu-central-1&_1616915876115"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
