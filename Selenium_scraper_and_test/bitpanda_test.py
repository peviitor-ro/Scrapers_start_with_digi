#
#
#
#
# Test for Bitpanda Company -> https://boards.eu.greenhouse.io/bitpanda
#
from browser_config import chromedriver_config
#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#
from bs4 import BeautifulSoup
from time import sleep


if __name__ == "__main__":
    driver = chromedriver_config(headless=False)

    try:
        driver.get('https://boards.eu.greenhouse.io/bitpanda')
    except:
        pass
    finally:
        sleep(3)
        driver.quit()
