#
#
#
#
# Company -> Masabi
# Link ----> https://careers.masabi.com/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def prepare_post_req() -> tuple:
    '''
    ...
    '''

    url = 'https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams'

    headers = {
        'authority': 'jobs.ashbyhq.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.6',
        'apollographql-client-name': 'frontend_non_user',
        'apollographql-client-version': '0.1.0',
        'content-type': 'application/json',
        'origin': 'https://jobs.ashbyhq.com',
        'referer': 'https://jobs.ashbyhq.com/masabi',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }

    data_raw = '''
    {
        "operationName": "ApiJobBoardWithTeams",
        "variables": {
            "organizationHostedJobsPageName": "masabi"
        },
        "query": "query ApiJobBoardWithTeams($organizationHostedJobsPageName: String\u0021) {\\n  jobBoard: jobBoardWithTeams(\\n    organizationHostedJobsPageName: $organizationHostedJobsPageName\\n  ) {\\n    teams {\\n      id\\n      name\\n      parentTeamId\\n      __typename\\n    }\\n    jobPostings {\\n      id\\n      title\\n      teamId\\n      locationId\\n      locationName\\n      employmentType\\n      secondaryLocations {\\n        ...JobPostingSecondaryLocationParts\\n __typename\\n      }\\n      compensationTierSummary\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment JobPostingSecondaryLocationParts on JobPostingSecondaryLocation {\\n  locationId\\n  locationName\\n  __typename\\n}"
    }
    '''

    return url, headers, data_raw


def make_post_req():
    '''
    ...
    '''

    url, headers, data_raw = prepare_post_req()

    res = requests.post(url=url, headers=headers, data=data_raw).json()

    lst_with_data = []
    for job in res['data']['jobBoard']['jobPostings']:

        cities = ['cluj', 'cluj-napoca', 'bucuresti', 'bucharest']
        # search by the city
        city = ''
        for loc in job['secondaryLocations']:
            if loc['locationName'].lower() in cities:
                city = loc['locationName']

                # end search

        if city == 'Remote':
            city = ''
            type = 'remote'
        else:
            type = 'on-site'

        if city.lower() in cities:
            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": job['title'],
                    "job_link": 'https://careers.masabi.com/?ashby_jid=' + job['id'],
                    "company": "masabi",
                    "country": "Romania",
                    "city": city,
                    "remote": type,
                    })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'masabi'
data_list = make_post_req()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('masabi',
                  'https://app.ashbyhq.com/api/images/org-theme-wordmark/be3ff8e3-f9b5-4a45-9069-c71c963b467c/bb795a43-4c37-4c60-abc9-bbc99f1e225a.png'
                  ))
