"""
help page

file:           src/app_plugin/help_page.py
file-id:        f9f740a7-c961-49d5-b5c8-d1e53537397a
project:        app_plugin
project-id:     dfd94fa7-1f2f-4784-901f-dcba7ffc5ef9
author:         felix@42sol.eu

description: |
    This module implements the help GUI  for `app_plugin`.
"""

# [Imports]
import icon
import theme
import message

from nicegui import ui


# [Code]
class HelpPage:
    def load_settings_to_ui(self, section: str) -> None:
        pass

    def __init__(self) -> None:
        """The page is created as soon as the class is instantiated.

            """
                        
        ui.markdown('This is the help page.')
            