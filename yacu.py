"""
There are two objects avalible with the public api, although the user is
welcome to dive deeper.

The Coin object can be used to predict the future prices of a given coin.

The Source object represents a a data source that can be used for prediciton.
All avalible Sources can be found in the SOURCES variable.

The YacuError Exception will be raised and can be caught if an error occurs
while prediciting coins.
"""
import os
import sys
import src.crypto_util
import src.gui
import src.get_data
from dataclasses import dataclass
from typing import List

def gui() -> None:
    """
    Start the gui.
    """
    src.gui.start_gui()

def cli() -> None:
    """
    Start the cli
    """
    src.crypto_util.main()


class YacuError(Exception):
    """
    Used to manage errors with the Yacu prediciton system.
    """
    ...

@dataclass()
class _CoinDataClass():
    """
    Internal Protoclass for coins. It is advised to just use the Coin class.
    """
    name: str
    source: str
    days: int = 7
    model: str = "ridge"
    lags: int = 300

class Coin(_CoinDataClass):
    """
    Represents a coin and its predicted values. After the object has been
    created, predicted prices will be avalible in the predicted_prices
    attribute.

    :arg name: The name of the coin.
    :arg source: The data source to train the AI. Can be 'cmc', 'kraken', or 'coingecko'.
    :arg days: The number of days you want to predict.
    :arg model: The learning model you want to use.
    :arg lags: The level of accuracy to use in the model.

    CALULATED DATA:
        Coin.predicted_prices --------- List of calculated prices.
    """
    def __init__(self, *args):
        """
        Uses the internals to find the pedicted values and then passes the rest
        to the data classes.
        """
        super().__init__(*args)
        try:
            self.predicted_prices = \
            src.crypto_util.main(['--crypto', str(self.name),
                                 '--model', str(self.model),
                                 '--source', str(self.source),
                                 '--days', str(self.days),
                                 '--lags', str(self.lags)])
            if (not isinstance(self.predicted_prices, list)):
                raise Exception("No predicted data returned.")
        except Exception as e:
            raise YacuError(f'Yacu could not predict the price of {self.name}'
                            f' due to the folowing error: {e}')

@dataclass()
class Source():
    """
    Represents a source of crypto data.
    """
    name: str

    def get_avalible_coins(self) -> List[str]:
        """
        Uses the internal get coin ids to generate a list of coin names.

        :returns: List of strings.
        """
        try:
            ret = src.get_data.get_available_symbols_from_source(self.name, True)
        except Exception as e:
            pass
        try:
            ret = src.get_data.get_available_symbols_from_source(self.name, False)
        except Exception as e:
            raise YacuError(f'Yacu could not generate a list of ids'
                            f' from {self.name}')
        return ret


SOURCES = [Source(x) for x in ["kraken", "coingecko"]]

if __name__ == "__main__":
    src.gui.start_gui()
