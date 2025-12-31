from time import perf_counter
from typing import Any, Callable
from loguru import logger
import os
from datetime import datetime, timedelta


def benchmark(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwrgs: Any) -> Any:
        start_time = perf_counter()
        value = func(*args, **kwrgs)
        end_time = perf_counter()
        logger.info(
            f"Finished [{func.__name__}] in [{(end_time-start_time):.2f}] seconds."
        )
        return value

    return wrapper


def is_file_old(filepath: str, minutes: int) -> bool:
    """
    Checks if the file at the given filepath is older than x minutes.

    Args:
        filepath (str): The path to the file.
        minutes (int/float): The age threshold in minutes.

    Returns:
        bool: True if the file is older than the specified minutes, False otherwise.
    """
    # Get the file's last modification timestamp (in seconds since the epoch)
    modification_timestamp = os.path.getmtime(filepath)

    # Convert the timestamp to a datetime object
    modification_time = datetime.fromtimestamp(modification_timestamp)

    # Calculate the time difference (duration) since the file was last modified
    time_difference = datetime.now() - modification_time

    # Define the threshold as a timedelta object
    threshold = timedelta(minutes=minutes)

    # Compare the time difference with the threshold
    return time_difference > threshold
