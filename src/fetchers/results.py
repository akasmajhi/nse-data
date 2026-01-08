from datetime import datetime
from loguru import logger
import requests
from http import HTTPStatus
import os

import pandas as pd

from src.constants import (
    DATE_FMT,
    FILES_BASE_DIR,
    NSE_RESULTS_URL,
    NSE_DUMMY_REQ_URL,
    REQ_HEADER,
)
from src.fetchers.common import dummy_request
from src.helpers.cross_cutting import benchmark


@benchmark
def fetch_result_calendar() -> pd.DataFrame:
    """
        Fetches the data results calendar from remote.

    Parameters
    ----------
       None

    Returns
    -------
        pandas.DataFrame
    Containing the data that is read from remote. Start date of fecth is today.
    """
    file_name = f"result-{datetime.today().strftime(DATE_FMT)}.json"
    # NOTE: If file exists for today, then don't fetch
    if os.path.exists(os.path.join(FILES_BASE_DIR, "RESULTS", file_name)):
        logger.info(f"Result [{file_name = }] already exists.")
        return pd.read_json(os.path.join(FILES_BASE_DIR, "RESULTS", file_name))

    data = pd.DataFrame()
    from_date: str = datetime.today().strftime("%d-%m-%Y")
    logger.info(f"{from_date = }")
    try:
        dummy_res = dummy_request(NSE_DUMMY_REQ_URL)
        """
            https://www.nseindia.com/api/event-calendar?index=equities&from_date=08-01-2026&to_date=08-03-2026
        """
        payload = {
            "index": "equities",
            "from_date": from_date,
            # "from_date": "08-01-2026",
            "to_date": "08-03-2026",
        }
        result_res = requests.get(
            url=NSE_RESULTS_URL,
            headers=REQ_HEADER,
            params=payload,
            cookies=dummy_res.cookies,
            timeout=8,
        )
        if result_res.status_code == HTTPStatus.OK:
            with open(os.path.join(FILES_BASE_DIR, "RESULTS", file_name), "w") as file:
                file.write(result_res.text)
                return pd.read_json(os.path.join(FILES_BASE_DIR, "RESULTS", file_name))
    except Exception as e:
        logger.error(f"Exception occured while fetching results calendar. [{e = }]")
    return data
