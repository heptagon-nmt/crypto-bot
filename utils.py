from datetime import datetime
from get_data import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import art
import random

def print_motd() -> None:
    """
    Prints the motd with random asci art.
    """
    print(art.text2art("Yet Another Crypto Util", "cybermedum"))
def convert_timestamp(timestamp):
    val = timestamp["Date"]
    return datetime.utcfromtimestamp(val / 1000)

def array_to_dataframe(data):
    df = pd.DataFrame(data, columns = ["Date", "Open", "High", "Low", "Close"])
    df["Date"] = df.apply(convert_timestamp, axis = 1)
    df = df.set_index("Date")
    return df

def plot_and_save_price_graph(data, filename, file_extension, crypto):
	assert file_extension in ["pdf", "png", "jpg"], "Supported file extensions are pdf, png and jpg"
	assert type(filename) is str
	assert type(file_extension) is str
	assert type(data) is list
	assert type(crypto) is str
	plt.plot([a for a in range(len(data))], data, "-b.", label=crypto)
	fig = plt.gcf()
	fig.set_size_inches(12, 8)
	plt.ylabel("USD price")
	plt.xlabel("Time index")
	plt.legend()
	plt.savefig("figures/"+filename+"."+file_extension)
	plt.close()
	print("Figure of price data has been written to "+"figures/"+filename+"."+file_extension)
	return None

def plot_and_save_price_graph_with_predictions(data, filename, file_extension, crypto, predictions):
	assert file_extension in ["pdf", "png", "jpg"], "Supported file extensions are pdf, png and jpg"
	assert type(filename) is str
	assert type(file_extension) is str
	assert type(data) is list
	assert type(crypto) is str
	assert type(predictions) is dict
	truncate_data = 50
	data = data[-truncate_data:]
	plt.plot([a for a in range(len(data))], data, "-b.", label=crypto)
	fig = plt.gcf()
	fig.set_size_inches(12, 8)
	plt.ylabel("USD price")
	plt.xlabel("Time index")
	for k in predictions:
		plt.plot([i+len(data) for i in range(len(predictions[k]))], predictions[k], color=(random.randint(1, 255)/255.0, random.randint(1, 255)/255.0, random.randint(1, 255)/255.0), marker="^", label=k)
	plt.legend()
	plt.savefig("figures/"+filename+"_prediction."+file_extension)
	plt.close()
	print("Figure of (truncated) price data for the last 50 days with predictions has been written to "+"figures/"+filename+"_prediction."+file_extension)
	return None

