from nicegui import ui
from presentation.pages.dashboards import daily_dashboard, index_analysis
from presentation.pages.filters.all_filters import (
    daily_filter_container,
    daily_grid_container,
    daily_summary_container,
    company_results_filter,
    announcement_filter,
    idx_analysis_filter,
    stock_scanner_filter,
)
from presentation.pages.filters.all_filters import (
    weekly_analysis_filter,
    weekly_stocks_filter,
)
from presentation.pages.grids import (
    index_grid,
    weekly_grid,
    weekly_analysis_grid,
    corporate_results_grid,
    company_results_grid,
)


def daily_layout():
    daily_filter_container()
    daily_summary_container()
    daily_grid_container()


def weekly_layout():
    weekly_stocks_filter()
    weekly_grid()
    # ui.label("Weekly Analysis")
    # with ui.tab_panels(tabs=weekly_tabs, value="wt_1").classes("w-full h-screen"):
    #     with ui.tab_pa:
    weekly_analysis_filter()
    weekly_analysis_grid()


def corp_announcement_layout():
    # ui.label("Announcements")
    announcement_filter()
    corporate_results_grid()
    company_results_filter()
    company_results_grid()


def index_layout():
    index_analysis()
    # idx_analysis_filter()
    with ui.row().classes("w-full items-stretch gap-0"):
        with (
            ui.card()
            # .tight()
            .props("flat bordered").classes(
                "w-3/4  p-0 rounded-1g border-blue-400 border-1 gap-0"
            )
            # .classes("w-3/4 h-[70]")
        ):
            with ui.row().classes("w-full bg-black-500 p-1 text-white justify-center"):
                ui.label(f"Index data as on Show Date Picker Here").classes(
                    "w-full flex justify-center items-center bg-blue-600 p-0 text-md text-bold rounded gap-0"
                )
                # with ui.row().classes("w-full flex-grow item-stretch gap-0"):
                #     with ui.element("div").classes("flex-1 flex flex-col h-full"):
                #         ui.label(f"Gainers").classes(
                #             "w-full flex justify-center items-center bg-green-700 font-bold text-md "
                #         )
                index_grid()
    # idx_analysis_insights()


def daily_dashboard_layout():
    daily_dashboard()


def stock_scanner_layout():
    stock_scanner_filter()
    # TODO: stock_scanner_result()
