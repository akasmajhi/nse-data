from nicegui import ui
from presentation.pages.dashboards import index_analysis
from presentation.pages.filters.all_filters import (
    daily_filter_container,
    daily_grid_container,
    daily_summary_container,
    company_results_filter,
    announcement_filter,
    idx_analysis_filter,
)
from presentation.pages.filters.all_filters import (
    weekly_analysis_filter,
    weekly_stocks_filter,
)
from presentation.pages.grids import (
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
    idx_analysis_filter()
    # idx_analysis_chart()
    # idx_analysis_insights()
