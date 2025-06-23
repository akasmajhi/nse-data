from src.constants import SUPPORTED_FILE_TYPES, MONTH_NAMES

def test_isFileTypeValid():
    valid_file_types = ('BHAVCOPY', 'PE')
    assert valid_file_types == SUPPORTED_FILE_TYPES

def test_month_names():
    valid_mon_keys = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

    assert valid_mon_keys == list(MONTH_NAMES.keys())

    valid_mon_values = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    assert valid_mon_values == list(MONTH_NAMES.values())

