# -*- coding: utf-8 -*-
"""
Created on Fri May 23 17:10:41 2025

@author: Alessio Incelli
"""

"""

Module for logging of CoinGecko scraping.
This script is the central place for the logging of the scraping activity from CoinGecko website;
TODO: describe what it does.

"""

# importing necessary libraries
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import sys

log_dir = Path("logs") # specifying path where the log file will be
log_file = log_dir / "CoinGecko_scraper.log" # name of the log file in the path created above

log_dir.mkdir(parents = True, exist_ok = True) # making sure that the directory of the logs does exist


def get_log(logger_name: str = 'CoinGecko_scraper', level: int = logging.INFO, log_rollover: bool = False, max_bytes: int = 1_000_000, backup_count: int = 3): # defining a function to obtain the logs, to actually perform the logger
    
    """
    Function to generate and specify the characteristics of the logger.
    
    The functions inputs can be described as per below:
        logger_name: this is the name of the logger, which can be identified as the name of the log file according to our logic
        level: threshold of severity
        log_rollover: turn on/off button for the optional rotating log file handler
        max_bytes: maximum size to reach for a log file rollover to happen
        backup_count: number of small log files to produce in case the log file rollover does happen
        
    """
    
    logger = logging.getLogger(logger_name) # activating the logger for the logger name inserted in the input of the function (in our case, it is the name in the variable log_file)
    
    if logger.handlers: # here we want to understand if there are already handlers, so that we prevent duplicate handlers or repeated imports (maybe for now it's not a risk but it might be in the future, up for discussion)
        return logger

    logger.setLevel(level) # setting a threshold of severity for the handler

    # Log format: include time, log level, filename, line number, and message
    formatter = logging.Formatter( # specifying the format of the log
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s", # for now, the format includes time, name of the log level, name of the log file, line number and message
        datefmt="%Y-%m-%d %H:%M:%S" # format for how dates appear
    )

    stream_handler = logging.StreamHandler(sys.stdout) # trying to set up a stream handler for the console, sending logging outputs to streams
    stream_handler.setFormatter(formatter) # the format of stream handler follows the characteristics specified in the previous block
    logger.addHandler(stream_handler) # adding the stream handler

    # now, it might happen that while writing logs file too much time passes by or maybe we want everything to run within a certain time interval
    # therefore, we can optionally set a rotating file handler, so that when a log file reaches a certain size or a specified time interval elapses, this optional block creates a new log file and continues writing logs to it
    if log_rollover: # the input in the function for now is set to False so that we don't run this but we can discuss and just turn it on
        log_file_handler = RotatingFileHandler( # defining the rotating file handler
            log_file, # the object is obviously the log file initially defined
            maxBytes = max_bytes, # maximum number of bytes as the size to reach
            backupCount = backup_count, # if this is set to 0, the rollover of the log file never happens; if it is set to 3, it means that for each rollover we get app.log.1, app.log.2 and app.log.3
            encoding = "utf-8" # default encoding
        )
        log_file_handler.setFormatter(formatter) # the optional activation of the file handler has the same format of the stream handler
        logger.addHandler(log_file_handler) # adding the optional file handler to the logger

    return logger 

LOGGER = get_log() # logger usage
    
    