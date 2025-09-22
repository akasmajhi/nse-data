import requests
from src.constants import REQ_HEADER, NSE_DUMMY_REQ_URL

def dummy_request(url: str = NSE_DUMMY_REQ_URL):
    session = requests.Session()
    r = session.get(url, headers=REQ_HEADER)
    return r

if __name__ == "__main__":
    dummy_request("https://www.nseindia.com/all-reports")

