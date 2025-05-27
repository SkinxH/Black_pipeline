# -*- coding: utf-8 -*-
"""
Created on Sun May 25 16:41:43 2025

@author: Alessio Incelli
"""

"""

Module for handling the behavior of CoinGecko API requests with attempts and logger.
Opens a session for connecting to CoinGecko API, establishes the characteristics of the request that will be launched,
and actually executes the request.

"""

# importing necessary libraries and modules
# modules
from scraper_config import API_BASE, API_KEY, HEADERS
from scraper_logger import get_log

# libraries
import requests # ? probably we need this to send HTTP request?? (Remember: The method is case-sensitive and should always be mentioned in uppercase
import time
from requests.exceptions import HTTPError, Timeout, RequestException
from typing import Any, Dict, Optional # let's explore later the possibility of assigning a type of outcome to each function, already have in mind what to do, let's see first how it comes out

LOGGER = get_log(__name__) # logger usage from scraper_logger.py (do we need this here?)

class coingecko_client: # defining a class to create the client object for CoinGecko API request
    
    """
    This class opens a session for connecting to CoinGecko API, establishes the characteristics of the request that will be launched,
    and actually executes the request.
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
    
    def scraper_request(self, method: str, endpoint: str, **kwargs): # defining a function with the request behavior
        
        """
        This function laids out the characteristics of the HTTP request that will be executed.
        Tentatives and timeout features are established.
        """
        
        website = f"{API_BASE}{endpoint}" # taking the website url from the variable defined in the scraper_config module and combining it with the endpoint path to produce the full URL
        kwargs.setdefault("headers", self.headers) # authentication headers are added only if by default no headers were passed
        kwargs.setdefault("timeout", self.request_timeout) # as well for timeout, if no default timeout is indicated, this line adds it
        
        for tentative in range(1, max_retries + 1): # looping from 1 to the maximum number of tentatives, we have to start from the first log file instead of from zero, so the loop will end at max_retries adding 1 
            try:
                response = self.session.request(method, website, **kwargs) # in the session initialized with previous function, the HTTP request is sent using a certain method (GET, POST, ...), the url of the website we are interested in and the keywords arguments
                response.raise_for_status() # raising HTTP error if occurs (probably in this case the status code of the error would be 404 or 5xx)
                return response.json() # if no error is raised for this request, return a JSON response
            
            except (HTTPError, Timeout) as error: # the exception for this tentative is
                LOGGER.warning("Request failed (tentative %s): %s", tentative, error) # a warning is added to the log file if the request does not produce the expected outcome due to HTTP error or due to a timeout reached for the request
                if tentative == max_retries: # if we are at a number of tentative equal to the maximum number that we set up
                    LOGGER.error("Maximum number of tentatives reached for %s", website) # an error is recorded in the log file
                    raise
                time.sleep(backoff_factor * tentative) # delay execution for a number of seconds, basically every time we reach the exception the waiting time before the new tentative is expanded
                
            except RequestException as error: # if we have any other unexpected errors with the request, not associated to HTTP status error or timeout
                LOGGER.critical("Critical HTTP error: %s", error) # record this as a critical error in the log file
                raise
        
    
    # GET is used to retrieve data and should only be used for that, not for changing anything
    # GET is to retrieve data, while POST is to send data via HTML format
    
    #r = requests.get(url, headers=headers) , we have some headers so we might probably need something similar for the request, they don't change request behavior but only final outcome
    
    #allow_redirects=False, let's check if we need this inside the GET method
    # DEFINITELY we need to include timeout= xxx, this is to raise an exception if the server has not issued a response for xxx seconds
    
    #r.status_code , we might need this to check the status of our GET request
    #r.raise_for_status() , if we get None with this there is probably no bad request (error)
    
    #r.cookies['example_cookie_name'] , we might want to check if there are a lot of cookies (I don't know if it may take up much space)
    
    # !!! r.json() might probably be what we need in the end, as the client should save the final scraping output as JSON
    
    def obtain(self, endpoint: str, parameters): # defining a function to execute the request characterized by the behavior defined in previous function
        
        """
        This function actually executes the GET HTTP request.
        The type of HTTP request can be modified.
        """
        
        return self._scraper_request("GET", endpoint, params = parameters) # launching the GET request (for now using GET, but we can add or modify as whatever we need, meaning POST, DELETE or others)
