"""
    This employs the CoinGecko API to get historical data and save it for easy 
access and analysis. We can use the OHLC prices from cryptodatadownload.com/data
instead of coingecko, since it seems to be more granular.
"""
import json
import requests
import time

url_prefix = "https://api.coingecko.com/api/v3/{}"

from cryptocmd import CmcScraper
import ast

def pull_CMC_scraper_data(cryptocurrency_name):
	"""
	Query CMC Scraper API to get the cryptocurrency price data
	"""
	assert type(cryptocurrency_name) is str, "Cryptocurrency name must be a string"
	scraper = CmcScraper(cryptocurrency_name)
	json_data = ast.literal_eval(scraper.get_data("json"))
	json_data.reverse()
	data = []
	for a in json_data:
		data.append(a["Open"])
		data.append(a["Close"])
	return data


def get_ids():
    with open("data/coin_list.json", "r") as f:
        data = json.load(f)
    ids = [data[i]['id'] for i in range(len(data))]
    return ids

"""
    Data Granularity:
    5-minute intervals: 1 day from query time
    hourly intervals: 1-90 days from query time
    daily intervals: More than 90 days from query time
    Use unix time for start and end

    Returns spot price/volume data in json format if coin_id is valid. 
    Otherwise, None is returned.
"""
def get_market_range(coin_id, start, end):
    if is_valid_id(coin_id):
        start = int(start); end = int(end)
        range_str = "coins/{}/market_chart/range?vs_currency=usd&from={}&to={}"\
            .format(coin_id, start, end)
        url = url_prefix.format(range_str)
        data = requests.get(url).json()
        return data
    else:
        print("Invalid ID.")

# The coin ID list from CoinGecko returns whether it contains the coin_id
def is_valid_id(coin_id):
    ids = get_ids()
    return coin_id in ids

# Retrieve the last n days of data
#   n = 1       : 5-minute intervals
#   1 < n <= 90 : 1-hour intervals
#   n > 90      : 1-day intervals
def get_n_days(coin_id, n):
    end = time.time()
    start = end - 24 * 60 * 60 * n
    return get_market_range(coin_id, start, end)

if __name__ == "__main__":
    pass

