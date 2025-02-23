

#!/usr/bin/env python3
# [Includes]
import api_router
import settings_page
import main_page
import theme

from nicegui import app, ui


# Example 1: use a custom page decorator directly and putting the content creation into a separate function
@ui.page('/')
def index_page() -> None:
    with theme.frame('Homepage'):
        main_page.content()



# Example 3: use a class to move the whole page creation into a separate file
settings_page.SettingsPage()

# Example 4: use APIRouter as described in https://nicegui.io/documentation/page#modularize_with_apirouter
app.include_router(api_router.router)

ui.run(title='App with Plugins')

if 0:
    # TODO: integrate the RSTEditorPlugin into the app
    from nicegui import ui
    from plugins.rst_editor import RSTEditorPlugin

    editor_plugin = RSTEditorPlugin()
    editor_plugin.render()

    ui.run()
