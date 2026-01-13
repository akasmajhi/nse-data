#!/usr/bin/env python3
from nicegui import ui

from presentation.handlers.user_actions import toggle_dark
from presentation.pages.grids import (
    corporate_results_grid,
    stock_grid,
    weekly_grid,
    weekly_analysis_grid,
    company_results_grid,
)
from presentation.pages.filters.all_filters import (
    stocks_filter,
    weekly_analysis_filter,
    weekly_stocks_filter,
    announcement_filter,
    company_results_filter,
)
from presentation.pages.stock_grid_summary import grid_summary

dark_mode = ui.dark_mode(value=True)

with ui.row().classes("w-full h-screen"):
    with ui.column().classes("flex-grow"):
        with ui.tabs().classes("w-full") as tabs:
            ui.tab(name="daily_gainers", label="Daily")
            ui.tab(name="weekly_gainers", label="Weekly")
            ui.tab(name="sector_analysis", label="Sector Analysis")
            ui.tab(name="value_scanner", label="Value Scanners")
            ui.tab(name="corp_announcement", label="Announcemnets")
            ui.tab(name="derivates", label="Derivatives Analysis")
            ui.tab(name="stock_scanner", label="scanners")
            ui.tab(name="ta", label="Tech Picks")
            ui.switch("D/L", on_change=lambda e: toggle_dark(e)).bind_value(
                dark_mode, "value"
            ).classes("rounded").props("icon=check_circle")

        with ui.tab_panels(tabs=tabs, value="corp_announcement").classes(
            "w-full h-screen"
        ):
            with ui.tab_panel("daily_gainers"):
                stocks_filter()
                stock_grid()
                grid_summary()
                # todos.daily_gainers()
            with ui.tab_panel("weekly_gainers").classes("w-full"):
                weekly_stocks_filter()
                weekly_grid()
                # ui.label("Weekly Analysis")
                weekly_analysis_filter()
                weekly_analysis_grid()
            with ui.tab_panel("sector_analysis"):
                ui.label("sector Analysis")
            with ui.tab_panel("value_scanner"):
                ui.label("Value Scanners")
            with ui.tab_panel("corp_announcement"):
                # ui.label("Announcements")
                announcement_filter()
                corporate_results_grid()
                company_results_filter()
                company_results_grid()
            with ui.tab_panel("derivates"):
                ui.label("OI Analysis")
            with ui.tab_panel("stock_scanner"):
                ui.label("Scan Stocks")
            with ui.tab_panel("ta"):
                ui.label("Tech Analysis")


ui.run(show=False, title="Paisa", storage_secret="NONE")

"""
    TailwindCSS

"""
