import pandas as pd

from loguru import logger
from src.constants import SUPPORTED_FILE_TYPES
from src.helpers.common import (
    get_last_monday,
    is_start_date_Monday,
    get_week_ending_date,
)
from src.helpers.file_readers import get_local_data


def compose_weekly_data(
    start_date: str = get_last_monday(),
    file_type: str = SUPPORTED_FILE_TYPES["STOCK"],
    instr_name: str = "",
) -> pd.DataFrame:
    """Composes the weekly data for a given instrument
    Parameters
    ----------

    start_date : str
        Starting date of the week. (Format: 'DD-Mon-YYYY. Ex., 12-Jun-2025)
    instr_type : str
        The type of instrument (STK, IDX, OPT, etc.)
        Invoke core.supported_instr_types for all the supported instr types.
        end_date : str
        Starting date. (Format: 'DD-Mon-YYYY. Ex., 12-Jun-2025)

    Returns
    -------
    pandas.DataFrame
        Data Frame containing the results

    Assumptions
    -----------
    1. Start of the week is Monday or #TODO: the following business day if Monday is a holiday.
    2.
    """
    data = pd.DataFrame()
    logger.debug(f"[{start_date = }], [{file_type = }], [{instr_name = }]")
    if start_date != get_last_monday():
        # Ensure that it is a Monday
        if not is_start_date_Monday(start_date):
            logger.error(f"[{start_date = }] is not a Monday.")
            return data
    end_date = get_week_ending_date(start_date)
    if not instr_name and file_type == SUPPORTED_FILE_TYPES["STOCK"]:
        return get_local_data(
            file_type=SUPPORTED_FILE_TYPES["BHAVCOPY"],
            start_date=start_date,
            end_date=end_date,
        )
    # There is a stock or index name provided
    else:
        # TODO: Handle this scenario
        pass

    return data


if __name__ == "__main__":
    data = compose_weekly_data()
    # data.to_csv("weekly_data.csv")
