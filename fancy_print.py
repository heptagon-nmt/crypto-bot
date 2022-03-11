"""
Utilities to print fancy intros becasue we are a very serious development group
and need to have a serious cli.
"""
import art

def print_motd() -> None:
    """
    Prints the motd with random asci art.
    """
    print(art.text2art("Yet Another Crypto Util", "random"))
