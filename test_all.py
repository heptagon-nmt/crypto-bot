"""
The unit test mechanism.
"""
import time
import get_data as gd

assert len(gd.get_ids()) > 0, "Id list is malformed"

assert gd.get_market_range(gd.get_ids()[0], time.time(),
        time.time() - 60 * 60 * 24 * 5) is dict, "Query does not return json"

assert gd.is_valid_id_coingecko("    ") is False, "Invalid id was found"

assert gd.is_valid_id_kraken(gd.get_ids()[0]) is True, "Valid id was not found"

from skforecast.model_selection import grid_search_forecaster
import ML_predictor_backend as ml

assert isinstance(ml.parameter_gridsearch,
        grid_search_forecaster), "Something is wrong?"

