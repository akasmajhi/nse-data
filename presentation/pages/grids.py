import json
from dataclasses import asdict
from datetime import datetime, timedelta
from nicegui import ui, app
import pandas as pd

from loguru import logger
import presentation.handlers.user_actions as UA
import presentation.constants as PC
from analytics.gainers import daily_gainer
from presentation.helpers.dc.all import (
    DGFilter,
    WeeklyFilter,
    WeeklyAnalysisFilter,
    AnnouncementsFilter,
)
from src.core import (
    industry_stock_map,
    stocks_for_industry,
    get_index_constituents,
    get_fno_stocks,
    get_data,
)
from presentation.helpers.common import (
    dg_filter_from_storage,
    set_adv_dec,
    set_filtered_grid_summary,
    weekly_analysis_filter_from_storage,
    weekly_filter_from_storage,
    announcement_filter_from_storage,
)
from presentation.pages.stock_grid_summary import grid_summary

import src.constants as C

from analytics.core import top_gainers
from src.core import get_result_calendar

ui.add_head_html(
    """
    <style>
        .rag-green-outer { background-color: #d4edda; }
        .rag-amber-outer { background-color: #fff3cd; }
        .rag-red-outer { background-color: #f8d7da; }
    </style>
"""
)


@ui.refreshable
def stock_grid() -> ui.aggrid:
    logger.info(f"Into stock_grid . . . [{dg_filter_from_storage() = }]")
    dg_filter: DGFilter = dg_filter_from_storage()
    # trading_date = datetime.datetime.today().strftime(C.DATE_FMT)
    trading_date = dg_filter.trading_date
    data = daily_gainer(
        file_type=C.SUPPORTED_FILE_TYPES["STOCK"],
        gain_type=C.GAIN_TYPE["PRICE"],
        duration=C.SUPPORTED_TIME_DURATIONS["DAY"],
        start_date=trading_date,
        series="",
    )
    error_message = "Error! No data found."
    if data.empty:
        # NOTE: Better approach is to handle the -VE case fist
        return ui.aggrid(
            {
                "columnDefs": [
                    {"headerName": "Message", "field": "col1"},
                ],
                "rowData": [
                    {"col1": error_message},
                ],
                "rowClass": "!bg-red-300",
            }
        )
    # print(data.columns)
    data_ui = pd.DataFrame()
    if not data.empty:
        data_ui = data[
            [
                "TradDt",
                "SctySrs",
                "TckrSymb",
                "OpnPric",
                "HghPric",
                "LwPric",
                "ClsPric",
                # "LastPric",
                "PrvsClsgPric",
                "TtlTradgVol",
                "pct_change",
                "total_m_cap",
            ]
        ]
    set_adv_dec(
        len(data_ui),
        len(data_ui.loc[data_ui["pct_change"] > 0]),
        len(data_ui.loc[data_ui["pct_change"] < 0]),
        len(data_ui.loc[data_ui["pct_change"] == 0]),
    )
    # NOTE: Gainer / Loser Filter
    match dg_filter.gl.upper():
        case "LOSS":
            data_ui = data_ui.loc[data_ui["pct_change"] < 0]
        case "GAIN":
            data_ui = data_ui.loc[data_ui["pct_change"] >= 0]
        case "ANY":  # Do nothing
            pass
        case _:
            logger.error("Gain type that is unhandled . . .")

    # NOTE: check if any index is selected
    if dg_filter.index and dg_filter.index.upper() != "ALL":
        data_ui = pd.DataFrame(
            data_ui[data_ui.TckrSymb.isin(get_index_constituents(dg_filter.index))]
        )
    # NOTE: Industry filter
    if dg_filter.industry.upper() != "ALL":
        logger.debug(f"Applying industry filter! [{dg_filter.industry.upper()} = ]")
        industry_to_stocks = industry_stock_map(i_trading_date=None)[dg_filter.industry]
        logger.info(f"Stocks in industry: [{industry_to_stocks  = }]")
        data_ui = data_ui.loc[data_ui["TckrSymb"].isin(industry_to_stocks)]

    # NOTE: For FnO Filter
    if dg_filter.fno:
        data_ui = pd.DataFrame(data_ui[data_ui.TckrSymb.isin(get_fno_stocks())])
    # NOTE: Check to see if there is a series in the filter
    if dg_filter.series:
        data_ui = pd.DataFrame(data_ui[data_ui["SctySrs"].isin(dg_filter.series)])
        if data_ui.empty:
            error_message = f"Some shit series you have entered {dg_filter.series} "
            return error_grid(error_message)
    # NOTE: Stock name concatenated with series name for readability
    data_ui["name_series"] = data_ui["TckrSymb"] + "-" + data_ui["SctySrs"]
    grid_summary.refresh()
    # NOTE: The following may be deprecated!
    set_filtered_grid_summary(
        len(data_ui),
        len(data_ui.loc[data_ui["pct_change"] >= 0]),
        len(data_ui.loc[data_ui["pct_change"] < 0]),
    )
    stk_grid = ui.aggrid.from_pandas(
        data_ui,
        theme="balham",
        options={
            "columnDefs": [
                # {
                #     "headerName": "Date",
                #     "field": "TradDt",
                #     "valueFormatter": f'new Date(value).toLocaleString("en-IN", { PC.date_fmt_opts })',
                # }, #NOTE: Date is moved as a part of stocks_filter
                # {
                #     "headerName": "Series",
                #     "field": "SctySrs",
                #     "filter": "agTextColumnFilter",
                # },
                {
                    "headerName": "Symbol",
                    "field": "name_series",
                    # "field": "TckrSymb",
                    "filter": "agTextColumnFilter",
                    # "floatingFilter": True,
                },
                {"headerName": "Open", "field": "OpnPric"},
                {"headerName": "High", "field": "HghPric"},
                {"headerName": "Low", "field": "LwPric"},
                {
                    "headerName": "Close",
                    "field": "ClsPric",
                    "filter": "agNumberColumnFilter",
                },
                # {"headerName": "Last", "field": "LastPric"},
                {"headerName": "Prev. Cls.", "field": "PrvsClsgPric"},
                {
                    "headerName": "Volume",
                    "field": "TtlTradgVol",
                    "valueFormatter": "value.toLocaleString()",
                },
                {
                    "headerName": "% Delta",
                    "field": "pct_change",
                    "valueFormatter": "value.toFixed(2)",
                    "cellClassRules": {
                        ":text-green font-bold": "(params) => params.data.pct_change >= 0",
                        ":text-red font-bold": "(params) => params.data.pct_change < 0",
                    },
                },
                {
                    "headerName": "MCAP",
                    "field": "total_m_cap",
                    "filter": "agNumberColumnFilter",
                    "valueFormatter": 'value.toLocaleString("en-IN", { style: "currency", currency: "INR" })',
                },
            ],
            # "rowStyle": {"background": "grey"},
            "rowClassRules": {
                # ":!bg-red-300": "(params) => params.data.pct_change < 0",
                # ":text-red": "(params) => params.data.pct_change < 0",
                # ":!bg-green-300": "(params) => params.data.pct_change > 0",
                # ":text-green": "(params) => params.data.pct_change > 0",
            },
            "pagination": True,
            "paginationPageSize": 20,
        },
        html_columns=[0],
    ).classes(add="ag-theme-alpine-dark h-550/1000")
    # ).classes("max-h-1240")
    stk_grid.on(type="click")
    return stk_grid


