from ML_predictor_backend import xgboost_forecast_single_step_predict
from get_data import pull_CMC_scraper_data

def main():
	cryptocurrency = "ETH"
	data = pull_CMC_scraper_data(cryptocurrency)
	next_day_prediction = xgboost_forecast_single_step_predict(data)
	print("The next predicted price of "+cryptocurrency+" is", next_day_prediction)
	return

if __name__ == "__main__":
	main()
