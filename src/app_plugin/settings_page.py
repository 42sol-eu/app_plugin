"""
settings page

file:           src/app_plugin/settings_page.py
file-id:        94173f39-36df-4a6a-bd22-757bc0dce22c
project:        app_plugin
project-id:     dfd94fa7-1f2f-4784-901f-dcba7ffc5ef9
author:         felix@42sol.eu

description: |
    This module implements the settings GUI  for `app_plugin`.
"""

import theme
from message import message

from nicegui import ui


class SettingsPage:

    def __init__(self) -> None:
        """The page is created as soon as the class is instantiated.

            """
        @ui.page('/settings')
        def page_settings():
            with theme.frame('Settings'):
                message('Page Settings')
                ui.label('This page is defined in a class.')