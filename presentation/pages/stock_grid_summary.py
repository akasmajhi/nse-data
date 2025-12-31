from nicegui import ui, app


@ui.refreshable
def grid_summary():
    with ui.row(align_items="center"):
        # ui.label().bind_text_from(app.storage.general, "grid_summary")
        # ui.label(f'Total stocks: {app.storage.general["grid_summary_total"]}')
        ui.label(f"Total:")
        ui.label().bind_text_from(app.storage.general, "grid_summary_total")
        ui.label(f"Gainers:")
        ui.label().bind_text_from(app.storage.general, "grid_summary_gainers")
        ui.label(f"Losers:")
        ui.label().bind_text_from(app.storage.general, "grid_summary_losers")
