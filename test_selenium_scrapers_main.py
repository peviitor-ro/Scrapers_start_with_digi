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
        print('In function')

        for site in os.listdir(self.return_path_data()):
            if site.endswith('.py') and site not in TestEngine.exclude:
                action = subprocess.run(['python', os.path.join(self.return_path_data(), site)], capture_output=True)
                if action.returncode != 0:
                    errors = action.stderr.decode('utf-8')
                    print("Error in " + site)
                    print(errors)
                else:
                    print(action)


if __name__ == "__main__":

    new_test = TestEngine()
    print(new_test.test_scrapers())


IDEEA = """
Deci ---> trebuie sa import toti scraperii cu "import os".
sa le scot decoratorii... dar asta ar insemna ca trebuie sa-i
bag intr-un al folderz4 de test? ... ?

Apoi, dupa ce import scraperii, sa incept testele...

-> evident va trebui de creat un dict in care key: name_scraper.py - valoare: {link: link_catre_site,
                                                                               search_elem: class, id or xpath,
                                                                               html_data: id_name, class_name}

--------------> Dupa aia, testele sa fie rulate intr-o singura clasa, intr-un -> for loop <-

-> o variabila care stocheaza numarul de joburi de la companie (aceasta variabila introdusa intr-o lista aparte pentru data visialization)
-> o functie in care selenium ia link-ul din dict-ul scraperului, merge si cauta dupa datele din html, sau le calculeaza si Selenium inca o data.
-> dupa care, un request merge prin toate cu head si verifica daca merge ok. # optional
-> numarul de joburi de stocat in data_visualization_jobs pentru vizualizare.
"""
