import matplotlib.pyplot as plt

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
