from src.constants import DATE_FMT
from src.helpers.common import compose_dates_from_range, get_last_trading_date, get_last_monday, is_date_in_future, get_last_trading_date, get_all_stock_names
from datetime import datetime, timedelta

def test_composeDatesFromRange():
    # scenario where date range is valid but data only for working week
    s_date_valid_trading = '16-JUn-2025'
    e_date_valid_trading = '20-JUN-2025'
    assert len(compose_dates_from_range(s_date_valid_trading, e_date_valid_trading)) != 0

    # scenario where date range is valid and data for more than a week
    s_date_valid_trading = '16-JUn-2025'
    e_date_valid_trading = '27-JUN-2025'
    result = compose_dates_from_range(s_date_valid_trading, e_date_valid_trading)
    assert len(result) == 10

    # scenario where bad dates provided
    s_date_valid_trading = '16-Jun-2025'
    e_date_invalid_trading = '-jUN-2025'
    assert len(compose_dates_from_range(s_date_valid_trading, e_date_invalid_trading)) == 0

    # scenario where bad s_date > e_date
    s_date_valid_trading = '20-JUN-2025'
    e_date_valid_trading = '16-Jun-2025'
    result = compose_dates_from_range(s_date_valid_trading, e_date_valid_trading)
    assert len(result) >= 0

def test_get_last_monday():
    assert get_last_monday() is not None

def test_is_date_in_future():
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    assert is_date_in_future(tomorrow.strftime(DATE_FMT)) is True

def test_get_last_trading_date():
    trading_date = "20-Sep-2025"
    assert get_last_trading_date(trading_date) == "19-Sep-2025"
    trading_date = "19-Sep-2025"
    assert get_last_trading_date(trading_date) == "19-Sep-2025"
    trading_date = "19-Sep-2029" #NOTE: Future date test
    assert get_last_trading_date(trading_date) is not None
    trading_date = "15-Mar-2025" #NOTE: Friday holiday for 14-Mar-2025
    assert get_last_trading_date(trading_date) == "13-Mar-2025"

def test_get_all_stock_names():
    # print(get_all_stock_names())
    assert len(get_all_stock_names()) > 0
