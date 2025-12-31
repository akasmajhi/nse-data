import json
from loguru import logger

from datetime import datetime, timedelta, date

import os
import glob

import pandas as pd

from src.fetchers.common import get_last_fetch_date
from src.helpers.validators import is_date_valid, is_NSE_holiday, get_latest_file
from src.constants import (
    DATE_FMT,
    SUPPORTED_FILE_TYPES,
    FILES_BASE_DIR,
    SUPPORTED_TIME_DURATIONS,
)


def compose_dates_for_duration(trading_date: str, duration: str) -> list[str] | list:
    """Composes a range of dates for the duration and starting date (a.k.a.)
    trading_date provided.

    Parameters
    ----------
        trading_date: str
    This is the upper boundary of the date. (src.constants.DATE_FMT formatted)
        duration: str
    The duration which is one of src.constants.SUPPORTED_TIME_DURATIONS.

    Business case, you may seek top gainers for a month. In which case,
    the trading_date is last date of the month and duration is "MONTH".
    """
    logger.debug(f"[{trading_date = }], [{duration = }]")
    d_range = list()
    # NOTE: Duration should be valid
    if duration not in SUPPORTED_TIME_DURATIONS:
        logger.error(f"Invalid [{duration = }]")
        return d_range
    if not is_date_valid(trading_date):
        logger.error(f"Invalid [{trading_date = }]")
        return d_range

    end_dt: datetime = datetime.strptime(trading_date, DATE_FMT)
    start_dt: datetime
    match duration:
        case "DAY" if duration == SUPPORTED_TIME_DURATIONS["DAY"]:
            start_dt = end_dt
        case "WEEK" if duration == SUPPORTED_TIME_DURATIONS["WEEK"]:
            start_dt = end_dt - timedelta(days=7)
            # logger.info(f'[{start_dt = }]')
        case "MONTH" if duration == SUPPORTED_TIME_DURATIONS["MONTH"]:
            start_dt = end_dt - timedelta(days=30)
        case _:
            logger.error(f"Unspported [{duration = }]")
            return d_range
    return compose_dates_from_range(
        start_dt.strftime(DATE_FMT), end_dt.strftime(DATE_FMT)
    )


def compose_dates_from_range(s_date: str, e_date: str) -> list[str] | list:
    """Compose a list of trading dates from the supplied range.

    Parameters
    ----------
        s_date: str
    Start date in the format of DD-Mon-YYYY. e.g., 14-Jun-2025
        e_date: str
    End date in the format of DD-Mon-YYYY. e.g., 20-Jun-2025

    Returns
    -------
        list
    List containing the valid trading dates. Blank list returned for invalid inputs.

    Validations
    -----------
    Both dates are validated against valid trading dates and holidays along with sanity.
    """
    # start_time = time.perf_counter()
    logger.debug(f"start_date: [{s_date = }], end_date: [{e_date = }]")
    d_range = list()
    # Validations - 1: Ensure both trading dates are valid
    if not (is_date_valid(s_date) and is_date_valid(e_date)):
        logger.error(f"Range dates are invalid")
        return d_range  # Empty list return (BAD IDEA). Returning empty struct is a global design.
    # Validations - 2: Ensure e_date >= s_date
    if datetime.strptime(s_date, DATE_FMT) > datetime.strptime(e_date, DATE_FMT):
        # Log the error and pass empty list
        logger.error(f"[{s_date = }] cannot be > than [{e_date = }]")
        return d_range

    # logger.debug(f"Valid trading dates: [{s_date = }, {e_date = }]")

    s_dt = datetime.strptime(s_date, DATE_FMT).date()
    e_dt = datetime.strptime(e_date, DATE_FMT).date()
    # Validations - 3: Add only weekdays and non-NSE-Holidays
    for cnt in range((e_dt - s_dt).days + 1):
        # Don't add weekends. Add only weekdays!
        # logger.debug(f"The week of day is: [{(s_dt + timedelta(days=cnt)).weekday()}]")
        trading_dt = s_dt + timedelta(days=cnt)
        # Add check for NSE Holidays
        if ((trading_dt.weekday()) <= 4) and (
            not is_NSE_holiday(trading_dt.strftime(DATE_FMT))
        ):
            d_range.append((s_dt + timedelta(days=cnt)).strftime("%d-%b-%Y"))
    # logger.debug(f"Date Range list: [{d_range = }]")
    # end_time = time.perf_counter()
    # elapsed_time = end_time - start_time
    # logger.debug(f"Total time taken: [{elapsed_time:.4f}] seconds")
    return d_range


