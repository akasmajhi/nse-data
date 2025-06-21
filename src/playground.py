
"""
import requests

# url = "https://www.nseindia.com"
url = 'https://api.github.com/events'
r = requests.get(url)
print(r.status_code)
for cookie in r.cookies:
    print(f"Name: {cookie.name}, Value: {cookie.value}")
# print(r.text)
print(f"Cookies are: [{r.cookies}]")
"""

import requests
url = "https://www.nseindia.com"
resp = requests.get(url, timeout=0.9)
print(f"Status code: {resp.status_code}")
for cookie in resp.cookies:
    print(f"Name: {cookie.name}, Value: {cookie.value}")



import requests
url = "https://www.nseindia.com"
resp = requests.head(url)
print(resp)
print(f"Status code: {resp.status_code}")


import requests
print('Start')
url = 'https://www.nseindia.com'
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    ":authority":"www.nseindia.com",
    ":method":"GET",
    ":scheme":"https",
    "accept":"*/*",
    "referer":"https://www.nseindia.com/",
    "sec-fetch-site":"same-origin",
    "sec-fetch-mode":"cors",
    "sec-fetch-dest":"empty",
}
session = requests.Session()
r = session.get(url=url)
print(r)
print('End')


