from loguru import logger

def get_local_data(file_type: str, start_date: str, end_date:str):
    """
        Gets the data from the local store. If data is valid and not found
        locally, then you source the data from remote.
    """
    logger.debug(f"Getting data for: file_type: {file_type}, start_date: {start_date}, \
            end_date: {end_date}")

    # Validate the date ranges
    # Look for data
    # If data not found locally, issue remote fetch
    return False
