import src.helpers.file_readers as file_readers

def test_get_local_data():
    assert file_readers.get_local_data("PE", "12-12-2025", "21-12-2025") == False 
