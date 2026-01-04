# nse-data
The data format changed for daily bhav copies on NSE w.e.f. Jul-08-2024. So, all this repo is to catch up with the changes.

## FETCHERS


| Fetcher       | Frquency  | Location   | Function      | Parameter                  |
|---------------|:---------:|------------|:-------------:|----------------------------|
| Daily BHAVCOPY| DAILY-EOD | BHAVCOPY   | get_data      |file_type='BHAVCOPY'        |
| PREOPEN       | DAILY-EOD | PREOPEN    | get_date      |file_type='PREOPEN'         |
| PE            | DAILY-EOD | PE         | get_data      |file_type='PE'              |
| INDEX         | DAILY-EOD | INDEX      | get_data      |file_type='INDEX'           |
| FNO BHAVCOPY  | DAILY-EOD | FNOBHAVCOPY| get_data      |file_type='FNOBHAVCOPY'     |
| Market Cap    | WEEKLY    |            | get_market_cap|file_type='STOCK'           |
| STOCK INFO    | WEEKLY    |            | get_stock_info|None                        |
| ind to stock  | WEEKLY    |            | industry_to   |datetime.today()            |
|               |           |            | stock         |                            |


All references are WRT BASE_DIR 

There must be at least 3 dashes separating each header cell.
The outer pipes (|) are optional, and you don't need to make the 
raw Markdown line up prettily. You can also use inline Markdown.

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3