@ui.refreshable
def daily_index_grid() -> ui.aggrid:
    logger.info(f"Into daily_index_grid . . . [{dg_filter_from_storage() = }]")
    dg_filter: DGFilter = dg_filter_from_storage()
    # trading_date = datetime.datetime.today().strftime(C.DATE_FMT)
    trading_date = dg_filter.trading_date
    data = get_data(file_type="INDEX", start_date=trading_date, end_date=trading_date)
    error_message = "Error! No data found."
    if data.empty:
        # NOTE: Better approach is to handle the -VE case fist
        return ui.aggrid(
            {
                "columnDefs": [
                    {"headerName": "Message", "field": "col1"},
                ],
                "rowData": [
                    {"col1": error_message},
                ],
                "rowClass": "!bg-red-300",
            }
        )
    data.rename(
        columns={
            "30_DAY_PCT_CHANGE": "PCT_CHANGE_30_D",
            "365_D_PCT_CHANGE": "PCT_CHANGE_365_D",
        },
        inplace=True,
    )
    data["PCT_CHANGE"] = pd.to_numeric(data["PCT_CHANGE"], errors="coerce")
    data = data.dropna(subset=["PCT_CHANGE"])
    app.storage.general["daily.index.total"] = len(data)
    app.storage.general["daily.index.gainers"] = len(data[data["PCT_CHANGE"] > 0])
    app.storage.general["daily.index.losers"] = len(data[data["PCT_CHANGE"] < 0])
    return ui.aggrid.from_pandas(
        data,
        theme="balham",
        auto_size_columns=True,
        options={
            "columnDefs": [
                {
                    "headerName": "Index",
                    "field": "INDEX",
                    "filter": "agTextColumnFilter",
                },
                {
                    "headerName": "Current",
                    "field": "CURRENT",
                },
                {
                    "headerName": "1 DAY %",
                    "field": "PCT_CHANGE",
                    "filter": "agNumberColumnFilter",
                    "cellClassRules": {
                        ":text-green font-bold": "(params) => params.data.PCT_CHANGE >= 0",
                        ":text-red font-bold": "(params) => params.data.PCT_CHANGE < 0",
                    },
                },
                {
                    "headerName": "1 MON %",
                    "field": "PCT_CHANGE_30_D",
                    "filter": "agNumberColumnFilter",
                    "cellClassRules": {
                        ":text-green font-bold": "(params) => params.data.PCT_CHANGE_30_D>= 0",
                        ":text-red font-bold": "(params) => params.data.PCT_CHANGE_30_D < 0",
                    },
                },
                {
                    "headerName": "1 YR. %",
                    "field": "PCT_CHANGE_365_D",
                    "filter": "agNumberColumnFilter",
                    "cellClassRules": {
                        ":text-green font-bold": "(params) => params.data.PCT_CHANGE_365_D>= 0",
                        ":text-red font-bold": "(params) => params.data.PCT_CHANGE_365_D < 0",
                    },
                },
                # NOTE: OHLC Data does not seem significant here!
                # {"headerName": "Open", "field": "OPEN"},
                # {"headerName": "High", "field": "HIGH"},
                # {"headerName": "Low", "field": "LOW"},
                # {
                #     "headerName": "Prev. Close",
                #     "field": "PREV_CLOSE",
                # },
                {"headerName": "1 WK", "field": "1_WEEK_AGO"},
                {"headerName": "1 MON", "field": "1_MONTH_AGO"},
                {"headerName": "1 YR.", "field": "1_YEAR_AGO"},
                {"headerName": "52_WK_LOW", "field": "52_WK_LOW"},
                {"headerName": "52_WK_HIGH", "field": "52_WK_HIGH"},
            ],
            "pagination": True,
            "paginationPageSize": 20,
        },
        html_columns=[0],
    ).classes(add="ag-theme-alpine-dark h-550/1000")


