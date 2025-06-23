from src.helpers.common import composeDatesFromRange

def test_composeDatesFromRange():
    s_date_valid_trading = '16-Jun-2025'
    e_date_valid_trading = '20-JUN-2025'
    assert len(composeDatesFromRange(s_date_valid_trading, e_date_valid_trading)) == 5


