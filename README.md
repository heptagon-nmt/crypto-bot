[![Code Is Passing All Unit Tests?](https://github.com/1103s/crypto-bot/actions/workflows/python-app.yml/badge.svg)](https://github.com/1103s/crypto-bot/actions/workflows/python-app.yml) [![Documentation Is Generated?](https://github.com/1103s/crypto-bot/actions/workflows/gh-pages.yml/badge.svg)](https://github.com/1103s/crypto-bot/actions/workflows/gh-pages.yml) [![Publish To Docker](https://github.com/1103s/crypto-bot/actions/workflows/publish.yml/badge.svg)](https://github.com/1103s/crypto-bot/actions/workflows/publish.yml) [![Publish To PyPi](https://github.com/1103s/crypto-bot/actions/workflows/publish-pypi.yml/badge.svg)](https://github.com/1103s/crypto-bot/actions/workflows/publish-pypi.yml)

# Crypto Util

Real time cryptocurrency price data prediction command line utility using machine learning regression. Cross platform compatible on Linux, macOS, and Windows. Written in Python 3. 

## Install

### Python
    
- `pip3 install yacu` or

- `python3 -m pip install yacu`

### Docker or Podman (CLI ONLY!)


- `docker pull yetanothercryptoutil/yacu` or

- `podman pull yetanothercryptoutil/yacu`

**NOTE:** If you use this method, only the CLI features of the program will be
available.

### Local installation via anaconda (for development)
- Download and install anaconda
- `git clone https://github.com/1103s/crypto-bot.git`
- `cd crypto-bot`
- `conda create --name crypto_util python=3.9.7`
- `source activate crypto_util`
- `python3 -m pip install -r requirements.txt`

## Usage

### GUI

- Default: `yacu`

- Anaconda: `python3 src/gui.py`

- Once installed via pip you will be able to initialize the GUI using the command `yacu` in the command line.
  - In some cases, such as in Linux Mint installations, this will fail. If the happens it means that `.bin` is not in your path (which you can check using `echo $PATH`). Therefore you need to add `.bin` to your path in order to fix this. 


### CLI

- Default: `yacu-cli`

- Podman: `podman run yacu`

- Docker: `docker run yacu`

- Anaconda: `python3 src/crypto_util.py`

#### Local command line usage

- `python3 crypto_util.py --crypto BTC`: The basic functionality requires the user to input at least the cryptocurrency symbol. Note that by default images of the data and predictions are saved to `figures/`
- `python3 crypto_util.py --crypto ETH --days 10 --lags 80`: More specific flags can be specified, such as the number of days into the future to predict the price.
- `python3 crypto_util.py --crypto ETH --days 50 --lags 400`: The larger `lags` is the longer the training time, but also the higher the accuracy will be. 
- `python3 crypto_util.py --ls --source kraken`: In order for the user to see what cryptocurrency symbols are available for an API source, the utility allows for this listing argument with no additional flags. 
- `python3 crypto_util.py --help`: Prints the usage instructions. 

#### Docker or podman

- `docker run yacu` or
- `podman run yacu`

### Example Docker or podman Usage
- `podman run yacu --crypto ETH`: In this case the settings are set to default. However, the cryptocurrency you want to analyze is a required flag. 

- `podman run yacu --help` displays the usage and required arguments for the utility to work. 

## Documentation

Documentation can be found [here](https://1103s.github.io/crypto-bot/).

## Requirements

- docker, podman, pip, or anaconda

## Installation problems
- On some Linus distributions the PySide6 import will throw an error like this: `ImportError: /lib/x86_64-linux-gnu/libc.so.6: version GLIBC_2.28 not found`
  - The fix for this is `sudo apt-get install libc6`


## TODOs

- Add method to save and load previously trained ML model files using the python library `pickle`.
- More color palettes for the MainWindow (variations of dark mode)
- Add moving averages toggling to graph
