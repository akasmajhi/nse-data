from datetime import datetime
from loguru import logger
from nicegui import props, ui, app
import presentation.handlers.user_actions as UA
from presentation.helpers.dc.daily_gainers_filters import (
    DGFilter,
    GainType,
    MarketCap,
    PriceDirection,
)
from src.constants import DATE_FMT, UI_DATE_FMT
from src.helpers.common import get_last_trading_date


def default_trading_date() -> str:
    if app.storage.user and app.storage.user["dg_filter"]:
        try:
            logger.info(f'[{app.storage.user["dg_filter"] = }]')
            dg_filter: DGFilter = app.storage.user["dg_filter"]
            logger.info(f"[{dg_filter = }]")
            return dg_filter.trading_date
            # return app.storage.user["trading_date"]
        except KeyError:
            logger.info(f'No trading_date locally! Default to last trading date"')
        except AttributeError:
            logger.error(f"AttributeError . . . .")
    dg_filter = DGFilter(
        trading_date=get_last_trading_date(),
        gain_type=GainType.PRICE,
        price_direction=PriceDirection.GAIN,
        index_size=MarketCap.LARGE_CAP,
    )
    app.storage.user["dg_filter"] = dg_filter
    # app.storage.user["trading_date"] = get_last_trading_date()
    return dg_filter.trading_date
    # return get_last_trading_date()


def stocks_filter():
    # TODO: Check if there is a dg_filter in storage
    # If it exists then adjust the control values as per the session data
    with ui.row():
        # with ui.card().tight().tooltip("Volume or Value giner"):
        # with ui.card_section():
        # with ui.card().tight():
        ui.select(
            options=["Volume", "Value", "OI"],
            label="What",
            value="Volume",
            on_change=UA.handle_filter_change,
        )
        ui.select(
            options=["Any", "Gain", "Loss"],
            label="G/L",
            value="Any",
            on_change=UA.handle_gain_type,
        ).props("flat bordered")
        ui.select(
            options=["Large Cap", "Midcap", "Small Cap"],
            label="Size",
            value="Large Cap",
            on_change=UA.handle_filter_change,
        )
        ui.select(
            options=["A", "B", "C"],
            label="Industry",
            value="C",
            on_change=UA.handle_filter_change,
        )
        ui.select(
            options=["A", "B", "C"],
            label="Industry",
            value="C",
            on_change=UA.handle_filter_change,
        )
        with ui.input(
            "Trading Date",
            # value=(
            #     app.storage.user["Trading_date"]
            #     if app.storage.user
            #     else datetime.today().strftime(DATE_FMT)
            # ),
            value=default_trading_date(),
            on_change=UA.handle_date_change_filter,
        ) as date:
            with ui.menu().props("no-parent-event") as menu:
                with ui.date(mask=UI_DATE_FMT).bind_value(date):
                    with ui.row().classes("justify-end"):
                        ui.button("Close", on_click=menu.close).props("flat")
            with date.add_slot("append"):
                ui.icon("edit_calendar").on("click", menu.open).classes(
                    "cursor-pointer"
                )