@ui.refreshable
def weekly_grid() -> ui.aggrid:
    logger.info(f"Into weekly grid . . . [{weekly_filter_from_storage() = }]")
    weekly_filter: WeeklyFilter = weekly_filter_from_storage()
    trading_date = weekly_filter.trading_date
    data = top_gainers(file_type="STOCK", start_date=trading_date)
    error_message: str = "Error! No data found."
    if data.empty:
        # NOTE: Better approach is to handle the -VE case fist
        return ui.aggrid(
            {
                "columnDefs": [
                    {"headerName": "Message", "field": "col1"},
                ],
                "rowData": [
                    {"col1": error_message},
                ],
                "rowClass": "text-white italic !bg-red-900",
            }
        ).classes(add="ag-theme-alpine-dark")
    # logger.info(f"[{data = }]")
    # logger.info(f"Rendering the grid now . . .")
    if weekly_filter.series:
        data = pd.DataFrame(data[data["SctySrs"].isin(weekly_filter.series)])
        if data.empty:
            error_message = f"Some shit series you have entered {weekly_filter.series} "
    data["name_series"] = data["TckrSymb"] + "-" + data["SctySrs"]
    data["change"] = (
        (data["ClsPric"] - data["PrvsClsgPric"]) / data["PrvsClsgPric"]
    ) * 100
    # NOTE: check if the industry is set in filter
    if weekly_filter.industry and weekly_filter.industry.upper() != "ALL":
        logger.debug(f"Industry filter is set [{weekly_filter.industry = }]")
        # Get all the stock names for the selected industry
        logger.debug(stocks_for_industry(weekly_filter.industry))
        data = pd.DataFrame(
            data[data.TckrSymb.isin(stocks_for_industry(weekly_filter.industry))]
        )

    # NOTE: check if any index is selected
    if weekly_filter.index and weekly_filter.index.upper() != "ALL":
        logger.debug(f"Index filter is set. [{weekly_filter.index = }]")
        logger.debug(f"[{get_index_constituents(weekly_filter.index)}]")
        data = pd.DataFrame(
            data[data.TckrSymb.isin(get_index_constituents(weekly_filter.index))]
        )
    # NOTE: check if any Gainer/Loser is selected
    match (weekly_filter.gl.upper()):
        case "ANY":
            pass
        case "GAINERS":
            data = pd.DataFrame(data[data.change >= 0])
        case "LOSERS":
            data = pd.DataFrame(data[data.change < 0])
        case _:
            logger.error(f"Not implemented GL type [{weekly_filter.gl}]")
    if weekly_filter.fno:
        data = pd.DataFrame(data[data.TckrSymb.isin(get_fno_stocks())])
    # TODO: Update Weekly summary in storage

    # data["tmp_val"] = (
    #     f'<a href="https://google.com" target="_blank">{data["TckrSymb"]}</a>'
    # )
    return ui.aggrid.from_pandas(
        data,
        theme="balham",
        auto_size_columns=True,
        options={
            "columnDefs": [
                {
                    "headerName": "Symbol",
                    "field": "name_series",
                    "filter": "agTextColumnFilter",
                    "cellStyle": {
                        # "color": "white",
                        # "background-color": "black",
                        "fontWeight": "bold",
                        # "bold-text": "params.value > 100000",
                    },
                },
                # {
                #     "headerName": "Symbol",
                #     "field": "TckrSymb",  # DONE: Concat symbol with series in 1 column
                # },
                # {
                #     "headerName": "Series",
                #     "field": "SctySrs",
                # },
                {
                    "headerName": "MCAP",
                    "field": "total_m_cap",
                    "filter": "agNumberColumnFilter",
                    "valueFormatter": 'value.toLocaleString("en-IN", { style: "currency", currency: "INR" })',
                    # "cellStyle": {
                    #     "background-color": "black",
                    # },
                    "cellClassRules": {
                        "bg-gray-600 italic": "x > 100000",
                    },
                },
                {
                    "headerName": "Open",
                    "field": "OpnPric",
                },
                {
                    "headerName": "High",
                    "field": "HghPric",
                },
                {
                    "headerName": "Low",
                    "field": "LwPric",
                },
                {
                    "headerName": "Close",
                    "field": "ClsPric",
                },
                {
                    "headerName": "Prev. close",
                    "field": "PrvsClsgPric",
                },
                {
                    "headerName": "Change %",
                    "field": "change",
                    "valueFormatter": "value.toFixed(2)",
                    "cellStyle": {
                        "fontSize": "14px",
                        "textAlign": "center",
                    },
                    "cellClassRules": {
                        ":text-green font-bold": "(params) => params.data.change >= 0",
                        ":text-red font-bold": "(params) => params.data.change < 0",
                    },
                },
                {
                    "headerName": "Volume",
                    "field": "TtlTradgVol",
                    "valueFormatter": "value.toLocaleString()",
                },
                {
                    "headerName": "Value",
                    "field": "TtlTrfVal",
                    "valueFormatter": "Math.floor(value).toLocaleString()",
                    # "valueFormatter": "value.toLocaleString()",
                },
            ],
            "pagination": True,
            "paginationPageSize": 15,
        },
        html_columns=[0],
    ).classes(add="ag-theme-alpine-dark h-475/1000")


