# -*- coding: utf-8 -*-
"""
Created on Sun May 25 16:41:46 2025

@author: Alessio Incelli
"""

"""

Module for generating an entry point of the script with CLI (command line).
It creates an entry point for the command line to execute the data retrieval and storing of cryptos market data.

"""

# importing necessary libraries and modules
# modules
from scraper_logger import get_log
from scraper_datafetcher import scraper_fetcher
from scraper_utils import save_data_json

# libraries
import argparse
from pathlib import Path


LOGGER = get_log(__name__) # logging, as it is set up for each module

def scraper_cli_parser(): # defining a function to parse data
    
    """
    This function defines an entry point with arguments and shows the progress
    of the execution of the coingecko market data scraper.
    """
    
    entry_point = argparse.ArgumentParser(description = "Retrieving cryptos market data from coingecko") # defining an object for parsing command line strings into Python object
    entry_point.add_argument( # adding the argument to the parser
        '-o', '--out', # short and long flags
        type = Path, # the command line will interact with a path, specifically the path where the output file will be stored
        default = Path("coingecko_market_data.json"), # output file
        help = 'Output json file name') # message that makes the user understand what is going on
    arguments = entry_point.parse_args() # the command line arguments are parsed into a namespace
    
    try: # trying to be successful with the execution of command line entry point
        LOGGER.info("Initializing the data fetching ..") # initial message for logging the starting point of the process of data retrieval
        data = scraper_fetcher() # launching the function to retrieve cryptos market data from coingecko website
        save_data_json(arguments.out, data) # launching the function to store retrieved data into json files at the desired path
        LOGGER.info("Data fetching has finished successfully! :)") # final message to acknowledge that everything was fine
    except Exception as error: # if there is an error
        LOGGER.exception("Error in command line execution: %s", error) # show this message
        
if __name__ == "__main__":
    scraper_cli_parser() # running

    
