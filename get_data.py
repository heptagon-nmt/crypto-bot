"""
    This module is to handle everything related to data collection (historical
or real-time). The command-line utility can call these functions for doing 
things such as getting the most recent price/volume data (spot prices or OHLC).
TODO Implement yahoo_finance and CmcScraper APIs
TODO Maybe make KrakenAPI/CoingeckoAPI interface classes since most of the 
    functionality is parallel between them
TODO validate Kraken data. The intervals between rows don't seem correct 
    currently. It may be that if you don't go far enough back in the range it
    simply returns some default data. Also it may be necessary to remove the 
    first row since it's the most recent value, so it doesn't have the closing 
    price
"""
import ast
from cryptocmd import CmcScraper
from html.parser import HTMLParser
import json
import numpy as np
import os
import re
import requests
import time
from yahoo_fin import stock_info as si

class KrakenCurrencyTableParser(HTMLParser):
    """
    This class is for the get_ids_kraken() function, which needs to parse a 
    specific HTML document from Kraken's website when the update_cache flag is
    passed for retrieving the coin list from the server.
    
    Attributes: 
        coins               A list to contain the symbols located on the webpage
        ignore_currencies   Currencies to ignore when parsing
    """
    def __init__(self):
        super().__init__()
        self.coins = []
        self.ignore_currencies = ["USD", "EUR", "CAD", "JPY", "GBP", "CHF", 
                                "AUD", "USDT"]
    def handle_starttag(self, tag, attrs):
        if tag == "strong":
            self.current = True
    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):
        if bool(re.search(r"[A-Z][A-Z][A-Z][A-Z]*", data)) and self.current \
                and data not in self.ignore_currencies:
            self.coins.append(data)
        self.current = False
    def get_coins(self):
        return self.coins

url_prefixes = {"coingecko": "https://api.coingecko.com/api/v3/{}", 
                "kraken" : "https://api.kraken.com/0/public/{}"}

def pull_CMC_scraper_data(cryptocurrency_name):
    """
    Query CMC Scraper API to get the cryptocurrency price data

    :arg cryptocurrency_name: String specifying which cryptocurrency to query. For example Bitcoin is BTC
    :return: Opening daily price data going back to the beginning of the cryptocurrency. 
    :rtype: list
    """
    assert type(cryptocurrency_name) is str, "Cryptocurrency name must be a string"
    scraper = CmcScraper(cryptocurrency_name)
    json_data = ast.literal_eval(scraper.get_data("json"))
    json_data.reverse()
    data = []
    for a in json_data:
        data.append(a["Open"])
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
    assert source in url_prefixes.keys(), "Source must be from the following %s" % url_prefixes.keys()
    if source == "coingecko":
        return get_ids_coingecko()
    elif source == "kraken":
        return get_ids_kraken()
    else:
        print("Unknown source.")

def get_ohlc_coingecko(id, vs_currency, days):
    """
    Coingecko's OHLC API for OHLC data. The time step intervals are 
    automatically set by Coingecko as follows:
        1-2 days: 30 minute intervals
        3 < days < 30: 4 hour intervals
        days > 31: 4 day intervals

    :param str id: The Coingecko coin ID (ethereum, litecoin, etc.)
    :param str vs_currency: The currency to weigh the coin against (usd, eur, etc.)
    :return: Timestamp (ms), Open, High, Low, Close in a numpy array
    """
    id = id.lower()
    assert is_valid_id_coingecko(id)
    url_suffix = "coins/{}/ohlc/?vs_currency={}&days={}".format(id, vs_currency.lower(), days)
    url = url_prefixes['coingecko'].format(url_suffix)
    response = requests.get(url)
    data = response.json()
    assert isinstance(data, list)
    return np.array(data)

def get_opening_price_coingecko(id, vs_currency, days):
    """
    Remember, granularity is determined by the number of days specified. 
    1-2 days: 30 minute intervals
    3 < days < 30: 4 hour intervals
    days > 31: 4 day intervals

    :return: Coingecko's opening price for each time interval 
    """
    data = get_ohlc_coingecko(id, vs_currency, days).transpose()
    assert len(data) > 1 
    return data[1]

def get_opening_price_kraken(pair, days, interval = 30):
    data = get_ohlc_kraken(pair, days, interval).transpose()
    assert len(data) > 1
    return data[1]

def get_ohlc_kraken(pair, days, interval = 30):
    """
    Retrieve OHLC that ranges from a specified date to current. The granularity 
    can be supplied as well. This one might be preferable to the user since it 
    is quite a bit more flexible with time step intervals.

    :param str pair: This is a ticker pair, such as ETHUSD, XRPUSD, BTCETH, etc.
    :param int days: Number of days to go back to 
    :type days: integer
    :param int interval: An integer which specifies the OHLC time interval in 
        minutes. Valid values are 1, 5, 15, 30, 60, 240, 1440, 10080, 21600
    :type interval: integer or None
    :param str kraken: The external source of the data
    :return: a numpy array of volume (USD) and OHLC data; or None if the request
        cannot be completed either because an invalid symbol pair was passed or
        for some other reason. All fields are converted to np.float32 type
    """
    assert is_valid_id_kraken(pair), "Symbol pair not found."
    since = time.time() - days * 24 * 60 * 60
    url_suffix = "OHLC?pair={}&since={}&interval={}".format(pair.upper(), \
        since, interval)
    url = url_prefixes['kraken'].format(url_suffix)
    response = requests.get(url)
    data = response.json()
    assert len(data['error']) == 0, "Kraken server returned {}.".format(data['error'][0])
    return np.array(data['result'][list(data['result'])[0]], dtype = np.float64)

def get_ids_coingecko(update_cache = False):
    """
    If the cache is updated, then the data is saved to a json file first
    then loaded back from that file. Inefficient? Maybe

    :return: a list of IDs (ethereum, litecoin, etc.) available for CoinGecko
    """
    file_name = "data/coingecko_id_list.json"
    if update_cache:
        r = requests.get(url_prefixes["coingecko"].format("coins/list"))
        data = r.json()
        with open(file_name, "w") as f:
            json.dump(data, f)
    with open(file_name, "r") as f:
        data = json.load(f)
    ids = [data[i]['id'] for i in range(len(data))]
    return ids

def get_ids_kraken(update_cache = False):
    """
    If update_cache pull the html from a table on Kraken's website and parse
    it for the available base currencies.

    :return: a list of available symbol pairs offered by Kraken. The base 
        currency will always be USD. (ETHUSD, BTCUSD, LTCUSD, etc.)
    """
    support_url = "https://support.kraken.com/hc/en-us/articles/201893658-Currency-pairs-available-for-trading-on-Kraken"
    file_name = "data/kraken_pairs_list.json"
    if update_cache or not os.path.isfile(file_name):
        r = requests.get(support_url, headers = {"User-Agent" : "Mozilla/5.0"})
        raw_text = r.text
        parser = KrakenCurrencyTableParser()
        parser.feed(raw_text)
        pairs_list = parser.get_coins()
        for i, coin in enumerate(pairs_list):
            pairs_list[i] = coin + "USD"
        with open(file_name, "w") as f:
            json.dump(pairs_list, f)
    assert(os.path.isfile(file_name))
    with open(file_name, "r") as f:
        pairs_list = list(json.load(f))
    return pairs_list

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
