import src.constants as C
from loguru import logger

from src.helpers.validators import is_date_valid


def validate_engulfers(start_date: str, instrument: str, duration: str):
    logger.debug(f"[{start_date = }], [{instrument = }], [{duration = }]")
    allowed_instruments: list = [
        C.SUPPORTED_FILE_TYPES["STOCK"],
        C.SUPPORTED_FILE_TYPES["INDEX"],
    ]
    if instrument not in allowed_instruments:
        raise ValueError(f"Invalid {instrument = }. Allowed are {allowed_instruments}")
    if not is_date_valid(i_date=start_date):
        raise ValueError(f"Invalid trading start date [{start_date = }]")
    allowed_durations: list = [
        C.SUPPORTED_TIME_DURATIONS["DAY"],
        C.SUPPORTED_TIME_DURATIONS["WEEK"],
        C.SUPPORTED_TIME_DURATIONS["MONTH"],
    ]
    if duration not in allowed_durations:
        raise ValueError(f"Invalid [{duration = }]. Supported are {allowed_durations}")
