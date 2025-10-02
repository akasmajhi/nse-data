from datetime import datetime
import json
import os
from http import HTTPStatus
import pandas as pd
import requests
from loguru import logger
from src.fetchers.common import dummy_request
from src.constants import DATE_FMT_1, SUPPORTED_FILE_TYPES, FILES_BASE_DIR, NSE_STOCK_HISTORY_URL, NSE_STOCK_QUOTE_URL, REQ_HEADER,FILES_BASE_DIR, DATE_FMT, MCAP_FOLDER
from src.helpers.common import get_stock_fetch_history, get_latest_history, register_failed_fetch, set_stock_fetch_history

def get_stock_data_since_listing(stock_name: str, skip_current_year: bool = False) -> pd.DataFrame:
    """
        Fetches the stock data from remote and stores in local file.

    Parameters
    ----------
       stock_name: str
    name of the stock
    Returns
    -------
        pandas.DataFrame
    Containing the data that is read from remote.
    """
    logger.info(f"Fetching since-listing data for [{stock_name = }]")
    #NOTE: First get the listing date of the stock
    stock_listing_date = get_listing_date(stock_name)
    stock_listing_year = stock_listing_date[-4:]
    #NOTE: NSE allows only upto 1-year download. So, divide the timeframe
    current_year = datetime.now().year
    logger.debug(f"[{stock_name = }], [{stock_listing_date = }], [{stock_listing_year = }], [{current_year = }]")
    
    to_year = current_year + 1
    if skip_current_year:
        to_year = current_year
    if stock_listing_year: # Do not process a stock if the listing year is not present
        # for year in range(int(stock_listing_year), current_year+1):
        for year in range(int(stock_listing_year), to_year):
            fetch_stock_data_for_a_year(stock_name, year, skip_current_year)
    #NOTE: Now, read and combine all individual files
    else:
        logger.error(f"Stock listing year not found for: [{stock_name = }]")
    return pd.DataFrame()

def get_listing_date(stock_name: str)->str:
    logger.info(f"Getting listing date for [{stock_name = }]")
    #NOTE: If there is a file already present, use it!
    listing_date = read_listing_date_from_file(stock_name)
    if listing_date:
        #NOTE: Listing date found in local file. No need to fetch again!
        return listing_date
    #NOTE: Assume that the stock name is valid, make a URL fetch
    dummy_res = dummy_request()

    payload = {
        "symbol":stock_name,
    }
    stock_quote_res = requests.get(
        url=NSE_STOCK_QUOTE_URL,
        headers=REQ_HEADER,
        params=payload,
        cookies=dummy_res.cookies,
        timeout=30)
    logger.debug(f"The stock_quote_res code is: [{stock_quote_res.status_code = }]")
    if(stock_quote_res.status_code == HTTPStatus.OK):
        # logger.info(stock_quote_res.text)
        #NOTE: Store the file inside the META folder
        STOCK = SUPPORTED_FILE_TYPES["STOCK"]
        file_name = os.path.join(FILES_BASE_DIR, STOCK, "META", f"{stock_name.upper()}_meta.json")
        with open(file_name, "w") as file:
            file.write(stock_quote_res.text)
        return read_listing_date_from_file(stock_name)
    return "" #NOTE: This should be interpreted as an error condition

def read_listing_date_from_file(stock_name: str) ->str:
    STOCK = SUPPORTED_FILE_TYPES["STOCK"]
    file_name = os.path.join(FILES_BASE_DIR, STOCK, "META", f"{stock_name.upper()}_meta.json")
    if os.path.exists(file_name):
        logger.debug(f"Meta file exists for [{stock_name = }]. Going to use it!")
        try:
            with open(file_name, "r") as file:
                data = json.load(file)
                try:
                    logger.debug(f"Listing Date: [{data['metadata']['listingDate']}] for [{stock_name}]")
                    return data['metadata']['listingDate']
                except KeyError:
                    logger.error(f"Listing date key not found in json for stock: [{stock_name = }]")
        except FileNotFoundError:
            logger.error(f"[file_name = ] not found!")
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from the file: [{file_name = }]")
    return "" #NOTE: Blank return for any error condition. Caller must check!

def fetch_stock_data_for_a_year(stock_name: str, year: int, skip_current_year: bool = False):
    STOCK = SUPPORTED_FILE_TYPES["STOCK"]
    logger.debug(f"Fetching data for [{stock_name = }] for [{year = }]")
    #NOTE: If a file exists for a year and if it's not current year then skip fetch for that year
    file_name = os.path.join(FILES_BASE_DIR, STOCK, f"{stock_name}_{year}.csv")
    current_year = datetime.now().year

    #NOTE: Current year 
    if (year == current_year) and (not skip_current_year): 
        from_date = datetime(year,1,1).strftime(DATE_FMT_1)
        to_date = datetime.today().strftime(DATE_FMT_1)
        if os.path.exists(file_name): # File exists!
            #TODO: If last fetch was today, then do not fetch again
            latest_fetch_history = get_latest_history(get_stock_fetch_history(stock_name))
            last_fetch_date = datetime.strptime(latest_fetch_history["fetch_date"], f"{DATE_FMT}:%H-%M-%S")
            if last_fetch_date.strftime(DATE_FMT) == datetime.today().strftime(DATE_FMT):
                return # DO NOT FETCH AGAIN
            #NOTE:Delete the earlier CSV
            os.remove(file_name)
            logger.info(f"Deleting Earlier file: [{file_name = }]")
        stock_fetch(stock_name, from_date, to_date)
    #NOTE: Fetch for past years (non-current)
    else:
        if os.path.exists(file_name): # For past years don't fetch if file exists
            logger.info(f"For the stock: [{stock_name = }], file exists for: [{year = }]")
            return
        else:
            from_date = datetime(year,1,1).strftime(DATE_FMT_1)
            to_date = datetime(year, 12, 31).strftime(DATE_FMT_1)
            stock_fetch(stock_name, from_date, to_date)

