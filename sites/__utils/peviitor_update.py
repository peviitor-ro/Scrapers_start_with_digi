#
#
#
#  Send data to Peviitor API!
#  ... OOP version
#
#
import requests
#
import os  # I do not have API KEY
#
import json
#
import time
#
import tempfile
from pathlib import Path
#
from fake_useragent import UserAgent

UA = UserAgent()
TOKEN_CACHE_PATH = Path(
    os.environ.get('PEVIITOR_TOKEN_CACHE_PATH')
    or Path(tempfile.gettempdir()) / 'peviitor_api_token_cache.json'
)
TOKEN_CACHE_TTL_SECONDS = int(os.environ.get('PEVIITOR_TOKEN_TTL_SECONDS', '3300'))


class UpdateAPI:
    '''
    - Method for clean data,
    - Method for update data,
    - Method for update logo.
    '''

    def __init__(self):
        self.email = os.environ.get('EMAIL') or 'laurentiumarianbaluta@gmail.com'
        self.access_token = None
        # self.logo_url = 'https://api.peviitor.ro/v1/logo/add/'

        self.logo_header = {
            'Content-Type': 'application/json',
            'User-Agent': UA.random,
        }

    def read_cached_token(self):
        if not TOKEN_CACHE_PATH.exists():
            return None

        try:
            with TOKEN_CACHE_PATH.open('r', encoding='utf-8') as cache_file:
                token_data = json.load(cache_file)
        except (OSError, json.JSONDecodeError):
            return None

        access_token = token_data.get('access_token')
        fetched_at = token_data.get('fetched_at', 0)

        if not access_token:
            return None

        if time.time() - fetched_at >= TOKEN_CACHE_TTL_SECONDS:
            return None

        return access_token

    def write_cached_token(self, access_token):
        TOKEN_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)

        cache_payload = {
            'access_token': access_token,
            'fetched_at': time.time(),
        }
        temp_cache_path = TOKEN_CACHE_PATH.with_suffix('.tmp')

        with temp_cache_path.open('w', encoding='utf-8') as cache_file:
            json.dump(cache_payload, cache_file)

        temp_cache_path.replace(TOKEN_CACHE_PATH)

    def get_token(self, force_refresh=False):
        if not force_refresh:
            cached_token = self.read_cached_token()
            if cached_token:
                self.access_token = cached_token
                return self.access_token

        payload = json.dumps({
        "email": self.email
        })

        post_header = {
        'Content-Type': 'application/json',
        'User-Agent': UA.random,
        }

        self.access_token = requests.request(
            "POST", "https://api.laurentiumarian.ro/get_token", headers=post_header, data=payload).json()['access']
        self.write_cached_token(self.access_token)

        return self.access_token


    def add_jobs(self, data_jobs, retry_on_auth=True):
        if not self.access_token:
            self.get_token()

        post_header = {
        'Authorization': f'Bearer {self.access_token}',
        'Content-Type': 'application/json',
        'User-Agent': UA.random,
        }

        res = requests.request("POST", "https://api.laurentiumarian.ro/jobs/add/", headers=post_header, data=json.dumps(data_jobs))

        if res.status_code == 401 and retry_on_auth:
            self.get_token(force_refresh=True)
            return self.add_jobs(data_jobs, retry_on_auth=False)

        print(json.dumps(data_jobs, indent=4))
        return res

    def update_jobs(self, company_name: str, data_jobs: list):
        '''
        ... update and clean data on peviitor

        '''
        self.get_token()
        time.sleep(0.2)
        self.add_jobs(data_jobs)


    def update_logo(self, id_company: str, logo_link: str):
        '''
        ... update logo on peviitor.ro
        '''
        pass

        # data = json.dumps([{"id": id_company, "logo": logo_link}])
        # response = requests.post(self.logo_url, headers=self.logo_header, data=data)

        # #  print(f'Logo update ---> succesfuly {response}')
        #
        # Changes --- For Test
