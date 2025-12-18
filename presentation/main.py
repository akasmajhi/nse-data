#!/usr/bin/env python3
from nicegui import ui

from presentation.pages.grids import stock_grid
from presentation.pages.filters import stocks_filter
from presentation.pages.stock_grid_summary import grid_summary
from presentation.pages import todos


with ui.tabs() as tabs:
    ui.tab("daily_gainers")
    ui.tab("sector_analysis")
    ui.tab("value_scanner")
    ui.tab("corp_announcement")
    ui.tab("derivates")
    ui.tab("stock_scanner")
    ui.tab("ta")

with ui.tab_panels(tabs=tabs, value="daily_gainers").classes("w-full"):
    with ui.tab_panel("daily_gainers"):
        stocks_filter()
        stock_grid()
        grid_summary()
        todos.daily_gainers()
    with ui.tab_panel("sector_analysis"):
        ui.label("sector Analysis")
    with ui.tab_panel("value_scanner"):
        ui.label("Value Scanners")
    with ui.tab_panel("corp_announcement"):
        ui.label("Corp. Announcements")
    with ui.tab_panel("derivates"):
        ui.label("OI Analysis")
    with ui.tab_panel("stock_scanner"):
        ui.label("Scan Stocks")
    with ui.tab_panel("ta"):
        ui.label("Tech Analysis")


ui.run(show=False, title="Paisa", storage_secret="NONE")