def compose_local_filename(
    i_file_type: str, i_stock_name: str = "", i_trading_date: str = "", i_year: str = ""
) -> str | None:
    """
        Composes a local file name from a given file type & trading date.
    Parameters
       file_type: str
    What type of file (PE, BHAVCOPY, etc.)
    ----------
        trading_date: str
    Trading Date in the form of DD-Mon-YYYY (e.g., 12-Jun-2025)

    Returns
    -------
        str
    File name in the form of a string.
    """
    logger.debug(
        f"Composing file name [{i_file_type = }],[{i_stock_name = }],[{i_trading_date = }]"
    )
    match i_file_type:
        case "STOCK" if i_file_type == SUPPORTED_FILE_TYPES["STOCK"]:
            return (
                os.path.join(
                    FILES_BASE_DIR,
                    SUPPORTED_FILE_TYPES["STOCK"],
                    f"{i_stock_name}_{i_year}.csv",
                )
                if i_stock_name and i_year
                else None
            )

        case "BHAVCOPY" if i_file_type == SUPPORTED_FILE_TYPES["BHAVCOPY"]:
            return (
                os.path.join(
                    FILES_BASE_DIR,
                    SUPPORTED_FILE_TYPES["BHAVCOPY"],
                    f'{SUPPORTED_FILE_TYPES["BHAVCOPY"].lower()}_{i_trading_date}.csv',
                )
                if i_trading_date
                else None
            )

        case "PE" if i_file_type == SUPPORTED_FILE_TYPES["PE"]:
            return (
                os.path.join(
                    FILES_BASE_DIR,
                    SUPPORTED_FILE_TYPES["PE"],
                    f'{SUPPORTED_FILE_TYPES["PE"].lower()}_{i_trading_date}.csv',
                )
                if i_trading_date
                else None
            )

        case "INDEX" if i_file_type == SUPPORTED_FILE_TYPES["INDEX"]:
            return (
                os.path.join(
                    FILES_BASE_DIR,
                    SUPPORTED_FILE_TYPES["INDEX"],
                    f'{SUPPORTED_FILE_TYPES["INDEX"].lower()}_{i_trading_date}.csv',
                )
                if i_trading_date
                else None
            )

        case "FNOBHAVCOPY" if i_file_type == SUPPORTED_FILE_TYPES["IFNOBHAVCOPY"]:
            return (
                os.path.join(
                    FILES_BASE_DIR,
                    SUPPORTED_FILE_TYPES["FNOBHAVCOPY"],
                    f'{SUPPORTED_FILE_TYPES["FNOBHAVCOPY"].lower()}_{i_trading_date}.csv',
                )
                if i_trading_date
                else None
            )

        case "MARKET_CAP" if i_file_type == SUPPORTED_FILE_TYPES["MARKET_CAP"]:
            # NOTE: Keeping market cap in folder named after fetch/trading date
            if i_trading_date and i_trading_date == datetime.today().strftime(DATE_FMT):
                # trading_date = datetime.today().strftime(DATE_FMT)
                # NOTE: Ideally, you should use last fetch_date
                # trading_date  = get_last_fetch_date(SUPPORTED_FILE_TYPES["MARKET_CAP"])
                # NOTE: Check if the folder exists for the trading_date
                # if trading_date:
                m_cap_folder = os.path.join(
                    FILES_BASE_DIR,
                    SUPPORTED_FILE_TYPES["STOCK"],
                    SUPPORTED_FILE_TYPES["MARKET_CAP"].lower(),
                    i_trading_date,
                )
                if not os.path.isdir(m_cap_folder):  # RESOLVED: Partial path checked
                    # NOTE: Create the folder if it does not exist
                    try:
                        os.mkdir(os.path.join(m_cap_folder))
                    except FileExistsError:
                        # NOTE: If the folder exists then do nothing
                        pass
                else:
                    logger.info(f"[{m_cap_folder = }] for [{i_trading_date = }]")
                return os.path.join(m_cap_folder, f"{i_stock_name.upper()}.json")
            else:  # NOTE: The input parameter contains the trading date
                logger.debug(
                    f"Going to check if m_cap exists for [{i_trading_date = }]"
                )
                m_cap_folder = os.path.join(
                    FILES_BASE_DIR,
                    SUPPORTED_FILE_TYPES["STOCK"],
                    SUPPORTED_FILE_TYPES["MARKET_CAP"].lower(),
                    i_trading_date,
                )
                logger.info(
                    f"M_Cap Folder: [{m_cap_folder = }], [{i_stock_name}],\
                                    [{i_trading_date = }]"
                )
                if not os.path.isdir(m_cap_folder):
                    logger.error(f"Market cap does not exist for [{i_trading_date = }]")
                    return None
                return os.path.join(m_cap_folder, f"{i_stock_name.upper()}.json")

        case "META" if i_file_type == SUPPORTED_FILE_TYPES["META"]:
            # NOTE: Use the last fetch date if no trading_date provided
            if not i_trading_date:
                trading_date = get_last_fetch_date(SUPPORTED_FILE_TYPES["META"])
                if trading_date:
                    meta_folder = os.path.join(
                        FILES_BASE_DIR,
                        SUPPORTED_FILE_TYPES["STOCK"],
                        SUPPORTED_FILE_TYPES["META"],
                        trading_date,
                    )
                    if not os.path.isdir(meta_folder):  # RESOLVED: Partial path checked
                        # NOTE: Create the folder if it does not exist
                        try:
                            os.mkdir(os.path.join(meta_folder))
                        except FileExistsError:
                            # NOTE: If the folder exists then do nothing
                            pass
                        except Exception as e:
                            logger.error(
                                f"Error occured while creating folder: [{meta_folder = }]"
                            )
                            logger.error(f"Exception is: [{e}]")
                    else:
                        logger.info(
                            f"[{meta_folder = }]Folder exists for [{trading_date = }]"
                        )
                    return os.path.join(
                        meta_folder, f"{i_stock_name.upper()}_meta.json"
                    )
                else:  # NOTE: Case for first-time fetch
                    trading_date = datetime.today().strftime(DATE_FMT)
                    meta_folder = os.path.join(
                        FILES_BASE_DIR,
                        SUPPORTED_FILE_TYPES["STOCK"],
                        SUPPORTED_FILE_TYPES["META"],
                        trading_date,
                    )
                    # NOTE: Create the folder
                    try:
                        os.mkdir(os.path.join(meta_folder))
                    except Exception as e:
                        logger.error(
                            f"Error occured while creating folder: [{meta_folder = }]"
                        )
                        logger.error(f"Exception is: [{e}]")
                    return os.path.join(
                        meta_folder, f"{i_stock_name.upper()}_meta.json"
                    )

            else:  # NOTE: The input parameter contains the trading date
                logger.debug(
                    f"Going to check if meta folder exists for [{i_trading_date = }]"
                )
                meta_folder = os.path.join(
                    FILES_BASE_DIR,
                    SUPPORTED_FILE_TYPES["STOCK"],
                    SUPPORTED_FILE_TYPES["META"],
                    i_trading_date,
                )
                logger.debug(
                    f"META Folder: [{meta_folder = }], [{i_stock_name = }],\
                                    [{i_trading_date = }]"
                )
                if not os.path.isdir(meta_folder):
                    logger.error(
                        f"Meta folder does not exist for [{i_trading_date = }]"
                    )
                    return None
                return os.path.join(meta_folder, f"{i_stock_name.upper()}_meta.json")
        case _:
            logger.error(f"Unknown [{i_file_type = }]")
    return None  # Return None for unknown file_type


