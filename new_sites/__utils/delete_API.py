#
#
# New version of Scrapers_Start_with_Digi
# ... new file for Clean_data from API
#
#
import os
import requests


class CleanData:

    def __init__(self, api_key):
        self.api_key = api_key
        self.clean_url = "https://api.peviitor.ro/v4/clean/"

    def clean_data(self, company_name: str) -> None:
        clean_header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "apikey": self.api_key
        }

        print(f"APY_KEY: {self.api_key}")

        clean_request = requests.post(url=self.clean_url, headers=clean_header,
                                      data={"company": company_name})
        print(f"{company_name} clean all Data -> {clean_request.status_code}")


class ConcreteCleanData(CleanData):

    def __fspath__(self):
        return self.clean_url


def main():

    # company name, from terminal
    input_company = input("Scrie numele companiei: ")

    # create a ConcreteCleanData object
    clean_data = ConcreteCleanData(api_key=os.environ.get("API_KEY"))

    # clean data
    clean_data.clean_data(input_company)


if __name__ == "__main__":
    main()
