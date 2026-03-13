
import os
import subprocess


class Scraper:
    def __init__(self, exclude):
        """
        Initialize the Scraper class with a list of files to exclude.
        """
        self.exclude = exclude

    def run(self):
        """
        Run the scraper for each Python file in the current directory, excluding the specified files.
        """
        path = os.path.dirname(os.path.abspath(__file__))

        for site in os.listdir(path):
            if site.endswith('.py') and site not in self.exclude:
                script_path = os.path.join(path, site)
                try:
                    print(f"Running: python3 {script_path}")
                    # Run the script with 'python3' using shell=True to simulate direct execution
                    result = subprocess.run(
                        f'python3 "{script_path}"', cwd=path, shell=True, check=True, env=os.environ)
                    print(
                        f"Success scraping {site} with exit code {result.returncode}")
                except subprocess.CalledProcessError as e:
                    print(
                        f"Error scraping {site} with exit code {e.returncode}: {e}")
                except Exception as e:
                    print(
                        f"An unexpected error occurred while scraping {site}: {e}")


if __name__ == "__main__":
    # exclude files
    exclude = ['__init__.py',
               '__create_scraper.py',
               '__main_RunnerFile.py',
               ]

    scraper = Scraper(exclude)
    scraper.run()
