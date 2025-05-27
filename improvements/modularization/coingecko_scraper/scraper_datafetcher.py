# -*- coding: utf-8 -*-
"""
Created on Sun May 25 16:41:45 2025

@author: Alessio Incelli
"""

"""

Module for handling the download of cryptos market data from CoinGecko website.
TODO: describe what it does (it would ideally work closely with the client module)

"""

# importing necessary libraries and modules
# modules
from scraper_config import API_KEY, vs_currency, per_page
from scraper_logger import get_log
from scraper_client import coingecko_client

# libraries
import time
from typing import Any, Dict, Optional # let's explore later the possibility of assigning a type of outcome to each function, already have in mind what to do, let's see first how it comes out


LOGGER = get_log(__name__) # logging

def scraper_fetcher(): # defining a function for retrieving market data for cryptos
    
    """
    TODO: describe what it does.
    """
    
    data = [] # initializing storage memory for the market data that will be retrieved
    gecko_client = coingecko_client() # calling the module which handles the HTTP request
    page = 1 # starting from the first page of the results obtained through the API
    
    while True: # until there is data to retrieve, consider the following
        # logger
        
        # define parameters
