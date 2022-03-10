from ML_predictor_backend import xgboost_forecast_single_step_predict
from get_data import pull_CMC_scraper_data
import argparse

models = ["xgboost", "random_forest", "linear"]
sources = ["kraken", "coingecko", "cmc"]

def main():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument("--crypto", "-c", type=str, required=False, help="Symbol of the cryptocurrency")
	parser.add_argument("--days", "-d", type=int, required=False, help="Days in the future to predict")
	parser.add_argument("--ls", "-l", action="store_true", required=False, help="List all the cryptocurrencies")
	parser.add_argument("--model", "-m", type=str, required=False, help="Model to use")
	parser.add_argument("--source", "-s", type=str, required=False, help="API source to use")
	args = parser.parse_args()

	# Check all arguments

	if args.ls:		# TODO: List all the cryptocurrencies
		exit(0)
	if args.model not in models:
		print("Invalid model. Options: {}".format(models))
		exit(1)
	if args.source not in sources:
		print("Invalid source. Options: {}".format(sources))
		exit(1)
	if args.crypto is None:
		print("Please specify a cryptocurrency")
		exit(1)
	if args.days is None:
		print("Please specify the number of days to predict")
		exit(1)
	if args.days < 1:
		print("Please specify a positive number of days to predict")
		exit(1)
	if args.model is None:
		args.model = "xgboost"		# Set default model
	if args.source is None:
		args.source = "kraken"		# Set default source


	
	# Get the data
	cryptocurrency = "ETH" if not args.crypto else args.crypto
	data = pull_CMC_scraper_data(cryptocurrency)
	next_day_prediction = xgboost_forecast_single_step_predict(data)
	print("The next predicted price of "+cryptocurrency+" is", next_day_prediction)
	return

if __name__ == "__main__":
	main()
