from cryptocmd import CmcScraper
from sklearn.linear_model import LinearRegression
import ast
#from pmdarima import auto_arima
import matplotlib.pyplot as plt
import numpy as np

cryptocurrency = "XRP"

scraper = CmcScraper(cryptocurrency)
json_data = ast.literal_eval(scraper.get_data("json"))

json_data.reverse()

data = []
for a in json_data:
	data.append(a["Open"])
	data.append(a["Close"])

plt.plot([a for a in range(len(data))], data, "-b.")
plt.savefig("figures/"+cryptocurrency+".pdf")

latest_datapoint = data[-1]
del data[-1]

lr = LinearRegression()
lr.fit(np.array([a for a in range(len(data))]).reshape(-1, 1), data)
lr_score = lr.score(np.array([a for a in range(len(data))]).reshape(-1, 1), data)
print("Overall linear regression score:", lr_score)

# Predicitng on one datapoint
print("predicted datapoint: ", lr.predict(np.array([len(data)]).reshape(-1, 1)))

print("Real datapoint:", latest_datapoint)
