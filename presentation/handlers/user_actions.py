import json
from dataclasses import asdict
from loguru import logger
from nicegui import ui, app

from presentation.pages.grids import stock_grid
from presentation.helpers.dc.all import DGFilter


def toggle_dark(e):
    dark = ui.dark_mode()  # NOTE: Start with Dark mode
    logger.debug(f"Before change [{dark.value = }]")
    if dark.value == False:
        dark.enable()
        e.sender.props("icon=img:/icons/icons8-dark-mode-50_dark.png")
        logger.debug(f"Dark mode is False. Making it: [{dark.value = }]")
    else:
        dark.disable()
        e.sender.props("icon=img:/icons/icons8-dark-mode-50_bright.png")
        logger.debug(f"Dark mode is True. Making it: [{dark.value = }]")


def handle_filter_change(e, control_name=""):
    logger.debug(f"Into handle filter change [{e = }], [{control_name = }]")
    try:
        if app.storage.general["DG_Filter"]:  # NOTE: Filter present
            DG_Filter_json = json.loads(app.storage.general["DG_Filter"])
            DG_Filter = DGFilter(**DG_Filter_json)
            match control_name:
                case "WHAT":
                    DG_Filter.what_type = e.sender.value
                case "GL":
                    DG_Filter.gl = e.sender.value
                case "SIZE":
                    DG_Filter.size = e.sender.value
                case "INDUSTRY":
                    DG_Filter.industry = e.sender.value
                case "RESERVED":
                    DG_Filter.reserved = e.sender.value
                case "DATE":
                    DG_Filter.trading_date = e.sender.value
                case _:
                    logger.error(f"Unknown control . . .")

            DG_Filter_Dict = json.dumps(asdict(DG_Filter))
            app.storage.general["DG_Filter"] = DG_Filter_Dict
    except KeyError:  # NOTE: Filter NOT present. Strange!!!
        logger.error(f"DG_Filter not found in local storage!")
    stock_grid.refresh()
