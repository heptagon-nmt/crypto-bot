from cryptocmd import CmcScraper
from sklearn.linear_model import LinearRegression
import ast
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

from skforecast.ForecasterAutoreg import ForecasterAutoreg
from skforecast.ForecasterAutoregCustom import ForecasterAutoregCustom
from skforecast.ForecasterAutoregMultiOutput import ForecasterAutoregMultiOutput
from skforecast.model_selection import grid_search_forecaster
from skforecast.model_selection import backtesting_forecaster
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.datasets import load_boston

def xgboost_forecast(data):
	X = [i for i in range(len(data))]
	model = XGBRegressor(objective='reg:squarederror', n_estimators=1000)
	model.fit(np.vstack(np.array(X)), np.vstack(np.array(data)))
	yhat = model.predict(np.vstack(np.array([len(data)])))
	return list(yhat)[0]

cryptocurrency = "ETH"

scraper = CmcScraper(cryptocurrency)
json_data = ast.literal_eval(scraper.get_data("json"))

json_data.reverse()

data = []
data_dict = {}
for a in json_data:
	data.append(a["Open"])
	data.append(a["Close"])

plt.plot([a for a in range(len(data))], data, "-b.")
plt.savefig("figures/"+cryptocurrency+".pdf")
plt.close()

steps = 10

data_train = data[:-steps]
data_test  = data[-steps:]
print(data_test)
out = xgboost_forecast(data_train)
print(out)

forecaster = ForecasterAutoreg(
                regressor = RandomForestRegressor(random_state=123),
                lags = 6
             )
print(len(data_train))
data_train = pd.Series(data_train)
forecaster.fit(y=data_train)
predictions = forecaster.predict(steps=10)
print(predictions)

param_grid = {'n_estimators': [500],
              'max_depth': [10]}

# Lags used as predictors
lags_grid = [10, 20]

results_grid = grid_search_forecaster(
                        forecaster         = forecaster,
                        y                  = data_train,
                        param_grid         = param_grid,
                        lags_grid          = lags_grid,
                        steps              = 10,
                        refit              = True,
                        metric             = 'mean_squared_error',
                        initial_train_size = int(len(data_train)*0.5),
                        return_best        = True,
                        verbose            = False
                   )

print(results_grid)
