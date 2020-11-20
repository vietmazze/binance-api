import logging
import os
import datetime
import time

from binance.client import Client
from typing import Optional, Dict, Any, List
from colorprint import ColorPrint
from colorama import Fore, Back, Style, init


path = './keys.env'
load_dotenv(dotenv_path=path, verbose=True)

logging.basicConfig(level=logging.INFO, format=(
    Fore.BLUE + '[+] ' + Style.RESET_ALL + '%(message)s '))


class BinanceClient:
    def __init__(self) -> None:
        self._api_key = os.getenv('BINANCE_TEST_API')
        self._api_secret = os.getenv('BINANCE_TEST_SECRET')
        self.cp = ColorPrint()
        self.market = None
        self.orderSide = None
        self.fatFinger = None

    def create_order(self, **params) -> None:

        ############################
        # -CANCEL ORDERS
        ############################
    def cancel_orders(self, **params) -> None:

        ############################
        # -GET OPEN ORDER
        ############################

    def get_open_orders(self, **params) -> None:

        ############################
        # -GET OPEN CONDITIONAL ORDER
        ############################

    def get_open_conditional_orders(self, market: str = None) -> List[dict]:

        ############################
        # -GET POSITION
        ############################

    def get_positions(self, show_avg_price: bool = False) -> List[dict]:

    def get_position(self, name: str, show_avg_price: bool = False) -> dict:

        ############################
        # -PLACE ORDER
        ############################

    def place_order(self) -> dict:

        ############################
        # -PLACE CONDITIONAL ORDER
        ############################

    def place_conditional_order(self) -> dict:

        ##############################
        # -ORDER CLEANUP
        ###############################

    def place_order_cleanup(self, currCommand):
