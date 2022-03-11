[![Code Is Passing All Unit Tests?](https://github.com/1103s/crypto-bot/actions/workflows/python-app.yml/badge.svg)](https://github.com/1103s/crypto-bot/actions/workflows/python-app.yml) [![Documentation Is Generated?](https://github.com/1103s/crypto-bot/actions/workflows/gh-pages.yml/badge.svg)](https://github.com/1103s/crypto-bot/actions/workflows/gh-pages.yml) [![Publish To Docker](https://github.com/1103s/crypto-bot/actions/workflows/publish.yml/badge.svg)](https://github.com/1103s/crypto-bot/actions/workflows/publish.yml)

# Yet Another Crypto Util

Your one-stop shop for calculating crypto prices and predicting what they will
be using cutting edge machine learning. Works on Linux, macOS, and Windows.

## Install

Use:
`docker pull yetanothercryptoutil/yacu`
or
`podman pull yetanothercryptoutil/yacu`
to install.

## Usage

Run with:
`docker run yacu`
or
`podman run yacu`.

### Example Usage
- `podman run yacu --crypto ETH`: In this case the settings are set to default. However, the cryptocurrency you want to analyze needs to specified. 

- `podman run yacu --help` displays the usage and required arguments for the utility to work. 

## Documentation

Auto-maigcly generated documentation can be found
[here](https://1103s.github.io/crypto-bot/).

## Requirements

- docker or podman

## Data Sources

### Real-time data collection
- https://finance.yahoo.com

- https://www.coingecko.com/en/coins/

Coin ID reference in [here](./data/coingecko_id_list.json) and
[here](./data/kraken_pairs_list.json).

### Historical BTC/USD, ETH/USD, LTC/USD
Go to https://www.cryptodatadownload.com/data/gemini/ and download the minute 
CSVs. Then move the CSV files into the data folder and run train\_model.py 
(doesn't yet exist :) )

