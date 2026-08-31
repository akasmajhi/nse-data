"""
import requests

# url = "https://www.nseindia.com"
url = 'https://api.github.com/events'
r = requests.get(url)
print(r.status_code)
for cookie in r.cookies:
    print(f"Name: {cookie.name}, Value: {cookie.value}")
# print(r.text)
print(f"Cookies are: [{r.cookies}]")
"""

from loguru import logger
import requests

url = "https://www.nseindia.com"
resp = requests.get(url, timeout=0.9)
print(f"Status code: {resp.status_code}")
for cookie in resp.cookies:
    print(f"Name: {cookie.name}, Value: {cookie.value}")


import requests

url = "https://www.nseindia.com"
resp = requests.head(url)
print(resp)
print(f"Status code: {resp.status_code}")


import requests

print("Start")
url = "https://www.nseindia.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    ":authority": "www.nseindia.com",
    ":method": "GET",
    ":scheme": "https",
    "accept": "*/*",
    "referer": "https://www.nseindia.com/",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
}
session = requests.Session()
r = session.get(url=url)
print(r)
print("End")

# %% NOTE: converting ind_to_stock to DF
from src.core import industry_stock_map

ind_stock_dict = industry_stock_map(i_trading_date=None)
from pandas import json_normalize

industr_name: str = "Industrial Minerals"
data = json_normalize(data=ind_stock_dict).T.explode(0)
data = data.reset_index()
data.rename(columns={"index": "industry"}, inplace=True)
data.rename(columns={0: "stock"}, inplace=True)
type(data[data.industry.isin(["Industrial Minerals"])].stock)
print(f"{data.head()}")

# %%
from src.fetchers.results import fetch_result_calendar

print(fetch_result_calendar())
# %% NOTE: Get only relevant industries for a stock
trading_date: str = "29-Dec-2025"
from src.fetchers.results import fetch_result_calendar

data = fetch_result_calendar()
data.head()
from src.core import industry_stock_map
from pandas import json_normalize

ind_stock_dict = industry_stock_map(i_trading_date=None)
ind_stock_df = json_normalize(data=ind_stock_dict).T.explode(0)
ind_stock_df = ind_stock_df.reset_index()
ind_stock_df.rename(columns={"index": "industry"}, inplace=True)
ind_stock_df.rename(columns={0: "symbol"}, inplace=True)
ind_stock_df.head()
list(["All"] + sorted(data.merge(ind_stock_df, on="symbol").industry.unique()))
# %% NOTE: For manual fetch of daily BHAVCOPY
from src.core import get_data

data = get_data(file_type="BHAVCOPY", start_date="09-Jan-2026", end_date="09-Jan-2026")
# %% NOTE: DEBUG: get_last_trading_date
from src.helpers.common import get_last_trading_date
from loguru import logger
from datetime import datetime
from src.constants import DATE_FMT

logger.debug(
    f"[{get_last_trading_date(i_date=datetime.today().strftime(DATE_FMT)) = }]"
)
working_day: str = datetime.strptime("13-Jan-2026", DATE_FMT).strftime(DATE_FMT)
logger.debug(f"{get_last_trading_date(working_day)}")

# %% SUB_SECTION: Test Reslts Calendar
from src.core import get_result_calendar
from loguru import logger

logger.info(get_result_calendar())  # NOTE: For all results gist
logger.info(
    f'BAJFINANCE: [{get_result_calendar(force_refresh=False, stock_name="BAJFINANCE")}]'
)
# SECTION: TA_LIB practice

# %% NOTE: Learning
"""
import numpy as np
import talib

close = np.random.random(100)

output = talib.SMA(close, 50)
print(output[-5:])

# dict of functions by group
for group, names in talib.get_function_groups().items():
    # print(group)
    for name in names:
        if "gulf".upper() in name:
            print(f"{group}\t  {name}")
"""
# %% SECTION: For individual get_data
from src.core import get_data
from datetime import datetime

# from src.core import daily_fetchers

# daily_fetchers()
get_data(
    file_type="FNOBHAVCOPY",
    start_date="27-Mar-2026",
    end_date="27-Mar-2026",
    # end_date=datetime.today().strftime(C.DATE_FMT),
)
# %% NOTE: DICT play
RESULT_CAL_NO_STOCK_NAME = {
    "index": "equities",
    "from_date": "replace",
    # "from_date": "08-01-2026",
    "to_date": "08-03-2026",
}
from_date = "01-Jan-2026"
payload = RESULT_CAL_NO_STOCK_NAME
payload["from_date"] = from_date
logger.debug(payload)
# %% SUB_SECTION: Sorting unique series names
from src.core import get_unique_series

