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
        self.cmd = []
        self.show_text = True

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

    def toggle_text(self) -> None:
        if self.show_text:
            for cmd in self.cmd:
                cmd.text = ""
            drawer_width = "w-4"
            self.left_drawer.props('mini dense')
        else:
            self.cmd[0].text = "Navigation"
            self.cmd[1].text = "RST Editor"
            self.cmd[2].text = "Code Editor"
            self.cmd[3].text = "Minifiy"
            self.cmd[4].text = "Close"
            drawer_width = "w-12"
            self.left_drawer.props('basic')
            
        self.show_text = not self.show_text
        self.left_drawer.style(f"width: {drawer_width}")
        self.left_drawer.update()

    def render(self) -> None:
        """Render the main application with a navigation drawer."""
        with ui.left_drawer(top_corner=True).classes("item stretch") as left_drawer:
            self.cmd.append(ui.label("Navigation").classes("p-4"))
            self.cmd.append(ui.button("RST Editor", icon="edit", on_click=self.show_rst_editor).classes("w-full"))
            self.cmd.append(ui.button("Code Editor", icon="code", on_click=self.show_monaco_editor).classes("w-full"))
            self.cmd.append(ui.button("Minifiy", icon="minimize", on_click=self.toggle_text).classes("w-full"))
            self.button3 = self.cmd[-1]
            self.cmd.append(ui.button("Close", icon="close").classes("w-full"))
            self.button2 = self.cmd[-1]
        self.left_drawer = left_drawer
        self.toggle_text()

        with ui.header().classes("w-full p-4 bg-gray-800 text-white"):
            self.button1 = ui.button(icon="apps").classes("margin-5")
            ui.label("Plugin powered application").classes("text-2xl")

        with ui.splitter().classes("w-full h-full") as main_splitter:
            with main_splitter.before:
                self.content_area = ui.column().classes("w-full h-full")
            with main_splitter.after:
                self._view_area = ui.card().classes("w-full h-full")

        # Show the default view
        self.show_rst_editor()

        # Set the on_click event handlers for the buttons
        self.button1.on_click(self.toggle_drawer)
        self.button2.on_click(self.toggle_drawer)
        self.rst_editor_plugin.register_view(self._view_area)

if __name__ in {"__main__", "__mp_main__"}:
    app = MainApp()
    app.render()
    ui.run()