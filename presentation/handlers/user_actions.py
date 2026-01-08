import json
from dataclasses import asdict
from loguru import logger
from nicegui import ui, app

from presentation.helpers.common import default_dg_filter
from presentation.pages.filters.all_filters import announcement_filter
from presentation.pages.grids import (
    corporate_results_grid,
    stock_grid,
    weekly_grid,
    weekly_analysis_grid,
)
from presentation.helpers.dc.all import (
    AnnouncementsFilter,
    DGFilter,
    WeeklyFilter,
    WeeklyAnalysisFilter,
)


def toggle_dark(e):
    logger.debug(f"[{e = }]")
    # if dark.value == False:
    #     dark.enable()
    #     e.sender.props("icon=img:/icons/icons8-dark-mode-50_dark.png")
    #     logger.debug(f"Dark mode is False. Making it: [{dark.value = }]")
    # else:
    #     dark.disable()
    #     e.sender.props("icon=img:/icons/icons8-dark-mode-50_bright.png")
    #     logger.debug(f"Dark mode is True. Making it: [{dark.value = }]")


def handle_filter_change(e, control_name=""):
    logger.debug(f"Into handle filter change [{e = }], [{control_name = }]")
    logger.debug(f"[{e.value = }], [{e.previous_value=}]")
    if e.sender.value is None and e.previous_value is not None:
        logger.debug(f"Same date is clicked twice. Ignore this event")
        return

    # TODO: If the date clicked is same as what you have in session
    # - - - - - Do not refresh the page  - - - - -

    # if e.sender.value == e.previous_value:
    #     logger.debug(f"No change in control value. Do not refresh!")
    #     return
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
                case "INDEX":
                    DG_Filter.index = e.sender.value
                case "INDUSTRY":
                    DG_Filter.industry = e.sender.value
                case "RESERVED":
                    DG_Filter.reserved = e.sender.value
                case "DATE":
                    DG_Filter.trading_date = e.sender.value
                case "CLEAR":
                    DG_Filter = default_dg_filter()
                    ui.notify(
                        f"Filters cleared . . . Not working now!",
                        type="negative",
                        position="center",
                        close_button=True,
                    )
                    return
                case _:
                    logger.error(f"Unknown control . . .")

            DG_Filter_Dict = json.dumps(asdict(DG_Filter))
            app.storage.general["DG_Filter"] = DG_Filter_Dict
    except KeyError:  # NOTE: Filter NOT present. Strange!!!
        logger.error(f"DG_Filter not found in local storage!")
    stock_grid.refresh()


def weekly_filter_change(e, control_name=""):
    logger.debug(f"Into weekly filter change [{e = }], [{control_name = }]")
    try:
        if app.storage.general["weekly_filter"]:  # NOTE: Filter present
            weekly_filter_json = json.loads(app.storage.general["weekly_filter"])
            weekly_filter = WeeklyFilter(**weekly_filter_json)
            weekly_filter.new_data_required = False
            match control_name:
                case "DATE":
                    if weekly_filter.trading_date != e.sender.value:
                        weekly_filter.new_data_required = True
                        weekly_filter.trading_date = e.sender.value
                        app.storage.general["trading_date"] = (
                            e.sender.value
                        )  # For Weekly Analysis Filter
                        weekly_analysis_grid.refresh()
                case "INSTRUMENT":
                    if e.sender.value.upper() in ["INDEX", "OI"]:
                        ui.notify(
                            f"Currently [{e.sender.value}] is not implemented",
                            close_button="Okay",
                            type="negative",
                        )
                        return
                    else:
                        weekly_filter.instrument_type = e.sender.value
                case "TYPE":
                    if e.sender.value.upper() in ["VOLUME", "OI"]:
                        ui.notify(
                            f"Currently [{e.sender.value}] is not implemented",
                            close_button="Okay",
                            type="negative",
                        )
                        return
                    else:
                        weekly_filter.kind = e.sender.value
                case "GL":
                    weekly_filter.gl = e.sender.value
                case "SIZE":
                    weekly_filter.size = e.sender.value
                case "INDEX":
                    weekly_filter.index = e.sender.value
                case "INDUSTRY":
                    weekly_filter.industry = e.sender.value
                case "SERIES":
                    # logger.error(f"TMP: [{e = }]")
                    if type(e) == list:
                        weekly_filter.series = e
                case "FNO":
                    weekly_filter.fno = e.sender.value
                case _:
                    logger.error(f"Unknown control . . .")
            weekly_filter_dict = json.dumps(asdict(weekly_filter))
            app.storage.general["weekly_filter"] = weekly_filter_dict
    except KeyError:  # NOTE: Filter NOT present. Strange!!!
        logger.error(f"Weekly not found in local storage!")
    weekly_grid.refresh()


def weekly_analysis_filter_change(e, control_name=""):
    # logger.debug(f"Into weekly analysis filter change [{e = }], [{control_name = }]")
    try:
        if app.storage.general["weekly_analysis_filter"]:  # NOTE: Filter present
            weekly_analysis_filter_json = json.loads(
                app.storage.general["weekly_analysis_filter"]
            )
            weekly_analysis_filter = WeeklyAnalysisFilter(**weekly_analysis_filter_json)
            weekly_analysis_filter.new_data_required = False
            match control_name:
                case "DURATION":
                    weekly_analysis_filter.duration = e.sender.value
                case "TYPE":
                    weekly_analysis_filter.what_type = e.sender.value
                case "MCAP":
                    weekly_analysis_filter.mcap = e.sender.value
                case "FNO":
                    weekly_analysis_filter.fno = e.sender.value
                case _:
                    logger.error(f"Unknown control . . .")
            weekly_analysis_filter_dict = json.dumps(asdict(weekly_analysis_filter))
            app.storage.general["weekly_analysis_filter"] = weekly_analysis_filter_dict
    except KeyError:  # NOTE: Filter NOT present. Strange!!!
        logger.error(f"Weekly not found in local storage!")
    # weekly_analysis_grid.refresh()


def handle_announcement_filter(e, control_name=""):
    try:
        if app.storage.general["announcement_filter"]:  # NOTE: Filter present
            announcement_filter_json = json.loads(
                app.storage.general["announcement_filter"]
            )
            announcement_filter = AnnouncementsFilter(**announcement_filter_json)
            match control_name:
                case "COMPANY":
                    announcement_filter.company = e.sender.value
                case "PURPOSE":
                    announcement_filter.purpose = e.sender.value
                case "MCAP":
                    announcement_filter.mcap = e.sender.value
                case "SIZE":
                    announcement_filter.size = e.sender.value
                case "INDUSTRY":
                    announcement_filter.selected_industry = e.sender.value
                case _:
                    logger.error(f"Unknown control . . .")
            announcement_filter_dict = json.dumps(asdict(announcement_filter))
            app.storage.general["announcement_filter"] = announcement_filter_dict
    except KeyError:  # NOTE: Filter NOT present. Strange!!!
        logger.error(f"Announcements Filter not found in local storage!")
    corporate_results_grid.refresh()
