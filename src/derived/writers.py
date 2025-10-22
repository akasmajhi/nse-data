import os
import json
import time

from loguru import logger

import src.constants as C


def industry_to_stock(trading_date: str) -> dict:
    """For a given trading date, this function writes and returns the industry-to-stock
    mapping.
    Parameters
    ----------
        str
    Trading date in src.constants.DATE_FMT format

    Returns
    -------

    """
    logger.debug(f"[{trading_date = }]")
    start_time = time.perf_counter()
    industry_stock: dict = dict()

    files_dir = os.path.join(
        C.FILES_BASE_DIR,
        C.SUPPORTED_FILE_TYPES["STOCK"],
        C.SUPPORTED_FILE_TYPES["META"],
    )
    files: list = list()
    try:
        files = os.listdir(os.path.join(files_dir, trading_date))
    except FileNotFoundError:
        logger.error(f"[{files_dir = }] does not exist!")
        end_time = time.perf_counter()
        logger.info(f"Elapsed: {(end_time - start_time):.6f} seconds")
        return dict()  # NOTE: Returning blank dict on error condition
    # NOTE: If the derived data already exists, no point re-building it
    if os.path.join(
        C.FILES_BASE_DIR,
        C.SUPPORTED_FILE_TYPES["DERIVED"],
        C.IND_TO_STOCK_FOLDER,
        f"{C.IND_TO_STOCK_FOLDER}-{trading_date}.json",
    ):
        logger.info(f"File already exists!")
        end_time = time.perf_counter()
        logger.info(f"Elapsed: {(end_time - start_time):.6f} seconds")
        return {}
    processed = 0
    ind_key = "industry"

    for file in files:
        with open(os.path.join(files_dir, trading_date, file), "r") as f:
            f_dict = json.loads(f.read())
            try:
                industry = f_dict["metadata"][ind_key]  # TODO: move it to constants
                if "NA" in industry.upper():
                    pass
                else:
                    try:
                        if industry in industry_stock:
                            industry_stock[industry].append(file[:-10])
                        else:
                            industry_stock[industry] = [file[:-10]]
                    except KeyError:  # HACK: This will probably never get executed!
                        industry_stock[industry] = [file[:-10]]

                processed = processed + 1
            except KeyError:
                pass
    logger.info(f"Total files {processed = }")
    end_time = time.perf_counter()
    logger.info(f"Elapsed: {(end_time - start_time):.6f} seconds")
    # NOTE: Write the contents to the file now
    write_dir = os.path.join(
        C.FILES_BASE_DIR, C.SUPPORTED_FILE_TYPES["DERIVED"], C.IND_TO_STOCK_FOLDER
    )
    if os.path.isdir(write_dir):
        with open(
            os.path.join(write_dir, f"{C.IND_TO_STOCK_FOLDER}-{trading_date}.json"), "w"
        ) as json_file:
            json.dump(industry_stock, json_file, indent=4)
    else:
        logger.error(f"{write_dir = } does not exist. Check config!")
    return industry_stock


if __name__ == "__main__":
    print(industry_to_stock("18-Oct-2025"))