@ui.refreshable
def weekly_analysis_grid() -> ui.aggrid:
    logger.info(
        f"Into weekly analysis grid . . . [{weekly_analysis_filter_from_storage()}]"
    )
    data: pd.DataFrame = pd.DataFrame()
    data_current: pd.DataFrame = pd.DataFrame()
    data_previous: pd.DataFrame = pd.DataFrame()
    trading_date: str = ""
    error_message: str = "Error! No data found."
    try:
        # DONE: Guard against exceptions
        trading_date = app.storage.general["trading_date"]
        previous_date = (
            datetime.strptime(trading_date, C.DATE_FMT) - timedelta(days=7)
        ).strftime(C.DATE_FMT)
        # NOTE: Default duration for top_gainers is WEEK
        data_current = top_gainers(file_type="STOCK", start_date=trading_date)
        data_previous = top_gainers(file_type="STOCK", start_date=previous_date)
        data = pd.DataFrame(
            data_current[data_current.ClsPric > data_current.PrvsClsgPric]
        )
    except Exception as e:
        logger.error(f"Eception occured! [{e = }]")

    if data.empty:
        # NOTE: Better approach is to handle the -VE case fist
        return ui.aggrid(
            {
                "columnDefs": [
                    {"headerName": "Message", "field": "col1"},
                ],
                "rowData": [
                    {"col1": error_message},
                ],
                "rowClass": "text-white italic !bg-red-900",
            }
        ).classes(add="ag-theme-alpine-dark")
    weekly_analysis_filter: WeeklyAnalysisFilter = weekly_analysis_filter_from_storage()
    # TODO: Use the weekly_analysis_filter to slice data
    return ui.aggrid.from_pandas(data)


