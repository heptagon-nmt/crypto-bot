"""
Utility module for plotting and printing information
"""

import matplotlib.pyplot as plt
import pandas as pd
import art
import random
import numpy as np

def print_motd() -> None:
    """
    Prints the motd with asci art.
    :return: None
    """
    print(art.text2art("Crypto Util", "cybermedum"))

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
	print("Figure of historical price data has been written to "+"figures/"+filename+"."+file_extension)
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
def print_summary_statistics_of_predicted_prices(predictions_for_different_models):
	"""
	Prints summary statistics for the predicted daily prices across the ensemble of ML models
	:arg predictions_for_different_models: A dictionary where keys are ML model names and values are the predicted prices over time
	:return: None
	"""
	print("\n=== Model Ensemble Statistics ===")
	N = len(predictions_for_different_models[list(predictions_for_different_models.keys())[0]])
	for i in range(N):
		vector = []
		for k in predictions_for_different_models:
			vector.append(predictions_for_different_models[k][i])
		print("Day "+str(i+1)+" mean predicted price across all ML models is "+str(round(np.mean(vector), 4))+" USD with a standard deviation of "+str(round(np.std(vector), 4)))
	print("=================\n")
