"""
The unit test mechanism.
"""
import numpy as np
import subprocess as sp

DO_DETAIL = False

def run(cmd):
    """
    A more detailed test.
    """
    if (not DO_DETAIL):
        return
    sp.    run(cmd, capture_output=True, shell=True, check=True)

def test_help():
    run("python3 crypto_util.py -h")


def test_list_kraken():
    run("python3 crypto_util.py --source kraken --ls")


def test_list_coingecko():
    run("python3 crypto_util.py --source coingecko --ls")


def test_list_cms():
    run("python3 crypto_util.py --source cmc --ls")


def test_predict_kraken():
    run("python3 crypto_util.py --source kraken -c USD -d 10")


def test_predict_coingecko():
    run("python3 crypto_util.py --source coingecko -c zeon -d 10")


def test_predict_cmc():
    run("python3 crypto_util.py --source cmc -c BTC -d 10")


def test_csv():
    run("python3 crypto_util.py --source coingecko -c zeon --csv")


def test_no_plot():
    run("python3 crypto_util.py --source coingecko -c zeon -p False")


def test_file_name():
    run("python3 crypto_util.py --source coingecko -c zeon -f test")


def test_file_png():
    run("python3 crypto_util.py --source coingecko -c zeon -f test -ft png")


def test_file_jpg():
    run("python3 crypto_util.py --source coingecko -c zeon -f test -ft jpg")


def test_lags():
    run("python3 crypto_util.py --source coingecko -c zeon --lags 100")

def test_default() -> None:
	"""
	The default tests to be     run.
	"""

	"""
	ML prediction module
	"""
	import ML_predictor_backend as ML
	pred = ML.predict_next_N_timesteps([1, 2, 3, 4, 5, 6], 3, 4, "linear")
	#Linear regression is expected to predict linear functions well, as opposed to other models
	assert type(pred) is list
	assert len(pred) == 4
	assert type(pred[0]) is float
	np.testing.assert_allclose(7, pred[0])
	np.testing.assert_allclose(8, pred[1])
	np.testing.assert_allclose(9, pred[2])
	np.testing.assert_allclose(10, pred[3])

	pred = ML.predict_next_N_timesteps([1, 2, 3, 4, 5, 6], 3, 4, "random_forest")
	assert type(pred) is list
	assert len(pred) == 4
	assert type(pred[0]) is float

	pred = ML.predict_next_N_timesteps([1, 2, 3, 4, 5, 6], 3, 4, "ridge")
	assert type(pred) is list
	assert len(pred) == 4
	assert type(pred[0]) is float

	pred = ML.predict_next_N_timesteps([1, 2, 3, 4, 5, 6], 3, 4, "bagging")
	assert type(pred) is list
	assert len(pred) == 4
	assert type(pred[0]) is float

	pred = ML.predict_next_N_timesteps([1, 2, 3, 4, 5, 6], 3, 4, "gradient_boosting")
	assert type(pred) is list
	assert len(pred) == 4
	assert type(pred[0]) is float

	pred = ML.predict_next_N_timesteps([1, 2, 3, 4, 5, 6], 3, 4, "lasso")
	assert type(pred) is list
	assert len(pred) == 4
	assert type(pred[0]) is float


	"""
	get_data module
	"""
	from get_data import CoinGecko, Kraken, pull_CMC_scraper_data
	price_data = pull_CMC_scraper_data("BTC")
	assert type(price_data) is list
	assert len(price_data) > 1
	price_data = get_data.pull_CMC_scraper_data("ETH")
	assert type(price_data) is list
	assert len(price_data) > 1

	cgi = CoinGecko()
	assert isinstance(cgi, CoinGecko)
	kraken = Kraken()
	assert isinstance(kraken, Kraken)

	
	"""
	utils module
	"""