@ui.refreshable
def corporate_results_grid() -> ui.aggrid:
    logger.debug(f"Into Corporate Results Grid")
    announcement_filter: AnnouncementsFilter = announcement_filter_from_storage()
    if announcement_filter.force_refresh:
        data = get_result_calendar(force_refresh=True)
        # NOTE: Turn-off the force_refresh after getting new data
        announcement_filter.force_refresh = False
        announcement_filter_dict = json.dumps(asdict(announcement_filter))
        app.storage.general["announcement_filter"] = announcement_filter_dict
    data = get_result_calendar(force_refresh=False)
    error_message: str = "Some error occured while fetching results/announcements"
    if data.empty:
        # NOTE: Better approach is to handle the -VE case fist
        return ui.aggrid(
            {
                "columnDefs": [
                    {"headerName": "Message", "field": "col1"},
                ],
                "rowData": [
                    {"col1": error_message},
                ],
                "rowClass": "text-white italic !bg-red-900",
            }
        ).classes(add="ag-theme-alpine-dark")
    options = {
        "columnDefs": [
            {
                "headerName": "Stock",
                "field": "symbol",
                "filter": "agTextColumnFilter",
                "cellStyle": {
                    "fontWeight": "bold",
                },
            },
            {
                "headerName": "Purpose",
                "field": "purpose",
                "filter": "agTextColumnFilter",
                "cellStyle": {
                    "fontWeight": "italic",
                },
            },
            {
                "headerName": "Date",
                "field": "date",
                "filter": "agTextColumnFilter",
                "cellStyle": {
                    "fontWeight": "italic",
                },
                "valueFormatter": f'new Date(value).toLocaleString("en-IN", { PC.date_fmt_opts })',
            },
            {
                "headerName": "Description",
                "field": "bm_desc",
                "tooltipField": "bm_desc",
                "cellStyle": {
                    "fontWeight": "italic",
                },
            },
        ],
        "pagination": True,
        "paginationPageSize": 15,
    }
    if announcement_filter.company:
        data = data[data.symbol.str.contains(announcement_filter.company.upper())]
    if announcement_filter.purpose:
        data = data[
            data.purpose.str.upper().str.contains(announcement_filter.purpose.upper())
        ]
    if announcement_filter.selected_industry.upper() != "ALL":
        # data_ui = data_ui.loc[data_ui["TckrSymb"].isin(industry_to_stocks)]
        ind_to_stk = industry_stock_map(i_trading_date=None)
        data = data.loc[data["symbol"].isin(ind_to_stk)][
            announcement_filter.selected_industry
        ]
    # TODO: Get only relevant industries
    # data_combined:pd.DataFrame =
    return (
        ui.aggrid.from_pandas(
            data, theme="alpine", auto_size_columns=True, options=options
        )
        .classes(add="ag-theme-alpine-dark h-610/1000")
        .on(
            "cellClicked",
            lambda event: UA.show_dialog(f'{event.args["value"]}'),
        )
    )


