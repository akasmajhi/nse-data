import pandas as pd
from pandas import DataFrame

import os

from pandas.core.arrays import period
from pandas.core.frame import IgnoreRaise

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

#%% NOTE: INDEX Related Data Processing
import pandas as pd
from pandas import DataFrame
import sys 
sys.path.append("/home/akasmajhi/anaconda3/envs/nse-data/lib/python3.11/site-packages")
from analytics.core import top_gainers
from src.constants import SUPPORTED_FILE_TYPES, SUPPORTED_TIME_DURATIONS

data: pd.DataFrame = top_gainers(file_type=SUPPORTED_FILE_TYPES["INDEX"], 
                                 duration=SUPPORTED_TIME_DURATIONS["WEEK"], 
                                 start_date="25-Aug-2025") 

data.index
data .columns
data.columns = data.columns.str.replace(' \n', '')
data.columns
new_line_char = 'INDEX'
data[f"{new_line_char}"]
# data.to_csv("XYZ.csv")

#%%
dt = "01-Sep-2025"
index_file_name = f"index_{dt}.csv"
daily_index_data = pd.read_csv(f"data_files/INDEX/{index_file_name}")
daily_index_data# pyright: ignore[reportUnusedExpression]
daily_index_data.index
daily_index_data.columns
replace_str = " \n"
daily_index_data.columns = daily_index_data.columns.str.replace(replace_str, '')
daily_index_data.index
daily_index_data.columns
daily_index_data["TRADING_DATE"] = dt

# pd.DataFrame.set_index(daily_index_data, "TRADING_DATE", inplace=True)
daily_index_data.set_index("TRADING_DATE", inplace=True)
daily_index_data.index
daily_index_data.columns


daily_index_data.loc[dt]
daily_index_data.to_csv(f"{dt}.csv")
# daily_index_data["2025"]
daily_index_data[daily_index_data["30 D % CHNG 01-Aug-2025"] > 0]. sort_values(
    by="30 D % CHNG 01-Aug-2025", ascending=False)[["INDEX", "30 D % CHNG 01-Aug-2025"]] # pyright: ignore

#NOTE: 1-Year Change 
daily_index_data[daily_index_data["365 D % CHNG 30-Aug-2024"].astype(float, errors="ignore") > 0]. sort_values(
    by="30 D % CHNG 01-Aug-2025", ascending=False)[["INDEX", "365 D % CHNG 30-Aug-2024"]] # pyright: ignore

daily_index_data["365 D % CHNG 30-Aug-2024"]
daily_index_data["365 D % CHNG 30-Aug-2024"]
daily_index_data["365 D % CHNG 30-Aug-2024"].astype(float, errors="ignore") 


#%% NOTE: Weekly index data massaging
import pandas as pd
from pandas import DataFrame
import sys 

sys.path.append("/home/akasmajhi/anaconda3/envs/nse-data/lib/python3.11/site-packages")
from src.core import get_data

# week_dates = ["25-Aug-2025","26-Aug-2025","28-Aug-2025","29-Aug-2025" ]
# week_data_list = list()
week_data_df: pd.DataFrame = get_data(file_type="INDEX", 
                                      start_date="01-Sep-2025", 
                                      end_date="02-Sep-2025")
week_data_df# pyright: ignore[reportUnusedExpression]
week_data_df.index
week_data_df.columns

week_data_df[week_data_df["TRADING_DATE"] == "02-Sep-2025"].sort_values(
    by="30_DAY_PCT_CHANGE", 
    ascending=False)
# daily_index_data.index
# daily_index_data.columns






































