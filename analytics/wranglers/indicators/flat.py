import os
from pandas import DataFrame

from loguru import logger
import src.constants as C

from src.helpers.cross_cutting import benchmark
from src.helpers.common import get_all_stock_names


@benchmark
def avg_volume(trading_date: str) -> DataFrame:
    """Calculate the last 1-year average volume for all the stocks.
    The start date is 1-day before the supplied trading date.

    Parameters
    ----------
        trading_date: str
    The trading date in the format of src.constants.DATE_FMT

    Returns
    -------
        pd.DataFrame
    The average volume DF.

    Assumptions
    -----------
    1.
    2.
    """
    logger.info(f"[{trading_date = }]")
    # NOTE: If the data file containing the average volume is present then do nothing.
    avg_vol_file = os.path.join(
        C.FILES_BASE_DIR,
        C.SUPPORTED_FILE_TYPES["STOCK"],
        C.AVG_VOL_FOLDER,
        f"{trading_date}.csv",
    )
    if os.path.isfile(avg_vol_file):
        logger.error(f"The average volume file exists for [{trading_date}]")
        logger.info(f"Use the derived.readers to get data")
        return DataFrame()
    # NOTE: Get all stock names
    required_series = ["EQ", "BE"]
    stocks = get_all_stock_names(series_list=required_series)
    # logger.debug(f"All stocks: [{stocks}]")
    # NOTE: For each stock read the past 1-year price data (BHAVCOPY)

    for stock in stocks:
        pass
    # NOTE: Calculate average volume

    # NOTE: Write the result to the file.
    return DataFrame()
