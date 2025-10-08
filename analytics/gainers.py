import pandas as pd
from loguru import logger
from src.constants import SUPPORTED_FILE_TYPES

def daily_gainer(file_type: str = SUPPORTED_FILE_TYPES['BHAVCOPY'],
                     series: str = 'EQ'):
    logger.debug(f'[{file_type = }], [{series = }]')
    return pd.DataFrame()

def weekly_gainer(file_type: str = SUPPORTED_FILE_TYPES['BHAVCOPY'],
                      series: str = 'EQ') -> pd.DataFrame :
    logger.debug(f'[{file_type = }], [{series = }]')
    return pd.DataFrame()

def monthly_gainer(file_type: str = SUPPORTED_FILE_TYPES['BHAVCOPY'],
                      series: str = 'EQ') -> pd.DataFrame :
    logger.debug(f'[{file_type = }], [{series = }]')
    return pd.DataFrame()
