# plugin_view.py
from nicegui.element import Element
from stevedore.extension import ExtensionManager
from nicegui import ui
import logging

logging.basicConfig(level=logging.INFO)

class PluginView(Element):
    """NiceGUI element that dynamically loads and renders plugins."""

    def __init__(self, namespace: str) -> None:
        """Initialize PluginView with a Stevedore namespace."""
        super().__init__('div')
        self.namespace = namespace
        self.plugins = {}
        self.current_plugin = None
        self.load_plugins()

        with self:
            self.plugin_container = ui.column()

    def load_plugins(self) -> None:
        """Discover and load available plugins."""
        try:
            mgr = ExtensionManager(
                namespace=self.namespace,
                invoke_on_load=True,
            )
            for ext in mgr:
                self.plugins[ext.name] = ext.obj
                logging.info(f"Loaded plugin: {ext.name}")
        except Exception as e:
            logging.error(f"Error loading plugins: {e}")

    def render_plugin(self, plugin_name: str) -> None:
        """Render a selected plugin."""
        self.plugin_container.clear()
        if plugin_name in self.plugins:
            self.current_plugin = self.plugins[plugin_name]
            with self.plugin_container:
                self.current_plugin.render()
