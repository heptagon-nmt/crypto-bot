from datetime import datetime
from get_data import *
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas as pd

def convert_timestamp(timestamp):
    val = timestamp["Date"]
    return datetime.utcfromtimestamp(val / 1000)

def array_to_dataframe(data):
    df = pd.DataFrame(data, columns = ["Date", "Open", "High", "Low", "Close"])
    df["Date"] = df.apply(convert_timestamp, axis = 1)
    df = df.set_index("Date")
    return df

def plot_and_save_price_graph(data, filename, file_extension):
	assert file_extension in ["pdf", "png", "jpg"], "Supported file extensions are pdf, png and jpg"
	assert type(filename) is str
	assert type(file_extension) is str
	assert type(data) is list
	plt.plot([a for a in range(len(data))], data, "-b.")
	plt.xlabel("USD price")
	plt.ylabel("Time index")
	plt.savefig("figures/"+filename+"."+file_extension)
	plt.close()
	return None

if __name__ == "__main__":
    data = get_ohlc_coingecko("litecoin", "usd", 90)
    df = array_to_dataframe(data)
    mpf.plot(df, type = "candle", style = "mike", mav = [5], tight_layout = True)

