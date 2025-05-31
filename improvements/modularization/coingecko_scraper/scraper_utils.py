# -*- coding: utf-8 -*-
"""
Created on Sun May 25 16:41:45 2025

@author: Alessio Incelli
"""

"""

Module for utilities of the CoinGecko scraper.
It handles the way CoinGecko market data are stored and where.

"""

# importing necessary libraries and modules
# modules
from scraper_logger import get_log

# libraries
import json
from pathlib import Path
from typing import Any, Dict, List # let's explore later the possibility of assigning a type of outcome to each function, already have in mind what to do, let's see first how it comes out


LOGGER = get_log(__name__) # logging, as it is set up for each module

def save_data_json(path, data): # defining a function to save cryptos market data to json
    
    """
    This function takes market data retrieved from CoinGecko website for cryptos
    as dictionaries and stores them into json files which are saved at the path of interest.
    """
    
    path = Path(path) # the path of interest is stored as a path object, so that even if it is passed as a string we have it in path
    
    try: # starting a try block to handle eventual situations of errors, such as no write permissions or path names which are not valid
        with path.open("w", encoding = 'utf-8') as f: # the target path is put in write mode (w) and the encoding is ensured to be the utf-8 one
            json.dump(data, f, indent = 4) # storing the retrieved data into json format, let's check if we can improve the indent (pretty print)
        LOGGER.info("A number of records equal to %d was saved to the path %s", len(data), path) # if everything works well, the log file will be filled with a success message which will show the count of records and the file name
    except Exception as error: # in case an error is raised
        LOGGER.exception("Writing json files at %s failed: %s", path, error) # the error is reported in the log file
        raise


