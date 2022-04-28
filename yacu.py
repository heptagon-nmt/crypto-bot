"""
Top level file for the application.
"""
import os
import sys
import src.crypto_util
import src.gui
from dataclasses import dataclass

def gui():
    """
    Start the gui.
    """
    src.gui.start_gui()

def cli():
    """
    Start the cli
    """
    src.crypto_util.main()


class YacuError(Exception):
    """
    Ued to manage errors with the Yacu prediciton system.
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
    Represents a coin and its predicted values.
    """
    def __init__(self, **args):
        """
        Uses the internals to find the pedicted values and then passes the rest
        to the data classes.
        """
        super().__init__(**args)
        try:
            self.predicted_prices = \
            src.crypto_util.main(f'--crypto {self.name}'
                                 f' --model {self.model}'
                                 f' --source {self.source}'
                                 f' --days {self.days}'
                                 f' --lags {self.lags}')
            if (not isinstance(self.predicted_prices, list)):
                raise Exception("No predicted data returned.")
        except Exception as e:
            raise YacuError(f'Yacu could not predict the price of {self.name}'
                            f' due to the folowing error: {e}')

if __name__ == "__main__":
    src.crypto_util.main()
