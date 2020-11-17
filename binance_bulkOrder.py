from requests import Request, Session, Response
import time
import collections
import datetime
import json
import logging
import hmac
import hashlib
import os
from dotenv import load_dotenv
import urllib
from typing import Optional, Dict, Any, List
from colorprint import ColorPrint
from colorama import Fore, Back, Style, init
path = './keys.env'
load_dotenv(dotenv_path=path, verbose=True)

logging.basicConfig(level=logging.INFO, format=(
    Fore.BLUE + '[+] ' + Style.RESET_ALL + '%(message)s '))


class BinanceClient:
    _ENDPOINT = ""

    def __init__(self):
