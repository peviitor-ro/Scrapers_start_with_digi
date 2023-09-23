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
          'accept-language': 'en-US,en;q=0.8',
          'apollographql-client-name': 'frontend_non_user',
          'apollographql-client-version': '0.1.0',
          'content-type': 'application/json',
          'origin': 'https://jobs.ashbyhq.com',
          'referer': 'https://jobs.ashbyhq.com/masabi?embed=js',
          'sec-fetch-dest': 'empty',
          'sec-fetch-mode': 'cors',
          'sec-fetch-site': 'same-origin',
          'sec-gpc': '1',
          'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
          }

    data = {
        "operationName": "ApiJobBoardWithTeams",
        "variables": {
            "organizationHostedJobsPageName": "masabi"
        },
        "query": "query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) {\\n  jobBoard: jobBoardWithTeams(\\n    organizationHostedJobsPageName: $organizationHostedJobsPageName\\n  ) {\\n    teams {\\n      id\\n      name\\n      parentTeamId\\n      __typename\\n    }\\n    jobPostings {\\n      id\\n      title\\n      teamId\\n      locationId\\n      locationName\\n      employmentType\\n      secondaryLocations {\\n        ...JobPostingSecondaryLocationParts\\n __typename\\n      }\\n      compensationTierSummary\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment JobPostingSecondaryLocationParts on JobPostingSecondaryLocation {\\n  locationId\\n  locationName\\n  __typename\\n}"
    }

    return url, headers, data


def make_post_req():
    '''
    ...
    '''

    url, headers, data = prepare_post_req()

    res = requests.post(url=url, headers=headers, json=data).json()

    return res


print(make_post_req())
