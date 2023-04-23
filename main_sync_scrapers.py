#
#
#
# Main fail ---> Run all Scripts here.
#
from scrapers_forzza import rcsrds_scrape, update_rcsrds
from scrapers_forzza import wirtek_scrape, update_wirtek

if __name__ == "__main__":
    rcsrds_scrape()
    update_rcsrds()
