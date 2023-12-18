#
#
#
import cfscrape 


url = 'https://romania.cgsinc.com/vino-in-echipa-cgs/'
scraper = cfscrape.create_scraper()

response = scraper.get(url)
print(response.content)
