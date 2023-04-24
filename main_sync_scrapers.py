#
#
#
# Main fail ---> Run all Scripts here.
#
# from scrapers_forzza import rcsrds_scrape, update_rcsrds
from scrapers_forzza import wirtek_scrape, update_wirtek
from scrapers_forzza import emag_scrape, update_emag


if __name__ == "__main__":

    # update wirtek
    wirtek_scrape()
    update_wirtek()

    # scrape DIGI
    # rcsrds_scrape()
    # pdate_rcsrds()

    # scrape emag

