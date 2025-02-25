"""
    file-name: test_colors.py
"""

from nicegui import ui, app,app
from nicegui.elements.mixins.color_elements import QUASAR_COLORS as colors_type 

QUASAR_COLORS = {'primary', 'secondary', 'accent', 'dark', 'positive', 'negative', 'info', 'warning'}

#Q: how create a data class from colors_type
#A: use the following code snippet
class the_colors:
    def __init__(self):
        for color in colors_type:
            if '-' in color
            setattr(self, color, color)

a_color = the_colors()

@ui.page("/")
def main():
    
    with ui.header().classes(f"w-full p-4 text-white").style(f"background-color: {a_color.dark}"):
        ui.label("Plugin powered application").classes("text-2xl")

    with ui.splitter().classes("w-full h-full") as main_splitter:
        with main_splitter.before:
            # create a list of active colors 
            for key in colors_type:
                ui.button(text=key, color=key)
        with main_splitter.after:
            ui.card().classes("w-full h-full")

ui.run()