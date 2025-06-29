import os
import pandas as pd

from loguru import logger

from src.helpers.common import composeDatesFromRange
from src.constants import FILES_BASE_DIR
from src.fetchers.historical_data import fetch_data

def get_local_data(file_type: str, start_date: str, end_date:str):
    """
        Gets the data from the local store. If data is valid and not found
        locally, then you source the data from remote.
    Parameters
    ----------
       file_type: str
    What type of file sought (PE, BHAVCOPY, etc.)
        start_date: str
    Start date in the format of DD-Mon-YYYY. e.g., 12-Jun-2025
        end_date: str
    End date in the format of DD-Mon-YYYY. e.g., 20-Jun-2025

    Returns
    -------
        pandas.DataFrame
    Dataframe containg the in-range values.
    
    Validations
    -----------
    #TODO
    """
    df = pd.DataFrame()
    logger.debug(f"Getting data for: file_type: {file_type}, start_date: {start_date}, \
            end_date: {end_date}")

    # Extract date ranges (Validations provided by the called method
    # Following call gets the DD-MMM-YYYY ranges as list
    d_range = composeDatesFromRange(start_date, end_date)
    # Look for data
    for trading_date in d_range:
        logger.debug(f"Getting data for [{trading_date}]")
        try:
            trd_dt_data = pd.read_csv(os.path.join(FILES_BASE_DIR,file_type.upper(),\
                                                   f'{file_type.lower()}_{trading_date}.csv'))
            if trd_dt_data.size == 0:
                #TODO Need to handle empty file case.
                logger.info(f"Data not found in local for [{trading_date}]")
            else:
                # Append data to DF 
                logger.debug(f"[{file_type}] Data found locally for [{trading_date}]")
                df = pd.concat([df,trd_dt_data], ignore_index=True)
        except pd.errors.EmptyDataError:
            #TODO 
            logger.error(f"WTF: No data for [{trading_date}]")
        except FileNotFoundError:
            # If data not found locally, issue remote fetch
            logger.info(f"No file for [{trading_date}]. Calling Fetcher")
            trd_dt_data = fetch_data(file_type, trading_date)
            df = pd.concat([df, trd_dt_data], ignore_index=True) 
    return df

def isFileExisting(file_type: str, trading_date: str):
    """
        Checks to see if a file is existing locally for a given type and trading date.
    Parameters
    ----------
       file_type: str
    What type of file sought (PE, BHAVCOPY, etc.)
        trading_date: str
    Trading date in the format of DD-Mon-YYYY. e.g., 12-Jun-2025

    Returns
    -------
        boolean
    True if the file exists; False otherwise
    """
    logger.debug(f"Checking for [{file_type}] for trading date [{trading_date}]")
