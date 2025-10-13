#### 07-Oct-2025
		- Refactor code for using compose_local_filename method in all source. #RESUME:
#### 08-Oct-2025
	- Complete the top_gainers module #RESUME:
	- market cap scrapper and sorted data using pd.DataFrame #DONE: 
#### 09-Oct-2025
    - Market cap dist of stocks #TODO:
#### 10-Oct-2025
    - Fix mcap errors for these fetches - '9MMFSML.json', 'MOS.json', 'WONDERLA.json', #TODO:
	- get_stock_info for all the meta info about the stock

#### 13-Oct-2025
	- Complete pending work from last week.



	core --> get_market_cap(file_type:str | None, stock_name:str | None) -> list[dict] | dict :
		get_all_stock_names()
		for each stock --> file_readers.get_local_market_cap(stock)
				--> stock_fetchers.read_market_cap_from_file()