get_unique_series("19-Jan-2026")
sorted_series = sorted(get_unique_series("26-Jan-2026"))
print(sorted_series)
# %% NOTE: For index gainers
from src.core import get_data
from loguru import logger
import pandas as pd

trading_date = "13-Feb-2026"

data = get_data(file_type="INDEX", start_date=trading_date, end_date=trading_date)
data["PCT_CHANGE"] = pd.to_numeric(data["PCT_CHANGE"], errors="coerce")
logger.debug(f"Total: {len(data)}")
data = data.dropna(subset=["PCT_CHANGE"])
gainers = data[data["PCT_CHANGE"] > 0]
losers = data[data["PCT_CHANGE"] < 0]
logger.debug(f"Total: {len(data)}, Gainers: [{len(gainers)}, Losers: {len(losers)}]")

# %% SECTION: Methods

# %% SUB_SECTION: get_t-1_date


def get_t_minus_1_date(t_date: str | None) -> str:
    from src.helpers.common import get_last_trading_date
    from datetime import datetime, timedelta
    from src.constants import DATE_FMT

    # NOTE:if t_date is blank or None, default it to last trading date
    if not t_date:
        t_date = get_last_trading_date()
    else:
        t_date = get_last_trading_date(t_date)
    logger.info(f"T-Date is: [{t_date}]")
    t_date_dt = datetime.strptime(t_date, DATE_FMT)
    t_minus_1 = t_date_dt - timedelta(days=1)
    logger.info(
        f"t: {t_date_dt.strftime(DATE_FMT)}, t-minus-1: [{t_minus_1.strftime(DATE_FMT)}]"
    )
    return ""


get_t_minus_1_date("14-Feb-2026")
# get_t_minus_1_date(None)
# %% SUB_SECTION: get_last_t_date
from src.constants import DATE_FMT
from loguru import logger
from datetime import datetime, timedelta
from src.helpers.common import is_date_in_future, is_NSE_holiday


def get_last_t_date(i_date: str = datetime.today().strftime(DATE_FMT)) -> str:
    logger.debug(f"Incoming date is: [{i_date = }]")
    today = datetime.today()
    trading_date = ""
    # NOTE: If a trading date is passed then it must be a valid date
    if i_date and i_date.strip():
        try:
            datetime.strptime(i_date, DATE_FMT)
        except ValueError:
            logger.error(f"Bad [{i_date = }] passed")
            return trading_date

    # NOTE: Is the date in future?
    if i_date and is_date_in_future(i_date):
        trading_date = today.strftime(DATE_FMT)
    else:
        trading_date = i_date

    # NOTE: If the i_date is today and time is before 7 AM, then use previous day
    if i_date == today.strftime(DATE_FMT) and today.hour < 19 and today.weekday() < 5:
        excess_days = 1
        logger.error(
            f"It is'a Weekday and befoer 7 PM. Use previous day. [{excess_days = }]"
        )
        prev_week_day = (
            datetime.strptime(trading_date, DATE_FMT) - timedelta(days=excess_days)
        ).strftime(DATE_FMT)
        trading_date = prev_week_day
    # NOTE: If i_date is weekend then calculate the immediate last weekday
    if datetime.strptime(trading_date, DATE_FMT).weekday() > 4 and (
        i_date == today.strftime(DATE_FMT)  # BUG: Why this check? `and today.hour < 19`
    ):
        excess_days = datetime.strptime(trading_date, DATE_FMT).weekday() - 4
        logger.error(f"[{excess_days = }]")
        prev_week_day = (
            datetime.strptime(trading_date, DATE_FMT) - timedelta(days=excess_days)
        ).strftime(DATE_FMT)
        trading_date = prev_week_day
    # NOTE: If the last weekday was a exchange holiday then try previous day
    if is_NSE_holiday(trading_date):
        prev_working_day = (
            datetime.strptime(trading_date, DATE_FMT) - timedelta(days=1)
        ).strftime(DATE_FMT)
        trading_date = prev_working_day
    return trading_date


logger.info(f"__Blank Date__ Last T Date : [{get_last_t_date()}]")  # TEST: Blank date
logger.info(
    f'__Bad Date__ Last T Date : [{get_last_t_date("010120261")}]'
)  # TEST: Blank date
# logger.info(f'__None Date__ Last T Date : [{get_last_t_date(None)}] ') #TEST: None date
logger.info(
    f"__Today Date__ Last T Date : [{get_last_t_date(datetime.today().strftime(DATE_FMT))}] "
)  # TEST: None date
