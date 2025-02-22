from nicegui import ui
from pathlib import Path
from plugins.rst_editor import RSTEditorPlugin
from plugins.monaco_editor import MonacoEditorPlugin

class MainApp:
    def __init__(self):
        self.rst_editor_plugin = RSTEditorPlugin()
        self.monaco_editor_plugin = MonacoEditorPlugin()
        self.current_view = None
        self.left_drawer = None

    def show_rst_editor(self) -> None:
        """Show the RST editor view."""
        self.content_area.clear()
        with self.content_area:
            self.rst_editor_plugin.render()
        self.current_view = "rst_editor"

    def show_monaco_editor(self) -> None:
        """Show the Monaco editor view."""
        self.content_area.clear()
        with self.content_area:
            self.monaco_editor_plugin.render()
        self.current_view = "monaco_editor"

    def toggle_drawer(self) -> None:
        if self.left_drawer:
            self.left_drawer.toggle()
        print("Drawer toggled")
        
    def render(self) -> None:
        """Render the main application with a navigation drawer."""
        with ui.left_drawer(top_corner=True).classes("w-32") as left_drawer:
            ui.label("Navigation").classes("p-4")
            ui.button("RST Editor", icon="edit", on_click=self.show_rst_editor).classes("w-full")
            ui.button("Editor", icon="code", on_click=self.show_monaco_editor).classes("w-full")
            self.button2 = ui.button(icon="close").classes("w-full")
        self.left_drawer = left_drawer
        with ui.header().classes("w-full p-4 bg-gray-800 text-white"):
            self.button1 = ui.button(icon="apps").classes("margin-5")
            ui.label("Plugin powered application").classes("text-2xl")

        with ui.splitter().classes("w-full h-full") as main_splitter:
            with main_splitter.before:
                self.content_area = ui.column().classes("w-full h-full")
            with main_splitter.after:
                self.markdown_area = ui.markdown('# Information').classes("w-full h-full")

        # Show the default view
        self.show_rst_editor()
        
        self.button1.on_click = self.toggle_drawer
        self.button2.on_click = self.toggle_drawer
        

if __name__ in {"__main__", "__mp_main__"}:
    app = MainApp()
    app.render()
    ui.run()