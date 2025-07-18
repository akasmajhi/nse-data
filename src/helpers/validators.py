"""
Central code for all the app specific validators.
"""
from datetime import datetime 

from loguru import logger

from src.constants import SUPPORTED_FILE_TYPES, NSE_HOLIDAYS

# for key in MONTH_NAMES:
#     print(f"Month Name: [{key}] Month Value: [{MONTH_NAMES[key]}]")

def isFileTypeValid(file_type: str):
    """
        Checks to see if the file type is valid.
        Valid types are defined in constants.


    Parameters
    ----------
        file_type : str
    The type pf file required.

    Returns
    -------
        boolean : True/False
    """
    logger.debug(f"file type is: {file_type.upper()}")
    # logger.debug(f"Supported File Types: {SUPPORTED_FILE_TYPES}")
    return True if file_type.upper() in SUPPORTED_FILE_TYPES else False 

def isDateValid(i_date: str):
    """ 
        The string i_date ('DD-Mon-YYYY') is checked for validity of format and 
        prevents future dates.

    Parameters
    ----------
        i_date: str
    Input date in the format of DD-Mon-YYYY. e.g., 14-Jun-2025

    Returns
    -------
        boolean
    True if the date is valid.
    """
    logger.debug(f"Input date is: [{i_date}]")
    trading_dt = ""
    if len(i_date.split('-')) == 3:
        try:
            trading_dt = datetime.strptime(i_date, '%d-%b-%Y')
            if (datetime.today() > trading_dt):
                return True
            else:
                logger.error(f"Future date [{i_date}] Not Allowed!")
                return False
        except ValueError:
            logger.error(f"Invalid date [{i_date}] passed. Reqd. format is DD-Mon-YYYY")
            return False

def isNSEHoliday(trading_dt: str):
    # Check if it is a valida date
    # Check if the valid date is in NSE holiday list
    logger.debug(f"Checking nse holiday for: [{trading_dt}]")
    if(isDateValid(trading_dt)):
        # Get the year from the trading date
        yyyy = trading_dt[-4:]
        # logger.debug(f"Getting holday list for {yyyy}")
        try:
            NSE_HOLIDAY_LIST = NSE_HOLIDAYS[yyyy]
            # If no holiday list then DONOT proceed
            if len(NSE_HOLIDAYS) == 0:
                logger.error(f"No NSE holiday calendar found for [{yyyy}]")
                return True
            logger.debug(f"Holiday list: [{NSE_HOLIDAY_LIST}]")
            # check if trading date is in the holiday list
            if (trading_dt.upper() in NSE_HOLIDAY_LIST):
                logger.info(f"{[trading_dt]} is a holiday!")
                return True
        except KeyError:
            logger.error(f"Holiday list not present for [{yyyy}]")
            # Do not fetch any data if calendar is absent in constants.py
            return True
    return False

