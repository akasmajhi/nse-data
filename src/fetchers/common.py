import requests
from src.constants import REQ_HEADER

def dummy_request(url: str):
    session = requests.Session()
    r = session.get(url, headers=REQ_HEADER)
    return r

if __name__ == "__main__":
    dummy_request("https://www.nseindia.com/all-reports")

