"""
The unit test mechanism.
"""
import numpy as np

def test_default() -> None:
	"""
	The default tests to be run.
	"""

	"""
	ML prediction module
	"""
	import ML_predictor_backend as ML
	pred = ML.predict_next_N_timesteps([1, 2, 3, 4, 5, 6], 2, 4, "linear")
	assert type(pred) is list
	assert len(pred) == 4
	assert type(pred[0]) is float
	np.testing.assert_allclose(7, pred[0])
	np.testing.assert_allclose(8, pred[1])
	np.testing.assert_allclose(9, pred[2])
	np.testing.assert_allclose(10, pred[3])

	pred = ML.predict_next_N_timesteps([1, 2, 3, 4, 5, 6], 2, 4, "random_forest")
	assert type(pred) is list
	assert len(pred) == 4
	assert type(pred[0]) is float
	np.testing.assert_allclose(7, pred[0])
	np.testing.assert_allclose(8, pred[1])
	np.testing.assert_allclose(9, pred[2])
	np.testing.assert_allclose(10, pred[3])

	"""
	get_data module
	"""
	from get_data import CoinGecko, Kraken, pull_CMC_scraper_data
	price_data = pull_CMC_scraper_data("BTC")
	assert type(price_data) is list
	assert len(price_data) > 1

	cgi = CoinGecko()
	assert isinstance(cgi, CoinGecko)
	kraken = Kraken()
	assert isinstance(kraken, Kraken)

	
	"""
	utils module
	"""

