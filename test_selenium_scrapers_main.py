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
import subprocess
import sys


class DownScrapers:
    """
    This class collect all fallen scrapers in list
    ... for future decisions.
    """

    down_scrapers_list = []
    data_visualization_jobs = []

    # + o functie de data visualization -> sa vedem care companie are cele mai multe joburi
    # and another methods for manipulate


class TestEngine:
    """
    This class is for testing all scrapers.
    """

    # exclude files
    exclude = ['__init__.py', 'A_OO_get_post_soup_update_dec.py', 'L_00_logo.py',]

    def return_path_data(self):
        """
        """
        test_scrapers_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_scrapers"))
        sys.path.append(test_scrapers_path)

        return test_scrapers_path

    def test_scrapers(self):
        """
        """
        print('Test Runs...')

        for site in os.listdir(self.return_path_data()):
            if site.endswith('.py') and site not in TestEngine.exclude:
                action = subprocess.run(['python', os.path.join(self.return_path_data(), site)], capture_output=True)
                if action.returncode != 0:
                    errors = action.stderr.decode('utf-8')
                    print("Error in " + site)
                    print(errors)

                    # append domain name to down scraper list!
                    DownScrapers.down_scrapers_list.append(site)
                else:
                    print(action)

            # deci, aici mai trebuie un selenium care sa verifice pe site-ul celalalt. Trebue un dict cu site-urile datele site-ului,
            # ... si un alt dict care sa preia comenzile pentru Selenium


if __name__ == "__main__":

    new_test = TestEngine()
    print(new_test.test_scrapers())

    # print down scrapers
    down = DownScrapers.down_scrapers_list
    print(f'Scrapers down -> {down}')
