from nicegui import ui
import pandas as pd


@ui.refreshable
def grid_summary(data: pd.DataFrame = pd.DataFrame()):
    with ui.card(align_items="center"):
        if not data.empty:
            ui.label(f"Total {len(data)} items")
        else:
            ui.label(f"No data. The wiring may be incorrect!")
