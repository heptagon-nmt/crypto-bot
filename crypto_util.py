from ML_predictor_backend import predict_next_N_timesteps
from get_data import *
from utils import *
import argparse

models = ["random_forest", "linear", "lasso", "gradient_boosting", "bagging", "ridge"]
sources = ["kraken", "coingecko", "cmc"]

def main():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument("--crypto", "-c", type=str, required=True, help="Symbol of the cryptocurrency")
	parser.add_argument("--days", "-d", type=int, required=False, help="Days in the future to predict. Default is 7")
	parser.add_argument("--ls", "-l", action="store_true", required=False, help="List all the cryptocurrencies available for an API source. If specified must also specify --source. If specified no other action will be taken. ")
	parser.add_argument("--model", "-m", type=str, required=False, help="Regression machine larning model to predict the price given historical data. Options are "+str(models)+" or all")
	parser.add_argument("--plot_historical", "-ph", action="store_true", required=False, help="Plot the past price data. Default True. File is written to figures/")
	parser.add_argument("--plot_prediction", "-pp", action="store_true", required=False, help="Plot the past data and predicted data. Default True. File is written to figures/")
	parser.add_argument("--filename", "-f", type=str, required=False, help="Filename (prefix) to save data to. Default is data")
	parser.add_argument("--filetype", "-ft", type=str, required=False, help="Image filetype to save data to. Must be either pdf png or jpg. Default is pdf")
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
	if (args.model not in models) and (args.model != None) and (args.model != "all"):
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
	if args.filename is None:
		args.filename = "data"
	if args.filetype is None:
		args.filetype = "pdf"
	if args.plot_historical is False:
		args.plot_historical = True
	if args.plot_prediction is False:
		args.plot_prediction = True

	# Get the data
	if args.source == "cmc":
		data = pull_CMC_scraper_data(args.crypto)
	elif args.source == "kraken":
		pass
	elif args.source == "coingecko":
		pass
	else:
		print("Data source not recognized, exiting")
		exit(1)
	if args.plot_historical == True:
		plot_and_save_price_graph(data, args.filename+"_"+args.crypto, args.filetype, args.crypto)
	print("\nNote that 'day 1' corresponds to the prediction of tomorrows prices of "+args.crypto+"\n")
	if args.model == "all":
		predictions_over_models = {}
		for model in models:
			prediction = predict_next_N_timesteps(data, args.lags, args.days, model)
			print("The predicted prices of "+args.crypto+" over the next "+str(args.days)+" days based on the "+model+" model are:\n")
			pairs = [tuple(prediction[i:i+2]) for i in range(0, len(prediction), 2)]
			for (index, p) in enumerate(pairs):
				print("Predicted Day "+str(index+1)+" price = "+str(p[0]))
			predictions_over_models[model] = prediction
			print("\n")
		if args.plot_prediction:
			plot_and_save_price_graph_with_predictions(data, args.filename+"_"+args.crypto, args.filetype, args.crypto, predictions_over_models)
	else:
		prediction = predict_next_N_timesteps(data, args.lags, args.days, args.model)
		print("The predicted prices of "+args.crypto+" over the next "+str(args.days)+" days based on the "+args.model+" model are:\n")
		for (index, p) in enumerate(prediction):
			print("Predicted Day "+str(index+1)+" price = "+str(p[0]))
		print("\n")
		if args.plot_prediction:
			plot_and_save_price_graph_with_predictions(data, args.filename+"_"+args.crypto, args.filetype, args.crypto, {args.model: prediction})
	return

if __name__ == "__main__":
	main()
