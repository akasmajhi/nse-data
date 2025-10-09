from analytics.filters import market_cap

def test_get_market_cap():
    assert market_cap.get_market_cap(file_type="INVALID", 
                                     source="INVALID",
                                     instr_name="").empty
    assert market_cap.get_market_cap(file_type="STOCK", 
                                     source="INVALID",
                                     instr_name="").empty
