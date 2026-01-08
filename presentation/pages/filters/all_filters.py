from loguru import logger
from nicegui import app, ui
import presentation.handlers.user_actions as UA
from src.constants import UI_DATE_FMT
from src.core import get_index_names, industry_stock_map
from presentation.helpers.common import (
    dg_filter_from_storage,
    weekly_filter_from_storage,
    weekly_analysis_filter_from_storage,
    announcement_filter_from_storage,
)


weekly_js_filter_function = "date => new Date(date).getDay() === 1 && \
    new Date(date) <= new Date()"
daily_js_filter_function = "date => new Date(date).getDay() > 0 && \
    new Date(date).getDay() < 6 && new Date(date) <= new Date()"


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
                    f':options="{daily_js_filter_function}"'
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
    with ui.row().classes("w-full glossy-rounded"):
        with ui.input(
            "Week Start",
            value=weekly_filter_from_storage().trading_date,
            on_change=(lambda e: UA.weekly_filter_change(e, "DATE")),
        ) as date:
            with ui.menu().props("no-parent-event") as menu:
                with ui.date(mask=UI_DATE_FMT).props(
                    f':options="{weekly_js_filter_function}"'
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
        ).bind_value_from(
            target_object=weekly_filter_from_storage(),
            target_name="instrument_type",
            strict=False,
        )
        ui.select(
            options=["Price", "Volume", "OI"],
            label="Type",
            value=weekly_filter_from_storage().kind,
            on_change=(lambda e: UA.weekly_filter_change(e, "TYPE")),
        ).bind_value_from(
            target_object=weekly_filter_from_storage(),
            target_name="kind",
            strict=False,
        )
        ui.select(
            options=["Any", "Gainers", "Losers"],
            label="G/L",
            value=weekly_filter_from_storage().gl,
            on_change=(lambda e: UA.weekly_filter_change(e, "GL")),
        )
        ui.select(
            options=["Large Cap", "Midcap", "Small Cap"],
            label="Size",
            value=weekly_filter_from_storage().size,
            on_change=(lambda e: UA.weekly_filter_change(e, "SIZE")),
        ).classes(
            "hidden"
        )  # TODO: Hidden since definition is UNKNOWN
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
        ui.input_chips(
            "Enter Series",
            value=weekly_filter_from_storage().series,
            on_change=lambda e: UA.weekly_filter_change(e, "SERIES"),
            new_value_mode="add-unique",
            validation=lambda e: UA.weekly_filter_change(e, "SERIES"),
        )
        ui.checkbox(
            "FnO",
            value=weekly_filter_from_storage().fno,
            on_change=lambda e: UA.weekly_filter_change(e, "FNO"),
        )


def weekly_analysis_filter():
    logger.info(f"Into Weekly scanners")
    opts_durations = ["1-Wk Engulfer", "2-Wk Engulfer"]
    opts_type = ["Bearish", "Bullish"]
    opts_mcap = [
        "All",
        "< 1K Cr.",
        "1K - 5K Cr.",
        "5K - 20K Cr.",
        "20K-50K Cr.",
        "50K - 1L Cr.",
        "> 1L Cr.",
    ]
    with ui.row().classes("w-full glossy-rounded"):
        # logger.debug(f"##################[{weekly_filter_from_storage().trading_date}]")
        ui.input(
            "Week Start",
            value=weekly_filter_from_storage().trading_date,
        ).bind_value(app.storage.general, "trading_date").disable()
        ui.radio(
            options=opts_durations,
            value=weekly_analysis_filter_from_storage().duration,
            on_change=lambda e: UA.weekly_analysis_filter_change(e, "DURATION"),
        )
        ui.radio(
            options=opts_type,
            value=weekly_analysis_filter_from_storage().what_type,
            on_change=lambda e: UA.weekly_analysis_filter_change(e, "TYPE"),
        )
        ui.select(
            options=opts_mcap,
            label="Market Cap",
            # value="All",
            value=weekly_analysis_filter_from_storage().mcap,
            on_change=lambda e: UA.weekly_analysis_filter_change(e, "MCAP"),
            # with_input=True,
        ).style("width: 100px")
        ui.checkbox(
            "FnO",
            value=weekly_analysis_filter_from_storage().fno,
            on_change=lambda e: UA.weekly_analysis_filter_change(e, "FNO"),
        )


def announcement_filter():
    logger.debug(f"Into announcemnt filter")
    with ui.row().classes("w-full glossy-rounded"):
        ui.input(
            label="Company",
            placeholder="Company Name",
            on_change=lambda x: UA.handle_announcement_filter(x, "COMPANY"),
            autocomplete=None,
            validation=None,
            value=announcement_filter_from_storage().company,
        )
        ui.input(
            label="Purpose",
            placeholder="Result, Fund, Dividend, etc.",
            on_change=lambda x: UA.handle_announcement_filter(x, "PURPOSE"),
            autocomplete=None,
            validation=None,
            value=announcement_filter_from_storage().purpose,
        )
        ui.select(
            options=announcement_filter_from_storage().all_industry,
            label="Industry",
            value=announcement_filter_from_storage().selected_industry,
            on_change=(lambda e: UA.handle_announcement_filter(e, "INDUSTRY")),
        ).classes("w-24")