def stock_fetch(stock_name: str, from_date: str, to_date: str):
    """Generic stock fetch utility to download the CSV for a given period. << Less than a year >>
    Parameters
    ----------
        stock_name: str
    Name of the stock
        from_date: str
    Fetch-From date in the string format (DATE_FMT_1)
        to_date
    Fetch-To date in the string format (DATE_FMT_1)
    Returns
    -------
        None
    """
    logger.info(f"Fetching data for stock: [{stock_name = }]")
    #TODO: Check that the year is less than 1
    dummy_res = dummy_request()
    payload = {
        'symbol':stock_name,
        'series':'["EQ"]',
        'from':from_date, 
        'to':to_date,
        "csv": "true",
    }
    stock_res = ""
    try:
        stock_res = requests.get(
            url=NSE_STOCK_HISTORY_URL,
            headers=REQ_HEADER,
            params=payload, 
            cookies=dummy_res.cookies,
            timeout=30,
            
        )
    except requests.exceptions.Timeout:
        logger.error(f"Timeout exception while fetching [{stock_name = }] for year [{from_date = }]")
        register_failed_fetch(stock_name, from_date, to_date, "requests.exceptions.Timeout" )
    except requests.exceptions.TooManyRedirects:
        logger.error(f"Too many redirects fetching [{stock_name = }] for year [{from_date = }]")
        register_failed_fetch(stock_name, from_date, to_date, "requests.exceptions.TooManyRedirects" )
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error fetching [{stock_name = }] for year [{from_date = }]")
        register_failed_fetch(stock_name, from_date, to_date, "requests.exceptions.ConnectionError" )
        logger.error(e)
    STOCK = SUPPORTED_FILE_TYPES["STOCK"]
    year = from_date[-4:]
    file_name = os.path.join(FILES_BASE_DIR, STOCK, f"{stock_name}_{year}.csv")
    if(stock_res and stock_res.status_code == HTTPStatus.OK):
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(stock_res.content.decode("utf-8")) #HACK: Keep this in mind for CSVs
            #NOTE: Write an entry into the history logfile
            set_stock_fetch_history(stock_name, from_date, to_date)
    else:
        # Something wrong happened while issuing fetch
        logger.error(f"Error occured while fetching [{stock_name = }]! for the year: [{year = }]")

def process_failed_fetches(file_name: str = ""):
    """Read the log file for failed fetches and try downloading them again.
    Parameters
    ----------
        file_path: str
    Path for the log file containing failed fetches.
    """
    logger.info(f"Processing failed fetches for file: [{file_name = }]")
    pass

def read_market_cap_from_file(stock_name: str) ->dict:
    STOCK = SUPPORTED_FILE_TYPES["STOCK"]
    file_name = os.path.join(FILES_BASE_DIR, STOCK, MCAP_FOLDER, f"{stock_name.upper()}.json")
    if os.path.exists(file_name):
        logger.debug(f"Market Cap file exists for [{stock_name = }]. Going to use it!")
        try:
            with open(file_name, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            logger.error(f"[file_name = ] not found!")
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from the file: [{file_name = }]")
    else:
        logger.info(f'File does not exist for [{stock_name = }]')
        #NOTE: Caller needs to fetch from remote. Caller to check for empty dict!
    return dict() #NOTE: Blank return for any error condition. Caller must check!

def fetch_market_cap(stock_name: str) -> dict:
    """Fetches the market cap for a stock.
    Parameters
    ----------
        stock_name: str
    The name of the stock.
    Returns
    -------
        dict
    Dictionary containing the details (along with market cap)
    """
    logger.debug(f'Fetching market cap for [{stock_name = }]')
    dummy_res = dummy_request()

    payload = {
        "symbol":stock_name,
        "section":"trade_info",
    }
    stock_quote_res = requests.get(
        url=NSE_STOCK_QUOTE_URL,
        headers=REQ_HEADER,
        params=payload,
        cookies=dummy_res.cookies,
        timeout=30)
    logger.debug(f"The stock_quote_res code is: [{stock_quote_res.status_code = }]")
    if(stock_quote_res.status_code == HTTPStatus.OK):
        #NOTE: Store the file inside the MCAP_FOLDER
        STOCK = SUPPORTED_FILE_TYPES["STOCK"]
        file_name = os.path.join(FILES_BASE_DIR, STOCK, MCAP_FOLDER, f"{stock_name.upper()}.json")
        with open(file_name, "w") as file:
            file.write(stock_quote_res.content.decode('utf-8'))
        return read_market_cap_from_file(stock_name)
    else:
        logger.error(f'HTTP Error occurred! [{stock_quote_res.status_code = }]')
        #TODO: Consider putting a retry logic here.
    return dict() # Empty dict return in case anything goes wrong
if __name__ == "__main__":
    # fetch_stock_data_for_a_year("UCOBANK", 2025)
    # get_stock_data_since_listing("UCOBANK")
    # get_stock_data_since_listing("UCOBANK")
    # get_stock_data_since_listing("HDFCBANK")
    # get_stock_data_since_listing("ICICIBANK")
    # get_listing_date(stock_name="9MMFSML")
    # fetch_market_cap("ICICIBANK")
    logger.info(read_market_cap_from_file("ICICIBANK1"))
