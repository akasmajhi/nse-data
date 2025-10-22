import os
import json
import time

from loguru import logger

import src.constants as C


def get_industry_to_stock(trading_date: str) -> dict:
    logger.debug(f"[{trading_date = }]")
    start_time = time.perf_counter()
    file_name = os.path.join(
        C.FILES_BASE_DIR,
        C.SUPPORTED_FILE_TYPES["DERIVED"],
        C.IND_TO_STOCK_FOLDER,
        f"{C.IND_TO_STOCK_FOLDER}-{trading_date}.json",
    )
    if file_name:
        logger.info(f"File existing!")
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                data: dict = json.load(file)
            end_time = time.perf_counter()
            logger.info(f"Elapsed: {(end_time - start_time):.6f} seconds")
            return data
        except FileNotFoundError:
            logger.error(f"{file_name = } does not exist!")
            return dict()
        except json.JSONDecodeError:
            logger.error(f"Error decoding {file_name = }")
            return dict()

    else:
        logger.error(f"{file_name = } does not exist!")
        return dict()


if __name__ == "__main__":
    print(get_industry_to_stock(trading_date="18-Oct-2025"))
