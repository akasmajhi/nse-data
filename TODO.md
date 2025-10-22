## 07-Oct-2025
    - [ DONE ] Refactor code for using compose_local_filename method in all source:
## 08-Oct-2025
	- [ TODO ] Complete the top_gainers module:
	- [ DONE ] market cap scrapper and sorted data using pd.DataFrame: 
## 09-Oct-2025
    - [ TODO ] Market cap dist of stocks.
## 10-Oct-2025
    - [ DONE ] Fix mcap errors for these fetches - '9MMFSML.json', 'MOS.json', 'WONDERLA.json', 
	- [ DONE ] get_stock_info for all the meta info about the stock  

## 13-Oct-2025
	- [ DONE ] Complete pending work from last week.

core --> get_market_cap(file_type:str | None, stock_name:str | None) -> list[dict] | dict :
    get_all_stock_names()
    for each stock --> file_readers.get_local_market_cap(stock)
                   --> stock_fetchers.read_market_cap_from_file()

#### GET STOCK INFO for META information

core.get_stock_info(stock, trading_date) -> list[dict] | dict:
  --> file_readers.get_local_stock_info(stock, trading_date) --> dict
    --> stock_fetchers.read_stock_info_from_file(stock, trading_date) --> dict
	OR  stock_fetchers.fetch_stock_info(stock) --> dict

## 14-Oct-2025
	- [ DONE ] Compete the META part for the stocks: 

## 15-Oct-2025
	- [ DONE ] Compete the META part for the stocks.

## 16-Oct-2025
    - [ DONE ] Pintoo PAN
    - [ DONE ] Pintoo AADHAR

## 17-Oct-2025, 18-Oct-2025
    - [ TODO ] Market cap dist of stocks.
	- [ TODO ] Complete the top_gainers module:
    - [ TODO ] get_last_monday() requires a bug fix.

## 20-Oct-2025
    - [ TODO ] Pandas: sorting of data frames 
# PARKING LOT 

## SHORT POSITIONS FILE FETCH
## CORP. ACTION FILE FETCH
## RESULTS CALENDAR FETCH
## REVIVE TESTING FRAMEWORK
