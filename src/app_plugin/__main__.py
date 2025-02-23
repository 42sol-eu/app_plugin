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

from . import api_router
from . import settings_page
from . import main_page
from . import theme

from nicegui import app, ui

import stevedore._cache
from pathlib import Path

# Patch the _hash_settings_for_path method
original_hash_settings_for_path = stevedore._cache._hash_settings_for_path

def patched_hash_settings_for_path(path):
    h = original_hash_settings_for_path(path)
    for entry in path.iterdir():
        if isinstance(entry, Path):
            entry = str(entry)
        h.update(entry.encode('utf-8'))
    return h

stevedore._cache._hash_settings_for_path = patched_hash_settings_for_path

# Your existing code
from stevedore import driver, ExtensionManager
from .plugin_view import PluginView


def load_plugins():
    manager = ExtensionManager(
        namespace='app_plugin.plugins',
        invoke_on_load=True,
        invoke_args=(),
    )
    for extension in manager:
        plugin = extension.obj
        if isinstance(plugin, PluginView):
            print(f"Loading plugin: {plugin.name}")
            plugin.execute()
        else:
            print(f"Plugin {plugin.name} is not a PluginView")


@ui.page('/')
def index_page() -> None:
    with theme.frame('Main Page'):
        main_page.content()


if __name__ in {"__main__", "__mp_main__"}:
    print("Starting main page content")
    load_plugins()

    settings_page.SettingsPage()

    app.include_router(api_router.router)

    ui.run(title='App with Plugins',
           reload=reload,
           native=False,)
    print("UI is running")

# TODO: integrate the RSTEditorPlugin into the app

