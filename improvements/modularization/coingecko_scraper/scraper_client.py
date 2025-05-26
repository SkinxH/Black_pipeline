# -*- coding: utf-8 -*-
"""
Created on Sun May 25 16:41:43 2025

@author: Alessio Incelli
"""

"""

Module for handling the behavior of CoinGecko API requests with attempts and logger.
TODO: describe what it does

"""

# importing necessary libraries and modules
# modules
from .scraper_config import API_BASE, API_KEY, HEADERS, vs_currency, per_page
from .scraper_logger import get_log

# libraries
import requests # ? probably we need this to send HTTP request?? (Remember: The method is case-sensitive and should always be mentioned in uppercase


LOGGER = get_log() # logger usage from scraper_logger.py (do we need this here?)

class coingecko_client: # defining a class to create the client object for CoinGecko API request
    
    """
    TODO: describe what this class is for
    """
    
    # would it make sense to assign each of the below functions to an expected type of variable with type hints? Let's think about it
    # we would just need to add "->" and the type of variable at the right of the function definition (?)
    
    def __init__(self): # initializing the constructor of this class
    
        """
        Definition of the constructor for this class, where self refers to the object that we want
        to keep using as a reference for this class.
        """
    
        self.session = requests.Session() # initializing a requests session
        self.headers = HEADERS # taking the headers from the scraper_config module (identification for accessing coingecko API, in this case)
    
    def scraper_request(self, ): # this would be the function with the request behavior, to understand what to include as inputs
        
        """
        TODO: describe what this function is for.
        """
        
        website = f"{API_BASE}" # taking the website url from the variable defined in the scraper_config module
        
    
    # GET is used to retrieve data and should only be used for that, not for changing anything
    # GET is to retrieve data, while POST is to send data via HTML format
    
    #r = requests.get(url, headers=headers) , we have some headers so we might probably need something similar for the request, they don't change request behavior but only final outcome
    
    #allow_redirects=False, let's check if we need this inside the GET method
    # DEFINITELY we need to include timeout= xxx, this is to raise an exception if the server has not issued a response for xxx seconds
    
    #r.status_code , we might need this to check the status of our GET request
    #r.raise_for_status() , if we get None with this there is probably no bad request (error)
    
    #r.cookies['example_cookie_name'] , we might want to check if there are a lot of cookies (I don't know if it may take up much space)
    
    # !!! r.json() might probably be what we need in the end, as the client should save the final scraping output as JSON
    
    def obtain(self, ): # ideally this is the function to actually run the request with the behavior laid out in previous function, to understand what to include as inputs
        
        """
        
        """
        
        