def get_last_monday(i_date: str = date.today().strftime(DATE_FMT)) -> str:
    """
    Gets the immediate last Monday in DD-MMM-YYYY format. Useful for analytics.
    If you are in any part of the week, then this function will return the
    Monday of the previous week.
    Note: If you are running this on a weekend then it returns the first day,
    which is Monday, of the week.
    """
    logger.debug(f"[{i_date = }]")
    today = date.today()
    if today.weekday() >= 5:  # NOTE: For weekends
        return (today - timedelta(days=(today.weekday()))).strftime(DATE_FMT)
    return (today - timedelta(days=(today.weekday() + 7))).strftime(DATE_FMT)


def get_last_friday() -> str:
    """Get's the Friday of the trading week"""
    days_until_friday = (4 - datetime.today().weekday() + 7) % 7
    friday_of_current_week = datetime.today() + timedelta(days=days_until_friday)
    return friday_of_current_week.strftime(DATE_FMT)


def is_start_date_Monday(i_date) -> bool:
    """
        Checks to see if the date provided is a Monday or not.
    Parameters
    ----------
       i_date: str
    The incoming date in 'DD-Mon-YYYY' format type of file (PE, BHAVCOPY, etc.)
    Returns
    -------
        Bool
    True if the incoming date is a Monday. False otherwise (even in error conditions)

    """
    # logger.debug(f"Incoming date [{i_date = }]")
    try:
        i_dt = datetime.strptime(i_date, DATE_FMT)
        if i_dt.weekday() == 0:  # For Monday == 0
            return True
    except ValueError:
        logger.error(f"Invalid date [{i_date = }] or fomrat provided!")
    return False


