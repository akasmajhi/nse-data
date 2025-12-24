from enum import Enum, auto


class GainType(Enum):
    PRICE = auto()
    VALUE = auto()
    VOLUME = auto()
    OI = auto()


class PriceDirection(Enum):
    ANY = auto()
    GAIN = auto()
    LOSS = auto()


class MarketCap(Enum):
    LARGE_CAP = auto()
    MID_CAP = auto()
    SMALL_CAP = auto()
