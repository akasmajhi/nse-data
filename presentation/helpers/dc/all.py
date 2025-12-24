from dataclasses import dataclass


@dataclass
class DGFilter:  # --- DAILY GAIN FILTER ---
    trading_date: str
    what_type: str
    gl: str
    size: str
    industry: str
    reserved: str
