from cryptocmd import CmcScraper

scraper = CmcScraper("BTC")

headers, data = scraper.get_data()

xrp_json_data = scraper.get_data("json")

print(xrp_json_data)
