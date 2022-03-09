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
"""
##### Real time data:
# Request OHLC data from Coingecko every 30 minutes
from keras.models import Sequential
from keras import layers
from keras.utils import to_categorical
import json
import requests
import time


def get_data(symbol):
    r = requests.get("https://api.coingecko.com/api/v3/coins/{}/ohlc?vs_currency=usd&days=1".format(symbol))
    data = r.json()

def summarize(prediction):
    pass

# Return classifier with 
def get_classifier():
    classifier = Sequential()
    classifier.add(layers.Dense(100, "relu"))
    classifier.add(layers.Dense(50, "relu"))
    classifier.add(layers.Dense(2, "softmax"))
    return classifier

if __name__ == "__main__":
    data_list = []
    initial_time = time.time()
    classifier = get_classifier()
    while(True):
        data = get_data("ethereum")
        data_list.append(data[-1])
        time.sleep(30 * 60)
        prediction = classifier.predict(data_list[-1])
        summarize(prediction)

if __name__ == "__main__":
    pass
"""
