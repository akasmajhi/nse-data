import requests
from http import HTTPStatus
import os

import pandas as pd
from loguru import logger

from src.constants import FILES_BASE_DIR

def fetch_data(file_type: str, trading_date: str):
    """
        Fetches the data from remote and stores in local file.

    Parameters
    ----------
       file_type: str
    What type of file sought (PE, BHAVCOPY, etc.)
        trading_date: str
    Trading date in the format of DD-Mon-YYYY. e.g., 12-Jun-2025

    Returns
    -------
        pandas.DataFrame
    Containing the data that is read from remote.
    True if the fetch was successful. False otherwise.
    """
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "authority":"www.nseindia.com",
        "method":"GET",
        "scheme":"https",
        "accept":"*/*",
        "referer":"https://www.nseindia.com/",
        "sec-fetch-site":"same-origin",
        "sec-fetch-mode":"cors",
        "sec-fetch-dest":"empty",
    }
    df = pd.DataFrame()

    # Block for fetching PE files
    if (file_type.lower() == 'pe'):
        logger.debug(f"Fetching [{file_type}] for trading date: [{trading_date}]")
        tmp_url = 'https://www.nseindia.com/all-reports'
        session = requests.Session()
        r = session.get(url=tmp_url, headers=headers)
        nse_reports_url = 'https://www.nseindia.com/api/reports'

        payload = {
            'archives':'[{"name":"PE Ratio","type":"daily-reports","category":"capital-market","section":"equities"}]',
            'date':trading_date,
            'type':'equities',
            'mode':'single',
        }
        pe_res = requests.get(
            url=nse_reports_url,
            headers=headers,
            params=payload, 
            cookies=r.cookies,
            timeout=8)
        logger.info(f"PE Response code: [{pe_res.status_code}]")
        if(pe_res.status_code == HTTPStatus.OK):
            # Write the data to the file
            with open(os.path.join(FILES_BASE_DIR, "PE", f"pe_{trading_date}.csv"), "w") as file:
                file.write(pe_res.text)
            # Read the same CSV and return as pandas dataframe
            df = pd.read_csv(os.path.join(FILES_BASE_DIR, "PE", f"pe_{trading_date}.csv"))
            logger.info(f"Data Size is: [{df.size}]")
            return df 
    return df

if __name__ == "__main__":
    logger.debug(f"Main Invoked")
    fetch_data('PE', '22-Jun-2025')





