from src.derived.writers import industry_to_stock
from src.helpers.common import get_last_friday


def daily():
    pass


def weekly():
    industry_to_stock(get_last_friday())


def monthly():
    pass
