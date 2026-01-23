import os
import json

import pandas as pd
from loguru import logger

import src.constants as C
from src.fetchers.common import get_last_fetch_date
from src.helpers.file_readers import get_local_stock_info
from src.helpers.cross_cutting import benchmark


@benchmark
def industry_to_stock(i_trading_date: str | None, i_file_name: str | None) -> dict:
    """For a given trading_date, this function returns a map of the
    industry-to-stocks in the form of a dict where the key the is
    the industry and the value is the list of stocks in that industry.

    Parameters:
    -----------
        i_trading_date:str
    The trading date.
        i_file_name: str
    Fully qualified file name of the derived ind_to_stock file.

    Returns
    -------
        dict
    dictionary containing the industry-to-stock mapping.
    """
    logger.info(f"[{i_file_name = }], [{i_trading_date = }]")
    if i_file_name is None and i_trading_date is None:
        logger.error(
            f"Need to provided at least 1 param. [{i_file_name = }], [{i_trading_date = }]"
        )
        return dict()
    if (
        i_file_name is not None
    ):  # NOTE: i_file_name takes precendence over i_trading_date
        file_name = i_file_name
    else:
        file_name = os.path.join(
            C.FILES_BASE_DIR,
            C.SUPPORTED_FILE_TYPES["DERIVED"],
            C.IND_TO_STOCK_FOLDER,
            f"{C.IND_TO_STOCK_FOLDER}-{i_trading_date}.json",
        )
    if file_name:
        logger.info(f"File existing [{file_name = }]!")
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                data: dict = json.load(file)
            return data
        except FileNotFoundError:
            logger.error(f"{file_name = } does not exist!")
            return dict()
        except json.JSONDecodeError:
            logger.error(f"Error decoding {file_name = }")
            return dict()

    else:
        logger.error(f"{file_name = } does not exist!")
        return dict()


@benchmark
def get_pe_for_industry(i_industry: str, i_trading_date: str | None) -> dict:
    """For a given trading_date, this function returns a map of the
    industry-to-PE in the form of a dict where the key the is
    the stock name(belonging to that industry) and the value is the
    PE that company.

    Parameters:
    -----------
        trading_date:str
    The trading date.

    Returns
    -------
        dict
    dictionary containing the industry-to-stock mapping.
    """
    logger.debug(f"[{i_industry = }], [{i_trading_date = }]")
    # NOTE: If no date is provided then use the latest data
    if i_trading_date is None:
        files_dir = os.path.join(
            C.FILES_BASE_DIR, C.SUPPORTED_FILE_TYPES["DERIVED"], C.IND_TO_STOCK_FOLDER
        )
        files: list = list()
        try:
            files = os.listdir(os.path.join(files_dir))
            if not files:
                logger.error(f"No data found in [{files_dir}]")
                return dict()
            logger.debug(f"all [{files = }]")
            all_files: list = list()
            for f in files:
                all_files.append(os.path.join(files_dir, f))
            latest_file = max(all_files, key=os.path.getmtime)
            ind_map = industry_to_stock(i_file_name=latest_file, i_trading_date=None)
            # logger.info(f"[{ind_map.keys() = }]")
            if i_industry not in ind_map.keys():
                logger.error(f"Non-existing [{i_industry = }] passed!")
                return dict()
            stocks = ind_map.get(i_industry)
            logger.info(f"[{stocks = }]")
            logger.debug(f"[{latest_file = }]")
            return_dict: dict = dict()
            if stocks:
                # NOTE: Read the STOCK/META/{trading_date} folder for PE
                trading_date: str = latest_file[-16:-5]
                for stock in stocks:
                    stock_meta = get_local_stock_info(
                        stock=stock, trading_date=trading_date
                    )
                    return_dict[stock] = stock_meta["metadata"]["pdSymbolPe"]
                return return_dict
        except OSError as e:
            logger.error(f"[{files_dir = }] does not exist! {e}")
            logger.info(f"[{files = }]")
            return dict()  # NOTE: Returning blank dict on error condition

    # NOTE: If a date is provided then use it.

    file_name = os.path.join(
        C.FILES_BASE_DIR,
        C.SUPPORTED_FILE_TYPES["DERIVED"],
        C.IND_TO_STOCK_FOLDER,
        f"ind_to_stock-{i_trading_date}.json",
    )
    if not os.path.exists(file_name):
        logger.error(f"No file [{i_trading_date = }], [{file_name = }]")
        return dict()
    ind_map = industry_to_stock(i_file_name=file_name, i_trading_date=None)
    stocks = ind_map.get(i_industry)
    return_dict: dict = dict()
    if stocks:
        try:
            # NOTE: Read the STOCK/META/{trading_date} folder for PE
            trading_date: str = file_name[-16:-5]
            for stock in stocks:
                stock_meta = get_local_stock_info(
                    stock=stock, trading_date=trading_date
                )
                return_dict[stock] = stock_meta["metadata"]["pdSymbolPe"]
            return return_dict
        except OSError as e:
            logger.error(f"Error Occured! {e}")
            return dict()  # NOTE: Returning blank dict on error condition

    logger.error(f"No stocks for [{i_industry = }]")
    return dict()


