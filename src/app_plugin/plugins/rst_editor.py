from nicegui import ui
from docutils.core import publish_parts
from docutils.utils import SystemMessage
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
from pathlib import Path

from ..plugin_view import PluginView
from .. import theme
from ..message import message

class RSTEditorPlugin(PluginView):
    """Pure RST editor with live preview, autosave, and linting."""

    AUTOSAVE_FILE = Path("rst_autosave.json")
    STYLE_FILE = Path("./application_data/_settings/custom_styles.css")
    DOCS_FOLDER = Path("./application_data/_docs")
    SETTINGS_FOLDER = Path("./application_data/_settings")
    name = "RST Editor"
    
    def __init__(self, loaded_plugins):
        """Initialize the RST editor with default content."""
        self.content = self.load_autosave() or "Hello from RST Plugin\n======================="
        self.editor = None
        self.error_box = None
        self._setup_autosave_watcher()
        self.create_page(loaded_plugins)

    def create_page(self, loaded_plugins) -> None:
        @ui.page('/rst_editor')
        def page() -> None:
            """Render the editor and linting."""
            with theme.frame('RST Editor', loaded_plugins):
                with ui.splitter().classes("w-full h-full").props("horizontal") as h_splitter:
                    with h_splitter.before:
                        # Left: RST Code Editor
                        ui.label("Edit")
                        self.editor = ui.codemirror(
                            language="rst",
                            value=self.content,
                            on_change=self.update_preview
                        )
                    with h_splitter.after:
                        ui.label("Linting:")
                        self.error_box = ui.markdown("")  # Display linting errors
            self.view_area = theme.view_area
            
    def register_view(self, view_area) -> None:
        """Register the view area for rendering the output."""
        self.view_area = view_area

    def _convert_rst(self, rst_text: str) -> str:
        """Convert RST to HTML for live preview and linting."""
        try:
            parts = publish_parts(source=rst_text, writer_name='html')
            head = '<head><style>'
            head += self.STYLE_FILE.open('r').read() if self.STYLE_FILE.exists() else ''
            head += '</style></head>'
            rst_content = head + parts['html_body']
            return rst_content
        except SystemMessage as e:
            return f"<p style='color: red;'>RST Error: {e}</p>"

    def update_preview(self) -> None:
        """Update the preview and linting when text changes."""
        self.content = self.editor.value
        self.lint_rst(self.content)
        self.save_autosave(self.content)
        if self.view_area:
            print(f"Updating view area")
            self.view_area.set_content(self._convert_rst(self.content))

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
