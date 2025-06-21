"""
    Entry method for the callers to request data from the service.
"""

from loguru import logger

import helpers.validators as validators
from constants import SUPPORTED_FILE_TYPES
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
    pandas,DataFrame
        Data Frame containing the results
    """
    logger.info(f"file_type: {file_type}, start_date: {start_date}, end_date: {end_date}")
    if validators.isFileTypeValid(file_type) :
        logger.debug(f"File type {file_type} is valid")        
        if validators.isDateValid(start_date):
            logger.debug(f"start_date: {start_date} is valid")
        else:
            logger.debug(f"start_date: {start_date} is invalid")
    else:
        logger.debug(f"File type {file_type} is Invalid")

#TODO: create a method for get_supported_file_types

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
    get_data('bhavcopy', '41-Jun-2025', '18-Jun-2025')
    # print (",".join(get_supported_file_types()))
