from loguru import logger

from datetime import datetime, timedelta
import  time

from src.helpers.validators import isDateValid, isNSEHoliday
from src.constants import DATE_FMT

def composeDatesFromRange(s_date: str, e_date:str):
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




