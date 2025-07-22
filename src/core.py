"""
    Entry method for the callers to request data from the service.
"""
from datetime import datetime

from loguru import logger

from src.helpers.validators import isDateValid, isFileTypeValid
from src.helpers import file_readers
from src.constants import SUPPORTED_FILE_TYPES, DATE_FMT

import pandas as pd 

def get_data(file_type: str, start_date: str, end_date: str):
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
        return False

    return data

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

if __name__ == '__main__':
    get_data(file_type='BHAVCOPY', start_date='07-Jul-2024', 
             end_date=datetime.today().strftime(DATE_FMT))

    get_data(file_type='PE', start_date='07-Jul-2024', 
             end_date=datetime.today().strftime(DATE_FMT))


