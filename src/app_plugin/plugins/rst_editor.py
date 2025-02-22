from docutils.core import publish_parts
from docutils.utils import SystemMessage
from nicegui import ui
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
from pathlib import Path

class RSTEditorPlugin:
    """Pure RST editor with live preview, autosave, and linting."""

    AUTOSAVE_FILE = Path("rst_autosave.json")
    STYLE_FILE = Path("custom_styles.css")
    DOCS_FOLDER = Path("./application_data/_docs")
    SETTINGS_FOLDER = Path("./application_data/_settings")
    
    def __init__(self):
        """Initialize the RST editor with default content."""
        self.content = self.load_autosave() or "Hello from RST Plugin\n======================="
        self.preview = None
        self.editor = None
        self.error_box = None
        self._setup_autosave_watcher()
        self.error_text = None 

    def render(self) -> None:
        """Render the editor and live preview."""
        with ui.splitter().classes("w-full h-full") as v_splitter:
            
            # Left: RST Code Editor
            with v_splitter.before:
                with ui.row().classes("w-full h-full").style('color: active;'):
                    ui.icon("edit").classes("text-xl margin-5")
                    ui.label("Edit").classes("text-xl")
                self.editor = ui.codemirror(
                    language="rst",
                    value=self.content,
                    on_change=self.update_preview
                ).classes("w-full h-full")

            # Right: Live Preview
            with v_splitter.after:
                
                with ui.splitter().classes("w-full h-full").props("horizontal") as h_splitter:
                    with h_splitter.before:
                        with ui.row().classes("p-2").style('color: active;'):
                            ui.icon("visibility").classes("text-xl margin-5")
                            ui.label("Live Preview:").classes('text-xl')
                        self.preview = ui.html(self._convert_rst(self.content))
                    with h_splitter.after:
                        ui.space()
                        with ui.row().classes("p-2").style('color: active;'):
                            ui.icon("rule").classes("text-xl margin-5")
                            ui.label("Linting:").classes("text-xl")
                        if self.error_text:
                            self.error_box = ui.markdown(f"❌ {self.error_text}").classes("w-full h-full")
                        self.error_box = ui.markdown("").classes("w-full h-full")  # Display linting errors

    def _convert_rst(self, rst_text: str) -> str:
        """Convert RST to HTML for live preview and linting."""
        try:
            parts = publish_parts(source=rst_text, writer_name='html')
            html_body = parts['html_body']
            head = '<head><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">'
            custom_styles = open(self.SETTINGS_FOLDER / self.STYLE_FILE, 'r').read()
            head += f'<style>{custom_styles}</style>'
            head += f'</head>'
            return head + html_body
        except SystemMessage as e:
            self.error_text = f"<p style='color: red;'>RST Error: {e}</p>"
            return  custom_styles + "<html><body>Error</body></html>"

    def update_preview(self) -> None:
        """Update the preview and linting when text changes."""
        self.content = self.editor.value
        self.preview.set_content(self._convert_rst(self.content))
        self.lint_rst(self.content)
        self.save_autosave(self.content)

    def lint_rst(self, rst_text: str) -> None:
        """Check for errors in RST syntax and show messages."""
        try:
            publish_parts(rst_text, writer_name='html')
            self.error_box.set_content("✅ No syntax errors!")
        except SystemMessage as e:
            self.error_box.set_content(f"❌ RST Error: {e}")

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
                if event.src_path == RSTEditorPlugin.AUTOSAVE_FILE:
                    with open(event.src_path, "r") as f:
                        data = json.load(f)
                        new_content = data.get("content", "")
                        self.content = new_content
                        self.editor.set_content(new_content)
                        self.preview.set_content(self._convert_rst(new_content))

        observer = Observer()
        event_handler = AutoSaveHandler()
        observer.schedule(event_handler, path=".", recursive=False)
        thread = threading.Thread(target=observer.start, daemon=True)
        thread.start()
