import src.helpers.file_readers as file_readers

def test_get_local_data():
    assert file_readers.get_local_data("PE", "11-Jun-2025", "14-Jun-2025").size > 0  
