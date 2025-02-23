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


def menu() -> None:
    ui.link('Home', '/').classes(replace='text-white')
    ui.link('Settings', '/settings').classes(replace='text-white')
    ui.link('B', '/b').classes(replace='text-white')
    ui.link('C', '/c').classes(replace='text-white')