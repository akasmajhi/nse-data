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
