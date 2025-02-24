"""
theme

file:           src/app_plugin/theme.py
file-id:        587363d8-80a4-4ca4-ad74-c97c378aedbc
project:        app_plugin
project-id:     dfd94fa7-1f2f-4784-901f-dcba7ffc5ef9
author:         felix@42sol.eu

description: |
    This module implements the theme  for `app_plugin`.
"""

# [Imports]
from contextlib import contextmanager

from .menu import menu
from .help_page import HelpPage
from . import icon
from .toggle_button import ToggleButton

from nicegui import ui
button_help = None 
button_menu = None
menu_drawer = None
view_area = None

# [Code]
@contextmanager
def frame(navigation_title: str, loaded_plugins):
    global menu_drawer
    global button_menu
    global button_help
    global view_area

    """Custom page frame to share the same styling and behavior across all pages"""
    ui.colors(primary='#6E93D6', secondary='#53B689', accent='#111B1E', positive='#53B689')
    with ui.header():
        button_menu = ToggleButton(icon=icon.menu)
        ui.label('App with Plugins').classes('font-bold')
        ui.space()
        ui.label(navigation_title).classes('text-2xl font-bold')
        ui.space()
        button_help = ToggleButton(icon=icon.help)

    with ui.left_drawer() as menu_drawer:
        menu(menu_drawer, button_menu, plugins=loaded_plugins)

    with ui.right_drawer() as help_drawer:
        view_area = HelpPage()
    
    with ui.column().classes('w-full h-full absolute-center items-center'):
        yield

    button_menu.on('click', menu_drawer.toggle)
    
    button_help.on('click', help_drawer.toggle)
    