def get_week_ending_date(start_date: str) -> str:
    """
        Gets the week ending date (=current date + 4 days)
    Parameters
    ----------
       start_date: str
    The incoming date in 'DD-Mon-YYYY'
    Returns
    -------
        str | Bool
    False if there is any problem with the date otherwise weend ending date ('DD-Mon-YYYY')

    """
    logger.debug(f"Incoming date is: [{start_date = }]")
    try:
        start_dt = datetime.strptime(start_date, DATE_FMT)
        end_dt = start_dt + timedelta(days=4)
        return end_dt.strftime(DATE_FMT)
    except ValueError:
        logger.error(f"Invalid date [{start_date = }] or fomrat provided!")
        return ""


# TODO: Delete this function. Use compose_local_filename instead
def compose_local_index_file_name(
    trading_date: str = datetime.today().strftime(DATE_FMT),
):
    """Compose a local index file name, with full path, based on supplied trading date.

    Parameters
    ----------
        trading_date: str
    The trading date or defaulted to today's date
    Returns
    -------
        str
    The local index file name.
    """
    IDX_FOLDER = SUPPORTED_FILE_TYPES["INDEX"]
    IDX_FILE_PREPEND = SUPPORTED_FILE_TYPES["INDEX"].lower()
    IDX_FILE_NAME = f"{IDX_FILE_PREPEND}_{trading_date}.csv"
    index_file = os.path.join(FILES_BASE_DIR, IDX_FOLDER, IDX_FILE_NAME)
    return index_file


def get_last_trading_date(i_date: str = datetime.today().strftime(DATE_FMT)) -> str:
    """Returns the immediate last trading trade or today, if it is a trading date.

    Parameters
    ----------
        i_date: str
    The input date in DD-Mon-YYYY format
    Returns
    -------
        str
    The last trading date
    """
    logger.debug(f"Incoming date is: [{i_date = }]")
    today = datetime.today()
    trading_date = ""
    # NOTE: (Validate i_date) If a trading date is passed then it must be a valid date
    if not i_date.strip():
        try:
            datetime.strptime(i_date, DATE_FMT)
        except ValueError:
            logger.error(f"Bad [{i_date = }] passed")
            return trading_date

    # NOTE: If i_date is None then default it to previous weekdays
    # BUG: Incoming date cannot be null. commenting below
    # if i_date is None and today.weekday() < 5 and today.hour < 19:
    #     logger.debug(f"This is a weekday and it's before 7PM")
    #     trading_date = (today - timedelta(days=1)).strftime(DATE_FMT)
    #     return trading_date

    # NOTE: Is the date in future?
    if i_date and is_date_in_future(i_date):
        trading_date = today.strftime(DATE_FMT)
    else:
        trading_date = i_date
    # NOTE: If the i_date is today and time is before 7 AM, then use previous day
    if i_date == today.strftime(DATE_FMT) and today.hour < 19 and today.weekday() < 5:
        excess_days = 1
        logger.error(
            f"It is'a Weekday and befoer 7 PM. Use previous day. [{excess_days = }]"
        )
        prev_week_day = (
            datetime.strptime(trading_date, DATE_FMT) - timedelta(days=excess_days)
        ).strftime(DATE_FMT)
        trading_date = prev_week_day
    # NOTE: If i_date is weekend then calculate the immediate last weekday
    if datetime.strptime(trading_date, DATE_FMT).weekday() > 4 and (
        i_date == today.strftime(DATE_FMT) and today.hour < 19
    ):
        excess_days = (7 + datetime.strptime(trading_date, DATE_FMT).weekday() + 1) % 5
        logger.error(f"[{excess_days = }]")
        prev_week_day = (
            datetime.strptime(trading_date, DATE_FMT) - timedelta(days=excess_days)
        ).strftime(DATE_FMT)
        trading_date = prev_week_day
    # NOTE: If the last weekday was a exchange holiday then try previous day
    if is_NSE_holiday(trading_date):
        prev_working_day = (
            datetime.strptime(trading_date, DATE_FMT) - timedelta(days=1)
        ).strftime(DATE_FMT)
        trading_date = prev_working_day
    return trading_date


