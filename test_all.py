"""
The unit test mechanism.
"""
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
	
	"""
	get_data module
	"""
	import get_data
	price_data = get_data.pull_CMC_scraper_data("BTC")
	assert type(price_data) is list
	
	#crypto_symbols_kraken = get_data.get_ids_kraken() This fails tests
	#assert type(crypto_symbols_kraken) is list
	#assert len(crypto_symbols_kraken) > 1
	
	crypto_symbols_coingecko = get_data.get_ids_coingecko()
	assert type(crypto_symbols_coingecko) is list
	assert len(crypto_symbols_coingecko) > 1
