#TODO: Make this program a cmdline-param based!
"""
    Entry method for the callers to request data from the service.
"""
from datetime import datetime
import pandas as pd 

from loguru import logger

from src.helpers.validators import is_date_valid, is_file_type_valid
from src.helpers import file_readers
from src.helpers.common import get_all_stock_names, get_first_day_of_month
from src.constants import SUPPORTED_FILE_TYPES, DATE_FMT
from src.fetchers.stock_fetchers import get_stock_data_since_listing


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
    logger.info(f"{file_type = }, {start_date = }, {end_date = }")
    data = pd.DataFrame()
    if is_file_type_valid(file_type):
        # logger.debug(f"File type {file_type} is valid")        
        if is_date_valid(start_date) and is_date_valid(end_date):
            logger.debug(f"Dates: {start_date = } and {end_date = } are valid")
            # param validatins okay. Read the files now.
            data = file_readers.get_local_data(file_type, start_date, end_date)
            # logger.info(f"Got data: {data}")
        else:
            logger.debug(f"[{start_date = }] or [{end_date = }]is invalid")
    else:
        logger.error(f"{file_type = }is Invalid")
    return data

def get_market_cap(file_type:str | None, stock_name:str | None) -> list[dict] | dict :
    """Gets the market cap of an index, if file_type=="INDEX", 
    or gets the market cap of a stock specified by the second parameter.
    If the file_type == SUPPORTED_FILE_TYPES["STOCK"] and stock_name is None then
    calculate/return the market cap of all the stocks.
    
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
    logger.info(f"{file_type = }, {stock_name = }")
    #NOTE: Case where we fetch m-cap for all stocks
    if file_type == SUPPORTED_FILE_TYPES["STOCK"] and stock_name is None:
        # Get the combined market cap of all the stocks
        all_stocks: list = get_all_stock_names()
        all_market_caps: list[dict] = list()
        for stock in all_stocks:
            # For a stock get it's market cap data
            all_market_caps.append(file_readers.get_local_market_cap(SUPPORTED_FILE_TYPES["STOCK"], stock))
        return all_market_caps

    #NOTE: Case where we fetch m-cap for a stock
    if file_type == SUPPORTED_FILE_TYPES["STOCK"] and stock_name:
        return file_readers.get_local_market_cap(SUPPORTED_FILE_TYPES["STOCK"], stock_name)

    #TODO: Case where we fetch m-cap for an index
    if file_type == SUPPORTED_FILE_TYPES["INDEX"] :
        pass
    return list(dict()) # Unhandled / unimplemented cases gets a blank dictionary


def get_supported_file_types() -> dict:
    """ Returns the file types supported.

    Parameters
    ----------
        None
    Returns
    -------
        dict
    Contains the SUPPORTED_FILE_TYPES from src.constants
    """
    return SUPPORTED_FILE_TYPES

def get_index_names() -> list:
    """ Returns names of all the indices.
    Parameters
    ----------
        None
    Returns
    -------
        list
    list containing all index names
    """
    return file_readers.get_local_index_names()

def get_all_index_constituents():
    logger.debug(f"Getting constituents for all indices")
    for index_name in get_index_names():
        if "/" in index_name:
            index_name = index_name.replace("/", "By")
        get_index_constituents(index_name)


def fetch_stock_data_since_listing(skip_current_year: bool = False):
    """Fetches the price information for all stocks since listing
    Parameters
    ----------
        None
    Returns
    -------
        None
    """
    logger.info(f"Fetching since-listing data for all stocks. Current year skipped? [{skip_current_year = }]")
    all_stocks = get_all_stock_names()
    logger.info(f"Total {len(all_stocks)} stocks data to process.")
    processed = 0
    for stock in all_stocks:
        logger.info(f"Processing {stock = }")
        #NOTE: Call the scraper for each stock
        get_stock_data_since_listing(stock, skip_current_year)
        processed += 1
        logger.info(f"{processed}/{len(all_stocks)} Stocks processed.")

def get_index_constituents(index_name: str) -> list:
    logger.debug(f"Getting constituents for index: [{index_name = }]")
    constituents = list()
    #NOTE: Index name should be non-null
    if not index_name:
        logger.error(f"[{index_name = }]cannot be null or blank")
        return constituents
    #NOTE: Index name should be valid
    if index_name not in get_index_names():
        logger.error(f"Invalid Index Name: [{index_name = }]")
        return constituents
    logger.debug(f"[{index_name = }]is valid")
    return file_readers.get_local_index_constituents(index_name)

def daily_fetchers():
    #TODO: Run the Preopen if the day is a weekday and time is > 9:08 AM
    
    get_data(file_type='PREOPEN', 
             start_date=datetime.today().strftime(DATE_FMT), 
             end_date=datetime.today().strftime(DATE_FMT))
    #
    get_data(file_type='BHAVCOPY',
             start_date=get_first_day_of_month(), 
             end_date=datetime.today().strftime(DATE_FMT))

    get_data(file_type='PE',
             start_date=get_first_day_of_month(), 
             end_date=datetime.today().strftime(DATE_FMT))

    # # TODO: Needs a design change revisit at a later time!
    # # Do not run it before 7 PM
    get_data(file_type='INDEX', 
             start_date=datetime.today().strftime(DATE_FMT), 
             end_date=datetime.today().strftime(DATE_FMT))

    get_data(file_type='FNOBHAVCOPY', 
             start_date=get_first_day_of_month(), 
             end_date=datetime.today().strftime(DATE_FMT))

    get_all_index_constituents()

if __name__ == "__main__":
    # daily_fetchers()
    # fetch_stock_data_since_listing(skip_current_year=True)
    get_market_cap(SUPPORTED_FILE_TYPES["STOCK"], None)

