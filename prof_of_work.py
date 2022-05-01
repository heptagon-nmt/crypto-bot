"""
A simple tool that generates a report on how accurate the yacu prediction tool
is.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as pat
import numpy as np
import src.get_data
import yacu
import time
from pathlib import Path
import pickle

MODELS = ['random_forest', 'linear',
          'lasso', 'gradient_boosting', 'bagging', 'ridge']

def run_sim(days: int,
        coin_name: str) -> tuple[list[float], dict[str, list[float]]]:
    """
    Actualy performs the prediction.

    :args days: The number of days to sim for.
    :args coin_name: the kraken coin id.
    :return: A touple with the (real, predicted) data.
    """
    now = time.time()
    print(f'TIME ACTUAL: {now}')
    kraken_api = src.get_data.Kraken()
    real_prices = kraken_api.get_opening_price(coin_name, "USD", days, 1)
    # Now, wihtout further aduo, it is TIME for some shenanigans.
    time_delta = days * 86400
    old_time = time.time
    time.time = lambda : old_time() - time_delta; print('TIME SIMULATED!')
    theoretic_prices = {}
    for m in MODELS:
        theoretic_prices[m] = yacu.Coin(coin_name,
                "kraken", days, m).predicted_prices
    return (real_prices, theoretic_prices)

def plot_comp_chart(real: np.ndarray,
        predicted: np.ndarray, prediction_type: str) -> None:
    """
    Takes two lists and plots them with header and all, then saves them as
    'comp_{prediction_type}.png

    :args real: The actual data.
    :args predicted: The predicted values.
    :args predicted_prices: The model styles.
    """
    days = list(range(len(predicted)))
    fig, ax = plt.subplots()
    if (len(real) > len(days)):
        real = real[:len(days)]
    plt.plot(days, np.ndarray.flatten(real),'ro',
            days, predicted, 'bo')
    plt.xlabel("Days")
    plt.ylabel("Market Price (USD)")
    plt.title(f'Accuracy of {prediction_type}.')
    real_patch = pat.Patch(color='red', label='Actual Market Price.')
    predicted_patch = pat.Patch(color='blue', label='YACU Predicted Price.')
    ax.legend(handles=[real_patch, predicted_patch])
    plt.savefig(Path(f'./comp_{prediction_type}.png'))


if __name__ == "__main__":
    try:
        with open(Path("./cache_real.pickle"), 'rb') as f:
            real = pickle.load(f)
        with open(Path("./cache_predicted.pickle"), 'rb') as f:
            predicted = pickle.load(f)
    except Exception as e:
        real, predicted = run_sim(7, 'BTC')
        with open(Path("./cache_real.pickle"), 'wb') as f:
            pickle.dump(real, f)
        with open(Path("./cache_predicted.pickle"), 'wb') as f:
            pickle.dump(predicted, f)
    for name, data in predicted.items():
        plot_comp_chart(real, data, name)
