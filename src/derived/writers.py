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
    start_time = time.perf_counter()
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
        end_time = time.perf_counter()
        logger.info(f"Execution time: {(end_time - start_time):.6f} seconds")
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
                    end_time = time.perf_counter()
                    logger.info(
                        f"Execution time: {(end_time - start_time):.6f} seconds"
                    )
        output_filename = os.path.join(mcap_folder, "combined.json")
        with open(output_filename, "w") as json_file:
            json.dump(mcap_dict, json_file, indent=4)
        end_time = time.perf_counter()
        logger.info(f"Execution time: {(end_time - start_time):.6f} seconds")
        return mcap_dict
    except FileNotFoundError:
        logger.error(f"Directory not found at [{mcap_folder = }]")
        end_time = time.perf_counter()
        logger.info(f"Execution time: {(end_time - start_time):.6f} seconds")
    except NotADirectoryError:
        logger.error(f"[{mcap_folder = }] is not a directory")
        end_time = time.perf_counter()
        logger.info(f"Execution time: {(end_time - start_time):.6f} seconds")
    except PermissionError:
        logger.error(f"Permission denied to access [{mcap_folder = }].")
        end_time = time.perf_counter()
        logger.info(f"Execution time: {(end_time - start_time):.6f} seconds")
    end_time = time.perf_counter()
    logger.info(f"Execution time: {(end_time - start_time):.6f} seconds")
    return dict()


if __name__ == "__main__":
    print(industry_to_stock("18-Oct-2025"))
