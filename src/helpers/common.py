from loguru import logger

from src.helpers.validators import isDateValid

def composeDatesFromRange(s_date: str, e_date:str):
    """
        Compose a list of trading dates from the supplied range.
    Parameters
    ----------
        s_date: str
    Start date in the format of DD-Mon-YYYY. e.g., 14-Jun-2025
        e_date: str
    End date in the format of DD-Mon-YYYY. e.g., 14-Jun-2025

    Returns
    -------
        list
    List containing the valid trading dates.
    """
    logger.debug(f"start_date: [{s_date}], end_date: [{e_date}]")
    # Validations - 1: Ensure both trading dates are valid
    if ( not isDateValid(s_date) and isDateValid(e_date) ):
        logger.error(f"Range dates are Invalid")
        return d_range # Empty list return (BAD IDEA) #TODO
    # Validations - 2: Ensure e_date >= s_date

    d_range = list()
    logger.info(f"Valid trading dates: [{d_range}]")
    return d_range
