import datetime
from nicegui import ui, app
import pandas as pd

from loguru import logger

from analytics.gainers import daily_gainer
import src.constants as C

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
    logger.info(f"Into stock_grid method")
    trading_date = datetime.datetime.today().strftime(C.DATE_FMT)
    try:
        if app.storage.user["Trading_date"]:
            trading_date = app.storage.user["Trading_date"]
            logger.info(f"Trading date found in session: [{trading_date}]")
    except KeyError:
        logger.info(f"No Trading_Date in local storage")
    data = daily_gainer(
        file_type=C.SUPPORTED_FILE_TYPES["STOCK"],
        gain_type=C.GAIN_TYPE["PRICE"],
        duration=C.SUPPORTED_TIME_DURATIONS["DAY"],
        start_date=trading_date,
        series="",
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
    if isinstance(data_ui, pd.DataFrame) and not data.empty:
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
                    ":!bg-red-300": "(params) => params.data.pct_change < 0",
                    ":!bg-green-300": "(params) => params.data.pct_change > 0",
                },
            },
        ).classes("max-h-1240")
        stk_grid.on(type="click")
        return stk_grid
    else:
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
