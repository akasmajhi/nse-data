"""
Top level wrapper for all analytics related queries.
"""

import pandas as pd
from datetime import datetime, timedelta

from loguru import logger
from analytics.composers import compose_weekly_data
from analytics.gainers import daily_gainer, index_gainers, weekly_gainers
import src.constants as C
from src.helpers.validators import is_date_valid
from analytics.validators.params import validate_engulfers


def top_gainers(
    start_date: str,
    file_type: str = C.SUPPORTED_FILE_TYPES["BHAVCOPY"],
    gain_type: str = C.GAIN_TYPE["PRICE"],
    duration: str = C.SUPPORTED_TIME_DURATIONS["WEEK"],
    series: str = "EQ",
) -> pd.DataFrame:
    """All top level gainers for a specific instrument and for a given period of time.

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
    The series of the instrument, defaulted to 'BE'

    Returns
    -------
    pandas.DataFrame
        Data Frame containing the results OR empty DF in case of any error/exceptions.
    """
    logger.info(
        f"[{file_type = }], [{gain_type = }], [{duration = }], [{start_date = }], [{series = }]"
    )
    data = pd.DataFrame()
    # NOTE: Basic validations
    if file_type.upper() not in C.SUPPORTED_FILE_TYPES:
        logger.error(f"Unsupported [{file_type = }]")
        return data

    if gain_type.upper() not in C.GAIN_TYPE:
        logger.error(f"Unsupported [{gain_type = }]")
        return data

    if duration.upper() not in C.SUPPORTED_TIME_DURATIONS:
        logger.error(f"Unsupported [{duration = }]")
        return data

    # NOTE:  Verify that the date is correct (not in future etc.)
    if not is_date_valid(start_date):
        logger.error(f"Invalid [{start_date = }]")
        return data

    # TODO: Get the dataset for the specified time
    match file_type:
        case "INDEX" if file_type == C.SUPPORTED_FILE_TYPES["INDEX"]:
            return index_gainers(duration, start_date)
        case "PE" if file_type == C.SUPPORTED_FILE_TYPES["PE"]:
            logger.error(f"NOT IMPLEMENTED . . . ")
            return data
        case "STOCK" if file_type == C.SUPPORTED_FILE_TYPES["STOCK"]:
            match duration.upper():
                case "WEEK" if duration.upper() == C.SUPPORTED_TIME_DURATIONS["WEEK"]:
                    return weekly_gainers(
                        file_type=C.SUPPORTED_FILE_TYPES["STOCK"],
                        series="",
                        start_date=start_date,
                    )
                case "DAY" if duration.upper() == C.SUPPORTED_TIME_DURATIONS["DAY"]:
                    return daily_gainer(
                        file_type=file_type.upper(),
                        gain_type=gain_type,
                        duration=duration,
                        start_date=start_date,
                        series=series.upper(),
                    )
                case _:
                    logger.error(f"NOT IMPLEMENTED {duration = }. . . ")
                    pd.DataFrame()
            return data
        case _:  # Unkown type
            logger.error(f"Unknown file type!")
            return data


def engulfers(start_date: str, instrument: str, duration: str) -> pd.DataFrame:
    """
    Returns the rngulfers for the given instrument type and duration.

    Parameters
    ----------
        start_date: str
    The starting date of analysis in DATE_FMT
        instrument : str
    Could be either STOCK or INDEX
        duration: str
    This could be one of DAILY or WEEKLY or MONTHLY

    Returns
    -------
    pandas.DataFrame
        Data Frame containing the results OR empty DF in case of any error/exceptions.
    """

    logger.debug(f"[{start_date = }], [{instrument = }], [{duration = }]")
    validate_engulfers(start_date, instrument, duration)
    past_week_start_date = (
        datetime.strptime(start_date, C.DATE_FMT) - timedelta(days=7)
    ).strftime(C.DATE_FMT)
    logger.debug(f"{past_week_start_date = }")
    if instrument == C.SUPPORTED_FILE_TYPES["STOCK"]:
        current_week_data: pd.DataFrame = top_gainers(
            file_type="STOCK", start_date=start_date
        )
        past_week_data: pd.DataFrame = top_gainers(
            file_type="STOCK", start_date=past_week_start_date
        )
        logger.debug(f"[{len(current_week_data) = }], [{len(past_week_data) = }]")
        logger.debug(f"[{current_week_data.columns = }], [{past_week_data.columns = }]")
    return pd.DataFrame()


if __name__ == "__main__":
    # logger.info(f"Main Called.")
    # data = top_gainers(
    #     file_type=C.SUPPORTED_FILE_TYPES["STOCK"],
    #     gain_type="PRICE",
    #     duration=C.SUPPORTED_TIME_DURATIONS["DAY"],
    #     start_date=datetime.today().strftime(C.DATE_FMT),
    #     series="BE",
    # )
    # logger.debug(f"The size of data is: [{len(pd.DataFrame(data))}]")
    # print(engulfers(start_date="XX", instrument="STOCaK", duration="YY"))
    print(engulfers(start_date="05-Jan-2026", instrument="STOCK", duration="DAY"))
    # print(engulfers(start_date="29-Dec-2025", instrument="INDEX", duration="MONTH"))
