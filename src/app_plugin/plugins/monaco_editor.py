from nicegui import ui
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
from pathlib import Path

class MonacoEditorPlugin:
    """Monaco-based Python code editor with log view."""

    AUTOSAVE_FILE = Path("monaco_autosave.json")
    DOCS_FOLDER = Path("./application_data/_docs")
    SETTINGS_FOLDER = Path("./application_data/_settings")

    def __init__(self):
        """Initialize the Monaco editor with default content."""
        self.content = self.load_autosave() or "# Hello from Monaco Editor Plugin\nprint('Hello, World!')"
        self.editor = None
        self.log_view = None
        self._setup_autosave_watcher()

    def render(self) -> None:
        """Render the editor and log view."""
        with ui.splitter().classes("w-full h-full").props("horizontal") as h_splitter:
            
            # Top: Monaco Code Editor
            with h_splitter.before:
                with ui.row().classes("p-2").style('color: active;'):
                    ui.icon("code").classes("text-xl margin-5")
                    ui.label("Monaco Editor").classes("text-xl")
                self.editor = ui.element('div').classes("w-full h-full").style('height: 400px;')
                self.initialize_monaco_editor()

            # Bottom: Log View
            with h_splitter.after:
                with ui.row().classes("p-2").style('color: active;'):
                    ui.icon("list_alt").classes("text-xl margin-5")
                    ui.label("Log View").classes("text-xl")
                self.log_view = ui.textarea().classes("w-full h-full")

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
        if os.path.exists(self.DOCS_FOLDER / self.AUTOSAVE_FILE):
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