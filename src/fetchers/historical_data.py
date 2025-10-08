from datetime import datetime
import requests
from http import HTTPStatus
import os
from io import BytesIO
import zipfile
import json

import pandas as pd
from loguru import logger

from src.constants import FILES_BASE_DIR, REQ_HEADER, NSE_REPORTS_URL, DATE_FMT, NSE_PREOPEN_URL, PREOPEN_SKIPROWS, PREOPEN_PAYLOADS, NSE_DUMMY_REQ_URL, SUPPORTED_FILE_TYPES, NSE_STOCK_INDICES

from src.fetchers.common import dummy_request
from src.fetchers import idx_fetchers

def fetch_data(file_type: str, trading_date: str) -> pd.DataFrame:
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
    # Processing for NOTE: PE
    if (file_type.lower() == 'pe'):
        logger.debug(f"Fetching [{file_type = }] for [{trading_date = }]")

        dummy_res = dummy_request(NSE_DUMMY_REQ_URL)

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
    # Processing for NOTE: BHAVCOPY
    if (file_type.lower() == 'bhavcopy'):
        logger.info(f"Fetching [{file_type = }] for [{trading_date = }]")
        dummy_res = dummy_request(NSE_DUMMY_REQ_URL)

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

    if (file_type.lower() == "preopen"):
        # Currently, we can fetch preopen for the current day
        #NOTE: PREOPEN is valid only for the current day. 
        # Exchanges do not have mechanism for historical dates being processed for PREOPEN
        trading_date = datetime.strftime(datetime.today(), DATE_FMT)
        logger.debug(f"Fetching [{file_type = }] for [{trading_date = }]")
        dummy_res = dummy_request(NSE_DUMMY_REQ_URL)

        for payload in PREOPEN_PAYLOADS:
            preopen_res = requests.get(
                url=NSE_PREOPEN_URL,
                headers=REQ_HEADER,
                params=PREOPEN_PAYLOADS[payload], 
                cookies=dummy_res.cookies,
                timeout=8)
            if(preopen_res.status_code == HTTPStatus.OK):
                # Write the data to the file
                with open(os.path.join(FILES_BASE_DIR, "PREOPEN", f"preopen_{payload}_{trading_date}.csv"), "w", encoding="utf-8") as file:
                    file.write(preopen_res.text)
                # Read the same CSV and return as pandas dataframe
                data = pd.read_csv(os.path.join(FILES_BASE_DIR, "PREOPEN", f"preopen_{payload}_{trading_date}.csv"), encoding="utf-8", skiprows=PREOPEN_SKIPROWS)
                df = pd.concat([df, data])
        return df 
    if (file_type.lower() == SUPPORTED_FILE_TYPES["FNOBHAVCOPY"].lower()):
        FNOBHAVCOPY = SUPPORTED_FILE_TYPES["FNOBHAVCOPY"]
        logger.info(f"Fetching [{file_type = }] for [{trading_date = }]")
        dummy_res = dummy_request(NSE_DUMMY_REQ_URL)

        payload = {
            'archives':'[{"name":"F&O - UDiFF Common Bhavcopy Final (zip)","type":"archives","category":"derivatives","section":"equity"}]',
            'date':trading_date,
            'type':'equity',
            'mode':'single',
        }
        fno_bhavcopy_res = requests.get(
            url=NSE_REPORTS_URL,
            headers=REQ_HEADER,
            params=payload, 
            cookies=dummy_res.cookies,
            timeout=8)
        # logger.info(f"BHAVCOPY Response code: [{bhavcopy_res.status_code}]")
        if(fno_bhavcopy_res.status_code == HTTPStatus.OK):
            zip_in_mem = BytesIO(fno_bhavcopy_res.content)
            with zipfile.ZipFile(zip_in_mem, 'r') as zf:
                # List contents/file names
                for name in zf.namelist():
                    with zf.open(name) as fno_bhavcopy:
                        fno_bhavcopy_content = fno_bhavcopy.read().decode('utf-8')
                        # Write the data to the file
                        with open(os.path.join(FILES_BASE_DIR, 
                                               FNOBHAVCOPY, 
                                               f"{FNOBHAVCOPY.lower()}_{trading_date}.csv"), 
                                  "w") as file:
                            file.write(fno_bhavcopy_content)
            # Read the same CSV and return as pandas dataframe
            df = pd.read_csv(os.path.join(FILES_BASE_DIR, 
                                          FNOBHAVCOPY, 
                                          f"{FNOBHAVCOPY.lower()}_{trading_date}.csv"))
            return df 
        else:
            logger.error(f"Error getting response for [{trading_date = }], [{file_type = }]")
            logger.error(f"The error URL is: [{fno_bhavcopy_res.url = }]")
    if (file_type.lower() == "index"):
        return idx_fetchers.fetch_idx_list(file_type)
    return df

def fetch_index_constituents_data(index_name: str) -> list:
    logger.debug(f"Fetching the constituents for index: [{index_name = }]")
    dummy_res = dummy_request(NSE_DUMMY_REQ_URL)
    payload = {
        'index':index_name,
    }
    res = requests.get(
        url=NSE_STOCK_INDICES,
        headers=REQ_HEADER,
        params=payload, 
        cookies=dummy_res.cookies,
        timeout=8)
    logger.info(f"The URL formed isL [{res.url = }]")
    if(res.status_code == HTTPStatus.OK):
        # Write the data to the file
        file_type:str = SUPPORTED_FILE_TYPES["IDX_CONSTITUENTS"]
        file_name = os.path.join(FILES_BASE_DIR,
                                        file_type.upper(),
                                        f'{file_type.lower()}_{index_name}.json')
        with open(file_name, "w") as file:
            file.write(res.text)
        data = json.load(open(file_name))
        df = pd.DataFrame(data["data"])
        return list(df["symbol"][1:])
    logger.error(f"Seems like url fetch error for index [{index_name = }]")
    return list() # Blank list returned in case of fetch error


if __name__ == "__main__":
    logger.debug(f"Main Invoked")
    # fetch_data('PREOPEN', '22-Jan-2025')
    fetch_data('PE', '22-Jun-2025')





