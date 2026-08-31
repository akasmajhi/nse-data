"""
Central code for all the app specific validators.
"""

import json

import pandas as pd
import os
import glob
from datetime import datetime
from loguru import logger
from src.constants import SUPPORTED_FILE_TYPES, NSE_HOLIDAYS, FILES_BASE_DIR


def is_file_type_valid(file_type: str):
    """
        Checks to see if the file type is valid.
        Valid types are defined in constants.


    Parameters
    ----------
        file_type : str
    The type pf file required.

    Returns
    -------
        boolean : True/False
    """
    logger.debug(f"file type {file_type.upper() = }")
    # logger.debug(f"Supported File Types: {SUPPORTED_FILE_TYPES}")
    return file_type.upper() in SUPPORTED_FILE_TYPES
    # return True if file_type.upper() in SUPPORTED_FILE_TYPES else False


def is_date_valid(i_date: str):
    """
        The string i_date ('DD-Mon-YYYY') is checked for validity of format and
        prevents future dates.

    Parameters
    ----------
        i_date: str
    Input date in the format of DD-Mon-YYYY. e.g., 14-Jun-2025

    Returns
    -------
        boolean
    True if the date is valid.
    """
    logger.debug(f"Input date [{i_date = }]")
    trading_dt = ""
    if len(i_date.split("-")) == 3:
        try:
            trading_dt = datetime.strptime(i_date, "%d-%b-%Y")
            if datetime.today() > trading_dt:
                return True
            else:
                logger.error(f"Future date [{i_date = }]Not Allowed!")
                return False
        except ValueError:
            logger.error(
                f"Invalid date [{i_date = }]passed. Reqd. format is DD-Mon-YYYY"
            )
            return False


def is_NSE_holiday(trading_dt: str):
    """Checks to see if the date provided is a NSE/exchange holiday or not
    Parameters
    ----------
        trading_dt: str
    Trading date in constants.DATE_FMT format
    Returns
    -------
        boolean
    If the date is not a NSE/exchange holiday. False otherwise.
    """
    # Check if it is a valida date
    # Check if the valid date is in NSE holiday list
    logger.debug(f"Checking nse holiday for: [{trading_dt = }]")
    if is_date_valid(trading_dt):
        # Get the year from the trading date
        yyyy = trading_dt[-4:]
        # logger.debug(f"Getting holday list for {yyyy}")
        try:
            NSE_HOLIDAY_LIST = NSE_HOLIDAYS[yyyy]
            # If no holiday list then DONOT proceed
            if len(NSE_HOLIDAYS) == 0:
                logger.error(f"No NSE holiday calendar found for [{yyyy = }]")
                return True
            # logger.debug(f"Holiday list: [{NSE_HOLIDAY_LIST = }]")
            # check if trading date is in the holiday list
            if trading_dt.upper() in NSE_HOLIDAY_LIST:
                logger.info(f"[{trading_dt = }] is a holiday!")
                return True
        except KeyError:
            logger.error(f"Holiday list not present for [{yyyy = }]")
            # Do not fetch any data if calendar is absent in constants.py
            return True
    return False


def get_latest_file(file_type_or_path: str) -> pd.DataFrame:
    """Reads the latest file type from the file system and returns the DF

    Parameters
    ----------
        file_type: str
    Should be a valid file type as present in constans.SUPPORTED_FILE_TYPES

    Return
    ------
        pd.DataFrame
    Pandas DataFrame containing the contents of the file, if found. Else empty DF.
    """

    # NOTE Is this a folder?
    if os.path.isdir(file_type_or_path):
        logger.info(f"Files path: [{file_type_or_path = }]")
        return latest_file_in_folder(file_type_or_path)
    if file_type_or_path not in SUPPORTED_FILE_TYPES.values():
        # NOTE: Invalid file type provided.
        logger.error(f"Invalid file type: [{file_type_or_path = }]")
        return pd.DataFrame()
    # NOTE: Valid File type handling
    files_path = os.path.join(FILES_BASE_DIR, file_type_or_path, "*")
    logger.info(f"Files path: [{files_path = }]")
    files_list = glob.glob(files_path)
    # Filter out directories; Keep only files
    only_files = [f for f in files_list if os.path.isfile(f)]
    if not only_files:
        logger.error(f"No files found for file_type: [{file_type_or_path = }]")
        return pd.DataFrame()
    latest_file = max(only_files, key=os.path.getmtime)
    # logger.info(f"The latest file is: [{latest_file = }]")
    # Now read the content and return the DF
    try:
        with open(latest_file, "r") as f:
            # NOTE: This file may not always be CSV. Handles JSON as well.
            if "csv" in latest_file:
                return pd.read_csv(f)
            if "json" in latest_file:
                return pd.read_json(f)
            logger.error(f"Unknown File Type for file: [{f = }]")
            return pd.DataFrame()
    except IOError:
        logger.error(f"Error reading file: [{latest_file = }]")
        return pd.DataFrame()


def latest_file_in_folder(folder_name: str):
    files_list = glob.glob(os.path.join(folder_name, "*"))
    # Filter out directories; Keep only files
    only_files = [f for f in files_list if os.path.isfile(f)]
    if not only_files:
        logger.error(f"No files found in folder: [{folder_name = }]")
        return pd.DataFrame()
    latest_file = max(only_files, key=os.path.getmtime)
    logger.debug(f"The [{latest_file = }]")
    # logger.info(f"The latest file is: [{latest_file = }]")
    # Now read the content and return the DF
    try:
        with open(latest_file, "r") as f:
            # NOTE: This file may not always be CSV. Handles JSON as well.
            if "csv" in latest_file:
                return pd.read_csv(f)
            if "json" in latest_file:
                data = json.load(f)
                # df = pd.json_normalize(data)
                # logger.debug(f"[{df.keys() = }]")
                return latest_file
            logger.error(f"Unknown File Type for file: [{f = }]")
            return pd.DataFrame()
    except IOError:
        logger.error(f"Error reading file: [{latest_file = }]")
        return pd.DataFrame()


def is_stock_valid(stock_name: str) -> bool:
    """Checks to see if the stock name is valid.
    The stock name is validated against the latest bhavcopy file.
    """
    logger.debug(f"The stock name is: [{stock_name = }]")
    if not stock_name:
        logger.error(f"Invalid stock name: [{stock_name = }]")
        return False
    # NOTE: Get the latest BHAVCOPY
    latest_bhavcopy = get_latest_file(SUPPORTED_FILE_TYPES["BHAVCOPY"])
    if latest_bhavcopy.empty:
        logger.error(f"Problem getting the bhavopy while looking for [{stock_name = }]")
        return False
    # NOTE: Check if the stock name is present in the latest bhavcopy
    symbol_col_name = "TckrSymb"
    try:
        if stock_name in latest_bhavcopy[symbol_col_name].unique():
            return True
    except KeyError:
        logger.error(f"Stock column name [{symbol_col_name = }] is invalid")
    logger.error(f"Error Occured while validating stock [{stock_name = }]")
    return False


# if __name__ == "__main__":
#     print(is_stock_valid("INFY"))
