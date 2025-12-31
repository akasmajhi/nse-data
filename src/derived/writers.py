import os
import json

import pandas as pd
from loguru import logger

import src.constants as C
from src.helpers.cross_cutting import benchmark


@benchmark
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
    industry_stock: dict = dict()

    # NOTE: THis is the META folder for the input files.
    meta_folder = os.path.join(
        C.FILES_BASE_DIR,
        C.SUPPORTED_FILE_TYPES["STOCK"],
        C.SUPPORTED_FILE_TYPES["META"],
        f"{trading_date}",
    )
    files: list = list()
    try:
        files = os.listdir(meta_folder)
    except FileNotFoundError:
        logger.error(f"Empty META folder [{meta_folder = }]for [{trading_date = }]")
        return dict()  # NOTE: Returning blank dict on error condition
    # NOTE: If the derived data already exists, no point re-building it
    ind_stock_file = os.path.join(
        C.FILES_BASE_DIR,
        C.SUPPORTED_FILE_TYPES["DERIVED"],
        C.IND_TO_STOCK_FOLDER,
        f"{C.IND_TO_STOCK_FOLDER}-{trading_date}.json",
    )
    logger.debug(f"[{ind_stock_file = }]")
    if os.path.exists(ind_stock_file):
        logger.error(f"File [{ind_stock_file = }] already exists!")
        return dict()
    # return dict()
    processed = 0
    ind_key = "industry"

    for file in files:
        with open(os.path.join(meta_folder, file), "r") as f:
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


@benchmark
def combine_m_caps(folder: str) -> dict:
    """Combine all the m_cap files data onto a fingle file for efficiency.
    Parameters
    ----------
        str
    Market Cap folder that contains all the individual m_cap file.
    (1 for each stock).

    Returns
    -------
        dict
    Dictionary containing the combined market caps.

    Note
    ----
    File name is hard-coded to combined.json
    """
    logger.info(f"Combining market caps for [{folder = }]")
    # NOTE: Check if the folder exists
    mcap_folder = os.path.join(
        C.FILES_BASE_DIR,
        C.SUPPORTED_FILE_TYPES["STOCK"],
        C.MCAP_FOLDER,
        folder,
    )
    if not os.path.isdir(mcap_folder):
        logger.error(f"Invalid [{mcap_folder = }]")
        return dict()
    # ERROR: do not combine if the combined file already exists
    if os.path.isfile(os.path.join(mcap_folder, "combined.json")):
        logger.error(f"Not combining since the combined file already exists!")
        logger.info(f"Use the readers.combined_m_caps for reading content")
        return {}
    # NOTE: Read each file and extract market cap
    try:
        mcap_files = os.listdir(mcap_folder)
        mcap_dict = dict()
        for m_cap_file in mcap_files:  # NOTE: Process each file
            mcap_json_file = os.path.join(mcap_folder, m_cap_file)
            with open(mcap_json_file, "r") as file:
                mcap_json = json.load(file)
                try:
                    mcap_dict[m_cap_file[:-5]] = mcap_json
                except KeyError:
                    logger.error(f"Error reading m_cap for [{m_cap_file = }]")
        output_filename = os.path.join(mcap_folder, "combined.json")
        with open(output_filename, "w") as json_file:
            json.dump(mcap_dict, json_file, indent=4)
        return mcap_dict
    except FileNotFoundError:
        logger.error(f"Directory not found at [{mcap_folder = }]")
    except NotADirectoryError:
        logger.error(f"[{mcap_folder = }] is not a directory")
    except PermissionError:
        logger.error(f"Permission denied to access [{mcap_folder = }].")
    return dict()


def write_weekly_data(start_date: str, file_type: str, data: pd.DataFrame):
    logger.info(f"Writing weekly file for [{start_date = }], [{file_type = }]")
    if file_type == C.SUPPORTED_FILE_TYPES["STOCK"]:
        file_name = os.path.join(
            C.FILES_BASE_DIR,
            C.SUPPORTED_FILE_TYPES["DERIVED"],
            C.WEEKLY_FOLDER,
            C.SUPPORTED_FILE_TYPES["STOCK"],
            f"{start_date}.csv",
        )
        logger.debug(f"Writing CSV path [{file_name}]")
        data.to_csv(file_name)


if __name__ == "__main__":
    # print(industry_to_stock("10-Oct-2025"))
    print(industry_to_stock("15-Oct-2025"))
    print(industry_to_stock("16-Oct-2025"))
    print(industry_to_stock("25-Oct-2025"))
    print(industry_to_stock("01-Nov-2025"))
    print(industry_to_stock("09-Nov-2025"))
    print(industry_to_stock("17-Nov-2025"))
    print(industry_to_stock("23-Nov-2025"))
    print(industry_to_stock("29-Nov-2025"))
    print(industry_to_stock("14-Dec-2025"))
    print(industry_to_stock("20-Dec-2025"))
    # print(industry_to_stock("18-Oct-2025"))
