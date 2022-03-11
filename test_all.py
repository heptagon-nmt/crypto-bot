"""
The unit test mechanism.
"""
def test_default() -> None:
    """
    The default tests to be run.
    """
    import time
    #import get_data as gd
    #assert len(gd.get_ids()) > 0, "Id list is malformed"

    import ML_predictor_backend as ML
    pred = ML.predict_next_N_timesteps([1, 2, 3, 4, 5, 6], 2, 4, "linear")
    assert type(pred) is list
    assert len(pred) == 4
    assert type(pred[0]) is float
