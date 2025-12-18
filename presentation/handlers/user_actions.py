from loguru import logger
from nicegui import ui, app

from presentation.pages.grids import stock_grid
from presentation.helpers.dc.daily_gainers_filters import DGFilter, PriceDirection


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
    logger.debug(f"Into handle_gain_type method.")
    logger.debug(f"[{e = }]")
    if app.storage.user:
        try:
            dg_filter: DGFilter = app.storage.user["dg_filter"]
            logger.info(f"[{dg_filter = }]")
            logger.info(f"[{e.sender.value = }]")
            dg_filter.gain_type = e.sender.value
            if e.sender.value == "Loss":
                logger.debug(f"setting DG Filter in storage")
                dg_filter.price_direction = PriceDirection.LOSS
            elif e.sender.value == "Gain":
                dg_filter.price_direction = PriceDirection.GAIN
            else:
                dg_filter.price_direction = PriceDirection.ANY
            app.storage.user["dg_filter"] = dg_filter
        except KeyError:
            logger.error(f"dg_filter not found in local storage!")
    stock_grid.refresh()


def handle_gain_loss(e):
    print(f"Into handle_gain_loss_radio: [{e}]")


def handle_filter_change(e):
    print(f"Into handle filter change [{e}], [{e.value = }]")


def handle_date_change_filter(e):
    logger.info(f"Event is: [{e}]")
    print(f"handle_date_change_filter_1 : [{e.sender.value}]")
    if app.storage.user:
        try:
            dg_filter: DGFilter = app.storage.user["dg_filter"]
            dg_filter.trading_date = e.sender.value
        except KeyError:
            logger.error(f"dg_filter not found in local storage!")
    stock_grid.refresh()
