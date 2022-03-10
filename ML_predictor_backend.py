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
from xgboost import XGBRegressor
import sys

def xgboost_forecast_single_step_predict(data):
	X = [i for i in range(len(data))]
	model = XGBRegressor(objective='reg:squarederror', n_estimators=1000)
	model.fit(np.vstack(np.array(X)), np.vstack(np.array(data)))
	yhat = model.predict(np.vstack(np.array([len(data)])))
	return list(yhat)[0]
def predict_next_N_timesteps(data, lags, N, model_name, random_state=10):
	assert type(data) is list, "price data must be a list"
	assert type(lags) is int, "lag parameter must be an integer"
	assert type(N) is int, "Number of steps to predict into the future must be an integer"
	assert type(model_name) is str, "model name must be a string"
	if model_name == "random_forest":
		forecaster = ForecasterAutoreg(regressor = RandomForestRegressor(), lags = lags)
	elif model_name == "linear":
		forecaster = ForecasterAutoreg(regressor = LinearRegression(), lags = lags)
	elif model_name == "lasso":
		forecaster = ForecasterAutoreg(regressor = Lasso(), lags = lags)
	elif model_name == "gradient_boosting":
		forecaster = ForecasterAutoreg(regressor=GradientBoostingRegressor(), lags=lags)
	elif model_name == "bagging":
		forecaster = ForecasterAutoreg(regressor=BaggingRegressor(), lags=lags)
	elif model_name == "ridge":
		forecaster = ForecasterAutoreg(regressor=Ridge(), lags=lags)
	else:
		print("model not recognized, exiting")
		sys.exit()
	data_train = pd.Series(data)
	forecaster.fit(y=data_train)
	predictions = forecaster.predict(steps=N)
	return list(predictions)
def parameter_gridsearch(data):
	assert type(data) is list, "price data must be a list"
	forecaster = ForecasterAutoreg(regressor = RandomForestRegressor())
	param_grid = {'n_estimators': [500], 'max_depth': [10]}
	lags_grid = [10, 20]
	results_grid = grid_search_forecaster(
			forecaster         = forecaster,
			y                  = data,
			param_grid         = param_grid,
			lags_grid          = lags_grid,
			steps              = 10,
			refit              = True,
			metric             = 'mean_squared_error',
			initial_train_size = int(len(data)*0.5),
			return_best        = True,
			verbose            = False
		)
	return results_grid
