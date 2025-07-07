import requests
from http import HTTPStatus
import os
from io import BytesIO
import zipfile

import pandas as pd
from loguru import logger

from src.constants import FILES_BASE_DIR, REQ_HEADER, NSE_REPORTS_URL

def dummy_request():
    tmp_url = 'https://www.nseindia.com/all-reports'
    session = requests.Session()
    r = session.get(url=tmp_url, headers=REQ_HEADER)
    return r

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
    df = pd.DataFrame()

    # Block for fetching PE files
    if (file_type.lower() == 'pe'):
        logger.debug(f"Fetching [{file_type}] for trading date: [{trading_date}]")

        dummy_res = dummy_request()

        payload = {
            'archives':'[{"name":"PE Ratio","type":"daily-reports","category":"capital-market","section":"equities"}]',
            'date':trading_date,
            'type':'equities',
            'mode':'single',
        }
        pe_res = requests.get(
            url=NSE_REPORTS_URL,
            headers=REQ_HEADER,
            params=payload, 
            cookies=dummy_res.cookies,
            timeout=8)
        if(pe_res.status_code == HTTPStatus.OK):
            # Write the data to the file
            with open(os.path.join(FILES_BASE_DIR, "PE", f"pe_{trading_date}.csv"), "w") as file:
                file.write(pe_res.text)
            # Read the same CSV and return as pandas dataframe
            df = pd.read_csv(os.path.join(FILES_BASE_DIR, "PE", f"pe_{trading_date}.csv"))
            return df 

    # For bhavcopy specific fetch
    if (file_type.lower() == 'bhavcopy'):
        logger.debug(f"Fetching [{file_type}] for trading date: [{trading_date}]")
        dummy_res = dummy_request()

        payload = {
            'archives':'[{"name":"CM-UDiFF Common Bhavcopy Final (zip)","type":"daily-reports","category":"capital-market","section":"equities"}]',
            'date':trading_date,
            'type':'equities',
            'mode':'single',
        }
        bhavcopy_res = requests.get(
            url=NSE_REPORTS_URL,
            headers=REQ_HEADER,
            params=payload, 
            cookies=dummy_res.cookies,
            timeout=8)
        # logger.info(f"BHAVCOPY Response code: [{bhavcopy_res.status_code}]")
        if(bhavcopy_res.status_code == HTTPStatus.OK):
            zip_in_mem = BytesIO(bhavcopy_res.content)
            with zipfile.ZipFile(zip_in_mem, 'r') as zf:
                # List contents/file names
                for name in zf.namelist():
                    with zf.open(name) as bhavcopy:
                        bhavcopy_content = bhavcopy.read().decode('utf-8')
                        # Write the data to the file
                        with open(os.path.join(FILES_BASE_DIR, "BHAVCOPY", f"bhavcopy_{trading_date}.csv"), "w") as file:
                            file.write(bhavcopy_content)
            # Read the same CSV and return as pandas dataframe
            df = pd.read_csv(os.path.join(FILES_BASE_DIR, "BHAVCOPY", f"bhavcopy_{trading_date}.csv"))
            # logger.info(f"Data Size is: [{df.size}]")
            return df 

    return df

if __name__ == "__main__":
    logger.debug(f"Main Invoked")
    fetch_data('PE', '22-Jun-2025')





