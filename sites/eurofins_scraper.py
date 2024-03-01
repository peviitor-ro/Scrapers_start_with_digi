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

            location_finish = get_county(location=location)

            # get jobs items from response
            job_list.append(Item(
                job_title=job.get('title'),
                job_link=job.get('applyUrl'),
                company='Eurofins',
                country='Romania',
                county=location_finish[0] if True in location_finish else None,
                city='all' if location.lower() == location_finish[0].lower()\
                            and True in location_finish and 'bucuresti' != location.lower()\
                                else location,
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
