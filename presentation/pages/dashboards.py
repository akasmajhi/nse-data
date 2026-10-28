from loguru import logger
from nicegui import app, ui
import pandas as pd

import presentation.handlers.user_actions as UA
from presentation.pages.grids import index_summary_grid, error_grid
from src import core
from src.constants import UI_DATE_FMT
from analytics.core import index_dashboard
from src.helpers.common import get_last_trading_date


@ui.refreshable
def index_analysis():

    t_5_data, b_5_data = (
        index_dashboard()
    )  # NOTE: Get the top/bottom data from core package
    # NOTE: Show error if no-data
    if t_5_data.empty or b_5_data.empty:
        error_message: str = "Error! No data found."
        return list([error_grid(error_message)])

    # t5 = index_analysis_summary_grid(t_5_data, is_top_data=True)
    columns = [
        {"name": "INDEX", "label": "INDEX", "field": "INDEX", "sortable": True},
        {
            "name": "% Chng.",
            "label": "% Change",
            "field": "PCT_CHANGE",
            "sortable": True,
        },
        {
            "name": "1 WK % Chng.",
            "label": "1 WK %",
            "field": "ONE_WK_PCT_CHANGE",
            "sortable": True,
        },
        {
            "name": "1 MON % Chng.",
            "label": "1 MON %",
            "field": "ONE_MON_PCT_CHANGE",
            "sortable": True,
        },
        {
            "name": "1 YR % Chng.",
            "label": "1 YR %",
            "field": "ONE_YR_PCT_CHANGE",
            "sortable": True,
        },
    ]
    with ui.row().classes("w-full items-stretch gap-0"):
        with (
            ui.card()
            .props("flat bordered")
            .classes("w-1/2  p-0 rounded-1g border-blue-400 border-1 gap-0")
        ):
            with ui.row().classes("w-full bg-black-500 p-1 text-white justify-center"):
                ui.label(f"Index Dashboard 👉 {get_last_trading_date()}").classes(
                    "w-full flex justify-center items-center bg-black-600 p-0 text-md text-bold rounded "
                )
            with ui.row().classes("w-full flex-grow item-stretch gap-0"):
                with ui.element("div").classes("flex-1 flex flex-col h-full"):
                    ui.label(f"Gainers").classes(
                        "w-full flex justify-center items-center bg-green-700 font-bold text-md "
                    )
                    index_summary_grid(t_5_data, is_top_data=True)
                with ui.element("div").classes("flex-1 flex flex-col h-full"):
                    ui.label(f"Losers").classes(
                        "w-full flex justify-center items-center bg-red-700 font-bold text-md "
                    )
                    index_summary_grid(b_5_data, is_top_data=False)

        with (
            ui.card()
            .props("flat bordered")
            .classes("w-1/2  p-0 rounded-1g border-blue-400 border-1 gap-0")
            # .classes("w-3/4 h-[70]")
        ):
            ui.label("Reserved for tracking sector/ind. rotations!")
            ui.label("Best performing since past 1 weeks")
            ui.label("Best performing since past 2 weeks")
            ui.label("Best performing since past 4 weeks")


def daily_dashboard():
    ui.label("Daily Dashboard . . .")