def is_date_in_future(i_date: str) -> bool:
    """Checks if a given date is in future.
    Parameters
    ----------
        i_date: str
    The inout date in DD-MMM-YYYY format (as present in src.constants.DATE_FMT)
    Returns
        bool
    True if the input date is in future; False otherwise
    """
    # logger.debug(f"Incoming Date is: [{i_date = }]")
    if datetime.strptime(i_date, DATE_FMT) > datetime.today():
        logger.error(f"Incoming date is: [{i_date = }] is in future!")
        return True
    return False


def get_first_day_of_month() -> str:
    """Returns the first day of the month in the form od DD-MMM-YYYY

    Parameters
    ----------
    Returns
    -------
        str
    First calendar day of the current month. For example, 01-Sep-2025
    """
    # TODO:
    return datetime.now().replace(day=1).strftime(DATE_FMT)


def get_all_stock_names(series: str = "", series_list: list = []) -> list:
    """Gets all the stock name from the latest bhavcopy.
    Parameter
    ---------
        None
    Returns
    -------
        list
    Containing all the stock names
    """
    logger.info(f"[{series = }],[{series_list = }]")
    latest_bhavcopy = get_latest_file(file_type=SUPPORTED_FILE_TYPES["BHAVCOPY"])
    symbol_col_name = "TckrSymb"  # TODO: Move these items to src.constants
    series_col_name = "SctySrs"
    if series_list:
        filtered_data = latest_bhavcopy[
            latest_bhavcopy[series_col_name].isin(series_list)
        ]
        return list(pd.Series(filtered_data[symbol_col_name]).unique())
    # TODO: Insert try-except below
    return list(latest_bhavcopy[symbol_col_name].unique())


def get_stock_fetch_history(stock_name: str) -> list:
    """Read the stock fetch history from the STOCK/META/HISTORY folder.
    Parameters
    ----------
        str
    Stock name
    Returns
    -------
        list
    List containing history, if it exists or blank list otherwise.
    """
    logger.info(f"Fetching stock history for [{stock_name = }]")
    stock_history = list()
    if not stock_name:
        logger.info(f"[{stock_name = }] cannot be blank")
        return stock_history
    file_type = SUPPORTED_FILE_TYPES["STOCK"]
    pattern = f"META/HISTORY/*{stock_name.upper()}*json"  # JSON files store history
    files_path = os.path.join(FILES_BASE_DIR, file_type, pattern)
    # logger.debug(f"Files path for [{stock_name}] is: [{files_path}]")
    files_list = glob.glob(files_path)
    # logger.info(f"History files for [{stock_name}] are: [{files_list}]")
    for f in files_list:
        # Read each file and add it to the stock_history list
        with open(f, "r") as file:
            json_history_dict = json.load(file)
            stock_history.append(json_history_dict)
    return stock_history


def set_stock_fetch_history(
    stock_name: str, start_trading_date: str = "", end_trading_date: str = ""
) -> bool:
    """Write the stock fetch history onto the META/HISTORY folder.
    Parameters
    ----------
        stock_name: str
    stock name
        start_of_fetch: str
    Strating date (DD-MMM-YYY format) for the stock fetch
        end_of_fetchL str
    Ending date (DD-MMM-YYY format) for the stock fetch

    Returns
    -------
        list
    List containing history, if it exists or blank list otherwise.
    """
    logger.info(f"Writing stock history for [{stock_name = }]")
    if not stock_name:
        logger.info(f"[{stock_name = }] cannot be blank")
        return False
    file_type = SUPPORTED_FILE_TYPES["STOCK"]
    ts = datetime.now().strftime(f"{DATE_FMT}_%H-%M-%S")
    pattern = f"META/HISTORY/{stock_name.upper()}-{ts}.json"
    file_path = os.path.join(FILES_BASE_DIR, file_type, pattern)
    # logger.info(f"Files path: [{file_path}]")
    history = {}
    history["stock_name"] = stock_name
    history["start_trading_date"] = start_trading_date
    history["end_trading_date"] = end_trading_date
    history["fetch_date"] = datetime.now().strftime(f"{DATE_FMT}:%H-%M-%S")
    try:
        with open(file_path, "w") as file:
            json.dump(history, file, indent=4)
    except:
        logger.error(f"Error writing history file! [{stock_name = }]")
    return True


