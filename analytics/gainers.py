from datetime import datetime, timedelta
import os
import pandas as pd
from loguru import logger
import src.constants as C
import src.headers as H
from src.helpers.common import (
    get_last_monday,
    compose_dates_from_range,
    compose_local_index_file_name,
)


def daily_gainer(
    file_type: str = C.SUPPORTED_FILE_TYPES["STOCK"],
    gain_type: str = C.GAIN_TYPE["PRICE"],
    duration: str = C.SUPPORTED_TIME_DURATIONS["DAY"],
    start_date: str = get_last_monday(),
    series: str = "EQ",
) -> pd.DataFrame:
    """Gets the daily gainers. If you reverse the sequence, you get daily losers.
    This method does not perform any validations on the input parameters because
    it assumes that the caller has performed the required validations of
    the input parameters.

    Parameters
    ----------
        file_type : str
    The type of file required. (bhavcopy, pe, etc.)
    Invoke core.supported_file_types for all the supported file types.
        gain_type: str
    This could be one of C.GAIN_TYPE collection
        duration: str
    This could be one of C.SUPPORTED_TIME_DURATIONS
        start_date : str
    Starting date. (Format: 'DD-Mon-YYYY. Ex., 12-Jun-2025)
        series: str
    The series of the instrument, defaulted to 'EQ'

    Returns
    -------
    pandas.DataFrame
        Data Frame containing the results OR empty DF in case of any error/exceptions.
    """
    logger.debug(
        f"[{file_type = }], [{gain_type = }], [{duration = }], [{start_date = }], [{series = }]"
    )
    file_name = ""
    # NOTE: If you are running this on a weekend then, default this immediate gone by Friday
    if datetime.strptime(start_date, C.DATE_FMT).weekday() > 4:
        start_date = (
            datetime.today()
            - timedelta(days=7 - datetime.strptime(start_date, C.DATE_FMT).weekday())
        ).strftime(C.DATE_FMT)
        logger.info(
            f"You are executing this on a weekend. Using last Fri's data. [{start_date = }]"
        )
    try:
        file_name = os.path.join(
            C.FILES_BASE_DIR,
            C.SUPPORTED_FILE_TYPES["BHAVCOPY"],
            f'{C.SUPPORTED_FILE_TYPES["BHAVCOPY"].lower()}_{start_date}.csv',
        )
        daily_data: pd.DataFrame = pd.read_csv(file_name)
        if not daily_data.empty:
            # NOTE: Re-arrange the data as per price % gain (compared to yesterday's value)
            # WARN: You must apply the series filter since dup symbol names are possible
            daily_data = pd.DataFrame(
                daily_data[daily_data[H.BHAVCOPY["series"]] == series]
            )

            previous_close = H.BHAVCOPY["previous_close"]
            close = H.BHAVCOPY["close"]

            daily_data["pct_change"] = (
                (daily_data[close] - daily_data[previous_close])
                / daily_data[previous_close]
            ) * 100
            daily_data.sort_values(by="pct_change", ascending=False, inplace=True)
            return daily_data

    except FileNotFoundError:
        logger.error(f"[{file_name = }] is not found. Returing empty DF.")
    return pd.DataFrame()


def weekly_gainers(
    file_type: str = C.SUPPORTED_FILE_TYPES["BHAVCOPY"], series: str = "EQ"
) -> pd.DataFrame:
    logger.debug(f"[{file_type = }], [{series = }]")
    return pd.DataFrame()


def monthly_gainer(
    file_type: str = C.SUPPORTED_FILE_TYPES["BHAVCOPY"], series: str = "EQ"
) -> pd.DataFrame:
    logger.debug(f"[{file_type = }], [{series = }]")
    return pd.DataFrame()


def index_gainers(
    duration: str = C.SUPPORTED_TIME_DURATIONS["WEEK"],
    start_date: str = get_last_monday(),
) -> pd.DataFrame:
    logger.info(f"[{duration = }], [{start_date = }]")
    data = pd.DataFrame()
    # NOTE: For weekly index data processing
    if duration == C.SUPPORTED_TIME_DURATIONS.get("WEEK"):
        end_date = datetime.strptime(start_date, C.DATE_FMT) + timedelta(days=5)
        date_range = compose_dates_from_range(start_date, end_date.strftime(C.DATE_FMT))
        # NOTE: You should not get an empty date range
        if not date_range:
            logger.error(
                f"Invalid start date: {start_date}. Please provide correct start date for the week!"
            )
            return data

        # NOTE: Read and merge all the index list files.
        weekly_data_list = list()  # Gather all daily data in a temporary list
        daily_index_data = pd.DataFrame()
        for dt in date_range:
            # TODO: try using get local file name
            index_file = compose_local_index_file_name(dt)
            try:
                daily_index_data = pd.read_csv(index_file)
                daily_index_data["TRADING_DATE"] = datetime.strptime(
                    dt, C.DATE_FMT
                )  # Add trading date field
                daily_index_data.set_index(
                    "TRADING_DATE"
                )  # set the index trading date field
                logger.info(f"The dataframe index is: [{daily_index_data.index}]")
                daily_index_data.to_csv(f"daily_index_data-{dt}.csv")
            except pd.errors.EmptyDataError:
                logger.error(f"Index data not found for file: [{index_file}]")
            except FileNotFoundError:
                logger.error(f"Index file [{index_file}] not found!")
            # logger.debug(f"Trade Data is: {trd_dt_data}")
            weekly_data_list.append(daily_index_data)
        data = pd.concat(
            weekly_data_list
        )  # All data in list is added to Pandas data frame for efficiency
        data.to_csv("nothing.csv")
        # REFERENCE: https://pandas.pydata.org/docs/user_guide/merging.html
        # logger.info(f"The Data is: {data}")
        # data.to_csv("All_data.csv")
        # TODO: Now, process the data for gainers.
        # data.groupby()
        return data
    return data
