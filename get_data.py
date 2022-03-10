"""
    This module is to handle everything related to data collection (historical
or real-time). The command-line utility can call these functions for doing 
things such as getting the most recent price/volume data (spot prices or OHLC).
TODO Implement yahoo_finance and CmcScraper APIs
TODO Maybe make KrakenAPI/CoingeckoAPI interface classes since most of the 
    functionality is parallel between them
TODO fix is_valid_ids_kraken. It doesn't work for values like "ETHUSD" or 
    "BTCUSD".
TODO validate Kraken data. The intervals between rows don't seem correct 
    currently. It may be that if you don't go far enough back in the range it
    simply returns some default data. Also it may be necessary to remove the 
    first row since it's the most recent value, so it doesn't have the closing 
    price
"""
import ast
from cryptocmd import CmcScraper
import json
import numpy as np
import os
import requests
import sys
import time
from yahoo_fin import stock_info as si

url_prefixes = {"coingecko": "https://api.coingecko.com/api/v3/{}", 
                "kraken" : "https://api.kraken.com/0/public/{}"}

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


def get_available_sources():
    """
    TODO Add CmcScraper and also yahoo_finance?
    :return: list of available sources
    """
    return list(url_prefixes.keys()).append("yahoo_fin")

def get_available_symbols_from_source(source):
    """
    :return: A list of available symbols 
    :rtype: list
    """
    if source == "coingecko":
        return get_ids_coingecko()
    elif source == "kraken":
        return get_ids_kraken()
    else:
        print("Unknown source.")

def get_ohlc_coingecko(id, vs_currency, days):
    """
    Coingecko's OHLC API for OHLC data
    :param str id: The Coingecko coin ID (ethereum, litecoin, etc.)
    :param str vs_currency: The currency to weigh the coin against (usd, eur, etc.)
    :return: 
    """
    assert is_valid_id_coingecko(id)
    url_suffix = "coins/{}/ohlc/?vs_currency={}&days={}".format(id, vs_currency, days)
    url = url_prefixes['coingecko'].format(url_suffix)
    response = requests.get(url)
    data = response.json()
    return np.array(data)

def get_ohlc_kraken(pair, since, interval = 30):
    """
    Retrieve OHLC that ranges from a specified date to current. The granularity 
    can be supplied as well. This one might be preferable to the user since it 
    is quite a bit more flexible with time step intervals.
    :param str pair: This is a ticker pair, such as ETHUSD, XRPUSD, BTCETH, etc.
    :param int since: UNIX timestamp for the beginning of the data
    :param int interval: An integer which specifies the OHLC time interval in 
        minutes. Valid values are 1, 5, 15, 30, 60, 240, 1440, 10080, 21600
    :type interval: integer or None
    :param str kraken: The external source of the data
    :return: a numpy array of volume (USD) and OHLC data; or None if the request
        cannot be completed either because an invalid symbol pair was passed or
        for some other reason. All fields are converted to np.float32 type
    """
    url_suffix = "OHLC?pair={}&since={}&interval={}".format(pair.upper(), \
        since, interval)
    url = url_prefixes['kraken'].format(url_suffix)
    response = requests.get(url)
    data = response.json()
    return np.array(data['result'][list(data['result'])[0]], dtype = np.float64)

def get_ids_coingecko():
    """
    :return: a list of IDs (ethereum, litecoin, etc.) available for CoinGecko
    """
    with open("data/coingecko_id_list.json", "r") as f:
        data = json.load(f)
    ids = [data[i]['id'] for i in range(len(data))]
    return ids

def get_ids_kraken():
    """
    :return: a list of available symbol pairs offered by Kraken 
        (ETHUSD, BTCUSD, BTCETH, etc.)
    """
    with open("data/kraken_pairs_list.json", "r") as f:
        data = json.load(f)
        pairs = list(data['result'].keys())
    return pairs

def get_market_range_coingecko(coin_id, start, end):
    """
    Granularity is automatically determined by Coingecko using the following 
    specifications: 
        5-minute intervals: 1 day from query time
        hourly intervals: 1-90 days from query time
        daily intervals: More than 90 days from query time
    Use unix UTC for start and end

    :param int start: The starting time in the range (UTC Unix Timestamp)
    :param int end: The ending time in the range (UTC Unix Timestamp)
    :return: Returns spot price/volume data in json format if coin_id is valid. 
        Otherwise, None is returned.
    :rtype: json 
    """
    assert start < end
    assert(is_valid_id_coingecko(coin_id))
    start = int(start); end = int(end)
    range_str = "coins/{}/market_chart/range?vs_currency=usd&from={}&to={}"\
        .format(coin_id, start, end)
    url = url_prefixes["coingecko"].format(range_str)
    data = requests.get(url).json()
    return data

def is_valid_id_coingecko(coin_id):
    """
    :return: whether a given coin ID is in the list of available Coingecko IDs
    :rtype: boolean
    """
    ids = get_ids_coingecko()
    return coin_id in ids

def is_valid_id_kraken(pair):
    """
    :return: whether a given symbol pair (e.g. ETHUSD) is in the list of 
        available Kraken symbol pairs.
    :rtype: boolean
    """
    pairs = get_ids_kraken()
    return pair in pairs

if __name__ == "__main__":
    pass
