"""
    Top level wrapper for all analytics related queries.
"""
import pandas as pd
from datetime import datetime, timedelta, date

from loguru import logger
from analytics.composers import compose_weekly_data
import analytics.gainers as gainers# daily_gainer, weekly_gainer, monthly_gainer
from src.helpers.common import get_last_monday, compose_dates_from_range, compose_local_index_file_name
import src.constants as C 
# import SUPPORTED_FILE_TYPES, SUPPORTED_TIME_DURATIONS, \ DATE_FMT 
from src.helpers.validators import is_date_valid

def top_gainers(file_type: str = C.SUPPORTED_FILE_TYPES["BHAVCOPY"], 
                gain_type: str = C.GAIN_TYPE['PRICE'],
                duration: str = C.SUPPORTED_TIME_DURATIONS["WEEK"], 
                start_date: str = get_last_monday(),
                series: str = 'BE') -> pd.DataFrame:
    """All top level gainers for a specific instrument and for a given period of time.
    
    Parameters
    ----------
        file_type : str
    The type of file required. (bhavcopy, pe, etc.) 
    Invoke core.supported_file_types for all the supported file types.
        start_date : str
    Starting date. (Format: 'DD-Mon-YYYY. Ex., 12-Jun-2025)
        end_date : str
    Starting date. (Format: 'DD-Mon-YYYY. Ex., 12-Jun-2025)
        series: str
    The series of the instrument, defaulted to 'BE'

    Returns
    -------
    pandas.DataFrame
        Data Frame containing the results OR empty DF in case of any error/exceptions.
    """
    logger.info(f"[{file_type = }], [{gain_type = }], [{duration = }], [{start_date = }], [{series = }]")
    data = pd.DataFrame()
    #NOTE: Basic validations
    if file_type.upper() not in C.SUPPORTED_FILE_TYPES:
        logger.error(f"Unsupported [{file_type = }]")
        return data

    if gain_type.upper() not in C.GAIN_TYPE:
        logger.error(f'Unsupported [{gain_type = }]')
        return data

    if duration.upper() not in C.SUPPORTED_TIME_DURATIONS:
        logger.error(f"Unsupported [{duration = }]")
        return data

    #NOTE:  Verify that the date is correct (not in future etc.)
    if not is_date_valid(start_date):
        logger.error(f"Invalid [{start_date = }]")
        return data
    #TODO: Get the dataset for the specified time
    match file_type:
        #TODO: FIX the hardcoded "INDEX" value. Read from SUPPORTED_FILE_TYPES
        case "INDEX":
            return get_index_gainers(duration, start_date)
        case "PE": #TODO: 
            logger.error(f"NOT IMPLEMENTED . . . . ..  ")
            return data
        case "STOCK":
            match duration.upper():
                case "WEEK":
                    return gainers.weekly_gainers(start_date, series)
                case _:
                    pd.DataFrame()
            return data 
        case _: #Unkown type
            logger.error(f"Unknown file type!")
            return data 

def get_index_gainers(
                duration: str = C.SUPPORTED_TIME_DURATIONS["WEEK"], 
                start_date: str = get_last_monday()) -> pd.DataFrame:
    logger.info(f"[{duration = }], [{start_date = }]")
    data = pd.DataFrame()
    #NOTE: For weekly index data processing
    if duration == C.SUPPORTED_TIME_DURATIONS.get("WEEK"):
        end_date = datetime.strptime(start_date, C.DATE_FMT) + timedelta(days=5)
        date_range = compose_dates_from_range(start_date, end_date.strftime(C.DATE_FMT))
        #NOTE: You should not get an empty date range
        if not date_range:
            logger.error(f"Invalid start date: {start_date}. Please provide correct start date for the week!")
            return data

        #NOTE: Read and merge all the index list files.
        weekly_data_list = list() # Gather all daily data in a temporary list
        daily_index_data = pd.DataFrame()
        for dt in date_range:
            #TODO: try using get local file name
            index_file = compose_local_index_file_name(dt)
            try:
                daily_index_data = pd.read_csv(index_file)
                daily_index_data["TRADING_DATE"] = datetime.strptime(dt, C.DATE_FMT) # Add trading date field
                daily_index_data.set_index("TRADING_DATE") # set the index trading date field
                logger.info(f"The dataframe index is: [{daily_index_data.index}]")
                daily_index_data.to_csv(f"daily_index_data-{dt}.csv")
            except pd.errors.EmptyDataError:
                logger.error(f"Index data not found for file: [{index_file}]")
            except FileNotFoundError:
                logger.error(f"Index file [{index_file}] not found!")
            # logger.debug(f"Trade Data is: {trd_dt_data}")
            weekly_data_list.append(daily_index_data)
        data = pd.concat(weekly_data_list) # All data in list is added to Pandas data frame for efficiency
        data.to_csv("nothing.csv")
        # REFERENCE: https://pandas.pydata.org/docs/user_guide/merging.html
        # logger.info(f"The Data is: {data}")
        # data.to_csv("All_data.csv")
        #TODO: Now, process the data for gainers.
        # data.groupby()
        return data
    return data

def get_stock_gainers(start_date, series: str):
    """
    """
    logger.debug(f'[{start_date = }], [{series = }]')
    weekly_data = compose_weekly_data(start_date, C.SUPPORTED_FILE_TYPES["STOCK"]) # Default falls back to STOCK


if __name__ == "__main__":
    logger.info(f"Main Called.")
    today = date.today()
    data = top_gainers(file_type=C.SUPPORTED_FILE_TYPES["INDEX"], 
                       duration=C.SUPPORTED_TIME_DURATIONS["WEEK"],
                       start_date=today.strftime(C.DATE_FMT)) 
    logger.debug(f"The size of data is: [{len(pd.DataFrame(data))}]")
