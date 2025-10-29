from datetime import datetime, timedelta
from loguru import logger

import src.constants as C


def get_last_trading_date() -> str:
    # NOTE: If it is a weekday and time is > 7 PM
    today = datetime.today()
    logger.info(f"[{today = }], [{today.weekday() = }], [{today.hour = }]")
    if today.weekday() < 5 and today.hour < 19:  # NOTE: Weekday before 7PM
        # print(f"[DDDDDDDDDDDDDDD: {common.get_last_trading_date()} = ]")
        return (today - timedelta(days=1)).strftime(C.DATE_FMT)

    if today.weekday() < 5 and today.hour >= 19:  # NOTE: Weekday after 7PM
        return today.strftime(C.DATE_FMT)

    # return common.get_last_friday()  # NOTE: For weekends
    return ""
