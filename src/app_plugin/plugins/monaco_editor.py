"""
Plugin Code Editor

file:         src/app_plugin/plugins/monaco_editor.py
file-id:      5539b2c3-788d-4566-a204-1d711a035108
project:      app_plugin
project-id:   dfd94fa7-1f2f-4784-901f-dcba7ffc5ef9
author:       felix@42sol.eu

description: |
    This module implements the "Monaco Code Editor" plugin  for `app_plugin`.
"""
# [Imports, global]
from nicegui import ui, app
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
from pathlib import Path

# [Imports from app_plugin]
from ..plugin_view import PluginView
from .. import theme
from ..message import message

# [Class::PluginView]
class MonacoEditorPlugin(PluginView):
    """Monaco-based Python code editor with log view."""

    AUTOSAVE_FILE = Path("monaco_autosave.json")
    DOCS_FOLDER = app.settings['_docs']
    SETTINGS_FOLDER = app.settings['_settings']
    name = "Monaco Editor"

    def __init__(self, loaded_plugins):
        """Initialize the Monaco editor with default content."""
        self.content = self.load_autosave() or "# Hello from Monaco Editor Plugin\nprint('Hello, World!')"
        self.editor = None
        self.log_view = None
        self._setup_autosave_watcher()
        self.create_page(loaded_plugins)

    def create_page(self, loaded_plugins) -> None:
        @ui.page('/monaco_editor')
        def page() -> None:
            with theme.frame('Monaco Editor', loaded_plugins):
                """Render the editor and log view."""
                with ui.splitter().classes("w-full h-full").props("horizontal") as h_splitter:
                    with h_splitter.before:
                        with ui.row().classes("p-2").style('color: active;'):
                            ui.icon("code").classes("text-xl margin-5")
                            ui.label("Monaco Editor").classes("text-xl")
                        self.editor = ui.element('div').classes("w-full h-full").style('height: 400px;')
                        self.initialize_monaco_editor()

                    with h_splitter.after:
                        with ui.row().classes("p-2").style('color: active;'):
                            ui.icon("list_alt").classes("text-xl margin-5")
                            ui.label("Log View").classes("text-xl")
                        self.log_view = ui.textarea().classes("w-full h-full")

    def register_view(self, view_area) -> None:
        """Register the view area for rendering the output."""
        self.view_area = None

    def initialize_monaco_editor(self) -> None:
        """Initialize the Monaco editor within the custom element."""
        ui.run_javascript(f"""
            require.config({{ paths: {{ 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.21.2/min/vs' }} }});
            require(['vs/editor/editor.main'], function() {{
                window.editor = monaco.editor.create(document.querySelector('#{self.editor.id}'), {{
                    value: `{self.content}`,
                    language: 'python'
                }});
                window.editor.onDidChangeModelContent(function() {{
                    const content = window.editor.getValue();
                    window.pywebview.api.update_log_view(content);
                }});
            }});
        """)

    def update_log_view(self, content: str) -> None:
        """Update the log view when text changes."""
        self.content = content
        self.log_view.set_value(f"Code updated:\n{self.content}")
        self.save_autosave(self.content)

    def save_autosave(self, content: str) -> None:
        """Save the editor content to a file."""
        with open(self.AUTOSAVE_FILE, "w") as f:
            json.dump({"content": content}, f)

    def load_autosave(self) -> str:
        """Load autosaved content, if available."""
        if os.path.exists(app.settings['_docs']  / self.AUTOSAVE_FILE):
            with open(self.AUTOSAVE_FILE, "r") as f:
                data = json.load(f)
                return data.get("content", "")
        return None

    def _setup_autosave_watcher(self) -> None:
        """Watch for autosave file changes to sync content."""
        class AutoSaveHandler(FileSystemEventHandler):
            def on_modified(self, event):
                if event.src_path == MonacoEditorPlugin.AUTOSAVE_FILE:
                    with open(event.src_path, "r") as f:
                        data = json.load(f)
                        new_content = data.get("content", "")
                        self.content = new_content
                        self.editor.set_value(new_content)
                        self.log_view.set_value(f"Code updated:\n{new_content}")

        observer = Observer()
        event_handler = AutoSaveHandler()
        observer.schedule(event_handler, path=".", recursive=False)
        thread = threading.Thread(target=observer.start, daemon=True)
        thread.start()