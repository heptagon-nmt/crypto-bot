"""
The unit test mechanism.
"""
import time
import get_data as gd

assert len(gd.get_ids()) > 0, "Id list is malformed"
#import get_historical as gh

import ML_predictor_backend as ML

pred = ML.predict_next_N_timesteps([1, 2, 3, 4, 5, 6], 2, 4)
assert type(pred) is list
assert len(pred) == 4
assert type(pred[0]) is float

"""
assert len(gh.get_ids()) > 0, "Id list is malformed"
>>>>>>> 576e17a92083ac6ad30aa592e06ec601ba1dcfaf

assert gd.get_market_range(gd.get_ids()[0], time.time(),
        time.time() - 60 * 60 * 24 * 5) is dict, "Query does not return json"

assert gd.is_valid_id_coingecko("    ") is False, "Invalid id was found"

assert gd.is_valid_id_kraken(gd.get_ids()[0]) is True, "Valid id was not found"

from skforecast.model_selection import grid_search_forecaster
import ML_predictor_backend as ml

assert isinstance(ml.parameter_gridsearch,
        grid_search_forecaster), "Something is wrong?"
"""
