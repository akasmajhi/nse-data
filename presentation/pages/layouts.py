from nicegui import ui
from presentation.helpers.common import index_analysis_grid_filter_from_storage
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


import presentation.handlers.user_actions as UA
from src.constants import UI_DATE_FMT


def index_layout():
    daily_js_filter_function = "date => new Date(date).getDay() > 0 && \
        new Date(date).getDay() < 6 && new Date(date) <= new Date()"
    index_analysis()
    with ui.row().classes("w-full h-full items-stretch gap-0"):
        with ui.card().classes("w-full h-full"):
            with ui.row().classes(
                "w-full h-full bg-black-500 p-0 text-white justify-center"
            ):
                with ui.column():
                    ui.select(
                        label="Timeframe",
                        options=["DAILY", "WEEKLY", "MONTHLY"],
                        value=index_analysis_grid_filter_from_storage().duration,
                        on_change=(
                            lambda e: UA.index_analysis_grid_change(e, "DURATION")
                        ),
                    ).props(
                        # 1. Strips out default margins, paddings, and background/borders
                        "dense borderless"
                    ).style(
                        # 2. Force the overall inner container heights to match text scale
                        "height: 1.5rem; min-height: 1.5rem;"
                    ).props(
                        # 3. Direct styling of the core inner elements to align selection text & arrows
                        'input-style="height: 1.5rem; min-height: 1.5rem; padding: 0;" '
                        'popup-content-class="text-sm"'
                    ).classes(
                        # 4. Tailor text size and overall wrapper widths via Tailwind
                        "text-sm w-28 font-bold"
                    )
                with ui.input(
                    "Date",
                    value=index_analysis_grid_filter_from_storage().trading_date,
                    on_change=(lambda e: UA.index_analysis_grid_change(e, "DATE")),
                ).classes("w-32") as date:
                    with ui.menu().props("no-parent-event") as menu:
                        with (
                            ui.date(mask=UI_DATE_FMT)
                            .props(f':options="{daily_js_filter_function}"')
                            .bind_value(date)
                        ):
                            with ui.row().classes("justify-end"):
                                ui.button("Close", on_click=menu.close).props("flat")
                    with date.add_slot("append"):
                        ui.icon("edit_calendar").on("click", menu.open).classes(
                            "cursor-pointer"
                        )
                index_grid()
    # idx_analysis_insights()


def daily_dashboard_layout():
    daily_dashboard()


def stock_scanner_layout():
    stock_scanner_filter()
    # TODO: stock_scanner_result()
