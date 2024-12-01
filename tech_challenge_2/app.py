import sys
import os

# Add the parent directory to the path so we can import the coins module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from coins import get_coins


def main():
    get_coins = get_coins()
    print(get_coins)
