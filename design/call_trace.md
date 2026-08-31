# def get_data(
    file_type: str, start_date: str, end_date: str
    ) -> pd.DataFrame:

# get_market_cap(
    file_type: str | None, 
    stock_name: str | None, 
    trading_date: str = datetime.today().strftime(C.DATE_FMT),
    ) -> list[dict] | dict:

## helpers.common.get_all_stock_names
    (series_list=C.SERIES_FOR_MCAP) -> pd.DataFrame

### helpers.validators.get_latest_file(file_type: str) -> pd.DataFrame:

## def get_local_market_cap(
    file_type: str,
    instr_name: str,
    trading_date: str = datetime.today().strftime(DATE_FMT),) -> dict:



# def get_supported_file_types() -> dict:

# def get_index_names() -> list[str]:

# def get_all_index_constituents() -> list[dict]:

# def get_index_constituents(index_name: str) -> list:

# def stock_data_since_listing(skip_current_year: bool = False):

# def daily_fetchers():

# def weekly_fetchers():

# def industry_stock_map(i_trading_date: str | None) -> dict:

# def stocks_for_industry(industry: str | None) -> pd.Series | pd.DataFrame:

# def get_stock_info(
    stock_name: str | None = None,
    trading_date: str = datetime.today().strftime(C.DATE_FMT),
    ) -> list[dict] | dict:

# def get_fno_stocks() -> list:

# def run_batch():

# def corporate_announcements(force_refresh: bool = False, stock_name: str = ""):

# def get_unique_series(trading_date: str) -> list:


* Top level calls are from core.py file.
