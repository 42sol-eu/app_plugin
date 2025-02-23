import os
import yaml
from nicegui import ui, app
from typing import List, Dict

# Directory for storing snippets
SNIPPET_DIR = "_snippets"

class MonacoEditor(ui.element):
    """A NiceGUI Monaco Code Editor that loads snippets from YAML files."""

    def __init__(self, language: str = "python", theme: str = "vs-dark", default_value: str = ""):
        super().__init__("div")
        self.language = language
        self.theme = theme
        self.default_value = default_value
        self.snippets = self._load_snippets(language)

        app.on_startup(self._setup_editor)
        app.on_startup(self._setup_snippets)

    def _load_snippets(self, language: str) -> List[Dict]:
        """Load snippets from _snippets/{language}/ folder."""
        snippet_dir = os.path.join(SNIPPET_DIR, language)
        if not os.path.exists(snippet_dir):
            os.makedirs(snippet_dir)
        snippets = []
        if os.path.exists(snippet_dir):
            for filename in os.listdir(snippet_dir):
                filepath = os.path.join(snippet_dir, filename)
                if filename.endswith(".yaml"):
                    with open(filepath, "r", encoding="utf-8") as file:
                        try:
                            snippet = yaml.safe_load(file)
                            snippets.append(snippet)
                        except yaml.YAMLError as e:
                            print(f"Error loading snippet {filename}: {e}")
        return snippets

    def _setup_editor(self) -> None:
        """Injects JavaScript to initialize Monaco."""
        ui.run_javascript(f"""
            if (!window.monaco) {{
                var script = document.createElement('script');
                script.src = 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs/loader.js';
                script.onload = function() {{
                    require.config({{ paths: {{ 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' }} }});
                    require(['vs/editor/editor.main'], function() {{
                        window.monaco = monaco;
                    }});
                }};
                document.head.appendChild(script);
            }}

            var editorContainer = document.getElementById('{self.id}');
            var monacoInterval = setInterval(function() {{
                if (window.monaco) {{
                    clearInterval(monacoInterval);
                    window.monaco_editor = monaco.editor.create(editorContainer, {{
                        value: `{self.default_value.replace('`', '\\`')}`,
                        language: '{self.language}',
                        theme: '{self.theme}'
                    }});
                }}
            }}, 100);
        """)

    def _setup_snippets(self) -> None:
        """Registers snippets in Monaco."""
        snippets_js = ", ".join([
            f"""{{ label: "{s['label']}", kind: monaco.languages.CompletionItemKind.Snippet, 
                  insertText: `{s['insertText']}`, detail: "{s['detail']}" }}""" 
            for s in self.snippets
        ])

        ui.run_javascript(f"""
            var snippetInterval = setInterval(function() {{
                if (window.monaco) {{
                    clearInterval(snippetInterval);
                    monaco.languages.registerCompletionItemProvider('{self.language}', {{
                        provideCompletionItems: function() {{
                            return {{ suggestions: [{snippets_js}] }};
                        }}
                    }});
                }}
            }}, 100);
        """)

    def reload_snippets(self) -> None:
        """Reloads snippets from YAML files."""
        self.snippets = self._load_snippets(self.language)
        self._setup_snippets()

    def set_language(self, language: str) -> None:
        """Change editor language and reload snippets."""
        self.language = language
        self.reload_snippets()
        ui.run_javascript(f"monaco.editor.setModelLanguage(window.monaco_editor.getModel(), '{language}')")

# Snippet Manager
def snippet_manager():
    """Manage YAML snippets (Create, Edit, Delete)."""

    selected_language = ui.select(["python", "yaml"], label="Select Language").bind_value(lambda: "python")

    def load_snippets():
        print(">>>>>>>>>>>>", selected_language.value)
        if not selected_language.value:
            selected_language.value = "python"
        snippet_dir = os.path.join(SNIPPET_DIR, selected_language.value)
        return [
            file for file in os.listdir(snippet_dir) if file.endswith(".yaml")
        ] if os.path.exists(snippet_dir) else []

    snippet_list = ui.select(load_snippets(), label="Available Snippets")

    editor_label = ui.input("Label")
    editor_insert_text = ui.textarea("Insert Text")
    editor_detail = ui.input("Detail")

    def load_snippet():
        """Load selected snippet for editing."""
        if snippet_list.value:
            file_path = os.path.join(SNIPPET_DIR, selected_language.value, snippet_list.value)
            with open(file_path, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
                editor_label.value = data["label"]
                editor_insert_text.value = data["insertText"]
                editor_detail.value = data["detail"]

    ui.button("Load Snippet", on_click=load_snippet)

    def save_snippet():
        """Save edited snippet to YAML file."""
        if editor_label.value and editor_insert_text.value:
            file_path = os.path.join(SNIPPET_DIR, selected_language.value, f"{editor_label.value}.yaml")
            data = {
                "label": editor_label.value,
                "insertText": editor_insert_text.value,
                "detail": editor_detail.value
            }
            with open(file_path, "w", encoding="utf-8") as file:
                yaml.safe_dump(data, file)
            snippet_list.options = load_snippets()
            editor.reload_snippets()

    ui.button("Save Snippet", on_click=save_snippet)

    def delete_snippet():
        """Delete selected snippet."""
        if snippet_list.value:
            file_path = os.path.join(SNIPPET_DIR, selected_language.value, snippet_list.value)
            os.remove(file_path)
            snippet_list.options = load_snippets()
            editor.reload_snippets()

    ui.button("Delete Snippet", on_click=delete_snippet, color="red")

# Main UI
ui.label("Monaco Editor with YAML Snippet Editor")

editor = MonacoEditor(language="python", theme="vs-dark", default_value="")

# Language Switch
ui.button("Switch to YAML", on_click=lambda: editor.set_language("yaml"))
ui.button("Switch to Python", on_click=lambda: editor.set_language("python"))

# Snippet Editor Section
ui.separator()
ui.label("Snippet Editor")
snippet_manager()

ui.run()
