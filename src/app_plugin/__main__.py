from nicegui import ui
from plugins.rst_editor import RSTEditorPlugin

editor_plugin = RSTEditorPlugin()
editor_plugin.render()

ui.run()
