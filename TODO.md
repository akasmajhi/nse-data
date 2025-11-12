## 07-Oct-2025
    - [ ✔️ ] Refactor code for using compose_local_filename method in all source:
## 08-Oct-2025
	- [ TODO ] Complete the top_gainers module:
	- [ ✔️ ] market cap scrapper and sorted data using pd.DataFrame: 
## 09-Oct-2025
    - [ TODO ] Market cap dist of stocks.
## 10-Oct-2025
    - [ ✔️ ] Fix mcap errors for these fetches - '9MMFSML.json', 'MOS.json', 'WONDERLA.json', 
	- [ ✔️ ] get_stock_info for all the meta info about the stock  

## 13-Oct-2025
	- [ ✔️ ] Complete pending work from last week.

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
	- [ ✔️ ] Compete the META part for the stocks: 

## 15-Oct-2025
	- [ ✔️ ] Compete the META part for the stocks.

## 16-Oct-2025
    - [ ✔️ ] Pintoo PAN
    - [ ✔️ ] Pintoo AADHAR

## 17-Oct-2025, 18-Oct-2025
    - [ TODO ] Market cap dist of stocks.
	- [ TODO ] Complete the top_gainers module:
    - [ TODO ] get_last_monday() requires a bug fix.

## 20-Oct-2025
    - [ ✔️ ] Pandas: sorting of data frames
        - Learning: sort_values should be used for in-place sorting
## 21-Oct-2025 & 22-Oct-2025
    - [ ✔️ ] Industry to stock mapping
## 23-Oct-2025
    - [ ✔️ ] Industry to PE mapping
        - For a given industry, find out the stock names and their corresponding PEs
        - src.derived.readers.get_pe_for_industry
## 24-Oct-2025
    - [ ✔️ ] Day 1 / 5 of NiceGUI
    - [ TODO ] get_last_monday() requires a bug fix.
## 25-Oct-2025 & 26-Oct-2025
    - [ ✔️ ] Day 2,3 / 5 of NiceGUI
    - [ TODO ] get_last_friday() needs a fix to return gone by Friday
## 27-Oct-2025
    - [ ✔️ ] Day 4 / 5 of NiceGUI << Not very productive but could put a filter on the grid >>
## 28-Oct-2025 & 29-Oct-2025
    - [ TODO ] Stock Analysis page with the follwoing filter
        - [ TODO ] STOCK find filter with name
        - [ TODO ] Sector Selection dropdown
        - [ TODO ] Valuation Filter (PE/PB)
        - [ TODO ] Growth Filter
    - [ ✔️ ] Day 5 of NiceGUI { Can proceed with it. Needs further learning as the code progresses. }
    - [ ✔️ ] Add market_cap to the daily_gainers data
    - [ ✔️ ] Combine all m_cap data into a single file to make it efficient.
        > Reading individual files take 25+ seconds { Takes less than a second now }
        - [ ✔️ ] Clean data for [revios fetches (using the writers.combine_m_caps
        - [ ✔️ ] Integrate writers.combine_m_caps with m_cap_fetches
## 30-Oct-2025
    - [ TODO ] NiceGUI life-cycle methods
        - [ TODO ] Identify the sequence of life-cycle methods
        - [ TODO ] - Why some of my methods are slow?(when rendering the grid)
    - [ TODO ] Style the grid { aggrid }
        - [ TODO ] Format the cell values properly
        - [ TODO ] Expand the grid
    - [ TODO ] Work on Page layout
## 31-Oct-2025
    >> Did nothing today!
        
## 12-Nov-2025
    - [ TODO ] Finish daily giners summary card
    - [ TODO ] get_all_industry method
    - [ TODO ] get_all_industry link with stocks_grid
    - [ DONE ] Linking the date selector to daily gainers stock grid

# PARKING LOT 

## SHORT POSITIONS FILE FETCH
## CORP. ACTION FILE FETCH
## RESULTS CALENDAR FETCH
## REVIVE TESTING FRAMEWORK

# Tools to explore
    > PyToolZ
    > Tabulate
    > Rich (For rich looking console output) - - | T R Y | - -
    > Hypothesis (extended Unit tests)
    > Pydantic (settings management)
        >> pip install pydantic-settings
    > HTTPX (improved version of requests)
    > fastapi-pagination
    > FastStream (I may not need it)
        >> Works with Kafka, Rabbit, etc.
    > NiceGUI
    > Flet for native feeling apps - - | T R Y | - -
        >> Alternative to NiceGUI
    > Reflex - A React site UI library
    > Textual - Another desktop based UI
    > Marimo -  - - | T R Y | - -
        >> Alternative to Jupiter with richer experience.
