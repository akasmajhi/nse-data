MONTH_NAMES = {
  "JAN":"Jan",
  "FEB":"Feb",
  "MAR":"Mar",
  "APR":"Apr",
  "MAY":"May",
  "JUN":"Jun",
  "JUL":"Jul",
  "AUG":"Aug",
  "SEP":"Sep",
  "OCT":"Oct",
  "NOV":"Nov",
  "DEC":"Dec",
}
SUPPORTED_FILE_TYPES = ("BHAVCOPY", "PE", "PREOPEN")
DATE_FMT="%d-%b-%Y"
FILES_BASE_DIR='data_files/'
NSE_HOLIDAYS={
    "2025": [ "26-FEB-2025", "14-MAR-2025", "31-MAR-2025", "10-APR-2025", "14-APR-2025", "18-APR-2025", 
             "01-MAY-2025", "15-AUG-2025", "27-AUG-2025", "02-OCT-2025", "21-OCT-2025", "22-OCT-2025", 
             "05-NOV-2025", "25-DEC-2025"],
    "2024": [ "22-JAN-2024", "26-JAN-2024", "08-MAR-2024", "25-MAR-2024", "29-MAR-2024", "11-APR-2024", 
             "17-APR-2024", "01-MAY-2024", "17-JUN-2024", "17-JUL-2024", "15-AUG-2024", "02-OCT-2024", 
             "01-NOV-2024", "15-NOV-2024", "20-NOV-2024", "25-DEC-2024"],
    "2023": [ "26-JAN-2023", "07-MAR-2023", "30-MAR-2023", "04-APR-2023", "07-APR-2023", "14-APR-2023", 
             "01-MAY-2023", "28-JUN-2023", "15-AUG-2023", "19-SEP-2023", "02-OCT-2023", "24-OCT-2023", 
             "14-NOV-2023", "27-NOV-2023", "25-DEC-2023"],
    "2022": [ "26-JAN-2022", "01-MAR-2022", "18-MAR-2022", "14-APR-2022", "15-APR-2022", "03-MAY-2022", 
             "09-AUG-2022", "15-AUG-2022", "31-AUG-2022", "05-OCT-2022", "26-OCT-2022", "08-NOV-2022" ],
    "2021": [ "01-JAN-2021", "26-JAN-2021", "11-MAR-2021", "29-MAR-2021", "02-APR-2021", "14-APR-2021", 
             "21-APR-2021", "13-MAY-2021", "21-JUL-2021", "19-AUG-2021", "10-SEP-2021", "15-OCT-2021", 
             "04-NOV-2021", "05-NOV-2021", "19-NOV-2021"],
    "2020": [], 
}
REQ_HEADER = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "authority":"www.nseindia.com",
    "method":"GET",
    "scheme":"https",
    "accept":"*/*",
    "referer":"https://www.nseindia.com/",
    "sec-fetch-site":"same-origin",
    "sec-fetch-mode":"cors",
    "sec-fetch-dest":"empty",
}
NSE_REPORTS_URL = "https://www.nseindia.com/api/reports"
NSE_PREOPEN_URL = "https://www.nseindia.com/api/market-data-pre-open"
PREOPEN_SKIPROWS = 12

PAYLOAD_NIFTY = {
    "key": "NIFTY",
    "csv": "true",
    "selectValFormat": "crores",
}
PAYLOAD_NIFTYBANK = {
    "key": "BANKNIFTY",
    "csv": "true",
    "selectValFormat": "crores",
}
PAYLOAD_SME = {
    "key": "SME",
    "csv": "true",
    "selectValFormat": "crores",
}
PAYLOAD_FO = {
    "key": "FO",
    "csv": "true",
    "selectValFormat": "crores",
}
PAYLOADS = {"nifty": PAYLOAD_NIFTY, "niftybank": PAYLOAD_NIFTYBANK,
            "sme": PAYLOAD_SME, "fo": PAYLOAD_FO}
