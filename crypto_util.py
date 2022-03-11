from ML_predictor_backend import predict_next_N_timesteps
from get_data import *
from utils import *
import argparse
import ast

models = ["random_forest", "linear", "lasso", "gradient_boosting", "bagging", "ridge"]
sources = ["kraken", "coingecko", "cmc"]

def main():
	parser = argparse.ArgumentParser(description="Command Line Cryptocurrency price prediction utility")
	parser.add_argument("--crypto", "-c", type=str, required=False, help="Symbol of the cryptocurrency. Required unless --ls is called")
	parser.add_argument("--days", "-d", type=int, required=False, help="Days in the future to predict. Default is 7")
	parser.add_argument("--ls", "-l", action="store_true", required=False, help="List all the cryptocurrencies available for an API source. If specified must also specify --source. If specified no other action will be taken. ")
	parser.add_argument("--model", "-m", type=str, required=False, help="Regression machine larning model to predict the price given historical data. Options are "+str(models)+" or all. Default is all")
	parser.add_argument("--plot_data", "-p", type=str, required=False, help="Plot the past data and predicted data. Options are True and False. Default is True. File is written to figures/")
	parser.add_argument("--filename", "-f", type=str, required=False, help="Filename (prefix) to save data to. Default is data")
	parser.add_argument("--filetype", "-ft", type=str, required=False, help="Image filetype to save data to. Must be either pdf png or jpg. Default is pdf")
	parser.add_argument("--source", "-s", type=str, required=False, help="API source to use. Options are "+str(sources)+". Default is CMC scraper")
	parser.add_argument("--lags", type=int, required=False, help="Model hyperparamater for training the specified --model. Defaults to 300. Larger lag values requires more training time, and also typically results in higher accuracy. ")
	parser.add_argument("--csv", action="store_true", help="Outputs prediction data to a csv in the `data/` directory to a file called `data_out.csv`")
	args = parser.parse_args()

	print_motd()

	# Check all arguments
	if args.source not in sources and args.source != None:
		print("Invalid source. Options: {}".format(sources))
		exit(1)
	if args.ls:
		if args.source is None:
			print("Querying available cryptocurrency symbols requires --source flag to be specified. Exiting")
			exit(1)
		print("\nFor the data source "+args.source+", the available cryptocurrency symbols you can query are:\n\n")
		print(get_available_symbols_from_source(args.source))
		exit(0)
	if args.crypto is None:
		print("Cryptocurrency symbol required. Specify using --crypto")
		exit(1)
	if args.lags is None:
		args.lags = 300
	if (args.model not in models) and (args.model != None) and (args.model != "all"):
		print("Invalid model. Options: {}".format(models))
		exit(1)
	if args.model is None:
		args.model = "all"
	if args.crypto is None:
		print("Please specify a cryptocurrency")
		exit(1)
	if args.days is None:
		args.days = 7
	if args.days < 1:
		print("Please specify a positive number of days to predict")
		exit(1)
	if args.days > 14:
		print("\nNOTE typicaly these machine learning models will have higher accuracy for more near term predictions\n")
	if args.source is None:
		args.source = "cmc"		# Set default source
	if args.filename is None:
		args.filename = "data"
	if args.filetype is None:
		args.filetype = "pdf"
	if args.plot_data is None:
		args.plot_data = True
	if args.plot_data not in ["True", "False", True]:
		print("plot_data argument must be either True or False. ")
		exit(1)
	if type(args.plot_data) is str:
		args.plot_data = ast.literal_eval(args.plot_data)

	# Get the data
	if args.source == "cmc":
		data = pull_CMC_scraper_data(args.crypto)
	elif args.source == "kraken":
		get_opening_price_kraken(args.crypto, "USD", 10000)
	elif args.source == "coingecko":
		data = get_opening_price_coingecko(args.crypto, "USD", 10000)
	else:
		print("Source not recognized, exiting")
		exit(1)
	if args.plot_data:
		plot_and_save_price_graph(data, args.filename+"_"+args.crypto, args.filetype, args.crypto)
	print("\nNote that 'day 1' corresponds to the prediction of tomorrows prices of "+args.crypto+"\n")
	if args.model == "all":
		predictions_over_models = {}
		for model in models:
			prediction = predict_next_N_timesteps(data, args.lags, args.days, model)
			print("The predicted prices of "+args.crypto+" over the next "+str(args.days)+" days based on the "+model+" model are:\n")
			for (index, p) in enumerate(prediction):
				print("Predicted Day "+str(index+1)+" price = "+str(p))
			predictions_over_models[model] = prediction
			print("\n")
		if args.plot_data:
			plot_and_save_price_graph_with_predictions(data, args.filename+"_"+args.crypto, args.filetype, args.crypto, predictions_over_models)
		print_summary_statistics_of_predicted_prices(predictions_over_models)
		if(args.csv):
			export.export_csv(predictions_over_models)
	else:
		prediction = predict_next_N_timesteps(data, args.lags, args.days, args.model)
		print("The predicted prices of "+args.crypto+" over the next "+str(args.days)+" days based on the "+args.model+" model are:\n")
		for (index, p) in enumerate(prediction):
			print("Predicted Day "+str(index+1)+" price = "+str(p))
		print("\n")
		if args.plot_data:
			plot_and_save_price_graph_with_predictions(data, args.filename+"_"+args.crypto, args.filetype, args.crypto, {args.model: prediction})
		if(args.csv):
			export.export_csv({args.model: prediction})
	return

if __name__ == "__main__":
	main()
