from nicegui import ui


def daily_gainers():
    with ui.card(align_items="center"):
        with ui.row(wrap=True, align_items="center"):
            with ui.card():
                ui.checkbox("Stocks Trading under 200 DMA", value=True).disable()
                ui.checkbox("Some other indicator: TODO").disable()
                ui.checkbox("Bull/Bear Price Action").disable()
                ui.checkbox("Close above past 2 days").disable()
            with ui.card():
                ui.checkbox("3 White Soldiers").disable()
                ui.checkbox("Place Holder . . . ").disable()
                ui.checkbox("Place Holder . . . ").disable()
                ui.checkbox("Place Holder . . . ").disable()
            with ui.card():
                ui.checkbox("Place Holder . . . ").disable()
                ui.checkbox("Place Holder . . . ").disable()
                ui.checkbox("Place Holder . . . ").disable()
                ui.checkbox("Place Holder . . . ").disable()
            with ui.card():
                ui.checkbox("Place Holder . . . ").disable()
                ui.checkbox("Place Holder . . . ").disable()
                ui.checkbox("Place Holder . . . ").disable()
                ui.checkbox("Place Holder . . . ").disable()
