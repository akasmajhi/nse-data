from loguru import logger

from datetime import datetime, timedelta, date
import  time
import os

from src.helpers.validators import isDateValid, isNSEHoliday
from src.constants import DATE_FMT, SUPPORTED_FILE_TYPES, FILES_BASE_DIR

def compose_dates_from_range(s_date: str, e_date:str):
    """
Compose a list of trading dates from the supplied range.

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
    start_time = time.perf_counter()
    logger.debug(f"start_date: [{s_date}], end_date: [{e_date}]")
    d_range = list()
    # Validations - 1: Ensure both trading dates are valid
    if (not (isDateValid(s_date) and isDateValid(e_date))):
        logger.error(f"Range dates are Invalid")
        return d_range # Empty list return (BAD IDEA) #TODO
    # Validations - 2: Ensure e_date >= s_date
    if(datetime.strptime(s_date, DATE_FMT) > datetime.strptime(e_date, DATE_FMT) ):
        # Log the error and pass empty list
        logger.error(f"Start date: [{s_date}] cannot be > than end date: [{e_date}]")
        return d_range 

    logger.info(f"Valid trading dates: [{s_date}, {e_date}]")
    
    s_dt = datetime.strptime(s_date, DATE_FMT).date()
    e_dt = datetime.strptime(e_date, DATE_FMT).date()
    # Validations - 3: Add only weekdays and non-NSE-Holidays
    for cnt in range((e_dt - s_dt).days + 1):
        #Don't add weekends. Add only weekdays!
        # logger.debug(f"The week of day is: [{(s_dt + timedelta(days=cnt)).weekday()}]")
        trading_dt = s_dt + timedelta(days=cnt)
        #Add check for NSE Holidays
        if ( ((trading_dt.weekday()) <= 4) and 
                (not isNSEHoliday(trading_dt.strftime(DATE_FMT)))):
            d_range.append((s_dt + timedelta(days=cnt)).strftime('%d-%b-%Y'))
    logger.debug(f"Date Range list: [{d_range}]")
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    logger.info(f"Total time taken: [{elapsed_time:.4f}] seconds")
    return d_range

def composeFileNameFromDate(trading_date: str):
    """
        Composes a valid (remote) file name from a trading date.
    Parameters
    ----------
        trading_date: str
    Trading Date in the form of DD-Mon-YYYY (e.g., 12-Jun-2025)

    Returns
    -------
        str
    File name in the form of a string.
    """
    logger.debug(f"trading date received: [{trading_date}]")

def compose_local_filename(file_type: str, trading_date: str):
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
    logger.debug(f"Composing local file name from type [{file_type}] and \
        trading date [{trading_date}]")
    if (file_type == 'PE'):
        logger.debug(f"Composing local PE file name")
        return f"pe_{trading_date}"
    return "" # Return nil for unknown file_type

def get_last_monday():
    """
        Gets the immediate last Monday in DD-MMM-YYYY format. Useful for analytics.
    """
    today = date.today()
    return (today - timedelta(days=(today.weekday()))).strftime(DATE_FMT)

def is_start_date_Monday(i_date) -> bool :
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
    logger.debug(f"Incoming date is: [{i_date}]")
    try:
        i_dt = datetime.strptime(i_date, DATE_FMT)
        if i_dt.weekday() == 0: # For Monday == 0
            return True
    except ValueError:
        logger.error(f"Invalid date [{i_date}] or fomrat provided!")
    return False

def get_week_ending_date(start_date: str) -> str :
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
    logger.debug(f"Incoming date is: [{start_date}]")
    try:
        start_dt = datetime.strptime(start_date, DATE_FMT)
        #TODO: Check if you need to add 4 days or 5
        end_dt = start_dt + timedelta(days=4)
        return end_dt.strftime(DATE_FMT)
    except ValueError:
        logger.error(f"Invalid date [{start_date}] or fomrat provided!")
        return ""

def compose_local_index_file_name(trading_date: str = datetime.today().strftime(DATE_FMT)):
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
    #TODO: 
    # Is the date in future
    # If i_date is weekend then calculate the immediate last weekday
    # If the last weekday was a exchange holiday then try previous day
    logger.debug(f"Incoming date is: [{i_date}]")
    return ""

def is_date_in_future(i_date: str) -> bool:
    logger.info(f"Incoming Date is: [{i_date}]")
    if datetime.strptime(i_date, DATE_FMT) > datetime.today():
        logger.error(f"Incoming date is: [{i_date}] is in future!")
        return True
    return False
