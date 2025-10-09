import os
import pandas as pd
from loguru import logger
from analytics.wranglers.fundamentals import m_cap
from src.constants import SUPPORTED_FILE_TYPES, MCAP_SOURCE
from src.fetchers.common import get_last_fetch_date

def get_market_cap(file_type: str, instr_name: str, source: str = MCAP_SOURCE["LAST_FETCHED"]) -> pd.DataFrame:
    """Returns the market cap along with other info.
    Parameters
    ----------
        file_type: str
    The file type could be any of the src.constants.SUPPORTED_FILE_TYPES
        source: str
    The source could be "last_fetched", -X- or "for any given date" -X- or "latest/today's".
    The source is validated against src.constants.MCAP_SOURCE

    """
    logger.info(f'[{file_type = }], [{source = }], [{instr_name}]')
    data = pd.DataFrame()
    #NOTE: Validation - 1 for checking file_type
    if file_type not in SUPPORTED_FILE_TYPES:
        logger.error(f'Invalid [{file_type = }]')
        return data
    #NOTE: Validation - 2 for checking source
    if source not in MCAP_SOURCE:
        logger.error(f'Invalid [{source = }]')
        return data

    match file_type:
        case "STOCK" if file_type == SUPPORTED_FILE_TYPES["STOCK"]:
            if instr_name: # NOTE: TODO: Market cap for a particular stock
                if source == MCAP_SOURCE["LAST_FETCHED"]: #NOTE: For last fetch date
                    pass
                else: #NOTE: For a particular date
                    pass
            else: #NOTE: Market cap for all the stocks
                if source == MCAP_SOURCE["LAST_FETCHED"]: #NOTE: For last fetch date
                    latest_fetch_folder = get_last_fetch_date(SUPPORTED_FILE_TYPES["MARKET_CAP"])
                    last_fetch_folder = latest_fetch_folder if latest_fetch_folder else ""
                    return m_cap(last_fetch_folder)
                    
                else: #NOTE: For a particular date
                    return m_cap(source) #TODO: source should be a valid date
        case "INDEX" if file_type == SUPPORTED_FILE_TYPES["INDEX"]:
            pass
        case _:
            logger.error(f'Invalid [{file_type = }]' )
            return data #NOTE: Unsupported file type

    return pd.DataFrame()

if __name__ == "__main__":
    get_market_cap(file_type="INVALID", instr_name="", source="INVALID").empty
    get_market_cap(file_type="STOCK", instr_name="", source="INVALID").empty
    # get_market_cap(file_type="STOCK", instr_name="", source="LAST_FETCHED").empty
    print(get_market_cap(file_type="STOCK", instr_name="", source="LAST_FETCHED"))
