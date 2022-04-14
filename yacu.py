"""
Top level file for the application.
"""
import os
import sys
import src.crypto_util
import src.gui

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

