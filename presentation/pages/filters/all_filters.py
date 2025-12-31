from nicegui import ui
import presentation.handlers.user_actions as UA
from src.constants import UI_DATE_FMT
from src.core import get_index_names, industry_stock_map
from presentation.pages.filters.common import MarketCap
from presentation.helpers.common import (
    dg_filter_from_storage,
    weekly_filter_from_storage,
)


def stocks_filter():
    js_filter_function = "date => new Date(date).getDay() > 0 && \
        new Date(date).getDay() < 6 && new Date(date) <= new Date()"
    with ui.row().classes("w-full glossy-rounded"):
        # with ui.card().tight().tooltip("Volume or Value giner"):
        # with ui.card_section():
        # with ui.card().tight():
        ui.select(
            options=["Volume", "Value", "OI"],
            label="What",
            value=dg_filter_from_storage().what_type,
            on_change=(lambda e: UA.handle_filter_change(e, "WHAT")),
        )  # .bind_value(dg_filter_from_storage(), "what_type", strict=False)
        ui.select(
            options=["Any", "Gain", "Loss"],
            label="G/L",
            value=dg_filter_from_storage().gl,
            on_change=(lambda e: UA.handle_filter_change(e, "GL")),
        ).props("flat bordered")
        ui.select(
            options=["Large Cap", "Midcap", "Small Cap"],
            label="Size",
            value=dg_filter_from_storage().size,
            on_change=(lambda e: UA.handle_filter_change(e, "SIZE")),
        )
        ui.select(
            options=["All"] + get_index_names(),
            label="Index",
            value=dg_filter_from_storage().index,
            on_change=(lambda e: UA.handle_filter_change(e, "INDEX")),
        ).classes("w-24")
        ui.select(
            options=["All"] + list(industry_stock_map(i_trading_date=None).keys()),
            label="Industry",
            value=dg_filter_from_storage().industry,
            on_change=(lambda e: UA.handle_filter_change(e, "INDUSTRY")),
        ).classes("w-24")
        ui.select(
            options=["A", "B", "C"],
            label="Reserved",
            value=dg_filter_from_storage().reserved,
            on_change=(lambda e: UA.handle_filter_change(e, "RESERVED")),
        ).classes("w-24")
        with ui.input(
            "Trading Date",
            value=dg_filter_from_storage().trading_date,
            on_change=(lambda e: UA.handle_filter_change(e, "DATE")),
        ) as date:
            with ui.menu().props("no-parent-event") as menu:
                with ui.date(mask=UI_DATE_FMT).props(
                    f':options="{js_filter_function}"'
                ).bind_value(date):
                    with ui.row().classes("justify-end"):
                        ui.button("Close", on_click=menu.close).props("flat")
            with date.add_slot("append"):
                ui.icon("edit_calendar").on("click", menu.open).classes(
                    "cursor-pointer"
                )
        ui.button(
            "Clear",
            icon="clear",
            on_click=lambda e: UA.handle_filter_change(e, "CLEAR"),
        )


def weekly_stocks_filter():
    js_filter_function = "date => new Date(date).getDay() === 1 && \
        new Date(date) <= new Date()"
    with ui.row().classes("w-full glossy-rounded"):
        with ui.input(
            "Week Start",
            value=weekly_filter_from_storage().trading_date,
            on_change=(lambda e: UA.weekly_filter_change(e, "DATE")),
        ) as date:
            with ui.menu().props("no-parent-event") as menu:
                with ui.date(mask=UI_DATE_FMT).props(
                    f':options="{js_filter_function}"'
                ).bind_value(date):
                    with ui.row().classes("justify-end"):
                        ui.button("Close", on_click=menu.close).props("flat")
            with date.add_slot("append"):
                ui.icon("edit_calendar").on("click", menu.open).classes(
                    "cursor-pointer"
                )
        ui.select(
            options=["STOCK", "INDEX", "OI"],
            label="Instrument",
            value=weekly_filter_from_storage().instrument_type,
            on_change=(lambda e: UA.weekly_filter_change(e, "INSTRUMENT")),
        )
        ui.select(
            options=["Price", "Volume", "OI"],
            label="Type",
            value=weekly_filter_from_storage().kind,
            on_change=(lambda e: UA.weekly_filter_change(e, "TYPE")),
        )
        ui.select(
            options=["Any", "Gain", "Loss"],
            label="G/L",
            value=weekly_filter_from_storage().gl,
            on_change=(lambda e: UA.weekly_filter_change(e, "GL")),
        )
        ui.select(
            options=["Large Cap", "Midcap", "Small Cap"],
            label="Size",
            value=weekly_filter_from_storage().size,
            on_change=(lambda e: UA.weekly_filter_change(e, "SIZE")),
        )
        ui.select(
            options=["All"] + get_index_names(),
            label="Index",
            value=weekly_filter_from_storage().index,
            on_change=(lambda e: UA.weekly_filter_change(e, "INDEX")),
        )
        ui.select(
            options=["All"] + list(industry_stock_map(i_trading_date=None).keys()),
            label="Industry",
            value=weekly_filter_from_storage().industry,
            on_change=(lambda e: UA.weekly_filter_change(e, "INDUSTRY")),
        )


def test(e):
    print(f"Changed . . . [{e}]")


def scanner_filter():
    with ui.row():
        ui.select(
            options=[market_cap.name for market_cap in MarketCap],
            label="Market Cap",
            # value="Select Mcap",
        )
        with ui.card():
            min_max_mcap_range = (
                ui.range(min=0.1, max=5, step=0.1, value={"min": 1, "max": 4})
                .props('label-always snap label-color="tertiary"')
                .on_value_change(test)
            )

            ui.label().bind_text_from(
                min_max_mcap_range,
                "value",
                backward=lambda v: f'From: {v["min"]:.2f}, To: {v["max"]:.2f} L Cr.',
            )
        ui.button(
            # value="Select Mcap",
        )
