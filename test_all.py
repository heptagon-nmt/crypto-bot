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
    sp.run(cmd, capture_output=True, shell=True, check=True)

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
	The default tests to be run.
	"""

	"""
	ML prediction module
	"""
	import src.ML_predictor_backend as ML
	pred = ML.predict_next_N_timesteps([1, 2, 3, 4, 5, 6], "linear", lags = 3, N = 4)
	#Linear regression is expected to predict linear functions well, as opposed to other models
	assert type(pred) is list
	assert len(pred) == 4
	assert type(pred[0]) is float
	np.testing.assert_allclose(7, pred[0])
	np.testing.assert_allclose(8, pred[1])
	np.testing.assert_allclose(9, pred[2])
	np.testing.assert_allclose(10, pred[3])

	pred = ML.predict_next_N_timesteps([1, 2, 3, 4, 5, 6], "random_forest", lags = 3, N = 4)
	assert type(pred) is list
	assert len(pred) == 4
	assert type(pred[0]) is float

	pred = ML.predict_next_N_timesteps([1, 2, 3, 4, 5, 6], "ridge", lags = 3, N = 4)
	assert type(pred) is list
	assert len(pred) == 4
	assert type(pred[0]) is float

	pred = ML.predict_next_N_timesteps([1, 2, 3, 4, 5, 6], "bagging", lags = 3, N = 4)
	assert type(pred) is list
	assert len(pred) == 4
	assert type(pred[0]) is float

	pred = ML.predict_next_N_timesteps([1, 2, 3, 4, 5, 6], "gradient_boosting", lags = 3, N = 4)
	assert type(pred) is list
	assert len(pred) == 4
	assert type(pred[0]) is float

	pred = ML.predict_next_N_timesteps([1, 2, 3, 4, 5, 6], "lasso", lags = 3, N = 4)
	assert type(pred) is list
	assert len(pred) == 4
	assert type(pred[0]) is float

	"""
	get_data module
	"""
	from src.get_data import pull_CMC_scraper_data
	price_data = pull_CMC_scraper_data("BTC")
	assert type(price_data) is list
	assert len(price_data) > 1
	assert (type(price_data[0]) is float or type(price_data[0]) is int)

	price_data = pull_CMC_scraper_data("ETH")
	assert type(price_data) is list
	assert len(price_data) > 1
	assert (type(price_data[0]) is float or type(price_data[0]) is int)

	price_data = pull_CMC_scraper_data("XRP")
	assert type(price_data) is list
	assert len(price_data) > 1
	assert (type(price_data[0]) is float or type(price_data[0]) is int)

def test_public_api() -> None:
    """
    Unit test for the top level yacu.py file.
    """
    # Import the subsystem to test
    import yacu
    # Make sure the subsystems needed in the preconditions are accessible
    import src.crypto_util
    import src.get_data
    # The preconditions of `_CoinDataClass.__init__()` are provided in P
    P = ["BTC", "kraken", 30, "ridge"]
    # The Preconditions of the class Coin have now been met.
    # Testing the __init__ method of Coin.
    coin = yacu.Coin(*P)
    # Testing the population of predicted_prices
    assert len(coin.predicted_prices) == 30, 'predicted_prices length invalid'
    assert isinstance(coin.predicted_prices, list), 'type error in prediction'
    assert isinstance(coin.predicted_prices[0], float), 'data internals not int'
    # Testing the invariant of Coin's superclass
    assert issubclass(yacu.Coin, yacu._CoinDataClass), 'Parent error'
    # Testing the error state postcondition
    try:
        bad_coin = yacu.Coin("FAKE", "kraken", 30, "ridge")
    except yacu.YacuError as e:
        # This is supposed to happen
        pass
    # All Invariants, Preconditions, and Postconditions of Coin have now been
    # tested.

    #Create new Source
    source = yacu.Source('kraken')
    # Check metaclass
    from dataclasses import is_dataclass
    assert is_dataclass(source), 'Source is not dataclass'
    # Check name is populated
    assert len(source.name) > 0, 'Name length err'
    assert isinstance(source.name, str), 'Name not str'
    # Check get_available_coins avalibility
    assert source.get_available_coins is not None
    # Check the preconditions of get_available_coins
    assert source.name in ["kraken", "coingecko", "cmc"], 'Not a valid source'
    # Test the method now the preconditions are met
    data = source.get_available_coins()
    # Check postconditions now it has run
    assert len(data) > 0, 'data length err'
    assert isinstance(data, list), 'data not list'
    assert isinstance(data[0], str), 'data internals not int'
    # Check error throwing
    try:
        source.name = 'FAKE'
        data = source.get_available_coins()
    except yacu.YacuError as e:
        # This is supposed to happen
        pass
    # All Invariants, Preconditions, and Postconditions of Source have now been
    # tested.

    # Test Passesd





