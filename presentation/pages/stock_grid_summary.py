from nicegui import ui, app


@ui.refreshable
def grid_summary():
    with ui.card(align_items="center"):
        try:
            summary = app.storage.user["grid_summary"]
        except KeyError:
            summary = "Loading"

        ui.label(summary)
