"""
Library code for the Machine Learning prediction backend
"""
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

from skforecast.ForecasterAutoreg import ForecasterAutoreg
from skforecast.ForecasterAutoregCustom import ForecasterAutoregCustom
from skforecast.ForecasterAutoregMultiOutput import ForecasterAutoregMultiOutput
from skforecast.model_selection import grid_search_forecaster
from skforecast.model_selection import backtesting_forecaster
import numpy as np
import pandas as pd
from xgboost import XGBRegressor

def xgboost_forecast_single_step_predict(data):
	X = [i for i in range(len(data))]
	model = XGBRegressor(objective='reg:squarederror', n_estimators=1000)
	model.fit(np.vstack(np.array(X)), np.vstack(np.array(data)))
	yhat = model.predict(np.vstack(np.array([len(data)])))
	return list(yhat)[0]
def predict_next_N_timesteps(data, lags, N, random_state):
	assert type(data) is list, "price data must be a list"
	forecaster = ForecasterAutoreg(regressor = RandomForestRegressor(random_state=random_state), lags = lags)
	data_train = pd.Series(data)
	forecaster.fit(y=data_train)
	predictions = forecaster.predict(steps=N)
	return list(predictions)
def parameter_gridsearch(data):
	assert type(data) is list, "price data must be a list"
	forecaster = ForecasterAutoreg(regressor = RandomForestRegressor()
	param_grid = {'n_estimators': [500], 'max_depth': [10]}
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
	return results_grid

