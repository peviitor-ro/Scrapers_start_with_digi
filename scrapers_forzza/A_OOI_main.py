#
#
#
#
#
import os
import subprocess

# exclude files
exclude = ['__init__.py',
           'A_OO_get_post_soup_update_dec.py',
           'A_OOI_main.py',
           'L_00_logo.py',
           "rcsrds_scraper.py",
           "seedblink_scraper.py",
           "ubisoft_scraper.py"]

path = os.path.dirname(os.path.abspath(__file__))

for site in os.listdir(path):
    if site.endswith('.py') and site not in exclude:
        action = subprocess.run(['python', os.path.join(path, site)], capture_output=True)
        if action.returncode != 0:
            errors = action.stderr.decode('utf-8')
            print("Error in " + site)
            print(errors)
        else:
            print("Success scraping " + site)
