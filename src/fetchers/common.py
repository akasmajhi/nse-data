from datetime import datetime
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from src.constants import (
    DATE_FMT,
    REQ_HEADER,
    NSE_DUMMY_REQ_URL,
    SUPPORTED_FILE_TYPES,
    FILES_BASE_DIR,
    MCAP_FOLDER,
)
from src.helpers.cross_cutting import benchmark
from loguru import logger


def dummy_request(url: str = NSE_DUMMY_REQ_URL):
    """Creates a dummy request to fetch headers so that
    the headers can be used in subsequent requests to the exchange.
    """
    retries = Retry(
        total=5,  # Total number of retries
        backoff_factor=0.1,  # Delay between retries
        status_forcelist=[429, 500, 502, 503, 504],  # Status codes to retry on
        allowed_methods=frozenset({"GET"}),  # Limit retries to GET requests
    )
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retries))
    # TODO: Incorporate exception handling here!
    r = session.get(url, headers=REQ_HEADER, timeout=3)
    return r


@benchmark
def get_subfolders(folder: str) -> list[str]:
    """Gets the dubfolders for a given folder.

    Parameters
    ----------
        folder: str
    The name of the folder.

    Returns
    -------
        list[str]
    The names of the subfolder(s).
    """
    logger.debug(f"[{folder = }]")
    subfolders = list()
    for item in os.listdir(folder):
        full_path = os.path.join(folder, item)
        if os.path.isdir(full_path):
            subfolders.append(item)
    return subfolders


@benchmark
def get_last_fetch_date(file_type: str) -> str | None:
    """Calculate the last fetch date from the locally stored files.

    Parameter
    ---------
        file_type: str
    One of SUPPORTED_FILE_TYPES.

    Returns
    -------
        str
    Last fetch date in the format src.constants.DATE_FMT
    """
    logger.debug(f"[{file_type = }]")
    if file_type not in SUPPORTED_FILE_TYPES:
        logger.error(f"Invalid [{file_type = }]")
        return None

    match file_type:
        case "STOCK" if file_type == SUPPORTED_FILE_TYPES["STOCK"]:
            pass
        case "META" if file_type == SUPPORTED_FILE_TYPES["META"]:
            meta_folder = os.path.join(
                FILES_BASE_DIR,
                SUPPORTED_FILE_TYPES["STOCK"],
                SUPPORTED_FILE_TYPES["META"],
            )

            meta_subfolders = get_subfolders(meta_folder)
            # NOTE: Check if the sub-folder is valid
            valid_subfolders = list()
            for item in meta_subfolders:
                try:
                    # logger.info(f'[{item = }]')
                    sub_folder_dt = datetime.strptime(item, DATE_FMT)
                    valid_subfolders.append(sub_folder_dt)
                except ValueError:
                    logger.error(f"Invalid subfolder [{item = }]")
            # NOTE: From the list of sub-folders, pick the latest one
            return (
                max(valid_subfolders).strftime(DATE_FMT) if valid_subfolders else None
            )
        case "MARKET_CAP" if file_type == SUPPORTED_FILE_TYPES["MARKET_CAP"]:
            # NOTE: Read names of all the sub-folder of M_CAP folder
            mcap_folder = os.path.join(
                FILES_BASE_DIR, SUPPORTED_FILE_TYPES["STOCK"], MCAP_FOLDER
            )
            mcap_subfolders = get_subfolders(mcap_folder)
            # NOTE: Check if the sub-folder is valid
            valid_subfolders = list()
            for item in mcap_subfolders:
                try:
                    # logger.info(f'[{item = }]')
                    sub_folder_dt = datetime.strptime(item, DATE_FMT)
                    valid_subfolders.append(sub_folder_dt)
                except ValueError:
                    logger.error(f"Invalid subfolder [{item = }]")
            # NOTE: From the list of sub-folders, pick the latest one
            return (
                max(valid_subfolders).strftime(DATE_FMT) if valid_subfolders else None
            )
        case _:
            logger.error(f"[{file_type = }] Not supported for this op.")
            return None


if __name__ == "__main__":
    # dummy_request("https://www.nseindia.com/all-reports")
    # logger.info(get_subfolders(folder='data_files/STOCK/market_cap'))
    logger.info(get_last_fetch_date(file_type=SUPPORTED_FILE_TYPES["MARKET_CAP"]))
    # logger.info(get_last_fetch_date(file_type=SUPPORTED_FILE_TYPES["META"]))
