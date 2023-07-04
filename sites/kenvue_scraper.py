#
#
#
#
# Company -> kenvue
# Link ----> https://www.kenvue.com/careers
# https://kenvue.taleo.net/careersection/rest/jobboard/searchjobs?lang=en&portal=101430233 (post)
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid


def prepare_post_request() -> tuple:
    '''
    ... here prepare post request for Kevue Company.
    '''

    curl 'https://kenvue.taleo.net/careersection/rest/jobboard/searchjobs?lang=en&portal=101430233' \
  -H 'Accept: application/json, text/javascript, */*; q=0.01' \
  -H 'Accept-Language: en-US,en;q=0.7' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: locale=en; OptanonAlertBoxClosed=2023-07-03T16:24:31.765Z; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Jul+03+2023+19%3A25%3A25+GMT%2B0300+(Eastern+European+Summer+Time)&version=202211.2.0&isIABGlobal=false&hosts=&consentId=d91acf9c-f7bf-430b-b07b-7980589f651d&interactionCount=1&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1&geolocation=RO%3BCT&AwaitingReconsent=false' \
  -H 'Origin: https://kenvue.taleo.net' \
  -H 'Referer: https://kenvue.taleo.net/careersection/2/jobsearch.ftl' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Sec-GPC: 1' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'tz: GMT+03:00' \
  -H 'tzname: Europe/Bucharest' \
  --data-raw '{"multilineEnabled":true,"sortingSelection":{"sortBySelectionParam":"3","ascendingSortingOrder":"false"},"fieldData":{"fields":{"KEYWORD":"","LOCATION":"1493840260991","CATEGORY":""},"valid":true},"filterSelectionParam":{"searchFilterSelections":[{"id":"POSTING_DATE","selectedValues":[]},{"id":"LOCATION","selectedValues":[]},{"id":"JOB_FIELD","selectedValues":[]}]},"advancedSearchFiltersSelectionParam":{"searchFilterSelections":[{"id":"ORGANIZATION","selectedValues":[]},{"id":"LOCATION","selectedValues":[]},{"id":"JOB_FIELD","selectedValues":[]},{"id":"JOB_NUMBER","selectedValues":[]},{"id":"URGENT_JOB","selectedValues":[]},{"id":"STUDY_LEVEL","selectedValues":[]},{"id":"WILL_TRAVEL","selectedValues":[]}]},"pageNo":1}' \
  --compressed
