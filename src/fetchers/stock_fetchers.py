from datetime import datetime
import json
import os
from http import HTTPStatus
import pandas as pd
import requests
from loguru import logger
from src.fetchers.common import dummy_request
from src.constants import DATE_FMT_1, SUPPORTED_FILE_TYPES, FILES_BASE_DIR, NSE_STOCK_HISTORY_URL, NSE_STOCK_QUOTE_URL, REQ_HEADER,FILES_BASE_DIR

def fetch_stock_data(stock_name: str, trading_date: str) -> pd.DataFrame:
    """
        Fetches the stock data from remote and stores in local file.

    Parameters
    ----------
       stock_name: str
    name of the stock
        trading_date: str
    Trading date in the format of DD-Mon-YYYY. e.g., 12-Jun-2025

    Returns
    -------
        pandas.DataFrame
    Containing the data that is read from remote.

    NOTE:
    ----
        You can not fetch data for a historical date; Rather you fetch as-of-now
        And stamp the data for the provided date.
    """
    logger.info(f"Fetching data for [{stock_name}], for [{trading_date}]")
    dummy_res = dummy_request()
    
    #NOTE: First get ths listing date of the stock
    stock_listing_date = get_listing_date(stock_name)
    #NOTE: NSE allows only upto 1-year download. So, divide the timeframe
    stock_listing_year = stock_listing_date[-4:]
    current_year = datetime.now().year
    logger.debug(f"stock_name: [{stock_name}], stock_listing_date: [{stock_listing_date}], stock_listing_year: [{stock_listing_year}], current_year: [{current_year}]")
    STOCK = SUPPORTED_FILE_TYPES["STOCK"]
    for year in range(int(stock_listing_year), current_year+1):
        # logger.info(year)
        #NOTE: If a file exists for a year then skip fetch for that year
        file_name = os.path.join(FILES_BASE_DIR, STOCK, f"{stock_name}_{year}.csv")
        if os.path.exists(file_name):
            continue
        from_date = datetime(year, 1, 1).strftime(DATE_FMT_1)
        to_date = datetime(year, 12, 31).strftime(DATE_FMT_1)
        logger.debug(f"Fetching from: [{from_date}], to: [{to_date}]")
        payload = {
            'symbol':stock_name,
            'series':'["EQ"]',
            'from':from_date,
            'to':to_date,
            "csv": "true",
        }
        stock_res = requests.get(
            url=NSE_STOCK_HISTORY_URL,
            headers=REQ_HEADER,
            params=payload, 
            cookies=dummy_res.cookies,
            timeout=8,
            
        )
        if(stock_res.status_code == HTTPStatus.OK):
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(stock_res.content.decode("utf-8")) #HACK: Keep this in mind for CSVs
    #NOTE: Now, read and combine all individual files
    return pd.DataFrame()

def get_listing_date(stock_name: str)->str:
    logger.info(f"Getting listing date for [{stock_name}]")
    #NOTE: If there is a file already present, use it!
    listing_date = read_listing_date_from_file(stock_name)
    if listing_date:
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
        timeout=8)
    logger.debug(f"The stock_quote_res code is: [{stock_quote_res.status_code}]")
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
        logger.info(f"Meta file exists for [{stock_name}]. Going to use it!")
        try:
            with open(file_name, "r") as file:
                data = json.load(file)
                logger.info(f"Listing Date: [{data['metadata']['listingDate']}]")
                return data['metadata']['listingDate']
        except FileNotFoundError:
            logger.error(f"[file_name] not found!")
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from the file: [{file_name}]")
    return "" #NOTE: Blank return for any error condition. Caller must check!

