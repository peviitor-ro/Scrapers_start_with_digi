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
from scrapers_forzza import scrape_tesla, update_tesla
from scrapers_forzza import sita_scrape, update_sita
from scrapers_forzza import farmexim_scrape, update_farmexim
from scrapers_forzza import makita_scrape, update_makita


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

    # scrape_tesla
    scrape_tesla()
    update_tesla()

    # scrape sita!
    sita_scrape()
    update_sita()

    # scrape farmexim!
    farmexim_scrape()
    update_farmexim()

    # scrape makita!
    makita_scrape()
    update_makita()
