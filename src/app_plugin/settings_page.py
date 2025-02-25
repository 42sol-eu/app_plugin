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
import yaml
from pathlib import Path
from . import theme
from .message import message
from . import icon
from . import theme

from nicegui import ui, app


# [Code]
class SettingsPage:
    def __init__(self, loaded_plugins) -> None:
        """The page is created as soon as the class is instantiated."""
        self.help_page = None
        
        self.app_settings_file = Path(app.settings['_settings']) / 'app_plugin.yaml'
        self.viewer_settings_file = Path(app.settings['_settings']) / 'viewer.yaml'
        self.app_settings = self.load_settings(self.app_settings_file)
        self.viewer_settings = self.load_settings(self.viewer_settings_file)
        self.settings_config = {'application': {'title': 'Application', 'icon': icon.settings}, 
                                'viewer': {'title': 'Viewer', 'icon': icon.close}}
        

        self.apply_theme()
        self.create_page(loaded_plugins)
        

    def register_help_page(self, help_page) -> None:
        """Register the help page for reloading the CSS file."""
        if self.help_page is None:
            self.help_page = theme.view_area
        else:
            pass

    def load_settings(self, settings_file: Path) -> dict:
        """Load settings from the YAML file."""
        with open(settings_file, 'r') as file:
            return yaml.safe_load(file)

    def save_settings(self, settings_file: Path, settings: dict) -> None:
        """Save settings to the YAML file."""
        with open(settings_file, 'w') as file:
            yaml.safe_dump(settings, file)

    def load_settings_to_ui(self, section: str) -> None:
        """Load settings to the UI for editing."""
        if section == 'application':
            settings_section = self.app_settings.get('user_interface', {})
        elif section == 'viewer':
            settings_section = self.viewer_settings.get('user_interface', {})
        else:
            return
        
        for key, value in sorted(settings_section.items()):
            if value['type'] == 'text':
                ui.input(label=key, value=value['value'], 
                    on_change=lambda e, k=key: self.update_setting(section, k, e.value)) \
                    .classes('w-full h-full')
            elif value['type'] == 'switch':
                ui.switch(text=key, value=value['value'], 
                    on_change=lambda e, k=key: self.update_setting(section, k, e.value)) \
                    .classes('w-full h-full')
            elif value['type'] == 'number':
                ui.number(label=key, value=value['value'], 
                    on_change=lambda e, k=key: self.update_setting(section, k, e.value)) \
                    .classes('w-full h-full')
            elif value['type'] == 'select':
                ui.select(label=key, options=value['options'].split(', '),
                    value=value['value'], on_change=lambda e, k=key: self.update_setting(section, k, e.value)) \
                    .classes('w-full h-full')

    def update_setting(self, section: str, key: str, value: any) -> None:
        """Update the setting value."""
        if section == 'application':
            self.app_settings['user_interface'][key]['value'] = value
            self.save_settings(self.app_settings_file, self.app_settings)
            if key == 'default_theme':
                self.apply_theme()
        elif section == 'viewer':
            self.viewer_settings['user_interface'][key]['value'] = value
            self.save_settings(self.viewer_settings_file, self.viewer_settings)

    def apply_theme(self) -> None:
        """Apply the theme based on the 'default_theme' setting."""
        self.register_help_page(theme.view_area)
        
        default_theme = self.app_settings['user_interface'].get('default_theme', {}).get('value', False)
        ui.dark_mode(default_theme)
        if default_theme:
            ui.add_head_html(f'<link rel="stylesheet" href="{app.settings["_settings"]}/custom_styles_dark.css">')
        else:
            ui.add_head_html(f'<link rel="stylesheet" href="{app.settings["_settings"]}/custom_styles_light.css">')
        if self.help_page:
            self.help_page.reload()

    def create_page(self, loaded_plugins) -> None:
        @ui.page('/settings')
        def settings_page() -> None:
            with theme.frame('Settings', loaded_plugins):
                with ui.splitter(value=25).classes('w-full h-full') as splitter:
                    with splitter.before:
                        with ui.tabs().props('vertical').classes('w-full') as tabs:
                            self.tabs = tabs

                            for key, value in self.settings_config.items():
                                setattr(self, key, ui.tab(value['title'], icon=value['icon']))
                            
                    with splitter.after:
                        with ui.tab_panels(self.tabs, value='Application').props('vertical').classes('w-full'):
                            with ui.tab_panel(self.application) as tab:
                                self.load_settings_to_ui('application')
                            with ui.tab_panel(self.viewer) as tab:
                                self.load_settings_to_ui('viewer')