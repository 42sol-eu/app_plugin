"""
help page

file:           src/app_plugin/help_page.py
file-id:        f9f740a7-c961-49d5-b5c8-d1e53537397a
project:        app_plugin
project:        app_plugin
project-id:     dfd94fa7-1f2f-4784-901f-dcba7ffc5ef9
author:         felix@42sol.eu

description: |
    This module implements the help page GUI in the `right_drawer`  for `app_plugin`.
"""

# [Imports, global]
from nicegui import ui, app
from pathlib import Path
from docutils.core import publish_parts
from docutils.utils import SystemMessage


# [Imports from app_plugin]
from . import icon
from . import theme
from . import message


# [Code]
class HelpPage:

    SETTINGS_FOLDER = app.settings['_settings']
    STYLE_FILE = SETTINGS_FOLDER / "custom_styles.css"

    def load_settings_to_ui(self, section: str) -> None:
        pass

    def __init__(self) -> None:
        """The page is created as soon as the class is instantiated."""
        with ui.card().classes('w-full h-full') as card:
            content = self._load_docs('index')
            self.html_element = ui.html(self._convert_rst(content)) \
                .classes('w-full h-full')

    def clear(self):
        self.html_element.set_content('')  # Clear the content of the html element
    
    def _load_docs(self, doc_name: str) -> str:
        """Load the content of a documentation file."""
        doc_file = app.settings['_docs']  / f"{doc_name}.rst"
        if doc_file.exists():
            with open(doc_file, 'r') as f:
                return f.read()
        else:
            return f"Documentation file '{doc_name}.rst' not found."
    
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

    def set_content(self, content: str, title : str = 'index') -> None:
        """Set the content of the help page.
        Args:
            content (str): The content of the help page.
            title (str): The title of the help page.
        
        """
        html_content = self._convert_rst(content)
        with open( app.settings['_docs'] / f'{title}.html', 'w') as f:
            f.write(html_content)
        self.html_element.set_content(html_content)  # Update the content of the html element
        self.html_element.update()
