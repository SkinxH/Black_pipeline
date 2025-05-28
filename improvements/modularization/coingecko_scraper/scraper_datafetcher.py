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
    This function retrieves market data for all cryptos by looking at all pages available at CoinGecko website.
    The parameters of this function, which may be adjustable if we deem it necessary, are:
        - currency of the market data we are retrieving
        - the order by which the market cap of cryptos need to be displayed
        - number of pages to be retrieved from CoinGecko website
        - number of the starting page
    """
    
    data = [] # initializing storage memory for the market data that will be retrieved
    gecko_client = coingecko_client() # calling the module which handles the HTTP request
    page = 1 # starting from the first page of the results obtained through the API
    
    while True: # until there is data to retrieve, consider the following
        LOGGER.info("Retrieving page %d", page) # logger information on what page we are working on
        
        parameters = { # these are the parameters which are part of the HTTP request execution function and which are defined in the config module
            "vs_currency": vs_currency, # data currency
            "order": order, # TO UNLOCK THE VARIABLE IN THE CONFIG MODULE, it's descending order by market cap
            "per_page": per_page, # how many cryptos per page to retrieve with the request
            "page": page} # number of the page we are at
        
        try:
            data = gecko_client.get("/coins/markets", parameters) # trying to get cryptos market data with parameters specified above connecting to coingecko API, the endpoint path is the one provided in the original script
        except Exception as error:
            LOGGER.exception("Issue retrieving data at page %d: %s", page, error) # if there is an error, the traceback of what happened is registered in the log file and the while loop is exited
            break
        
        if not data: # if no more data is available
            LOGGER.info("End of available data is reached at page number %d", page) # logging information
            break # while loop is exited
        
        data.extend(data) # extending the initially empty storing list by appending retrieved data, it should be coins for an amount of 250 pages
        
        if len(data) < per_page: # if the length of the found data available is less than 250, it means the current page of the while loop is the last one we are going to get
            break # therefore we need to exit the while loop here as well
        
        page += 1 # dynamically moving to the next page
        time.sleep(1) # delaying the API connections by 1 second, just to make sure it doesn't get mixed up, to respect API rate limits
        
    LOGGER.info("Total number of cryptos retrieved: %d", len(data)) # once the while loop is exited, in whichever case, it might be useful to understand how many cryptos we were able to retrieve market data for
    return data








