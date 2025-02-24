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
from . import icon
from . import theme
from . import message

from nicegui import ui
from pathlib import Path

# [Code]
class HelpPage:
    def load_settings_to_ui(self, section: str) -> None:
        pass

    def __init__(self) -> None:
        """The page is created as soon as the class is instantiated."""
        with ui.card().classes('w-full h-full') as card:
            if Path('help.html').exists():
                with open('help.html', 'r') as f:
                    self.html_element = ui.html(f.read()).classes('w-full h-full')
            else:
                self.html_element = ui.html('no content found.').classes('w-full h-full')

    def clear(self):
        self.html_element.set_content('')  # Clear the content of the html element
    
    def set_content(self, text: str):
        with open('help.html', 'w') as f:
            f.write(text)
        self.html_element.set_content(text)  # Update the content of the html element
        self.html_element.update()
