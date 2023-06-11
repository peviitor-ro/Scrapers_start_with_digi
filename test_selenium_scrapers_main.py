#
#
#
# ---> Run all scraper here1
#
# import config driver here!
from browser_configured_py import chromedriver_config
#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#
import os
import importlib
import sys


class DownScrapers:
    """
    This class collect all fallen scrapers in list
    ... for future decisions.
    """

    down_scrapers_list = []
    data_visualization_jobs = []

    # def visualization ---> for data jobs visualitation

    # + o functie de data visualization -> sa vedem care companie are cele mai multe joburi
    # and another methods for manipulate


class TestEngineScrapers:
    pass


class TestEngine:
    """
    This class is for testing all scrapers.
    """

    # exclude files
    exclude = ['__init__.py', 'A_OO_get_post_soup_update_dec.py', 'L_00_logo.py',]

    def test_scrapers(self):
        test_data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_scrapers/here_scrapers"))
        sys.path.append(test_data_path)

        for filename in os.listdir(test_data_path):
            if filename.endswith('.py') and filename not in TestEngine.exclude:
                module_name = f"test_scrapers.here_scrapers.{filename[:-3]}"
                module = importlib.import_module(module_name)

                data_run = module.run_scraper()

                if data_run:
                    print(f'{filename} -> {data_run[1]}')
                else:
                    DownScrapers.down_scrapers_list.append(filename)

        # deci, aici mai trebuie un selenium care sa verifice pe site-ul celalalt. Trebue un dict cu site-urile datele site-ului,
        # ... si un alt dict care sa preia comenzile pentru Selenium


if __name__ == "__main__":

    new_test = TestEngine()
    print(new_test.test_scrapers())

    down = DownScrapers.down_scrapers_list
    print(f'Scrapers down -> {down}')
