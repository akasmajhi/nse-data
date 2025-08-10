# from datetime import datetime

from src import core
# from src.constants import DATE_FMT
def test_get_data():
    # TESTS for non-existing file type data fetch 

    assert core.get_data(file_type='JUNK', start_date='01-Jul-2025', end_date='04-Jul-2025') is not True
    # TESTS for PE data fetch 

    # assert core.get_data("PE", '12-12-2025', '') is False
    # assert core.get_data('PE', '01-Jun-2024', datetime.today().strftime(DATE_FMT)) is not None
    # assert core.get_data("PE", '12-12-2025', '') is False
    # assert core.get_data('PE', '01-Jul-2025', datetime.today().strftime(DATE_FMT)) is not None
    assert core.get_data('PE', '01-Jul-2024', '01-Jul-2024') is not None
    # assert core.get_data('PE', '01-Jul-2023', '05-Jul-2023') is not None

    # TESTS for BHAVCOPY data fetch 

    assert core.get_data(file_type='BHAVCOPY', 
                         start_date='04-Jul-2025', 
                         end_date='04-Jul-2024') is not None

    # assert core.get_data(file_type='BHAVCOPY', 
    #                      start_date='07-Jul-2024', 
    #                      end_date=datetime.today().strftime(DATE_FMT)) is not None
