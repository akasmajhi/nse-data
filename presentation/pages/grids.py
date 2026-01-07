from datetime import datetime, timedelta
from nicegui import ui, app
import pandas as pd

from loguru import logger

from analytics.gainers import daily_gainer
from presentation.helpers.dc.all import DGFilter, WeeklyFilter, WeeklyAnalysisFilter
from src.core import (
    industry_stock_map,
    stocks_for_industry,
    get_index_constituents,
    get_fno_stocks,
)
from presentation.helpers.common import (
    dg_filter_from_storage,
    set_grid_summary,
    weekly_analysis_filter_from_storage,
    weekly_filter_from_storage,
)
import src.constants as C

from analytics.core import top_gainers
from src.fetchers.results import fetch_result_calendar

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
    if data.empty:
        # NOTE: Better approach is to handle the -VE case fist
        return ui.aggrid(
            {
                "columnDefs": [
                    {"headerName": "Message", "field": "col1"},
                ],
                "rowData": [
                    {"col1": "Error! No data found."},
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
    set_grid_summary(
        len(data_ui),
        len(data_ui.loc[data_ui["pct_change"] >= 0]),
        len(data_ui.loc[data_ui["pct_change"] < 0]),
    )
    match dg_filter.gl.upper():
        case "LOSS":
            data_ui = data_ui.loc[data_ui["pct_change"] < 0]
        case "GAIN":
            data_ui = data_ui.loc[data_ui["pct_change"] >= 0]
        case "ANY":  # Do nothing
            pass
        case _:
            logger.error("Gain type that is unhandled . . .")

    if dg_filter.industry.upper() != "ALL":
        logger.debug(f"Applying industry filter! [{dg_filter.industry.upper()} = ]")
        industry_to_stocks = industry_stock_map(i_trading_date=None)[dg_filter.industry]
        logger.info(f"Stocks in industry: [{industry_to_stocks  = }]")
        data_ui = data_ui.loc[data_ui["TckrSymb"].isin(industry_to_stocks)]

    # if isinstance(data_ui, pd.DataFrame) and not data.empty:
    stk_grid = ui.aggrid.from_pandas(
        data_ui,
        theme="balham",
        options={
            "columnDefs": [
                {
                    "headerName": "Date",
                    "field": "TradDt",
                    # "valueFormatter": '(new Date(value)).toLocaleDateString("en-IN")',
                },
                {
                    "headerName": "Series",
                    "field": "SctySrs",
                    "filter": "agTextColumnFilter",
                },
                {
                    "headerName": "Symbol",
                    "field": "TckrSymb",
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
        },
    ).classes("max-h-1240")
    stk_grid.on(type="click")
    return stk_grid


@ui.refreshable
def weekly_grid() -> ui.aggrid:
    logger.info(f"Into weekly grid . . . [{weekly_filter_from_storage() = }]")
    weekly_filter: WeeklyFilter = weekly_filter_from_storage()
    trading_date = weekly_filter.trading_date
    data = top_gainers(file_type="STOCK", start_date=trading_date)
    error_message: str = "Error! No data found."
    if weekly_filter.series:
        data = pd.DataFrame(data[data["SctySrs"].isin(weekly_filter.series)])
        if data.empty:
            error_message = f"Some shit series you have entered {weekly_filter.series} "
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
    return ui.aggrid.from_pandas(data)


@ui.refreshable
def corporate_results_grid() -> ui.aggrid:
    logger.debug(f"Into Results Grid")
    data = fetch_result_calendar()
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
    return ui.aggrid.from_pandas(
        data, theme="alpine", auto_size_columns=True, options=options
    ).classes(add="ag-theme-alpine-dark h-610/1000")
