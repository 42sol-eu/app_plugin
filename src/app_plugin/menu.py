"""
menu

file:           src/app_plugin/menu.py
file-id:        5da0db80-6ed4-4b91-96b7-e96abf398d89
project:        app_plugin
project-id:     dfd94fa7-1f2f-4784-901f-dcba7ffc5ef9
author:         felix@42sol.eu

description: |
    This module implements the menu GUI  for `app_plugin`.
"""
from nicegui import ui
from . import icon
from .toggle_button import ToggleButton

def menu(drawer, button, plugins) -> None:
    with ui.column().classes(add='w-full h-full'):
        ui.label('Menu:').classes(add='font-bold text-xl')
        with ui.link('Home', '/').classes(add='text-xl'):
            ui.icon(icon.home).classes(add='text-xl')
        ui.link('Settings', '/settings').classes(add='text-xl')
        
        # Dynamically add plugin links
        for plugin_name in plugins:
            ui.link(plugin_name, f'/{plugin_name.lower()}').classes(add='text-xl')

        close_button = ui.button(icon=icon.close) \
            .on('click', drawer.toggle) \
            .classes(add='absolute bottom-0 center-0 m-4')
        
        if isinstance(button, ToggleButton):
            close_button.on('click', drawer.toggle)