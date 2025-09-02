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
        The name of the index as presented in the index listing page.
        https://www.nseindia.com/market-data/live-market-indices

    Returns
    -------
    pandas.DataFrame
        Data Frame containing the results
    """
    logger.info(f"Index is: {idx}")
    if idx not in IDX_NAMES:
        return 
    return 100
