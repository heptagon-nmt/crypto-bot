"""
from tkinter import W
from keras.models import Sequential
from keras import layers
from keras.utils import to_categorical
import calendar
import datetime
import numpy as np
import os
import pandas as pd
import sys

# Global hyperparameters for the neural network
EPOCHS = 5
BATCH_SIZE = 20

# Global column selection parameter
cols = ["Open", "High", "Low", "Close", "Volume", "Time"]
ohlc = ["Open", "High", "Low", "Close"]

#   Temporarily store the CSV file in the data/ folder for training. The most 
# current data can be downloaded from 
# https://www.cryptodatadownload.com/data/gemini/. 
# Get 2022_1minute data for BTC/ETH/LTC/XRP.
#   Note: apparently, there are holes in the Gemini 2022_1minute data, so you 
# should also download 1minute from FTX, which can be used to patch the Gemini
# datasets. 
def load_data(filename):
    # Check if the file exists
    if not os.path.isfile(os.path.join("data/", filename)):
        print("{} not found. Exiting".format(filename))
        sys.exit(1)
    with open(os.path.join("data/", filename), "r") as f:
        data = pd.read_csv(f)
    return data

#   Pull the data from both Gemini and FTX for specified symbol, then combine 
# missing entries.
def get_patched_data(gemini, FTX):
    columns = ["Unix Timestamp", "Date", "Symbol", "Open", "High", "Low", "Close", "Volume"]
    df1 = load_data(gemini)[::-1]
    df2 = load_data(FTX)[::-1]
    start, end = int(df1["Unix Timestamp"][:1]), int(df1["Unix Timestamp"][-1:])
    all_timestamps = pd.DataFrame({"Unix Timestamp" : [start + 60000 * i for i in range(int((end - start) / 60000) + 1)]})
    missing_timestamps = np.array(all_timestamps[~all_timestamps["Unix Timestamp"].isin(df1["Unix Timestamp"])].dropna())
    df2 = df2[df2["Unix Timestamp"].isin(missing_timestamps.flatten())][columns]
    return pd.concat([df1, df2]).sort_values("Unix Timestamp")

# Return a DataFrame column containing the 24-hour time values in minutes divided by 1440
def modify_date(row):
    split = row["Date"].split()[1].split(":")
    return (60 * int(split[0]) + int(split[1])) / 1440

#  TODO Convert 1-minute OHLC to 30-minute OHLC

#   Write function to format the data to be fed to the network. 
# Takes the dataframe and returns an ordered pair of the inputs with the 
# corresponding labels. The shape of the output labels needs to be considered
# when writing get_classifier (e.g. if the actual output is a single boolean output, 
# then the last layer needs to have one unit)
#   Example function: Takes the pandas dataframe, calculates the percent change 
# of the OHLC between each thirty minute interval, then partitions the resulting
# numpy matrix into frames with a specified frame size. In this example, the labels
# simply indicate whether the next. THIS IS REALLY FUCKING SLOW CURRENTLY
def create_inputs_and_labels(df, lag = 30, frame_size = 10):
    df["Time"] = df.apply(modify_date, axis = 1)
    percent_change = get_ohlc_lag(df, lag)
    percent_change["Time"] = df["Time"][lag:]
    if frame_size > len(percent_change):
        print("Frame size is too large.")
        sys.exit(1)
    inputs = np.array(percent_change[0 : frame_size])
    labels = np.array(percent_change[ohlc][frame_size : frame_size + 1]) \
                    >= np.array(percent_change[ohlc][frame_size - 1 : frame_size])
    for i in range(1, len(percent_change) - frame_size - 1):
        inputs = np.concatenate((inputs, np.array(percent_change[i : frame_size + i])))
        labels = np.concatenate((labels, np.array(percent_change[ohlc][frame_size + i: frame_size + i + 1]) \
                    >= np.array(percent_change[ohlc][frame_size + i - 1 : frame_size + i])))
        print(i)
    return inputs, labels

#   Return the percent change of the OHLC data from minute k to minute k + n
# as a pandas dataframe
def get_ohlc_lag(df, n):
    return df[ohlc][n:] / df[ohlc][0 : -n].values - 1

def get_test_data():
    data = np.fromfile("data/test_inputs.bin")
    data.reshape(data.shape[0] // 50, 50)
    print(data.shape)
    labels = np.fromfile("data/test_labels.bin")
    print(labels.shape)
    return data, labels

#   This function converts the OHLC price data into percent changes with 
# specified time intervals. If you have k price points then you'll get k-1
# percent changes. Since the first entry in the CSV is the most current price
# available, the dataframe must be reversed before processing.
def percent_change(df, lag):
    rev = df[::-1]
    delta = np.array(rev[ohlc][1:]) / np.array(rev[cols][0 : -1]) - 1

# Classifier architecture specification
# Keras documentation: https://keras.io/getting_started/intro_to_keras_for_engineers/
### Example function
def get_classifier():
    classifier = Sequential()
    classifier.add(layers.Dense(20, activation = "sigmoid"))
    classifier.add(layers.Dense(4, activation = "sigmoid"))
    classifier.compile(optimizer = "sgd", loss = "mse", metrics = ["accuracy"])
    return classifier

if __name__ == "__main__":
    classifier = get_classifier()
    #gemini = "gemini_BTCUSD_2022_1min.csv"
    FTX = "FTX_BTCUSD_minute.csv"
    #df = get_patched_data(gemini, FTX)
    #data, labels = create_inputs_and_labels(df)
    data, labels = get_test_data()
    classifier.fit(data, labels, batch_size = BATCH_SIZE, epochs = EPOCHS)
"""
