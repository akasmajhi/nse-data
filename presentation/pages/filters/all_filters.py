from nicegui import ui
import presentation.handlers.user_actions as UA
from src.constants import UI_DATE_FMT
from presentation.pages.filters.common import MarketCap
from presentation.helpers.common import dg_filter_from_storage


def stocks_filter():
    with ui.row().classes("w-full glossy-rounded"):
        # with ui.card().tight().tooltip("Volume or Value giner"):
        # with ui.card_section():
        # with ui.card().tight():
        ui.select(
            options=["Volume", "Value", "OI"],
            label="What",
            value=dg_filter_from_storage().what_type,
            on_change=(lambda e: UA.handle_filter_change(e, "WHAT")),
        )
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
            options=["A", "B", "C"],
            label="Industry",
            value=dg_filter_from_storage().industry,
            on_change=(lambda e: UA.handle_filter_change(e, "INDUSTRY")),
        )
        ui.select(
            options=["A", "B", "C"],
            label="Reserved",
            value=dg_filter_from_storage().reserved,
            on_change=(lambda e: UA.handle_filter_change(e, "RESERVED")),
        )
        with ui.input(
            "Trading Date",
            value=dg_filter_from_storage().trading_date,
            on_change=(lambda e: UA.handle_filter_change(e, "DATE")),
        ) as date:
            with ui.menu().props("no-parent-event") as menu:
                with ui.date(mask=UI_DATE_FMT).bind_value(date):
                    with ui.row().classes("justify-end"):
                        ui.button("Close", on_click=menu.close).props("flat")
            with date.add_slot("append"):
                ui.icon("edit_calendar").on("click", menu.open).classes(
                    "cursor-pointer"
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
