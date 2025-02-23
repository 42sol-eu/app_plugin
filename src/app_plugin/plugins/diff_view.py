import os
import yaml
import shutil
import zipfile
from pathlib import Path
from nicegui import ui
from typing import List, Dict
import difflib

SNIPPET_DIR = Path("_snippets")
IMPORT_DIR = Path("_imported_snippets")

def export_snippets(language: str):
    """Exports snippets to a ZIP file."""
    export_file = Path("_snippets_export.zip")
    shutil.make_archive(export_file.stem, 'zip', SNIPPET_DIR, language)
    ui.download(export_file)

def import_snippets(file: Path):
    """Imports snippets from a ZIP file with overwrite handling."""
    IMPORT_DIR.mkdir(exist_ok=True)
    
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(IMPORT_DIR)

    imported_files = list(IMPORT_DIR.rglob("*.yaml"))
    if not imported_files:
        ui.notify("No valid YAML snippets found!", color="red")
        return

    def handle_snippet(yaml_file: Path):
        """Check if a snippet exists and ask for overwrite confirmation."""
        lang_folder = yaml_file.parent.name
        target_file = SNIPPET_DIR / lang_folder / yaml_file.name
        target_file.parent.mkdir(parents=True, exist_ok=True)

        if target_file.exists():
            with ui.dialog() as dlg:
                ui.label(f"Snippet '{yaml_file.name}' already exists. Do you want to overwrite or skip?")
                
                with ui.row():
                    ui.button("Show Diff", on_click=lambda: show_diff(yaml_file, target_file))
                    ui.button("Overwrite", on_click=lambda: overwrite_snippet(yaml_file, target_file, dlg))
                    ui.button("Skip", on_click=dlg.close)
            dlg.open()
        else:
            shutil.move(str(yaml_file), str(target_file))

    def show_diff(new_file: Path, old_file: Path):
        """Show the diff between the existing and the imported snippet."""
        with open(new_file, "r") as nf, open(old_file, "r") as of:
            new_content = nf.readlines()
            old_content = of.readlines()
        
        diff = difflib.unified_diff(old_content, new_content, fromfile="Existing", tofile="Imported", lineterm="")
        
        # Display diff content in a scrollable box
        diff_view = ui.column()
        diff_view.style("max-height: 300px; overflow-y: auto;")
        for line in diff:
            diff_view.label(line)

    def overwrite_snippet(src: Path, dest: Path, dlg):
        """Overwrite an existing snippet."""
        shutil.move(str(src), str(dest))
        ui.notify(f"Snippet {dest.name} overwritten!", color="green")
        dlg.close()

    for yaml_file in imported_files:
        handle_snippet(yaml_file)

    ui.notify("Import completed!", color="blue")

# Stepper for Export/Import
def snippet_share_stepper():
    """Stepper for exporting/importing snippets as ZIP files."""
    with ui.stepper() as stepper:
        with ui.step("Choose Action"):
            action = ui.select(["Export", "Import"], value="Export")

        with ui.step("Export Snippets", disabled=True).bind_visibility(action, "value", value="Export"):
            selected_lang = ui.select(["python", "yaml"], value="python")
            ui.button("Export as ZIP", on_click=lambda: export_snippets(selected_lang.value))

        with ui.step("Import Snippets", disabled=True).bind_visibility(action, "value", value="Import"):
            ui.label("Upload a ZIP file containing snippets:")
            ui.file_upload(on_change=lambda e: import_snippets(Path(e.files[0]['path'])))
    
        ui.button("Finish", on_click=stepper.reset)

# UI Integration
ui.label("Snippet Export & Import with Diff View")
snippet_share_stepper()
ui.run()
