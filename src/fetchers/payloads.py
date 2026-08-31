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
PAYLOAD_ALL = {
    "key": "ALL",
    "csv": "true",
    "selectValFormat": "crores",
}
PREOPEN_PAYLOADS = {
    "nifty": PAYLOAD_NIFTY,
    "niftybank": PAYLOAD_NIFTYBANK,
    "sme": PAYLOAD_SME,
    "fo": PAYLOAD_FO,
    "all": PAYLOAD_ALL,
}
IDX_LIST = {
    "csv": "true",
}
RESULT_CAL_NO_STOCK_NAME = {
    "index": "equities",
    "from_date": "replace",
    # "from_date": "08-01-2026",
    "to_date": "08-03-2026",
}
RESULT_CAL_WITH_STOCK_NAME = {
    "index": "equities",
    "symbol": "replace",
}
