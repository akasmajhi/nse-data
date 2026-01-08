from dataclasses import dataclass


@dataclass
class DGFilter:  # --- DAILY GAIN FILTER ---
    trading_date: str
    what_type: str
    gl: str
    size: str
    index: str
    industry: str
    reserved: str


@dataclass
class WeeklyFilter:  # Weekly Analysis Filter
    trading_date: str
    new_data_required: bool
    instrument_type: str
    kind: str
    gl: str
    size: str
    index: str
    industry: str
    series: list
    fno: bool


@dataclass
class WeeklyAnalysisFilter:
    trading_date: str
    duration: str
    what_type: str
    mcap: str
    fno: bool
    new_data_required: bool


@dataclass
class AnnouncementsFilter:
    company: str
    purpose: str
    all_industry: list
    selected_industry: str
    size: str
    mcap: float
    force_refresh: bool
