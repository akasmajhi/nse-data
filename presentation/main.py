#!/usr/bin/env python3
from nicegui import ui

from presentation.pages.grids import stock_grid, weekly_grid
from presentation.pages.filters.all_filters import (
    scanner_filter,
    stocks_filter,
    weekly_stocks_filter,
)
from presentation.pages.stock_grid_summary import grid_summary

# from presentation.pages import todos


with ui.tabs() as tabs:
    ui.tab(name="daily_gainers", label="Daily")
    ui.tab(name="weekly_gainers", label="Weekly")
    ui.tab(name="sector_analysis", label="Sector Analysis")
    ui.tab(name="value_scanner", label="Value Scanners")
    ui.tab(name="corp_announcement", label="Announcemnets")
    ui.tab(name="derivates", label="Derivatives Analysis")
    ui.tab(name="stock_scanner", label="scanners")
    ui.tab(name="ta", label="Tech Picks")

with ui.tab_panels(tabs=tabs, value="weekly_gainers").classes("w-full"):
    with ui.tab_panel("daily_gainers"):
        stocks_filter()
        stock_grid()
        grid_summary()
        # todos.daily_gainers()
    with ui.tab_panel("weekly_gainers"):
        weekly_stocks_filter()
        weekly_grid()
        ui.label("Weekly Analysis")
    with ui.tab_panel("sector_analysis"):
        ui.label("sector Analysis")
    with ui.tab_panel("value_scanner"):
        ui.label("Value Scanners")
    with ui.tab_panel("corp_announcement"):
        ui.label("Corp. Announcements")
    with ui.tab_panel("derivates"):
        ui.label("OI Analysis")
    with ui.tab_panel("stock_scanner"):
        # ui.label("Scan Stocks")
        scanner_filter()
    with ui.tab_panel("ta"):
        ui.label("Tech Analysis")


ui.run(show=False, title="Paisa", storage_secret="NONE")

"""
    TailwindCSS

"""
