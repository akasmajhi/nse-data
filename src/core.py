#TODO: Make this program a cmdline-param based!
"""
    Entry method for the callers to request data from the service.
"""
from datetime import datetime

from loguru import logger

from src.helpers.validators import isDateValid, isFileTypeValid
from src.helpers import file_readers
from src.constants import SUPPORTED_FILE_TYPES, DATE_FMT

import pandas as pd 

def get_data(file_type: str, start_date: str, end_date: str) -> pd.DataFrame:
    """ Gets the data for the 'file_type' supplied.

    Parameters
    ----------

    file_type : str
        The type of file required. (bhavcopy, pe, etc.) 
        Invoke core.supported_file_types for all the supported file types.
    start_date : str
        Starting date. (Format: 'DD-Mon-YYYY. Ex., 12-Jun-2025)
    end_date : str
        Starting date. (Format: 'DD-Mon-YYYY. Ex., 12-Jun-2025)

    Returns
    -------
    pandas.DataFrame
        Data Frame containing the results
    """
    logger.info(f"file_type: {file_type}, start_date: {start_date}, end_date: {end_date}")
    data = pd.DataFrame()
    if isFileTypeValid(file_type):
        # logger.debug(f"File type {file_type} is valid")        
        if isDateValid(start_date) and isDateValid(end_date):
            logger.debug(f"Dates: {start_date} and {end_date} are valid")
            # param validatins okay. Read the files now.
            data = file_readers.get_local_data(file_type, start_date, end_date)
            # logger.info(f"Got data: {data}")
        else:
            logger.debug(f"start_date: [{start_date}] or end_date: [{end_date}]is invalid")
    else:
        logger.error(f"File type {file_type} is Invalid")
    return data

def get_market_cap(file_type:str | None, stock_name:str | None) -> dict :
    """Gets the market cap of an index, if file_type=="INDEX", or gets the market cap of a stock specified by the second parameter.
    
    Parameters
    ----------

    file_type : str
        As enumerated by src/constants/SUPPORTED_FILE_TYPES 
    stock_name : str
        Name of the stock if file_type=STOCK

    Returns
    -------
    pd.array
        Dictionary with key as attribute and pd.DataFrame as value
    """
    logger.info(f"file_type: {file_type}, stock_name: {stock_name}")
    if file_type and isFileTypeValid(file_type):
        return {}
    return {}


def get_supported_file_types():
    """ Returns the file types supported.

    Parameters
    ----------
        None
    Returns
    -------
        set
    Contains the supported file types
    """
    return SUPPORTED_FILE_TYPES

def get_index_names() -> pd.DataFrame:
    """ Returns names of all the indices.
    Parameters
    ----------
        None
    Returns
    -------
        pd.DataFrame
    DataFrame contains a row for each index.
    """
    return file_readers.get_local_index_names()

if __name__ == '__main__':
    #TODO: Run the Preopen if the day is a weekday and time is > 9:08 AM
    get_data(file_type='PREOPEN', 
             start_date=datetime.today().strftime(DATE_FMT), 
             end_date=datetime.today().strftime(DATE_FMT))

    get_data(file_type='BHAVCOPY', start_date='01-Sep-2025', 
             end_date=datetime.today().strftime(DATE_FMT))

    get_data(file_type='PE', start_date='01-Sep-2025', 
             end_date=datetime.today().strftime(DATE_FMT))

    # # TODO: Needs a design change revisit at a later time!
    # # Do not run it before 7 PM
    get_data(file_type='INDEX', 
             start_date=datetime.today().strftime(DATE_FMT), 
             end_date=datetime.today().strftime(DATE_FMT))
    #
    # get_index_names()
