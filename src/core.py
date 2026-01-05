# TODO: Make this program a cmdline-param based!
"""
Entry method for the callers to request data from the service.
"""
from datetime import datetime
import pandas as pd
from pandas import json_normalize
import os
from loguru import logger

from src.derived import readers
from src.fetchers.common import get_latest_file
from src.helpers.validators import is_date_valid, is_file_type_valid
from src.helpers import file_readers
from src.helpers.common import (
    get_all_stock_names,
    get_first_day_of_month,
)
import src.constants as C
from src.fetchers.stock_fetchers import get_stock_data_since_listing
from src.derived import writers
from src.helpers.common import get_last_trading_date


def get_data(file_type: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Gets the data for the 'file_type' supplied.

    Parameters
    ----------
    file_type : str
        The type of file required. (bhavcopy, pe, etc.)
        Invoke src.core.supported_file_types for all the supported file types.
    start_date : str
        Starting date. (Format: 'DD-Mon-YYYY. Ex., 12-Jun-2025)
    end_date : str
        Starting date. (Format: 'DD-Mon-YYYY. Ex., 12-Jun-2025)

    Returns
    -------
    pandas.DataFrame
        Data Frame containing the results
    """
    logger.info(f"{file_type = }, {start_date = }, {end_date = }")
    data = pd.DataFrame()
    if is_file_type_valid(file_type):
        # logger.debug(f"File type {file_type} is valid")
        if is_date_valid(start_date) and is_date_valid(end_date):
            logger.debug(f"Dates: {start_date = } and {end_date = } are valid")
            # param validatins okay. Read the files now.
            data = file_readers.get_local_data(file_type, start_date, end_date)
            # logger.info(f"Got data: {data}")
        else:
            logger.debug(f"[{start_date = }] or [{end_date = }]is invalid")
    else:
        logger.error(f"{file_type = }is Invalid")
    return data


def get_market_cap(
    file_type: str | None,
    stock_name: str | None,
    trading_date: str = datetime.today().strftime(C.DATE_FMT),
) -> list[dict] | dict:
    """Gets the market cap of an index, if file_type=="INDEX",
    or gets the market cap of a stock specified by the second parameter.
    If the file_type == SUPPORTED_FILE_TYPES["STOCK"] and stock_name is None then
    calculate/return the market cap of all the stocks (as a list of dict).

    Parameters
    ----------

        file_type : str
    As enumerated by src/constants/SUPPORTED_FILE_TYPES
        stock_name : str
    Name of the stock if file_type=STOCK
        trading_date: str
    Trading date. Defauted to today if not provided.

    Returns
    -------
    list(dict) | dict
        List containing dicts if there are more than 1 items or
        a dictionary if the data is for a single item like, single stock
        market cap.
    """
    logger.debug(f"{file_type = }, {stock_name = }")
    # NOTE: Case where we fetch m-cap for all stocks
    if file_type == C.SUPPORTED_FILE_TYPES["STOCK"] and stock_name is None:
        # Get the combined market cap of all the stocks
        all_stocks: list = get_all_stock_names()
        all_stocks.sort(key=None, reverse=False)
        all_market_caps: list[dict] = list()
        total_stocks = len(all_stocks)
        processed_stocks = 0
        for stock in all_stocks:
            # For a stock get it's market cap data
            all_market_caps.append(
                file_readers.get_local_market_cap(
                    C.SUPPORTED_FILE_TYPES["STOCK"], stock, trading_date
                )
            )
            processed_stocks = processed_stocks + 1
            logger.info(f"[{processed_stocks = }] of [{total_stocks = }]")
        # NOTE: Write the combined.json for combined market cap
        writers.combine_m_caps(folder=trading_date)
        return all_market_caps

    # NOTE: Case where we fetch m-cap for a stock
    if file_type == C.SUPPORTED_FILE_TYPES["STOCK"] and stock_name:
        return file_readers.get_local_market_cap(
            C.SUPPORTED_FILE_TYPES["STOCK"], stock_name, trading_date
        )

    # TODO: Case where we fetch m-cap for an index
    if file_type == C.SUPPORTED_FILE_TYPES["INDEX"]:
        pass
    return list(dict())  # Unhandled / unimplemented case gets a blank dictionary


def get_supported_file_types() -> dict:
    """Returns the file types supported.

    Parameters
    ----------
        None
    Returns
    -------
        dict
    Contains the SUPPORTED_FILE_TYPES from src.constants
    """
    return C.SUPPORTED_FILE_TYPES


def get_index_names() -> list[str]:
    """Returns names of all the indices.
    Parameters
    ----------
        None
    Returns
    -------
        list
    list containing all index names
    """
    return file_readers.get_local_index_names()


def get_all_index_constituents() -> list[dict]:
    """Returns the constituents for each index.
    Parameters
    ----------
        None
    Returns
    -------
        list[dict]
    Each list item contains a dict and each dict contains index name
    (as key) and a list of constient items as value.
    """
    logger.debug(f"Getting constituents for all indices")
    all_indices: list[dict] = list()
    for index_name in get_index_names():
        if "/" in index_name:
            index_name = index_name.replace("/", "By")
        index_dict: dict = dict()
        index_dict[index_name] = get_index_constituents(index_name)
        all_indices.append(index_dict)
    return all_indices


def get_index_constituents(index_name: str) -> list:
    """For a gievn index name, returns all it's constituents
    Parameters
    ----------
        index_name: str
    The name of the index.

    Returns
    -------
        list[str] or blank list (if the index name is invalid)
    List containing the index constituents

    """
    logger.debug(f"Getting constituents for index: [{index_name = }]")
    constituents = list()
    # NOTE: Index name should be non-null
    if not index_name:
        logger.error(f"[{index_name = }]cannot be null or blank")
        return constituents
    # NOTE: Index name should be valid
    if index_name not in get_index_names():
        logger.error(f"Invalid Index Name: [{index_name = }]")
        return constituents
    logger.debug(f"[{index_name = }]is valid")
    return file_readers.get_local_index_constituents(index_name)


def fetch_stock_data_since_listing(skip_current_year: bool = False):
    """Fetches the price information for all stocks since listing
    Parameters
    ----------
        None
    Returns
    -------
        None
    """
    logger.info(
        f"Fetching since-listing data for all stocks. Current year skipped? [{skip_current_year = }]"
    )
    all_stocks = get_all_stock_names()
    logger.info(f"Total {len(all_stocks)} stocks data to process.")
    processed = 0
    for stock in all_stocks:
        logger.info(f"Processing {stock = }")
        # NOTE: Call the scraper for each stock
        get_stock_data_since_listing(stock, skip_current_year)
        processed += 1
        logger.info(f"{processed}/{len(all_stocks)} Stocks processed.")


def daily_fetchers():
    """Group of operations that fetch data on a daily/EOD basis"""
    get_data(
        file_type="BHAVCOPY",
        start_date=get_first_day_of_month(),
        end_date=datetime.today().strftime(C.DATE_FMT),
    )
    # TODO: Run the Preopen if the day is a weekday and time is > 9:08 AM
    get_data(
        file_type="PREOPEN",
        start_date=datetime.today().strftime(C.DATE_FMT),
        end_date=datetime.today().strftime(C.DATE_FMT),
    )

    get_data(
        file_type="PE",
        start_date=get_first_day_of_month(),
        end_date=datetime.today().strftime(C.DATE_FMT),
    )

    # # TODO: Needs a design change revisit at a later time!
    # # Do not run it before 7 PM
    get_data(
        file_type="INDEX",
        start_date=datetime.today().strftime(C.DATE_FMT),
        end_date=datetime.today().strftime(C.DATE_FMT),
    )

    get_data(
        file_type="FNOBHAVCOPY",
        start_date=get_first_day_of_month(),
        end_date=datetime.today().strftime(C.DATE_FMT),
        # start_date="31-Oct-2025",
        # end_date="31-Oct-2025",
    )

    # get_all_index_constituents() #TODO: Check why it was there in the first place!


def weekly_fetchers():
    """Fetchers for weekending dates"""
    get_market_cap(file_type=C.SUPPORTED_FILE_TYPES["STOCK"], stock_name=None)
    get_stock_info()
    writers.industry_to_stock(datetime.today().strftime(C.DATE_FMT))


def industry_stock_map(i_trading_date: str | None) -> dict:
    """
    For the last fetch date for META, this returns the industry-to-stocks map.

    Parameters
    ----------
        None

    """
    # TODO: this needs to change based on i_trading_date
    logger.info(f"[{i_trading_date = }]")
    # return readers.industry_to_stock(
    #     get_last_fetch_date(SUPPORTED_FILE_TYPES["META"]), None
    # )
    folder_name = os.path.join(
        C.FILES_BASE_DIR,
        C.SUPPORTED_FILE_TYPES["DERIVED"],
        C.IND_TO_STOCK_FOLDER,
    )

    return readers.industry_to_stock(
        i_trading_date=None, i_file_name=get_latest_file(folder_name)
    )


def stocks_for_industry(industry: str | None) -> pd.Series | pd.DataFrame:
    """
    Returns the stocks belonging to the specified industry

    Parameters
    ----------
        industry: str
    The name of the industry (case-sensitive)

    Returns
    -------
        pd.Series
    The stocks (names) belonging to the supplied industry.
    """
    # ind_stock_dict = industry_stock_map(i_trading_date=None)

    # industry: str = "Industrial Minerals"
    data = json_normalize(data=industry_stock_map(i_trading_date=None)).T.explode(0)
    data = data.reset_index()
    data.rename(columns={"index": "industry"}, inplace=True)
    data.rename(columns={0: "stock"}, inplace=True)
    if industry == None:
        return data
    return data[data.industry.isin([industry])].stock


def get_stock_info(
    stock_name: str | None = None,
    trading_date: str = datetime.today().strftime(C.DATE_FMT),
) -> list[dict] | dict:
    """Fetches/reads the meta information associated with a stock(s)

    Parameters
    ----------
        stock_name: str
    The name of the stock. Pass None to fetch meta for all stocks

    Returns
    -------
        pd.DataFrame
    Meta info(s) associated with stock(s)

    """
    logger.debug(f"[{stock_name = }], [{trading_date = }]")
    if stock_name:  # NOTE: Meta info for single stock
        return file_readers.get_local_stock_info(stock_name, trading_date)
    # NOTE: Meta info for all stock
    all_stocks: list = get_all_stock_names()
    all_stocks.sort(key=None, reverse=False)
    all_stocks_info: list[dict] = list()
    total_stocks = len(all_stocks)
    processed_stocks = 0
    for stock in all_stocks:
        all_stocks_info.append(file_readers.get_local_stock_info(stock, trading_date))
        processed_stocks = processed_stocks + 1
        logger.info(f"[{processed_stocks = }] of [{total_stocks = }]")
    return all_stocks_info


def get_fno_stocks() -> list:
    """Returns the list of stock names that are in FnO.
    Note: The latest Fno Bhavcopy is read and stock names are returned.
    Parameters
    ----------
        None
    Returns
    -------
        list
    List containing the names of the FnO Stocks

    """
    logger.debug(f"Reading latest FnO bhavcopy")
    trading_date = get_last_trading_date()
    file_name = os.path.join(
        C.FILES_BASE_DIR,
        C.SUPPORTED_FILE_TYPES["FNOBHAVCOPY"],
        f'{C.SUPPORTED_FILE_TYPES["FNOBHAVCOPY"]}_{trading_date}.csv',
    )
    data = pd.read_csv(file_name)
    logger.debug(f"Total: [{len(data.TckrSymb.unique())}]")
    return data.TckrSymb.unique()


# TODO: Run the batch programs to prepare data for efficiency
def run_batch():
    """
    1. For preparing weekly data - End of week
    2. Industry to stock map - Everyday
    3. Index to stock map - Everyday
    4. Stock to Index map - Everyday
    """
    pass


if __name__ == "__main__":
    """
    daily_fetchers()
    fetch_stock_data_since_listing(skip_current_year=False)
    weekly_fetchers()
    """
    """
    """
    anything_executed: bool = False
    transient_test: bool = False
    # transient_test: bool = True
    if transient_test:
        data = get_data(
            file_type="BHAVCOPY", start_date="13-Oct-2025", end_date="16-Oct-2025"
        )
        logger.info(f"[{data = }]")
        data.columns
        anything_executed = True
    # NOTE:  Run daily fetchers after 7 PM
    print(f"[{datetime.today().weekday() = }], [{datetime.today().hour = }]")
    if datetime.today().weekday() < 5 and datetime.today().hour >= 19:
        daily_fetchers()
        anything_executed = True
    # logger.debug(get_index_names())
    # logger.debug(f'<<{get_all_index_constituents()}>>')
    # logger.debug(f'<<{get_index_constituents("NIFTY 50")}>>')
    # fetch_stock_data_since_listing(skip_current_year=True)
    # NOTE:  Run weekly fetchers only on Saturdays
    if datetime.today().weekday() >= 5:
        weekly_fetchers()
        anything_executed = True
    if not anything_executed:
        print("Nothing Executed . . . ")
