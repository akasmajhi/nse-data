from loguru import logger

import pandas as pd

from src.constants import SUPPORTED_FILE_TYPES, SUPPORTED_TIME_DURATIONS
from src.helpers.validators import get_latest_file
from src.fetchers.common import get_last_fetch_date
from src.derived.readers import combined_m_caps


class Scanner:
    def __init__(self, scanner, *args, **kwargs):
        logger.debug(f"{scanner = }, {args = }, {kwargs = }")
        self.scanner = scanner
        self.args = args
        self.kwargs = kwargs

    def run(self):
        return self.scanner(*self.args, **self.kwargs)


def inverted_hammer(timeframe: str, shadow_multiplier: int = 9):
    logger.debug(f"Scanning for inverted hammer with {timeframe = }")
    # NOTE: Get the latest BHAVCOPY
    if timeframe != SUPPORTED_TIME_DURATIONS["DAY"]:
        print(f"This {timeframe = } is not supported")
        return pd.DataFrame()  # NOTE: Empty dataframe for ay error
    data = get_latest_file(SUPPORTED_FILE_TYPES["BHAVCOPY"])
    if not data.empty:
        # Step-1 Ensure it's a green candle
        is_green = data["ClsPric"] > data["OpnPric"]
        # Step-2 Calculate the size of the candle body
        body_size = data["ClsPric"] - data["OpnPric"]
        # Step-3 Calculate the length of the upper shadow
        upper_shadow_size = data["HghPric"] - data["ClsPric"]
        # Step-4 Define the condition for a "Long" upper shadow

        # The shadow must be significantly longer than the body (param)

        has_long_upper_shadow = upper_shadow_size > (body_size * shadow_multiplier)

        # NOTE: Combine both conditions

        data["Is_Green_Long_Upper_Shadow"] = is_green & has_long_upper_shadow
        data_without_m_cap = data[data["Is_Green_Long_Upper_Shadow"] == True]

        logger.info(f"Total stocks  {len(data_without_m_cap) =}")
        # DONE: Combine this with market cap of the stock
        m_cap_date = get_last_fetch_date(file_type=SUPPORTED_FILE_TYPES["MARKET_CAP"])
        if m_cap_date:
            m_cap_data = combined_m_caps(folder=m_cap_date)
            m_cap_data_df = pd.DataFrame(
                {"TckrSymb": m_cap_data.keys(), "total_m_cap": m_cap_data.values()}
            )
            # logger.info(f"{m_cap_data = }")
            data_with_m_cap: pd.DataFrame = pd.merge(
                data_without_m_cap,
                m_cap_data_df,
                on="TckrSymb",
                # data, m_cap_data_df, on="TckrSymb", how="left", indicator="exists_in"
            )
            return data_with_m_cap
        return data_without_m_cap
    return pd.DataFrame()  # NOTE: Empty dataframe for any error
