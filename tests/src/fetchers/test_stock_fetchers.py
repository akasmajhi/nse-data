import datetime
from src.fetchers.stock_fetchers import get_listing_date, read_listing_date_from_file, fetch_stock_data
from src.constants import DATE_FMT

def test_get_listing_date():
    assert get_listing_date("HDFCBANK") == "08-Nov-1995"
    assert get_listing_date("UCOBANK") == "09-Oct-2003"

def test_read_listing_date_from_file():
    assert read_listing_date_from_file(stock_name="UCOBANK") == "09-Oct-2003"
    assert read_listing_date_from_file(stock_name="JUNK_STOCK") == ""

def test_fetch_stock_data():
    assert fetch_stock_data("UCOBANK", datetime.datetime.today().strftime(DATE_FMT)) is not None



# https://www.nseindia.com/api/historicalOR/cm/equity?symbol=UCOBANK&series=[%22EQ%22]&from=01-01-2004&to=31-12-2004&csv=true

