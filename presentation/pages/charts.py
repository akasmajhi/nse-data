from nicegui import ui, app
from loguru import logger


def daily_container():
    pass


@ui.refreshable
def adv_dec(
    # total=app.storage.general["grid_summary_total"],
    # advances=app.storage.general["grid_summary_gainers"],
    # declines=app.storage.general["grid_summary_losers"],
):
    try:
        total = app.storage.general["total_stocks"]
        advances = app.storage.general["gainer_stocks"]
        declines = app.storage.general["loser_stocks"]
        unchanged = app.storage.general["unchanged_stocks"]
    except KeyError:
        logger.error(f"Error reading adv/dec data from storage. Defaulting to 1's")
        total = advances = declines = unchanged = 1

    # echart = ui.echart(

    options = {
        "animation": True,
        "legend": {
            "bottom": 0,
            "left": "center",
            "data": ["Advance", "Decline", "Unchanged"],
            "textStyle": {
                "color": "white",
                "fontSize": 12,
            },
        },
        "height": "70px",
        "width": "100%",
        "top": 0,
        "bottom": 0,
        "grid": {
            "top": "0%",
            "bottom": "0%",
            "left": "0%",
            "right": "0%",
            "containLabel": False,
            "show": False,
        },
        "xAxis": {
            "inverse": False,
            "splitLine": {
                "show": False,
            },
            "axisLabel": {
                "color": "#FFFFFF",
                "show": False,
                "text": "adv./Dec.",
            },
        },
        "yAxis": {
            "data": "Dist.",
            "show": False,
        },
        # "aria": {
        #     "enabled": True,
        #     "description": "Advance / Declines",
        #     # "decal": {"show": True},
        # },
        # "title": {
        #     "text": "Advance / Decline",
        #     "textStyle": {
        #         "color": "white",
        #         "fontSize": 12,
        #     },
        # },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "none",
            },
        },
        # "legend": {"textStyle": {"color": "white"}},
        # "axisLabel": {"color": "#FFFFFF"},
        "series": [
            {
                "label": {
                    "show": True,
                    "position": "inside",
                    "color": "#FFFFFF",
                    "fontSize": 14,
                    "fontWeight": "bold",
                    "formatter": f"{advances/total * 100:.2f} %",
                    # "formatter": f"{advances} ( {advances/total * 100:.2f} %)",
                },
                "data": [advances],
                "type": "bar",
                "color": "green",
                "name": "Advance",
                "stack": "adv_dec",
            },
            {
                "label": {
                    "show": True,
                    "position": "inside",
                    "color": "#FFFFFF",
                    "fontSize": 14,
                    "fontWeight": "bold",
                    "formatter": f"{declines/total * 100:.2f} %",
                    # "formatter": f"{declines} ( {declines/total * 100:.2f} %)",
                },
                "data": [declines],
                "type": "bar",
                "color": "red",
                "name": "Decline",
                "stack": "adv_dec",
            },
            {
                "label": {
                    "show": False,
                    "position": "inside",
                    "color": "#000000",
                    "fontSize": 14,
                    "fontWeight": "bold",
                    "formatter": f"{unchanged/total * 100:.2f} %",
                    # "formatter": f"{unchanged} ( {unchanged/total * 100:.2f} %)",
                },
                "data": [unchanged],
                "type": "bar",
                "color": "white",
                "name": "Unchanged",
                "stack": "adv_dec",
                # "series-line.tooltip": {
                #     "trigger": "axis",
                #     "formatter": r"""{c}: {d}""",
                # },
            },
        ],
    }
    ui.echart(options=options, renderer="canvas").classes(add="h-8 ")
    # echart = ui.echart(options=options, renderer="canvas").classes("h-8")
    # )  # For click events.on("click", lambda params: ui.notify(f"[{params}]"))

    # async def get_dimensions():
    #     width = await echart.run_chart_method("getWidth")
    #     height = await echart.run_chart_method("getHeight")
    #     ui.notify(f"Width: {width} height: {height}")
    #
    # ui.button("Get Width", on_click=get_dimensions)


def adv_dec_filtered():
    ui.label("Summary of filtered data")
    pass


def daily_index_charts():
    pass
