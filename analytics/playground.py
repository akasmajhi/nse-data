import pandas as pd
import numpy as np
from pandas import DataFrame, Series

import os

#%% Constants
PE_DATA_DIR='/home/akasmajhi/source/nse-data/data_files/PE/'
BHAV_DATA_DIR='/home/akasmajhi/source/nse-data/data_files/BHAVCOPY/'
PREOPEN_DATA_DIR='/home/akasmajhi/source/nse-data/data_files/PREOPEN/'
#%% SECTION: Reading & Writing Data in Text Format

bhav_file = "bhavcopy_12-Aug-2025.csv"

def read_data_file(file_name: str):

    df = DataFrame()
    try:
        df = pd.read_csv(os.path.join(BHAV_DATA_DIR, file_name))
    except FileNotFoundError:
        print(f"The File [{file_name}]is not found!")
    return df

df = read_data_file(bhav_file)
df.columns
df[df.TckrSymb == "INFY"][["Src", "OpnPric", "HghPric", "LwPric", "ClsPric", "LastPric", "PrvsClsgPric", "TtlTradgVol"]]

cols = ["trade_dt", "biz_dt", "segment", "source", "FinInstrmTp", "FinInstrmId", \
                 "ISIN", "symbol", "SctySrs", "expiry_dt", "FininstrmActlXpryDt", \
                 "strike_price", "OptnTp", "FinInstrmNm", "open", "high", "low", "close", \
                 "last", "previous_close", "UndrlygPric", "settlement_price", "oi", 
                 "change_in_oi", "total_traded_volume", "total_traded_value", "TtlNbOfTxsExctd", 
                 "SsnId", "NewBrdLotQty", "Rmks", "Rsvd1", "Rsvd2", "Rsvd3", "Rsvd4"]

# cols # pyright: ignore[reportUnusedExpression]

# bhav_data = pd.read_csv(os.path.join(BHAV_DATA_DIR, bhav_file), header=None)
bhav_data = pd.read_csv(os.path.join(BHAV_DATA_DIR, bhav_file), names=cols, header=None, skiprows=1)
bhav_data["pct_change"] = (bhav_data['close'] - bhav_data['previous_close']) / bhav_data['previous_close'] * 100
# bhav_data # pyright: ignore[reportUnusedExpression]
required_symbols = ["trade_dt", "symbol", "open", "high", "low", "close", "last", "previous_close", "pct_change"]
bhav_data[bhav_data.segment == "CM"][required_symbols]


gainers = DataFrame(bhav_data[bhav_data.close > bhav_data.previous_close][required_symbols])

gainers # pyright: ignore[reportUnusedExpression]
# top_gainers = gainers.sort_values()
losers = DataFrame(bhav_data[bhav_data.close <= bhav_data.previous_close][required_symbols])

losers.head()


