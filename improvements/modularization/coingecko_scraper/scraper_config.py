# -*- coding: utf-8 -*-
"""
Created on Thu May 22 17:15:39 2025

@author: Alessio Incelli
"""

"""

Module for configuration of CoinGecko scraping.
Reads the API key for entering the website specified in API_BASE;
to check if we can get the environmental variable to adapt dynamically to the presence or absence of the key.

"""

# importing necessary libraries
import os # do we really need this? Let's see

API_BASE = "https://pro-api.coingecko.com/api/v3" # url of coingecko API website
API_KEY = os.getenv("COINGECKO_API_KEY", "CG-q5nxd4AYP3hCaWC4GfrdRDG8") # the idea here is to have an environmental variable that takes this key but otherwise it takes the hardcoded one if a key is not provided, let's see how to do it

HEADERS = {"x-cg-pro-api-key": API_KEY} # here we specify the header needed for authentication on CoinGecko website

# defining the parameters of the request as variables
vs_currency = 'usd' # market data currency
#order = 'market_cap_desc' # order at which cryptos are displayed
per_page = 250 # how many cryptos per page to retrieve with the request
request_timeout = 15 # seconds to pass by for a request timeout (an idea, up for discussion)
max_retries = 3 # maximum number of tentative for the request to work (an idea, up for discussion)
backoff_factor = 1 # exponential-backoff factor (again in seconds), it's like a time multiplier between tentatives (retries), (an idea, up for discussion)



