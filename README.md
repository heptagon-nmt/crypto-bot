[![Code Is Passing All Unit Tests?](https://github.com/1103s/crypto-bot/actions/workflows/python-app.yml/badge.svg)](https://github.com/1103s/crypto-bot/actions/workflows/python-app.yml) [![Documentation Is Generated?](https://github.com/1103s/crypto-bot/actions/workflows/gh-pages.yml/badge.svg)](https://github.com/1103s/crypto-bot/actions/workflows/gh-pages.yml) [![Publish To Docker](https://github.com/1103s/crypto-bot/actions/workflows/publish.yml/badge.svg)](https://github.com/1103s/crypto-bot/actions/workflows/publish.yml)

# Crypto Util

Real time cryptocurrency price data gathering and future price prediction command line utility using machine learning regression. Cross platform capabilities on Linux, macOS, and Windows. 

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
- `podman run yacu --crypto ETH`: In this case the settings are set to default. However, the cryptocurrency you want to analyze is a required flag. 

- `podman run yacu --help` displays the usage and required arguments for the utility to work. 

## Documentation

Documentation can be found [here](https://1103s.github.io/crypto-bot/).

## Requirements

- docker or podman
