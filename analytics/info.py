"""
    Get the data (from the exchanges) that is informational in nature.
"""
from loguru import logger
from src.constants import IDX_NAMES

def get_idx_market_cap(idx: str):
    """Gets the market at the basket level. It's an aggregated market cap.
    Parameters
    ----------

    idx : str
        The name of the index as enumerated in src/constants.IDX_NAMES
        Invoke core.supported_file_types for all the supported file types.
    start_date : str
        Starting date. (Format: 'DD-Mon-YYYY. Ex., 12-Jun-2025)
    end_date : str
        Starting date. (Format: 'DD-Mon-YYYY. Ex., 12-Jun-2025)

    Returns
    -------
    pandas.DataFrame
        Data Frame containing the results
    """
    logger.info(f"Index is: {idx}")
    if idx not in IDX_NAMES:
        return 
    return 100
