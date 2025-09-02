"""
    Top level wrapper for all analytics related queries.
"""
import pandas as pd
from datetime import datetime, timedelta, date

from loguru import logger
from src.helpers.common import get_last_monday, composeDatesFromRange, compose_local_index_file_name
from src.constants import SUPPORTED_FILE_TYPES, SUPPORTED_TIME_DURATIONS, \
    DATE_FMT 
from src.helpers.validators import isDateValid

def top_gainers(file_type: str = SUPPORTED_FILE_TYPES["INDEX"], 
                duration: str = SUPPORTED_TIME_DURATIONS["WEEK"], 
                start_date: str = get_last_monday()) -> pd.DataFrame:
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

    Returns
    -------
    pandas.DataFrame
        Data Frame containing the results
    """
    logger.info(f"file_type: [{file_type}], duration: [{duration}], start_date: [{start_date}]")
    data = pd.DataFrame()
    if file_type not in SUPPORTED_FILE_TYPES.values():
        logger.error(f"Invalid file type: [{file_type}]")
        return data
    if duration not in SUPPORTED_TIME_DURATIONS.values():
        logger.error(f"Invalid time duration: [{duration}]")
        return data
    #NOTE:  Verify that the date is correct (not in future etc.)
    if not isDateValid(start_date):
        logger.error(f"Invalid start date: [{start_date}]")
        return data
    #TODO: Get the dataset for the specified time
    match file_type:
        #TODO: FIX the hardcoded "INDEX" value. Read from SUPPORTED_FILE_TYPES
        case "INDEX":
            return get_index_gainers(duration, start_date)
        case "PE": #TODO: 
            logger.error(f"NOT IMPLEMENTED . . . . ..  ")
            return data
        case _: #Unkown type
            logger.error(f"Unknown file type!")
            return data 

def get_index_gainers(
                duration: str = SUPPORTED_TIME_DURATIONS["WEEK"], 
                start_date: str = get_last_monday()) -> pd.DataFrame:
    logger.info(f"duration: [{duration}], start_date: [{start_date}]")
    data = pd.DataFrame()
    #NOTE: For weekly index data processing
    if duration == SUPPORTED_TIME_DURATIONS.get("WEEK"):
        end_date = datetime.strptime(start_date, DATE_FMT) + timedelta(days=5)
        date_range = composeDatesFromRange(start_date, end_date.strftime(DATE_FMT))
        #NOTE: You should not get an empty date range
        if not date_range:
            logger.error(f"Invalid start date: {start_date}. Please provide correct start date for the week!")
            return data

        #NOTE: Read and merge all the index list files.
        weekly_data_list = list() # Gather all daily data in a temporary list
        daily_index_data = pd.DataFrame()
        for dt in date_range:
            index_file = compose_local_index_file_name(dt)
            try:
                daily_index_data = pd.read_csv(index_file)
                daily_index_data["TRADING_DATE"] = datetime.strptime(dt, DATE_FMT) # Add trading date field
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

if __name__ == "__main__":
    logger.info(f"Main Called.")
    today = date.today()
    data = top_gainers(file_type=SUPPORTED_FILE_TYPES["INDEX"], 
                       duration=SUPPORTED_TIME_DURATIONS["WEEK"],
                       start_date=today.strftime(DATE_FMT)) 
    logger.debug(f"The size of data is: [{len(pd.DataFrame(data))}]")