def get_latest_history(hist_list: list) -> dict:
    if len(hist_list) > 0:
        # NOTE: Determine the latest fetch history
        if len(hist_list) == 1:
            latest_fetch_dict = hist_list[0]
        else:
            D_T_FMT = f"{DATE_FMT}:%H-%M-%S"
            latest_fetch_dict = hist_list[0]
            for cnt in range(len(hist_list) - 1):
                # Compare
                dt_cnt = datetime.strptime(latest_fetch_dict["fetch_date"], D_T_FMT)
                dt_cnt_plus_1 = datetime.strptime(
                    hist_list[cnt + 1]["fetch_date"], D_T_FMT
                )
                if dt_cnt > dt_cnt_plus_1:
                    pass
                    # latest_fetch_dict = hist_list[cnt]
                else:
                    latest_fetch_dict = hist_list[cnt + 1]
        logger.debug(f"The latest history dict is: [{latest_fetch_dict = }]")
        return latest_fetch_dict
    return dict()  # Return empty dictionary if the history_list is empty


def register_failed_fetch(stock_name: str, from_date: str, to_date: str, err: str):
    """In case the fetch fails, call this method to register a fetch failure."""
    failure_dict = dict()
    failure_dict["stock_name"] = stock_name
    failure_dict["from_date"] = from_date
    failure_dict["to_date"] = to_date
    failure_dict["year"] = from_date[-4:]  # useful for re-trying yearly failed fetches
    failure_dict["error"] = err
    try:
        with open("failed_fetches.json", "a") as file:
            json.dump(failure_dict, file, indent=4)
    except:
        logger.error(f"Error writing fetch failure! [{stock_name = }]")


if __name__ == "__main__":
    # stock_name = "STOCK_NON_EXISTING"
    # stock_name = "UNIT_TEST_STOCK"
    # stock_name = "NON_EXISTING_STOCK"
    # stock_name = "UCOBANK"
    # print(get_latest_history(get_stock_fetch_history(stock_name)))
    # logger.debug(compose_dates_for_duration(duration="DADDY", trading_date="0-Oct-2025"))
    # logger.info('****************************************************')
    # logger.debug(compose_dates_for_duration(duration="DAY", trading_date="0-Oct-2025"))
    # logger.info('****************************************************')
    # logger.debug(compose_dates_for_duration(duration="DAY", trading_date="10-Oct-2025"))
    # logger.info('****************************************************')
    # logger.debug(compose_dates_for_duration(duration="WEEK", trading_date="10-Oct-2025"))
    # logger.info('****************************************************')
    # logger.debug(compose_dates_for_duration(duration="MONTH", trading_date="10-Oct-2025"))
    # logger.debug(compose_local_filename(i_file_type="PE",
    #                        i_trading_date="10-Oct-2025",
    #                        i_stock_name="",
    #                        i_year="2025"))
    # logger.debug(compose_local_filename(i_file_type="MARKET_CAP",
    #                        i_trading_date="10-Oct-2025",
    #                        i_stock_name="ICICIBANK",
    #                        i_year="2025"))
    # logger.debug(compose_local_filename(i_file_type="MARKET_CAP",
    #                        i_trading_date="09-Oct-2025",
    #                        i_stock_name="ICICIBANK",
    #                        i_year="2025"))
    # logger.debug(compose_local_filename(i_file_type="MARKET_CAP",
    #                        i_trading_date="",
    #                        i_stock_name="ICICIBANK",
    #                        i_year="2025"))
    # logger.debug(compose_local_filename(i_file_type="META",
    #                        i_trading_date="",
    #                        i_stock_name="ICICIBANK",
    #                        i_year="2025"))
    logger.debug(get_last_trading_date(i_date=""))
    logger.debug(get_last_trading_date(i_date="  "))
    logger.debug(get_last_trading_date(i_date="19-Oct-2025"))
    logger.debug(get_last_trading_date())
