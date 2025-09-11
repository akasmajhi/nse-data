from datetime import date, timedelta
import pandas

from analytics.core import top_gainers
from src.constants import SUPPORTED_FILE_TYPES, SUPPORTED_TIME_DURATIONS , DATE_FMT

def test_top_gainers():
    assert top_gainers() is not None
    #NOTE: Invalid file type
    assert top_gainers(file_type="ABC").empty is True
    #NOTE: Invalid time duration
    assert top_gainers(file_type=SUPPORTED_FILE_TYPES["INDEX"], duration="DEF").empty is True
    #NOTE: Valid file type and duration
    assert top_gainers(file_type=SUPPORTED_FILE_TYPES["INDEX"], 
                       duration=SUPPORTED_TIME_DURATIONS["WEEK"]) is not None
    
    #NOTE: Invalid start_date 
    today = date.today()
    future_date =  (today + timedelta(days=( today.weekday()))).strftime(DATE_FMT)
    assert top_gainers(file_type=SUPPORTED_FILE_TYPES["INDEX"], 
                       duration=SUPPORTED_TIME_DURATIONS["WEEK"],
                       start_date=future_date).empty is True
    #NOTE: Should all params be fine, you should get "not None" return
    assert top_gainers(file_type="PE",
                       duration="WEEK",
                       start_date=today.strftime(DATE_FMT)).empty is True
    assert top_gainers(file_type=SUPPORTED_FILE_TYPES["INDEX"], 
                       duration=SUPPORTED_TIME_DURATIONS["WEEK"],
                       # start_date="25-Aug-2025") is not None
                       start_date=today.strftime(DATE_FMT)) is not None

