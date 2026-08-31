from loguru import logger
from nicegui import app, ui
import presentation.handlers.user_actions as UA
from presentation.pages.charts import adv_dec, adv_dec_filtered
from src.constants import UI_DATE_FMT
from src.core import get_index_names, industry_stock_map, get_unique_series
from presentation.helpers.common import (
    dg_filter_from_storage,
    weekly_filter_from_storage,
    weekly_analysis_filter_from_storage,
    announcement_filter_from_storage,
)
from presentation.pages.grids import daily_index_grid, stock_grid

# from presentation.pages.stock_grid_summary import grid_summary

weekly_js_filter_function = "date => new Date(date).getDay() === 1 && \
    new Date(date) <= new Date()"
daily_js_filter_function = "date => new Date(date).getDay() > 0 && \
    new Date(date).getDay() < 6 && new Date(date) <= new Date()"


@ui.refreshable
def daily_filter_container():
    with ui.row():
        with (
            ui.card()
            .tight()
            .props("flat bordered")
            .classes("border-red-400 border-[3px]")
        ):
            with ui.row().classes("w-full glossy-rounded"):
                with ui.input(
                    "Trading Date",
                    value=dg_filter_from_storage().trading_date,
                    on_change=(lambda e: UA.handle_filter_change(e, "DATE")),
                ).classes("w-32") as date:
                    with ui.menu().props("no-parent-event") as menu:
                        with (
                            ui.date(mask=UI_DATE_FMT)
                            .props(f':options="{daily_js_filter_function}"')
                            .bind_value(date)
                        ):
                            with ui.row().classes("justify-end"):
                                ui.button("Close", on_click=menu.close).props("flat")
                    with date.add_slot("append"):
                        ui.icon("edit_calendar").on("click", menu.open).classes(
                            "cursor-pointer"
                        ).classes("w-8")
                ui.select(
                    options=["STOCK", "INDEX", "OI"],
                    label="Instr",
                    value=dg_filter_from_storage().instrument,
                    on_change=(lambda e: UA.handle_filter_change(e, "INSTRUMENT")),
                )
                ui.select(
                    options=["DAILY", "WEEKLY", "MONTHLY"],
                    label="TIME",
                    value=dg_filter_from_storage().timeframe,
                    on_change=(lambda e: UA.handle_filter_change(e, "TIMEFRAME")),
                ).classes("w-24")
        match (dg_filter_from_storage().instrument):
            case "STOCK":
                stocks_filter()
            case "INDEX":
                index_filters()
            case "OI":
                oi_filters()
            case _:
                logger.error(f"WTF : Unknown Filter for instrument")
                ui.notify("I do not understand this filter")


@ui.refreshable
def daily_grid_container():
    match (dg_filter_from_storage().instrument):
        case "STOCK":
            return stock_grid()
        case "INDEX":
            return daily_index_grid()
        case "OI":
            logger.info(f"Not yet implemented")
            ui.notify(f"Not yet implemented")
        case _:
            logger.error(f"WTF : not implemented")


@ui.refreshable
def daily_summary_container():
    match (dg_filter_from_storage().instrument):
        case "STOCK":
            # grid_summary()
            adv_dec()  # NOTE: Advance/Decline for the day
            adv_dec_filtered()  # NOTE: Advance/Decline for the filter
        case "INDEX":
            # advances = (app.storage.general["daily.index.gainers"],)
            # declines = (app.storage.general["daily.index.losers"],)
            # total = (app.storage.general["daily.index.total"],)
            adv_dec()
        case "OI":
            logger.info(f"Not yet implemented")
            ui.notify(f"Not yet implemented")
        case _:
            logger.error(f"WTF : not implemented")


