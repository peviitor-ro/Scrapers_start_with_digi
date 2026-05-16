#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> Eurofins
# Link ------> https://api.smartrecruiters.com/v1/companies/Eurofins/postings?country=ro
#
from __utils import (
    GetRequestJson,
    get_county,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from Eurofins scraper.
    '''
    json_data = GetRequestJson(
        "https://api.smartrecruiters.com/v1/companies/Eurofins/postings?country=ro&limit=100"
    )

    job_list = []
    for job in json_data.get('content', []):

        if job.get('location', {}).get('country') != 'ro':
            continue

        location = job.get('location', {})
        city = location.get('city', '')
        if city.lower() == 'bucharest':
            city = 'București'

        location_finish = get_county(location=city)

        remote = location.get('remote', False)
        hybrid = location.get('hybrid', False)
        remote_type = 'remote' if remote else ('hybrid' if hybrid else 'on-site')

        apply_url = f"https://www.smartrecruiters.com/Eurofins/{job.get('id')}"

        job_list.append(Item(
            job_title=job.get('name'),
            job_link=apply_url,
            company='Eurofins',
            country='Romania',
            county=location_finish[0] if True in location_finish else None,
            city='all' if city.lower() == location_finish[0].lower()
                        and True in location_finish and 'bucuresti' != city.lower()
                            else city,
            remote=remote_type,
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
