"""
main_page.py

file:           src/app_plugin/main_page.py
file-id:        eaa08c1e-6592-4441-9c77-19f74e173c9a
project:        app_plugin
project-id:     dfd94fa7-1f2f-4784-901f-dcba7ffc5ef9
author:         felix@42sol.eu

description: |
    This module implements the main page for `app_plugin`.
"""

# [Imports]

# Add the directory containing the modules to the Python path
import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from . import message

from nicegui import ui


def content() -> None:
    message.message('This is the home page.').classes('font-bold')
    ui.label('Use the menu on the top right to navigate.')