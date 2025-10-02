import os
from datetime import datetime
import requests
from http import HTTPStatus

import pandas as pd
from loguru import logger

from src.constants import INDEX_LIST_URL, INDEX_LIST_SKIPROWS, REQ_HEADER, FILES_BASE_DIR, DATE_FMT, INDEX_LIST_COLUMNS
from src.fetchers.common import dummy_request

def fetch_idx_list(file_type: str = "INDEX", trading_date:str = datetime.strftime(datetime.today(), DATE_FMT)):
    """ Fetch all the index names along with OHLC for a given trading date.
    """
    logger.info(f"Fetching details for the indices with [{file_type = }], [{trading_date = }]")
    df = pd.DataFrame()
    dummy_res = dummy_request("https://www.nseindia.com/market-data/live-market-indices") 
    payload = {
        "csv": "true",
    }
    idx_res = requests.get(
        url=INDEX_LIST_URL,
        headers=REQ_HEADER,
        params=payload,
        cookies=dummy_res.cookies,
        timeout=10
    )
    # https://www.nseindia.com/api/allIndices?csv=true
    if (idx_res.status_code == HTTPStatus.OK):
        
        with open(os.path.join(FILES_BASE_DIR, file_type.upper(), "raw/", f"{file_type.lower()}_{trading_date}_raw.csv"), "w") as file:
            file.write(idx_res.content.decode("utf-8"))
        # Read the same CSV and return as pandas dataframe
        df = pd.read_csv(os.path.join(FILES_BASE_DIR, file_type.upper(), "raw/", f"{file_type.lower()}_{trading_date}_raw.csv"), names=INDEX_LIST_COLUMNS, header=None, skiprows=INDEX_LIST_SKIPROWS)
        
        #NOTE: Raw file does not have TRADING_DATE column.
        # The calling block is adding the TRADING_DATE column
        # The csv file has trading_date in the file name
        # df.columns = pd.array(IDX_LIST_COLUMNS)
        df.to_csv(os.path.join(FILES_BASE_DIR, file_type.upper(), f"{file_type.lower()}_{trading_date}.csv"))
        # logger.info(idx_res.content)
    return df

def fetch_index_constituents(idx: str):
    """Fetch details about the index constituent.
    """
    #TODO:
    logger.info(f"Fetching details for the index [{idx = }] ")
    return

if __name__ == "__main__":
    fetch_idx_list(file_type="INDEX")
