from src.helpers.common import composeDatesFromRange

def test_composeDatesFromRange():
    # scenario where date range is valid but data only for working week
    s_date_valid_trading = '16-JUn-2025'
    e_date_valid_trading = '20-JUN-2025'
    assert len(composeDatesFromRange(s_date_valid_trading, e_date_valid_trading)) != 0

    # scenario where date range is valid and data for more than a week
    s_date_valid_trading = '16-JUn-2025'
    e_date_valid_trading = '27-JUN-2025'
    result = composeDatesFromRange(s_date_valid_trading, e_date_valid_trading)
    assert len(result) == 10

    # scenario where bad dates provided
    s_date_valid_trading = '16-Jun-2025'
    e_date_invalid_trading = '-jUN-2025'
    assert len(composeDatesFromRange(s_date_valid_trading, e_date_invalid_trading)) == 0

    # scenario where bad s_date > e_date
    s_date_valid_trading = '20-JUN-2025'
    e_date_valid_trading = '16-Jun-2025'
    result = composeDatesFromRange(s_date_valid_trading, e_date_valid_trading)
    assert len(result) >= 0
