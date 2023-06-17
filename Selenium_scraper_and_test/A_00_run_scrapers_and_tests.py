#
#
#
#
from browser_config import chromedriver_config
from B_00_send_data_to_API import UpdateAPI
#
from xogito_scraper_selenium import ScraperXogito, TestScraperXogito
#
import time


if __name__ == "__main__":

    browser = chromedriver_config(headless=False)

    # TEST XOGITO: START
    # start collect data from xogito
    xogito = ScraperXogito(link='https://www.xogito.com/careers/', browser=browser)
    scraped_xogito = xogito.store_in_list()

    # xogito test!
    xogito_test = TestScraperXogito(browser=browser, data_from_xogito=scraped_xogito)
    xogito_test_result = xogito_test.test_links_xogito()

    if len(scraped_xogito) == len(xogito_test_result):
        print(f'Len scraped {len(scraped_xogito)} versus Len tested {len(xogito_test_result)}')
        print('Tests PASS. Xogito is OK!')

        # update API peviitor
        update_api = UpdateAPI()
        update_api.update_data(company_name='xogito', data_jobs=scraped_xogito)
        update_api.update_logo(id_company='xogito', logo_link='https://xogito.wpenginepowered.com/wp-content/themes/xgrebranding/images/logo-w-tagline-on-dark.svg')
    else:
        print(f'Len scraped {len(scraped_xogito)} versus Len tested {len(xogito_test_result)}')
        print('Test for -> Xogito <- didn\'t passed...')
    # END TEST XOGITO

    # quit browser
    time.sleep(1)
    browser.quit()
