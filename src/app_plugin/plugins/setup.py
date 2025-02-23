# filepath: /Users/ahaeberle/Desktop/42/3_Areas/42sol/app_plugin/setup.py
from setuptools import setup, find_packages

setup(
    name='app_plugin',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'app_plugin.plugins': [
            'monaco_editor = app_plugin.plugins.monaco_editor:MonacoEditorPlugin',
            'rst_editor = app_plugin.plugins.rst_editor:RSTEditorPlugin',
            # Add other plugins here
        ],
    },
)