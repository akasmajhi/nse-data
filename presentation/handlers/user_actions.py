from nicegui import ui, app


def toggle_dark(e):
    dark = ui.dark_mode()  # NOTE: Start with Dark mode
    print(f"Before change [{dark.value = }]")
    if dark.value == False:
        dark.enable()
        e.sender.props("icon=img:/icons/icons8-dark-mode-50_dark.png")
        print(f"Dark mode is False. Making it: [{dark.value = }]")
    else:
        dark.disable()
        e.sender.props("icon=img:/icons/icons8-dark-mode-50_bright.png")
        print(f"Dark mode is True. Making it: [{dark.value = }]")
