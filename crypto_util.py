from ML_predictor_backend import xgboost_forecast_single_step_predict, predict_next_N_timesteps
from get_data import *
from utils import *
import argparse

models = ["xgboost", "random_forest", "linear", "lasso", "gradient_boosting", "bagging", "ridge"]
sources = ["kraken", "coingecko", "cmc"]

def main():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument("--crypto", "-c", type=str, required=True, help="Symbol of the cryptocurrency")
	parser.add_argument("--days", "-d", type=int, required=False, help="Days in the future to predict. Default is 7")
	parser.add_argument("--ls", "-l", action="store_true", required=False, help="List all the cryptocurrencies available for an API source. If specified must also specify --source. If specified no other action will be taken. ")
	parser.add_argument("--model", "-m", type=str, required=False, help="Regression machine larning model to predict the price given historical data. Options are "+str(models)+" or all")
	parser.add_argument("--plot_historical", "-ph", action="store_true", required=False, help="Plot the past price data. If specified then --filename and --filetype must also be specified. File is written to figures/")
	parser.add_argument("--plot_prediction", "-pp", action="store_true", required=False, help="Plot the past data and predicted data. If specified then --filename and --filetype must also be specified. File is written to figures/")
	parser.add_argument("--filename", "-f", type=str, required=False, help="Filename (prefix) to save data to. Default is data")
	parser.add_argument("--filetype", "-ft", type=str, required=False, help="Image filetype to save data to. Must be either pdf png or jpg. Default is jpg")
	parser.add_argument("--source", "-s", type=str, required=False, help="API source to use. Options are "+str(sources))
	parser.add_argument("--lags", "-lg", type=int, required=False, help="Model hyperparamater for training the specified --model. Defaults to 20")
	args = parser.parse_args()
	
	print_motd()

	# Check all arguments

	if args.ls:		# TODO: List all the cryptocurrencies
		if args.source is None:
			print("Querying available cryptocurrency symbols requires --source flag to be specified")
			exit(1)
		if args.source == "kraken":
			print(get_ids_kraken())
		elif args.source == "cmc":
			pass
		elif args.source == "coingecko":
			pass
		exit(0)
	if args.lags is None:
		args.lags = 20
	if args.model not in models and args.model != None:
		print("Invalid model. Options: {}".format(models))
		exit(1)
	if args.model is None:
		args.model = "all"
	if args.source not in sources and args.source != None:
		print("Invalid source. Options: {}".format(sources))
		exit(1)
	if args.crypto is None:
		print("Please specify a cryptocurrency")
		exit(1)
	if args.days is None:
		args.days = 7
	if args.days < 1:
		print("Please specify a positive number of days to predict")
		exit(1)
	if args.model is None:
		args.model = "xgboost"		# Set default model
	if args.source is None:
		args.source = "cmc"		# Set default source
	if args.plot_historical:
		if args.filename is None:
			args.filename = "data"
		if args.filetype is None:
			args.filetype = "jpg"

	# Get the data
	if args.source == "cmc":
		data = pull_CMC_scraper_data(args.crypto)
	elif args.source == "kraken":
		pass
	elif args.source == "coingecko":
		pass
	else:
		print("Source not recognized, exiting")
		exit(1)
	if args.plot_historical:
		plot_and_save_price_graph(data, "test", "pdf")
	if args.model == "xgboost":
		next_day_prediction = xgboost_forecast_single_step_predict(data)
		print("The next predicted price of "+args.crypto+" is", next_day_prediction)
	elif args.model == "all":
		pass
	else:
		prediction = predict_next_N_timesteps(data, args.lags, args.days*2, args.model)
		print("\nThe predicted prices of "+args.crypto+" over the next "+str(args.days*2)+" time steps (this corresponds to the predicted opening and closing prices over the next "+str(args.days)+" days):\n")
		print("Day 1 corresponds to the prediction of tomorrows prices of "+args.crypto+"\n")
		pairs = [tuple(prediction[i:i+2]) for i in range(0, len(prediction), 2)]
		for (index, p) in enumerate(pairs):
			print("Predicted Day "+str(index+1)+" Open price = "+str(p[0]))
			print("Predicted Day "+str(index+1)+" Close price = "+str(p[1]))
	return

if __name__ == "__main__":
	main()
