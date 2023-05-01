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
from scrapers_forzza import proctergamble_scrape, update_proctergamble
from scrapers_forzza import threatconnect_scrape, update_threatconnect
from scrapers_forzza import jti_scrape, update_jti
from scrapers_forzza import cec_scrape, update_cec

# this scripts have turbo with bash
from autototal_scraper import scrape_autototal
from autototal_update_peviitor import update_autototal

# here import scripts from scrapers_forzza_2
from scrapers_forzza_2 import egger_scraper, update_egger
from scrapers_forzza_2 import scrape_eastmen, update_eastmen
from scrapers_forzza_2 import scrape_axintor, update_axintor
from scrapers_forzza_2 import scrape_jumbo, update_jumbo
from scrapers_forzza_2 import scrape_scania, update_scania


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

    # scraper proctergamble!
    proctergamble_scrape()
    update_proctergamble()

    # scrape threatconnect!
    threatconnect_scrape()
    update_threatconnect()

    # scrape jti!
    jti_scrape()
    update_jti()

    # scrape cec!
    cec_scrape()
    update_cec()

    # from scrapers_forzza_2
    egger_scraper()
    update_egger()

    # autototal.ro
    scrape_autototal()
    update_autototal()

    # eastmen
    scrape_eastmen()
    update_eastmen()

    # axintor
    scrape_axintor()
    update_axintor()

    # update jumbo
    scrape_jumbo()
    update_jumbo()

    # update scrape!
    scrape_scania()
    update_scania()
