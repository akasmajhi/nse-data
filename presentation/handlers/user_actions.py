from loguru import logger
from nicegui import ui, app

from presentation.pages.grids import stock_grid


def toggle_dark(e):
    dark = ui.dark_mode()  # NOTE: Start with Dark mode
    print(f"Before change [{dark.value = }]")
    if dark.value == False:
        dark.enable()
        e.sender.props("icon=img:/icons/icons8-dark-mode-50_dark.png")
        print(f"Dark mode is False. Making it: [{dark.value = }]")
    else:
        dark.disable()
        e.sender.props("icon=img:/icons/icons8-dark-mode-50_bright.png")
        print(f"Dark mode is True. Making it: [{dark.value = }]")


def handle_gain_type(e):
    print(f"Clicked on filter dropdown")
    print(e)


def handle_gain_loss(e):
    print(f"Into handle_gain_loss_radio: [{e}]")


def handle_filter_change(e):
    print(f"Into handle filter change [{e}]")


def handle_date_change_filter_1(e):
    logger.info(f"Event is: [{e}]")
    print(f"handle_date_change_filter_1 : [{e.sender.value}]")
    app.storage.user["trading_date"] = e.sender.value
    stock_grid.refresh()
