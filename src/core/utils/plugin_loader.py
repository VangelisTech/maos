import importlib

def load_plugin(plugin_name):
    return importlib.import_module(f"src.plugins.{plugin_name}")