#
#
#
# Main fail ---> Run all Scripts here.
#
# from scrapers_forzza import rcsrds_scrape, update_rcsrds
from scrapers_forzza import wirtek_scrape, update_wirtek
from scrapers_forzza import emag_scrape, update_emag
from scrapers_forzza import scrape_molTALEO, update_molTaleo
from scrapers_forzza import scrape_pmi, update_pmi
from scrapers_forzza import scrape_ursus, update_ursus


if __name__ == "__main__":

    # update wirtek
    wirtek_scrape()
    update_wirtek()

    # scrape DIGI
    # rcsrds_scrape()
    # pdate_rcsrds()

    # scrape emag
    emag_scrape()
    update_emag()

    # scrape MolGroup Taleo
    scrape_molTALEO()
    update_molTaleo()

    # scrape pmi.com!
    scrape_pmi()
    update_pmi()

    # scrape ursus
    scrape_ursus()
    update_ursus()
