from datetime import datetime

from src import core
from src.constants import DATE_FMT
def test_get_data():
    # assert core.get_data("PE", '12-12-2025', '') is False
    # assert core.get_data('PE', '01-Jun-2024', datetime.today().strftime(DATE_FMT)) is not None
    # assert core.get_data("PE", '12-12-2025', '') is False
    assert core.get_data('PE', '01-Jul-2025', datetime.today().strftime(DATE_FMT)) is not None
    assert core.get_data('PE', '01-Jul-2024', '05-Jul-2024') is not None
    assert core.get_data('PE', '01-Jul-2023', '05-Jul-2023') is not None
