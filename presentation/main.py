from nicegui import ui, app

from presentation.pages.grids import stock_grid
from presentation.pages.filters import stocks_filter
from presentation.pages.stock_grid_summary import grid_summary
from presentation.pages import todos


def entry():
    with ui.row(align_items="center"):
        with ui.tabs().classes("w-full") as tabs:
            daily_gainers = ui.tab("Daily Gainers")
            sector_analysis = ui.tab("Sector Analysis")
            value_scanner = ui.tab("Value Scanner")
            copr_announcement = ui.tab("Corporate Announcements")
            derivates = ui.tab("Derivatives")
            stock_scanner = ui.tab("Stock Scanner")
            ta = ui.tab("TA")
        with ui.tab_panels(tabs=tabs, value=daily_gainers).classes("w-full"):
            with ui.tab_panel(daily_gainers):
                stocks_filter()
                stock_grid()
                grid_summary()
                todos.daily_gainers()
            with ui.tab_panel(sector_analysis):
                ui.label("sector Analysis")
            with ui.tab_panel(value_scanner):
                ui.label("Value Scanners")
            with ui.tab_panel(copr_announcement):
                ui.label("Corp. Announcements")
            with ui.tab_panel(derivates):
                ui.label("OI Analysis")
            with ui.tab_panel(stock_scanner):
                ui.label("Scan Stocks")
            with ui.tab_panel(ta):
                ui.label("Tech Analysis")


entry()
# root()
ui.run(root=entry, show=False, title="Paisa", storage_secret="NONE")
# ui.run(native=True, window_size=(1024, 768), fullscreen=False, title="Native App")