@ui.refreshable
def stocks_filter():
    # with ui.row().classes("w-full glossy-rounded"):
    ui.select(
        options=["Volume **", "Value", "OI **"],
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
    # NOTE: Hidden since implementation is unknown!
    ui.select(
        options=["Large Cap", "Midcap", "Small Cap"],
        label="Size",
        value=dg_filter_from_storage().size,
        on_change=(lambda e: UA.handle_filter_change(e, "SIZE")),
    ).classes("hidden")
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
        sorted(get_unique_series(dg_filter_from_storage().trading_date)),
        multiple=True,
        value=dg_filter_from_storage().series,
        label="Select Series",
        on_change=lambda e: UA.handle_filter_change(e, "SERIES"),
    ).classes(
        "w-32"
    )  # .props("use-chips")
    ui.checkbox(
        text="FnO",
        value=dg_filter_from_storage().fno,
        on_change=(lambda e: UA.handle_filter_change(e, "FNO")),
    ).classes("self-center").props(
        "label-position"
    )  # .classes("w-24")
    with ui.column():
        ui.label("Tradind Date")
        ui.label("").bind_text_from(
            dg_filter_from_storage(), target_name="trading_date", strict=True
        )

    # ui.button(
    #     "Clear",
    #     icon="clear",
    #     on_click=lambda e: UA.handle_filter_change(e, "CLEAR"),
    # )


def index_filters():
    ui.label("WIP").props("flat bordered").classes("border-yellow-400 border-[3px]")


def oi_filters():
    pass


def weekly_stocks_filter():
    with ui.row().classes("w-full glossy-rounded"):
        with ui.input(
            "Week Start",
            value=weekly_filter_from_storage().trading_date,
            on_change=(lambda e: UA.weekly_filter_change(e, "DATE")),
        ).classes("w-32") as date:
            with ui.menu().props("no-parent-event") as menu:
                with (
                    ui.date(mask=UI_DATE_FMT)
                    .props(f':options="{weekly_js_filter_function}"')
                    .bind_value(date)
                ):
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
        ).classes(
            "w-24"
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
        ).classes(
            "w-24"
        )
        ui.select(
            options=["Any", "Gainers", "Losers"],
            label="G/L",
            value=weekly_filter_from_storage().gl,
            on_change=(lambda e: UA.weekly_filter_change(e, "GL")),
        ).classes("w-24")
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
        ).classes("w-24")
        ui.select(
            options=["All"] + list(industry_stock_map(i_trading_date=None).keys()),
            label="Industry",
            value=weekly_filter_from_storage().industry,
            on_change=(lambda e: UA.weekly_filter_change(e, "INDUSTRY")),
        ).classes("w-24")
        ui.select(
            sorted(get_unique_series(weekly_filter_from_storage().trading_date)),
            multiple=True,
            value=weekly_filter_from_storage().series,
            label="Select Series",
            on_change=lambda e: UA.weekly_filter_change(e, "SERIES"),
        ).classes(
            "w-32"
        )  # .props("use-chips")
        # ui.input_chips(
        #     "Enter Series",
        #     value=weekly_filter_from_storage().series,
        #     on_change=lambda e: UA.weekly_filter_change(e, "SERIES"),
        #     new_value_mode="add-unique",
        #     validation=lambda e: UA.weekly_filter_change(e, "SERIES"),
        # )
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
        ).props('input-class="text-uppercase"')
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
        ui.button(
            "Server Refresh",
            on_click=lambda x: UA.handle_announcement_filter(x, "REFRESH"),
            color="primary",
            icon="refresh",
        )


def company_results_filter():
    company = ""
    force_refresh = False
    try:
        if app.storage.general["company_results_filter.company_name"]:
            company = app.storage.general["company_results_filter.company_name"]
        if app.storage.general["company_results_filter.force_refresh"]:
            force_refresh = app.storage.general["company_results_filter.force_refresh"]
            logger.info(f"[{force_refresh = }]")
    except KeyError:
        company = ""

    with ui.row().classes("w-full glossy-rounded"):
        ui.input(
            label="Company",
            placeholder="Company Name",
            on_change=lambda x: UA.handle_company_results_filter(x, "COMPANY"),
            autocomplete=None,
            validation=None,
            value=company,
        ).on(
            "keydown.enter", lambda x: UA.handle_company_results_filter(x, "FETCH")
        ).props(
            'input-class="text-uppercase"'
        )
        ui.checkbox(
            "Server Refresh",
            value=force_refresh,
            on_change=lambda x: UA.handle_company_results_filter(x, "FORCE_REFRESH"),
        )
        ui.button(
            "Get",
            on_click=lambda x: UA.handle_company_results_filter(x, "FETCH"),
            color="primary",
            icon="refresh",
        )


def idx_analysis_filter():
    with ui.row(align_items="stretch"):
        ui.select(
            get_index_names(),
            value="NIFTY 50",
            multiple=False,
        )
