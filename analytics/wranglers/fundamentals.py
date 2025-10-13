import json
import pandas as pd
import os

from loguru import logger

import src.constants as const
from src.helpers.validators import is_date_valid
from src.helpers.common import compose_dates_for_duration, compose_local_filename

def m_cap(folder: str) -> pd.DataFrame:
    """
    Reads the market cap JSON files from folder and creates structured data.

    Parameters
    ----------
        folder: str
    Folder containing the individual JSON files with market cap and other details.

    Returns
    -------
        pandas.DataFrame
    DF containing structured data
    """
    logger.debug(f'[{folder = }]')
    mcap_folder = os.path.join(const.FILES_BASE_DIR,\
                             const.SUPPORTED_FILE_TYPES["STOCK"],\
                             const.MCAP_FOLDER,\
                             folder)
    logger.debug(f'[{mcap_folder = }]')
    #NOTE: Check if the folder exists
    if not os.path.isdir(mcap_folder):
        logger.error(f'Invalid [{mcap_folder = }]')
        return pd.DataFrame()
    #NOTE: Read each file and extract market cap
    try:
        mcap_files = os.listdir(mcap_folder)
        mcap_dicts: list[dict] = list()
        for m_cap_file in mcap_files: #NOTE: Process each file
            mcap_json_file = os.path.join(mcap_folder, m_cap_file)
            # logger.debug(f'[{mcap_json_file = }]')
            with open(mcap_json_file, "r") as file:
                mcap_json = json.load(file)
                try:
                    mcap_dict = dict()
                    mcap_dict["STOCK"] = m_cap_file[:-4]
                    mcap_dict["FF_MCAP"] = mcap_json["marketDeptOrderBook"]["tradeInfo"]["ffmc"] 
                    mcap_dict["TOTAL_MCAP"] = mcap_json["marketDeptOrderBook"]["tradeInfo"]["totalMarketCap"]
                    mcap_dict["DATE_MCAP"] = folder
                    mcap_dicts.append(mcap_dict)
                except KeyError:
                    logger.error(f'Error reading m_cap for [{m_cap_file = }]')
        return pd.DataFrame(mcap_dicts)
    except FileNotFoundError:
        logger.error(f'Directory not found at [{mcap_folder = }]')
    except NotADirectoryError:
        logger.error(f'[{mcap_folder = }] is not a directory')
    except PermissionError:
        logger.error(f'Permission denied to access [{mcap_folder = }].')
    return pd.DataFrame()

def ratios(folder: str) -> pd.DataFrame:
    """Reads the STOCK/META/dd-Mon-YYYY folder for stock info 
    and returns ratios associated with the stock. (PE)

    Parameters
    ----------
        folder: str
    Folder containing the individual JSON files with PEs and other details.

    Returns
    -------
        pandas.DataFrame
    DF containing structured data
    """
    logger.debug(f'[{folder = }]')
    return pd.DataFrame()

def pe(file_type: str, instr_name: str, trading_dt: str, duration: str) -> pd.DataFrame:
    """Reads the PE files present in FILES_BASE_DIR/PE and gets teh data back
    """
    logger.debug(f'[{file_type = }], [{instr_name = }], [{trading_dt = }], [{duration = }], ')
    pe_folder = os.path.join(const.FILES_BASE_DIR, const.SUPPORTED_FILE_TYPES["PE"])
    if not pe_folder:
        logger.error(f'Something critically wrong! [{pe_folder = }]Does not exist.')
    match file_type:
        case "STOCK" if file_type == const.SUPPORTED_FILE_TYPES["STOCK"]:
            # NOTE: Read the folder data for the duration and trading date
            if trading_dt and is_date_valid(trading_dt):
                date_range = compose_dates_for_duration(trading_dt, duration)
                data_list: list[pd.DataFrame] = list()
                for trading_date in date_range:
                    #NOTE: Read the PE file for each trading_date
                    pe_file_name = compose_local_filename(const.SUPPORTED_FILE_TYPES["PE"],
                                               i_trading_date=trading_date,
                                               i_stock_name="",
                                               i_year="")

                    logger.debug(f'[{pe_file_name = }]')
                    if pe_file_name:
                        df = pd.read_csv(pe_file_name)
                        df["TRADING_DATE"] = trading_date #NOTE: Add trading_date col
                        data_list.append(df)
                    # END FOR each trading_date
                if instr_name:
                    all_data: pd.DataFrame = pd.concat(data_list, ignore_index=True)
                    only_stock:pd.DataFrame = all_data[all_data.SYMBOL == instr_name] # pyright: ignore [reportAssignmentType]
                    if (not all_data.empty) and (type(only_stock) == pd.DataFrame) :
                        return only_stock
                return pd.concat(data_list, ignore_index=True)
            # NOTE: Filter out the instr_name if provided
            return pd.DataFrame()
        case "INDEX" if file_type == const.SUPPORTED_FILE_TYPES["INDEX"]:
            logger.error(f'Not implemented for [{file_type = }]')
            return pd.DataFrame()
        case _:
            logger.error(f'Invalid [{file_type = }]')
    return pd.DataFrame()
if __name__ == "__main__":
    # print(m_cap("09-Oct-2025"))
    logger.debug(pe(file_type="STOCK",
                    instr_name="NESTLEIND",
                    trading_dt="10-Oct-2025",
                    duration="MONTH"))
