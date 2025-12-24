from nicegui import ui
import pandas as pd

from loguru import logger

from analytics.gainers import daily_gainer
from presentation.helpers.dc.all import DGFilter
from presentation.pages.stock_grid_summary import grid_summary
from presentation.helpers.common import dg_filter_from_storage, set_grid_summary
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
    match dg_filter.gl.upper():
        case "LOSS":
            data_ui = data_ui.loc[data_ui["pct_change"] < 0]
            set_grid_summary(f"Total {len(data_ui)} losers!")
        case "GAIN":
            data_ui = data_ui.loc[data_ui["pct_change"] >= 0]
            set_grid_summary(f"Total {len(data_ui)} gainers!")
        case "ANY":  # Do nothing
            set_grid_summary(f"Total {len(data_ui)} items!!")
        case _:
            logger.error("Gain type that is unhandled . . .")
    grid_summary.refresh()
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
