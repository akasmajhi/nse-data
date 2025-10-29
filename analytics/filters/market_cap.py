import pandas as pd
from loguru import logger
from analytics.wranglers.fundamentals import m_cap
from src.constants import SUPPORTED_FILE_TYPES, MCAP_SOURCE
from src.fetchers.common import get_last_fetch_date
from src.core import get_index_names, get_index_constituents
from src.core import get_market_cap as src_core_m_cap


def get_market_cap(
    file_type: str, instr_name: str, source: str = MCAP_SOURCE["LAST_FETCHED"]
) -> pd.DataFrame:
    """Returns the market cap along with other info.
    Parameters
    ----------
        file_type: str
    The file type could be any of the src.constants.SUPPORTED_FILE_TYPES
        source: str
    The source could be "last_fetched", -X- or "for any given date" -X- or "latest/today's".
    The source is validated against src.constants.MCAP_SOURCE

    """
    logger.info(f"[{file_type = }], [{source = }], [{instr_name}]")
    data = pd.DataFrame()
    # NOTE: Validation - 1 for checking file_type
    if file_type not in SUPPORTED_FILE_TYPES:
        logger.error(f"Invalid [{file_type = }]")
        return data
    # NOTE: Validation - 2 for checking source
    if source not in MCAP_SOURCE:
        logger.error(f"Invalid [{source = }]")
        return data

    match file_type:
        case "STOCK" if file_type == SUPPORTED_FILE_TYPES["STOCK"]:
            if instr_name:  # NOTE: TODO: Market cap for a particular stock
                if source == MCAP_SOURCE["LAST_FETCHED"]:  # NOTE: For last fetch date
                    pass
                else:  # NOTE: For a particular date
                    pass
            else:  # NOTE: Market cap for all the stocks
                if source == MCAP_SOURCE["LAST_FETCHED"]:  # NOTE: For last fetch date
                    latest_fetch_folder = get_last_fetch_date(
                        SUPPORTED_FILE_TYPES["MARKET_CAP"]
                    )
                    last_fetch_folder = (
                        latest_fetch_folder if latest_fetch_folder else ""
                    )
                    return m_cap(last_fetch_folder)
                else:  # NOTE: For a particular date
                    return m_cap(source)  # TODO: source should be a valid date
        case "INDEX" if file_type == SUPPORTED_FILE_TYPES["INDEX"]:
            pass
        case _:
            logger.error(f"Invalid [{file_type = }]")
            return data  # NOTE: Unsupported file type

    return pd.DataFrame()


def get_idx_market_cap(index: str, trading_date: str = "") -> dict | None:
    """Gets the market at the basket level. It's an aggregated market cap.
    Parameters
    ----------

    idx : str
        The name of the index as presented in the index listing page.
        https://www.nseindia.com/market-data/live-market-indices

    Returns
    -------
    pandas.DataFrame
        Data Frame containing the results
    """
    logger.info(f"[{index = }], [{trading_date = }]")
    # NOTE: Get all valid indeax names and check that incoming index is valid
    valid_indices: list[str] = get_index_names()
    if index not in valid_indices:
        logger.error(f"[{index = }] is invalid!")
        return None
    # TODO: For the valid index, get all it's constituents
    index_constituents = get_index_constituents(index_name=index)
    if not index_constituents:
        logger.error(f"Something is wrong! [{index_constituents = }] for [{index = }]")
        return None
    # TODO: For each constituent, get it's market cap and aggregate
    for item in index_constituents:
        # m_cap = src_core_m_cap(file_type='STOCK', stock_name=item)
        # logger.debug(m_cap)
        pass
    return {"NIFTY 50": 10_000}


if __name__ == "__main__":
    # get_market_cap(file_type="INVALID", instr_name="", source="INVALID").empty
    # get_market_cap(file_type="STOCK", instr_name="", source="INVALID").empty
    # get_market_cap(file_type="STOCK", instr_name="", source="LAST_FETCHED").empty
    # print(get_market_cap(file_type="STOCK", instr_name="", source="LAST_FETCHED"))
    # print(get_idx_market_cap("NIFTY 500000")) #NOTE: Invalid Index name
    print(get_idx_market_cap("NIFTY 50"))  # NOTE: Valid Index name
