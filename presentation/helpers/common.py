from dataclasses import asdict
import json
from nicegui import app

from presentation.helpers.dc.all import DGFilter, WeeklyFilter
from src.helpers.common import get_last_monday, get_last_trading_date
from loguru import logger


def default_dg_filter() -> DGFilter:
    logger.info(f"Creating fresh DG_Filter.")
    DG_Filter = DGFilter(
        trading_date=get_last_trading_date(),
        what_type="Value",
        gl="Gain",
        size="Large Cap",
        index="All",
        industry="All",
        reserved="B",
    )
    DG_Filter_Dict = json.dumps(asdict(DG_Filter))
    app.storage.general["DG_Filter"] = DG_Filter_Dict
    logger.info(f'Cleared DG Filter. [{app.storage.general["DG_Filter"]} = ]')
    return DG_Filter


def dg_filter_from_storage() -> DGFilter:
    try:
        if app.storage.general["DG_Filter"]:
            DG_Filter_json = json.loads(app.storage.general["DG_Filter"])
            DG_Filter = DGFilter(**DG_Filter_json)
            logger.info(f"DG_Filter found in local storage. [{DG_Filter = }]")
            return DG_Filter
    except KeyError:
        logger.info(f"No DG_Filter locally!")
    except AttributeError as ae:
        logger.error(f"AttributeError . . . . {ae = }")
    except Exception as e:
        logger.error(f"Some Error I did not catch. [{e = }]")
    return default_dg_filter()


def default_weekly_filter() -> WeeklyFilter:
    logger.debug(f"Clearing and making Weekly filter afresh.")
    weekly_filter = WeeklyFilter(
        new_data_required=True,
        trading_date=get_last_monday(),
        instrument_type="STOCK",
        kind="Price",
        gl="Gain",
        size="Large Cap",
        index="All",
        industry="All",
        series=list(["EQ"]),
        fno=False,
    )
    weekly_filter_dict = json.dumps(asdict(weekly_filter))
    app.storage.general["weekly_filter"] = weekly_filter_dict
    logger.info(
        f'Default weekly filter stored. [{app.storage.general["weekly_filter"]}]'
    )
    return weekly_filter


def weekly_filter_from_storage() -> WeeklyFilter:
    try:
        if app.storage.general["weekly_filter"]:
            weekly_filter_json = json.loads(app.storage.general["weekly_filter"])
            weekly_filter = WeeklyFilter(**weekly_filter_json)
            logger.info(f"Weekly Filter found in local storage. [{weekly_filter = }]")
            return weekly_filter
    except KeyError:
        logger.info(f"No weekly filter locally!")
    except AttributeError as ae:
        logger.error(f"AttributeError . . . . {ae = }")
    except Exception as e:
        logger.error(f"Some Error I did not catch. [{e = }]")
    # DG_Filter ilter
    return default_weekly_filter()


# def set_grid_summary(summary: str):
#     app.storage.general["grid_summary"] = summary
def set_grid_summary(total: int, gainers: int, losers: int):
    app.storage.general["grid_summary_total"] = total
    app.storage.general["grid_summary_gainers"] = gainers
    app.storage.general["grid_summary_losers"] = losers
