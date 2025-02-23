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

from menu import menu

from nicegui import ui


@contextmanager
def frame(navigation_title: str):
    """Custom page frame to share the same styling and behavior across all pages"""
    ui.colors(primary='#6E93D6', secondary='#53B689', accent='#111B1E', positive='#53B689')
    with ui.header():
        ui.label('App with Plugins').classes('font-bold')
        ui.space()
        ui.label(navigation_title)
        ui.space()
        with ui.row():
            menu()
    with ui.column().classes('absolute-center items-center'):
        yield