from analytics import info
from src.constants import IDX_NAMES

def test_get_market_cap():
    assert info.get_idx_market_cap("Junk") is None
    # assert info.get_market_cap(COMPANY_CATEGORIES["FO"]) is None
