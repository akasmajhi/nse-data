from src.constants import SUPPORTED_FILE_TYPES, MONTH_NAMES, DATE_FMT, NSE_HOLIDAYS, REQ_HEADER, NSE_REPORTS_URL, FILES_BASE_DIR

def test_month_names():
    valid_mon_keys = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

    assert valid_mon_keys == list(MONTH_NAMES.keys())

    valid_mon_values = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    assert valid_mon_values == list(MONTH_NAMES.values())

def test_supported_file_types():
    valid_file_types = ("BHAVCOPY", "PE", "PREOPEN")
    assert valid_file_types == SUPPORTED_FILE_TYPES

def test_date_fmt():
    valid_date_fmt = "%d-%b-%Y"
    assert valid_date_fmt == DATE_FMT

def test_files_base_dir():
    valid_base_dir = "data_files/"
    assert FILES_BASE_DIR == valid_base_dir
def test_nse_holidays():
    valid_2025_holiday = "26-FEB-2025"
    invalid_2025_holiday = "13-JAN-2025"

    assert valid_2025_holiday in NSE_HOLIDAYS["2025"]
    assert invalid_2025_holiday not in NSE_HOLIDAYS["2025"]

def test_req_header():
    valid_header_method = "GET"
    valid_header_referer = "https://www.nseindia.com/"

    assert REQ_HEADER["method"] == valid_header_method 
    assert REQ_HEADER["referer"] == valid_header_referer

def test_nse_reports_url():
    valid_reports_url = "https://www.nseindia.com/api/reports"
    assert NSE_REPORTS_URL == valid_reports_url

