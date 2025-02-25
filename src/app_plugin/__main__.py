#!/usr/bin/env python3
# [Imports, global]
import os 
from pathlib import Path
import sys
from nicegui import ui, app
sys.path.append(Path(__file__).parent)  

if __package__ is None or __package__ == '':
    reload = True
    __package__ = "app_plugin"
else:
    # we are running as a package
    reload = False


# [Imports from app_plugin]
app.settings = {}
app.settings['_docs'] = Path('./application_data/_docs')
app.settings['_settings'] = Path('./application_data/_settings')

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
from .menu import menu

def load_plugins():
    plugins = entry_points(group='app_plugin.plugins')
    print(f"Loading: {[ep.name for ep in plugins]}")
    loaded_plugins = {}
    for ep in plugins:
        plugin_class = ep.load()
        if issubclass(plugin_class, PluginView):
            print(f"Loading plugin: {plugin_class.__name__}")
            loaded_plugins[ep.name] = ep
        else:
            print(f"Plugin {plugin_class.__name__} is not a PluginView")
    return loaded_plugins

# [Main]
@ui.page('/')
def index_page() -> None:
    global loaded_plugins
    with theme.frame('Main Page', loaded_plugins.keys()):
        main_page.content()

    for key, plugin in loaded_plugins.items():
        print(f"Create instance: {key}")
        plugin_class = plugin.load()
        plugin_instance = plugin_class(loaded_plugins.keys())
        plugin_instance.register_view(theme.view_area)

if __name__ == "__main__":
    print("Loading plugins")
    loaded_plugins = load_plugins()
    
    

    print("Loading GUI")
    settings_page.SettingsPage(loaded_plugins)

    app.include_router(api_router_extended.router)

    # Create the menu with the loaded plugins
    menu(drawer=ui.left_drawer(), button=ui.button(), plugins=loaded_plugins)

    ui.run(title='App with Plugins', reload=False, native=False)
    print("UI is running")

# TODO: integrate the RSTEditorPlugin into the app

