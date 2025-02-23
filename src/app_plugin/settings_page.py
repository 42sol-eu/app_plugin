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

# [Imports]
import theme
from message import message
import icon

from nicegui import ui


# [Code]
class SettingsPage:
    def load_settings_to_ui(self, section: str) -> None:
        pass

    def __init__(self) -> None:
        """The page is created as soon as the class is instantiated.

            """
        
        self.settings_config = {'application': {'title': 'Application', 'icon': icon.settings}, 
                                'viewer': {'title': 'Viewer', 'icon': icon.close}}
                         
        @ui.page('/settings')
        def page_settings():
            with theme.frame('Settings'):
                message('Page Settings')
                with ui.splitter(value=10).classes('w-full h-full') as splitter:
                    with splitter.before:
                        with ui.tabs().props('vertical').classes('w-full') as tabs:
                            self.tabs = tabs
                            print(self.tabs)

                            for key, value in self.settings_config.items():
                                setattr(self, key, ui.tab(value['title'], icon=value['icon']))
                            
                    with splitter.after:
                        with ui.tab_panels(self.tabs, value='Application').props('vertical').classes('w-full'):
                            
                            with ui.tab_panel(self.application) as tab:
                                self.load_settings_to_ui('application')
                            with ui.tab_panel(self.viewer) as tab:
                                self.load_settings_to_ui('viewer')
            