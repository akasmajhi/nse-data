from datetime import datetime
from nicegui import ui, app
import presentation.handlers.user_actions as UA
from src.constants import DATE_FMT, UI_DATE_FMT


def stocks_filter():
    with ui.row():
        # with ui.card().tight().tooltip("Volume or Value giner"):
        # with ui.card_section():
        ui.select(
            options=["Volume", "Value", "OI"],
            label="What",
            value="Volume",
            on_change=UA.handle_filter_change,
        )
        # with ui.card().tight():
        ui.select(
            options=["Gain", "Loss"],
            label="G/L",
            value="Gain",
            on_change=UA.handle_filter_change,
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
            value=datetime.today().strftime(DATE_FMT),
            on_change=UA.handle_date_change_filter_1,
        ) as date:
            with ui.menu().props("no-parent-event") as menu:
                with ui.date(mask=UI_DATE_FMT).bind_value(date):
                    with ui.row().classes("justify-end"):
                        ui.button("Close", on_click=menu.close).props("flat")
            with date.add_slot("append"):
                ui.icon("edit_calendar").on("click", menu.open).classes(
                    "cursor-pointer"
                )
