## nse-data
The data format changed for daily bhav copies on NSE w.e.f. Jul-08-2024. So, all this repo is to catch up with the changes.

#### FETCHERS


| Fetcher       | Frquency  | Location   | Function      | Parameter                  |
|---------------|:---------:|------------|:-------------:|----------------------------|
| Daily BHAVCOPY| DAILY-EOD | BHAVCOPY   | get_data      |file_type='BHAVCOPY'        |
| PREOPEN       | DAILY-EOD | PREOPEN    | get_date      |file_type='PREOPEN'         |
| PE            | DAILY-EOD | PE         | get_data      |file_type='PE'              |
| INDEX         | DAILY-EOD | INDEX      | get_data      |file_type='INDEX'           |
| FNO BHAVCOPY  | DAILY-EOD | FNOBHAVCOPY| get_data      |file_type='FNOBHAVCOPY'     |
| Market Cap    | WEEKLY    |            | get_market_cap|file_type='STOCK'           |
| STOCK INFO    | WEEKLY    |            | get_stock_info|None                        |
| ind to stock  | WEEKLY    |            | industry_to_stock|datetime.today()         |
|               |           |            | |             |                            |
---------------------------------------------------------------------------------------


- All references are WRT BASE_DIR 

