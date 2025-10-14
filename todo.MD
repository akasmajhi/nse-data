#### 07-Oct-2025
		- Refactor code for using compose_local_filename method in all source. #DONE:
#### 08-Oct-2025
	- Complete the top_gainers module #RESUME:
	- market cap scrapper and sorted data using pd.DataFrame #DONE: 
#### 09-Oct-2025
    - Market cap dist of stocks #TODO:
#### 10-Oct-2025
    - Fix mcap errors for these fetches - '9MMFSML.json', 'MOS.json', 'WONDERLA.json', #DONE:
	- get_stock_info for all the meta info about the stock

#### 13-Oct-2025
	- Complete pending work from last week.

	core --> get_market_cap(file_type:str | None, stock_name:str | None) -> list[dict] | dict :
		get_all_stock_names()
		for each stock --> file_readers.get_local_market_cap(stock)
				--> stock_fetchers.read_market_cap_from_file()

### GET STOCK INFO for META information

core.get_stock_info(stock, trading_date) -> list[dict] | dict:
  --> file_readers.get_local_stock_info(stock, trading_date) --> dict
    --> stock_fetchers.read_stock_info_from_file(stock, trading_date) --> dict
	OR  stock_fetchers.fetch_stock_info(stock) --> dict


#### 14-Oct-2025
	- Compete the META part for the stocks #TODO: 

------------------------------------------------------------------------------
vim:tw=78:ts=4:ft=help:norl:

