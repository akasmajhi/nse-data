from src.helpers.validators import isDateValid, isNSEHoliday, get_latest_file, is_stock_valid

def test_isDateValid():
    # Valid Date
    assert isDateValid('21-JUN-2025') is True
    # Invalid Date
    assert isDateValid('00-00-00') is False
    # Invalid Date - Wrong Format
    assert isDateValid('-Jun-2025') is False
    # Invalid Date - Wrong Format
    assert isDateValid('Jun-21-2025') is False
    # Invalid Date - Wrong Format
    assert isDateValid('2025-Jun-21') is False
    # Invalid Date - Future Date
    assert isDateValid('21-Jun-2050') is False


def test_isNSEHoliday():
    # Valid trading date; Expect a False
    assert isNSEHoliday('16-JUN-2025') is False
    # Case for a non-existent calendar year
    assert isNSEHoliday('16-JUN-2019') is True
    # Case for a valida holiday
    assert isNSEHoliday('14-Mar-2025') is True

# def test_get_local_stock_data():
#     stock_name = "HDFCBANK"
    # assert get_local_stock_data(stock_name) is not None
def test_get_latest_file():
    assert get_latest_file("INVALID_STOCK").empty is True 
    assert get_latest_file("BHAVCOPY").empty is False 
    assert get_latest_file("STOCK").empty is False 

def test_is_stock_valid():
    stock_name = "Some Junk Stock"
    assert is_stock_valid(stock_name) is False
    stock_name = "HDFCBANK"
    assert is_stock_valid(stock_name) is True
    stock_name = "HDCFBANK"
    assert is_stock_valid(stock_name) is False
    stock_name = ""
    assert is_stock_valid(stock_name) is False
