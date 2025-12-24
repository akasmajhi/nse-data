from dataclasses import asdict
import json
from nicegui import app

from presentation.helpers.dc.all import DGFilter
from src.helpers.common import get_last_trading_date
from loguru import logger


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
    DG_Filter = DGFilter(
        trading_date=get_last_trading_date(),
        what_type="OI",
        gl="Gain",
        size="Large Cap",
        industry="A",
        reserved="B",
    )
    DG_Filter_Dict = json.dumps(asdict(DG_Filter))
    app.storage.general["DG_Filter"] = DG_Filter_Dict
    return DG_Filter


def set_grid_summary(summary: str):
    app.storage.general["grid_summary"] = summary
