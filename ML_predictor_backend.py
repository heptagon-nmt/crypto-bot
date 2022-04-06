"""
Library code for the Machine Learning prediction backend
"""
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.linear_model import Ridge
from skforecast.model_selection import grid_search_forecaster
import numpy as np
import pandas as pd
import time

def predict_next_N_timesteps(data, model_name, **kwargs): 
	"""
	Forecasts price data given an input of historical price data, and a ML regression model to do the prediction. 

	:arg data: Input time-ordered historical price data to predict on
	:arg lags: Integer hyperparamater for the forecasting prediction
	:arg N: Integer number of time steps (days) in the future to predict the price
	:arg model_name: String machine learning model name. Corresponds to a sklearn regression algorithm. 
	:return: List of time-ordered price predictions. Exits if the specified model_name is not recognized. 
	:rtype: list
	"""
	params = {
		"lags" : len(data),
		"N" : 10,
		"n_estimators" : 200,
		"max_depth" : 1000,
		"max_iter" : 1000,
	}
	params.update(kwargs)
	data = list(data)
	assert type(data) is list, "price data must be a list"
	assert type(params["lags"]) is int, "lag parameter must be an integer"
	assert type(params["N"]) is int and params["N"] > 0, "Number of steps to predict into the future must be an integer"
	assert type(model_name) is str, "model name must be a string"
	if model_name == "random_forest":
		forecaster = ForecasterAutoreg(regressor = RandomForestRegressor(n_estimators=params["n_estimators"], max_depth=params["max_depth"]), lags = params["lags"])
	elif model_name == "linear":
		forecaster = ForecasterAutoreg(regressor = LinearRegression(), lags = params["lags"])
	elif model_name == "lasso":
		forecaster = ForecasterAutoreg(regressor = Lasso(max_iter=params["max_iter"]), lags = params["lags"])
	elif model_name == "gradient_boosting":
		forecaster = ForecasterAutoreg(regressor=GradientBoostingRegressor(n_estimators=params["n_estimators"], max_depth=params["max_depth"]), lags=params["lags"])
	elif model_name == "bagging":
		forecaster = ForecasterAutoreg(regressor=BaggingRegressor(n_estimators=params["n_estimators"]), lags=params["lags"])
	elif model_name == "ridge":
		forecaster = ForecasterAutoreg(regressor=Ridge(max_iter=params["max_iter"]), lags=params["lags"])
	else:
		print("model not recognized, exiting")
		exit(0)
	data_train = pd.Series(data)
	print("Training model "+str(model_name)+" ...")
	start = time.time()
	forecaster.fit(y=data_train)
	end = time.time()
	print("Total training time = "+str(round(end-start, 4))+" seconds")
	predictions = forecaster.predict(steps=params["N"])
	return list(predictions)
