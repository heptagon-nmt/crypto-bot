"""
The unit test mechanism.
"""
import time
#import get_historical as gh

import ML_predictor_backend as ML

ML.predict_next_N_timesteps([1, 2, 3, 4, 5, 6], 2, 4)

"""
assert len(gh.get_ids()) > 0, "Id list is malformed"

assert gh.get_market_range(gh.get_ids()[0], time.time(),
        time.time() - 60 * 60 * 24 * 5) is dict, "Query does not return json"

assert gh.is_valid_id("    ") is False, "Invalid id was found"

assert gh.is_valid_id(gh.get_ids()[0]) is True, "Valid id was not found"

assert gh.get_n_days(gh.get_ids()[0], 1) is dict, "Query does not return json"

import get_real_time as gr
from keras.models import Sequential

assert gr.get_data("ethereum") is dict, "Query does not return json"

assert isinstance(gr.get_classifier(), Sequential), "Something is wrong?"

from skforecast.model_selection import grid_search_forecaster
import ML_predictor_backend as ml

assert isinstance(ml.parameter_gridsearch,
        grid_search_forecaster), "Something is wrong?"
"""
