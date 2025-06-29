"""
Central code for all the app specific validators.
"""
from datetime import datetime 

from loguru import logger

from src.constants import SUPPORTED_FILE_TYPES  

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
    logger.debug(f"Supported File Types: {SUPPORTED_FILE_TYPES}")
    return True if file_type.upper() in SUPPORTED_FILE_TYPES else False 

def isDateValid(i_date: str):
    """ 
        The string i_date ('DD-Mon-YYYY') is checked for validity.

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
    if len(i_date.split('-')) == 3:
        try:
            datetime.strptime(i_date, '%d-%b-%Y')
        except ValueError:
            logger.error(f"Invalid date [{i_date}] passed. Reqd. format is DD-Mon-YYYY")
            return False
        return True

#TODO
def isDateInFuture(i_date: str):
    logger.debug(f"Input date is: {i_date}")
    pass
#TODO
def validateTradingDate(i_date: str):
    """
        Check if the trading date is valid.
    Parameters
    ----------
        i_date: str
    Input date in the format of DD-Mon-YYYY. e.g., 14-Jun-2025

    Returns
    -------
        boolean
    True if the trading date is valid.
    """
    logger.debug(f"Input date is: {i_date}")
    return False