@ui.refreshable
def company_results_grid() -> ui.aggrid:
    company = ""
    try:
        if app.storage.general["company_results_filter.company_name"]:
            company = app.storage.general["company_results_filter.company_name"]
    except KeyError:
        logger.info(f"Company name not set")
    force_refresh = False
    try:
        if app.storage.general["company_results_filter.force_refresh"]:
            force_refresh = app.storage.general["company_results_filter.force_refresh"]
    except KeyError:
        logger.info(f"Force Refresh name not set")
    if not company:
        return error_grid("No company name provided")
    # NOTE: Fetch the results for the company
    logger.debug(f"Calling fetcher for {company = }, {force_refresh = }")
    data = get_result_calendar(force_refresh, company)
    if data.empty:
        return error_grid(f"Company << {company} >>not found")
    data = data.sort_values(by="date", ascending=False)
    options = {
        "columnDefs": [
            # {
            #     "headerName": "Stock",
            #     "field": "symbol",
            #     "filter": "agTextColumnFilter",
            #     "cellStyle": {
            #         "fontWeight": "bold",
            #     },
            # },
            # {
            #     "headerName": "Full Name",
            #     "field": "company",
            #     "filter": "agTextColumnFilter",
            #     "cellStyle": {
            #         "fontWeight": "italic",
            #     },
            # },
            {
                "headerName": "Purpose",
                "field": "purpose",
                "filter": "agTextColumnFilter",
                "cellStyle": {
                    "fontWeight": "italic",
                },
            },
            {
                "headerName": "Event Date",
                "field": "date",
                "filter": "agTextColumnFilter",
                "cellStyle": {
                    "fontWeight": "italic",
                },
                "valueFormatter": f'new Date(value).toLocaleString("en-IN", { PC.date_fmt_opts })',
                # "valueFormatter": """new Date(value).toLocaleString("en-IN", { weekday: "long", year: "numeric", month: "long", day: "numeric" })""",
                # "valueFormatter": 'data.toLocaleString("en-IN", "month": "long")', #TODO: Fix this
            },
            {
                "headerName": "Description",
                "field": "bm_desc",
                "tooltipField": "bm_desc",
                "cellStyle": {
                    "fontWeight": "italic",
                },
            },
        ],
        "pagination": True,
        "paginationPageSize": 15,
    }
    return (
        ui.aggrid.from_pandas(
            data, theme="alpine", auto_size_columns=True, options=options
        )
        .on(
            "cellClicked",
            lambda event: UA.show_dialog(f'{event.args["value"]}'),
        )
        .classes(add="ag-theme-alpine-dark h-610/1000")
    )


def error_grid(msg: str) -> ui.aggrid:

    return ui.aggrid(
        {
            "columnDefs": [
                {"headerName": "Message", "field": "col1"},
            ],
            "rowData": [
                {"col1": msg},
            ],
            "rowClass": "text-white italic !bg-red-900",
        }
    ).classes(add="ag-theme-alpine-dark")
