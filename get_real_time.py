# Request OHLC data from Coingecko every 30 minutes
from keras.models import Sequential
from keras import layers
from keras.utils import to_categorical
import json
import requests
import time


def get_data(symbol):
    r = requests.get("https://api.coingecko.com/api/v3/coins/{}/ohlc?vs_currency=usd&days=1".format(symbol))
    data = r.json()

def summarize(prediction):
    pass

# Return classifier with 
def get_classifier():
    classifier = Sequential()
    classifier.add(layers.Dense(100, "relu"))
    classifier.add(layers.Dense(50, "relu"))
    classifier.add(layers.Dense(2, "softmax"))
    return classifier

if __name__ == "__main__":
    data_list = []
    initial_time = time.time()
    classifier = get_classifier()
    while(True):
        data = get_data("ethereum")
        data_list.append(data[-1])
        time.sleep(30 * 60)
        prediction = classifier.predict(data_list[-1])
        summarize(prediction)
