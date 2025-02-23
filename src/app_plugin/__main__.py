#!/usr/bin/env python3
# [Includes]
import os 
from pathlib import Path
import sys
sys.path.append(Path(__file__).parent)  

if __package__ is None or __package__ == '':
    reload = True
    __package__ = "app_plugin"
else:
    # we are running as a package
    reload = False

from . import api_router_extended
from . import settings_page
from . import main_page
from . import theme

from nicegui import app, ui

import stevedore._cache
from pathlib import Path

# Your existing code
from importlib.metadata import entry_points
from .plugin_view import PluginView
from . import api_router_extended 

def load_plugins():
    plugins = entry_points(group='app_plugin.plugins')
    print(f"Loading: {[ep.name for ep in plugins]}")
    for ep in plugins:
        plugin = ep.load()
        if isinstance(plugin, PluginView):
            print(f"Loading plugin: {plugin.name}")
            plugin().execute()
        else:
            print(f"Plugin {plugin.name} is not a PluginView")

# [Main]
@ui.page('/')
def index_page() -> None:
    with theme.frame('Main Page'):
        main_page.content()


if __name__ == "__main__":
    print("Loading plugins")
    load_plugins()

    print("Loading GUI")
    settings_page.SettingsPage()

    app.include_router(api_router_extended.router)

    ui.run(title='App with Plugins',
           reload=False,
           native=False,)
    print("UI is running")

# TODO: integrate the RSTEditorPlugin into the app

