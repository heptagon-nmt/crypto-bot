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

@dataclass()
class Coin():
    """
    Use this to make you crypto bot!
    """
    name: str
    source: str
    days: int = 7
    model: str = "all"
    lags: int = 300

if __name__ == "__main__":
    src.crypto_util.main()
