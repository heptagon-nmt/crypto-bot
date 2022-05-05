import numpy as np
from src.get_data import *
import subprocess as sp

"""
Kraken unit tests
"""
def test_kraken_status():
    k = Kraken()
    assert k.get_server_status(), "Kraken server unreachable"

def test_kraken_ids():
    k = Kraken()
    ids = k.get_ids()
    assert type(ids) is list, "Kraken ids must be a list"

def test_kraken_asset_pairs():
    k = Kraken()
    asset_pairs = k.get_asset_pairs()
    assert type(asset_pairs) is list, "Kraken asset pairs must be a list"

def test_kraken_current_price():
    k = Kraken()
    current_price = k.get_current_price("BTC", "USD")
    assert type(current_price) is float or type(current_price) is int, "Kraken current price must be a number"
    assert current_price >= 0, "Kraken current price "

def test_kraken_intervals():
    k = Kraken()
    valid_intervals = [1, 5, 15, 30, 60, 240, 1440, 10080, 21600]
    intervals = k.get_intervals()
    assert intervals == valid_intervals, "Kraken must return the following intervals: {}".format(valid_intervals)

def test_kraken_ohlc():
    k = Kraken()
    ohlc = k.get_ohlc("BTC", "USD", 1, 1)
    assert len(ohlc) == 720, "Kraken should have returned 720 data points for get_ohlc at 1 minute intervals at 1 day range"
    assert len(ohlc[0]) == 8, ("Kraken OHLC should have 8 columns: "  
                              "UNIX Timestamp (s) | Open | High | Low | Close | "
                              "Volume-Weighted average Interval Price | "
                              "Interval Volume (Amount of currency in terms of currency |"
                              "Number of trades in interval")

def test_kraken_opening_price():
    k = Kraken()
    opening = k.get_opening_price("LTC", "USD", 1, 1)
    assert type(opening) is np.ndarray, "Kraken opening prices should be a numpy array"
    assert len(opening) == 720, "Kraken should have return 720 data points"

def test_kraken_is_valid_id():
    k = Kraken()
    assert not k.is_valid_id("asdf"), "\"asdf\" is not a valid Kraken id"
    assert k.is_valid_id("BTC"), "\"BTC\" is a valid Kraken id"
    assert not k.is_valid_id("btc"), "\"btc\" is not a valid Kraken id"

def test_kraken_search_symbols():
    k = Kraken()
    assert len(k.search_symbols("BTC")) > 0, "Kraken search for \"BTC\" should have returned at least 1 item."
    assert len(k.search_symbols("asdf")) == 0, "Kraken search for \"asdf\" should have returned 0 items."

"""
CoinGecko unit tests
"""
def test_coingecko_status():
    c = CoinGecko()
    assert c.get_server_status(), "CoinGecko server unreachable"

def test_coingecko_ids():
    c = CoinGecko()
    ids = c.get_ids()
    assert type(ids) is list, "CoinGecko ids must be a list"

def test_coingecko_current_price():
    c = CoinGecko()
    cp = c.get_current_price("bitcoin", "usd")
    assert type(cp) is float or type(cp) is int, "CoinGecko current price should be a float."
    assert cp >= 0, "CoinGecko current price should not be negative"

def test_coingecko_dict_ids():
    """
    dict_ids supposed to be a list of coingecko IDs, each stored in dictionary format
    """
    c = CoinGecko()
    dict_ids = c.get_dict_ids()
    assert type(dict_ids) is list, "CoinGecko dict_ids should be type \"dict\""
    assert len(dict_ids) > 0, "CoinGecko should return at least 1 valid dict_id"

def test_coingecko_intervals():
    c = CoinGecko()
    valid_intervals = [30, 60 * 4, 60 * 24 * 4]
    intervals = c.get_intervals()
    assert intervals == valid_intervals, "CoinGecko must return the following intervals: {}".format(valid_intervals)

def test_coingecko_range():
    c = CoinGecko()
    valid_ranges = np.array([1, 7, 14, 30, 90, 180, 365])
    assert type(valid_ranges) is np.ndarray, "CoinGecko valid ranges must be returned in numpy ndarray format."
    assert np.array_equiv(valid_ranges, c.get_range()), "CoinGecko returned the incorrect ranges"

def test_coingecko_current_price():
    c = CoinGecko()
    price = c.get_current_price("bitcoin", "usd")
    assert type(price) is float or type(price) is int, "CoinGecko current price value should be a number"
    assert price >= 0, "CoinGecko current price should be nonnegative"

def test_coingecko_ohlc():
    c = CoinGecko()
    ohlc = c.get_ohlc("bitcoin", "usd", 7)
    assert 41 <= len(ohlc) <= 43, "The returned OHLC values for CoinGecko should be within a the range of 41 to 43 days"
    assert len(ohlc[0]) == 5, "CoinGecko OHLC must have 5 fields: UNIX Timestamp (ms) | Open | High | Low | Close"

def test_coingecko_opening_price():
    c = CoinGecko()
    opening = c.get_opening_price("ethereum", "usd", 7)
    assert 41 <= len(opening) <= 43, "CoinGecko opening price should be between 41 and 43 entries for 7 day range"

def test_coingecko_market_range():
    c = CoinGecko()
    mrange = c.get_market_range("ethereum", "usd", 1)
    assert type(mrange) is dict, "CoinGecko should have returned a dictionary"
    assert list(mrange.keys()) == ['prices', 'market_caps', 'total_volumes'], "Invalid market range returned by CoinGecko"
