#!/usr/bin/env python3
from nicegui import ui

from presentation.handlers.user_actions import toggle_dark
from presentation.pages.layouts import (
    corp_announcement_layout,
    daily_layout,
    weekly_layout,
    index_layout,
)

dark_mode = ui.dark_mode(value=True)

with ui.row().classes("w-full h-screen"):
    with ui.column().classes("flex-grow"):
        with ui.tabs().classes("w-full") as tabs:
            ui.tab(name="daily_gainers", label="Daily")
            ui.tab(name="weekly_gainers", label="Weekly")
            ui.tab(name="sector_analysis", label="Sector Analysis")
            ui.tab(name="index_analysis", label="Index Analysis")
            ui.tab(name="corp_announcement", label="Announcemnets")
            ui.tab(name="derivates", label="Derivatives Analysis")
            ui.tab(name="stock_scanner", label="scanners")
            ui.tab(name="ta", label="Tech Picks")
            ui.switch("D/L", on_change=lambda e: toggle_dark(e)).bind_value(
                dark_mode, "value"
            ).classes("rounded").props("icon=check_circle")

        with ui.tab_panels(tabs=tabs, value="daily_gainers").classes("w-full h-screen"):
            with ui.tab_panel("daily_gainers"):
                daily_layout()
            with ui.tab_panel("weekly_gainers").classes("w-full"):
                weekly_layout()
            with ui.tab_panel("sector_analysis"):
                ui.label("sector Analysis")
            with ui.tab_panel("index_analysis"):
                index_layout()
            # with ui.tab_panel("corp_announcement"):
            #     corp_announcement_layout()
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
