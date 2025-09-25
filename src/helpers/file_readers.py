from datetime import datetime, timedelta
import json
import os
import pandas as pd

from loguru import logger

from src.helpers.common import compose_dates_from_range, get_last_trading_date
from src.constants import FILES_BASE_DIR, PREOPEN_SKIPROWS, PREOPEN_PAYLOADS, SUPPORTED_FILE_TYPES, DATE_FMT
from src.fetchers.historical_data import fetch_data, fetch_index_constituents_data
from src.fetchers.stock_fetchers import get_stock_data_since_listing

def get_local_data(file_type: str, start_date: str, end_date:str) -> pd.DataFrame:
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
    d_range = compose_dates_from_range(start_date, end_date)
    if not d_range:
        logger.info(f"No dates to process for file_type: [{file_type}], start_date: [{start_date}] end_date: [{end_date}]")
        return df
    
    for trading_date in d_range:
        try:
            if(file_type.upper() == "PREOPEN"):
                for payload in PREOPEN_PAYLOADS:
                    data = pd.read_csv(os.path.join(FILES_BASE_DIR, "PREOPEN", f"preopen_{payload}_{trading_date}.csv"), encoding="utf-8", skiprows=PREOPEN_SKIPROWS)
                    df = pd.concat([df, data ])
                return df

            trd_dt_data = pd.read_csv(os.path.join(FILES_BASE_DIR,file_type.upper(),\
                                                   f'{file_type.lower()}_{trading_date}.csv'))
            #NOTE: For index file add trading_date column since it's absent in data file content
            if (file_type.upper() == SUPPORTED_FILE_TYPES["INDEX"]):
                trd_dt_data["TRADING_DATE"] = trading_date
            #TODO: Need to handle empty file case. Refresh with fetch???
            if trd_dt_data.size == 0:
                logger.error(f"Data not found in local for [{trading_date}]")
            # Data found in local; Append data to DF 
            else:
                logger.debug(f"[{file_type}] Data found locally for [{trading_date}]")
                df = pd.concat([df,trd_dt_data], ignore_index=True)
        #TODO Should be similar to the first case
        except pd.errors.EmptyDataError:
            logger.error(f"WTF: No data for [{trading_date}], for file_type: [{file_type}]")
        # If data not found locally, issue remote fetch
        except FileNotFoundError:
            logger.info(f"No file for [{trading_date}], file_type: {file_type}. Calling Fetcher")
            trd_dt_data = fetch_data(file_type, trading_date)
            if (file_type.upper() == SUPPORTED_FILE_TYPES["INDEX"]):
                trd_dt_data["TRADING_DATE"] = trading_date
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

def get_local_index_names(i_date: str = datetime.today().strftime(DATE_FMT)) -> list:
    """
        Retunr the list containing all index names for given date. 
        For weekends, date is defaulted to the latest Friady.
    Parameters
    ----------
       i_date: str
    Trading date for which the data is sought!
    Returns
    -------
        list
    list containing all the index names
    """
    index_names = list()
    i_weekday = datetime.strptime(i_date, DATE_FMT).weekday()
    if i_weekday > 4:
        days_to_go_back = (i_weekday + 3) % 7
        i_date = (datetime.strptime(i_date, DATE_FMT) - timedelta(days=days_to_go_back)).strftime(DATE_FMT)
    #TODO: What if the last Friday was a exchange holiday?
    try:
        data = get_local_data(file_type=SUPPORTED_FILE_TYPES["INDEX"],
                          start_date=i_date,
                          end_date=i_date)
        index_names = list(data["INDEX"].unique())
        # logger.info(f"Index Names are: [{index_names}]")
        return index_names
    except:
        logger.error(f"Error Occured fetching data")
        return index_names # Reurn Blank Index names

def get_local_index_constituents(index_name: str) -> list:
    """
        Get's the index constituents for the passed index name. It is assumed that 
        the index_name passed is valid.
    
    Parameters
    ----------
        index_name: str
    The name of the valid index
    Returns
    -------
        list
    List containing the names of stocks in the index
    """
    logger.debug(f"Index name is [{index_name}]")
    constituents = list()
    #NOTE: Check if there is a file already present with index names
    file_type:str = SUPPORTED_FILE_TYPES["IDX_CONSTITUENTS"]
    try:
        file_name = os.path.join(FILES_BASE_DIR,
                                        file_type.upper(),
                                        f'{file_type.lower()}_{index_name}.json')
        data = json.load(open(file_name))
        df = pd.DataFrame(data["data"])
        constituents = list(df["symbol"][1:])
        # logger.info(f"The index [{index_name}] constituents are [{constituents}]")
        # logger.info(df)
    except pd.errors.EmptyDataError:
        logger.error(f"WTF: File Present but No data for [{index_name}]")
    #TODO: If such file is not present then fetch and store in the file
    except FileNotFoundError:
        return fetch_index_constituents_data(index_name)
    return constituents

def get_local_stock_data(stock_name: str) -> pd.DataFrame:
    """Gets the since-listing stock data from local files. If data not found locally,
        then issue a remote fetch.
    Parameters
    ----------
    stock_name
        str
    The name of the stock.
    Returns
    -------
        pandas.DataFrame
    Data frame containing the since-listing stock data.
    """
    logger.debug(f"Stock Name : [{stock_name}]")
    #NOTE: Read the local file, if it exists. Use meta-info files to check past fectches.
    file_type:str = SUPPORTED_FILE_TYPES["STOCK"]
    trading_date: str= get_last_trading_date(datetime.today().strftime(DATE_FMT))
    logger.info(f"Getting data for stock: [{stock_name}], for date: [{trading_date}]")
    try:
        file_name = os.path.join(FILES_BASE_DIR,
                                        file_type.upper(),
                                        f'{file_type.lower()}_{stock_name}.json')
        data = json.load(open(file_name))
        df = pd.DataFrame(data["data"])
    except FileNotFoundError:
        logger.error(f"File not found for [{stock_name}], for date [{trading_date}]")
        #NOTE: If the local file does not exist then issue a fetch
        return get_stock_data_since_listing(stock_name, trading_date)
    return pd.DataFrame()

if __name__ == "__main__":
    get_local_index_names("30-AUG-2025")
