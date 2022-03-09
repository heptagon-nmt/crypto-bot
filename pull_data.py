from cryptocmd import CmcScraper
import ast

def pull_CMC_scraper_data(cryptocurrency_name)
	assert type(cryptocurrency_name) is str, "Cryptocurrency name must be a string"
	scraper = CmcScraper(cryptocurrency)
	json_data = ast.literal_eval(scraper.get_data("json"))
	json_data.reverse()
	data = []
	for a in json_data:
		data.append(a["Open"])
		data.append(a["Close"])
	return data

