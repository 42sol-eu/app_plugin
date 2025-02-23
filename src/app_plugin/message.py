"""
theme

file:           src/app_plugin/message.py
file-id:        587363d8-80a4-4ca4-ad74-c97c378aedbc
project:        app_plugin
project-id:     dfd94fa7-1f2f-4784-901f-dcba7ffc5ef9
author:         felix@42sol.eu

description: |
    This module implements the message GUI  for `app_plugin`.
"""

# [Imports]
from nicegui import ui

# [Components]
class message(ui.label):

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.classes('text-h4 text-grey-8')