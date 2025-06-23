from src.helpers.validators import isDateValid

def test_isDateValid():
    assert isDateValid('21-JUN-2025') is True
    assert isDateValid('00-00-00') is False
    assert isDateValid('-Jun-2025') is False


def test_isDateInFuture():
    pass

