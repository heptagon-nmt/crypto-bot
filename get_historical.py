"""
This employs the CoinGecko API to get historical data and save it for easy 
    access and analysis.
"""
import json
from tkinter import W
import requests
import time

url_prefix = "https://api.coingecko.com/api/v3/{}"

def get_ids():
    with open("coin_list.json", "r") as f:
        data = json.load(f)
    ids = [data[i]['id'] for i in range(len(data))]
    return ids

"""
    Data Granularity:
    5-minute intervals: 1 day from query time
    hourly data: 1-90 days from query time
    daily data: More than 90 days from query time
    Use unix time for start and end
"""
def get_range(coin_id, start, end):
    if is_valid_id(coin_id):
        start = int(start); end = int(end)
        range_str = "coins/{}/market_chart/range?vs_currency=usd&from={}&to={}"\
            .format(coin_id, start, end)
        url = url_prefix.format(range_str)
        print(url)
    #data = requests.get(url).json()
    #return data

# The coin ID list from CoinGecko returns whether it contains the coin_id
def is_valid_id(coin_id):
    ids = get_ids()
    return coin_id in ids

if __name__ == "__main__":
    get_range("ethereum", time.time() - 24 * 60 * 60, time.time())