@benchmark
def combined_m_caps(folder: str) -> dict:
    """Read combined m_cap file for efficiency.
    Parameters
    ----------
        str
    Market Cap folder that contains combined m_cap file.

    Returns
    -------
        dict
    Dictionary containing the combined market caps.
    {"STOCK": total_m_cap} format.

    Note
    ----
    File name is hard-coded to combined.json
    """
    logger.info(f"Combining market caps for [{folder = }]")
    # NOTE: Check if the folder exists
    mcap_folder = os.path.join(
        C.FILES_BASE_DIR,
        C.SUPPORTED_FILE_TYPES["STOCK"],
        C.MCAP_FOLDER,
        folder,
    )
    if not os.path.isdir(mcap_folder):
        logger.error(f"Invalid [{mcap_folder = }]")
        return dict()
    # ERROR: if the combined file does not exist then it's an error
    combined_m_cap_file_name: str = os.path.join(mcap_folder, "combined.json")
    if not os.path.isfile(combined_m_cap_file_name):
        logger.error(f"Combined file [{combined_m_cap_file_name = }]DOES NOT exists!")
        logger.info(f"Use the writers.combine_m_caps for writing content")
        return {}
    output_filename = os.path.join(mcap_folder, "combined.json")
    data: dict = dict()
    mcap_dict: dict = dict()
    with open(output_filename, "r") as json_file:
        data = json.load(json_file)

    for key in data.keys():
        try:
            mcap_dict[key] = data[key]["marketDeptOrderBook"]["tradeInfo"][
                "totalMarketCap"
            ]
        except KeyError:
            logger.error(f"Error reading market cap for [{key = }]")
    return mcap_dict


def read_weekly_data(start_date: str, file_type: str) -> pd.DataFrame | None:
    """
    Reads the weekly file from local file system.
    """
    logger.info(f"Reading weekly file for [{start_date = }]")
    if file_type == C.SUPPORTED_FILE_TYPES["STOCK"]:
        file_name = os.path.join(
            C.FILES_BASE_DIR,
            C.SUPPORTED_FILE_TYPES["DERIVED"],
            C.WEEKLY_FOLDER,
            C.SUPPORTED_FILE_TYPES["STOCK"],
            f"{start_date}.csv",
        )
        logger.debug(f"Reading CSV path [{file_name}]")
        if os.path.exists(file_name):
            return pd.read_csv(file_name)
        else:
            logger.info(f"Local weekly file does not exist for [{start_date}]")
            return None
    return None


if __name__ == "__main__":
    # print(get_industry_to_stock(i_trading_date="18-Oct-2025", i_file_name=None))
    print(industry_to_stock(get_last_fetch_date("META"), i_file_name=None))
