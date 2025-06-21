from src.constants import  SUPPORTED_FILE_TYPES

def test_constant_file_types():
    print(SUPPORTED_FILE_TYPES)
    assert "BHAVCOPY" in SUPPORTED_FILE_TYPES

