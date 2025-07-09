# This module is responsible for loading the application's configuration.

import yaml
from pathlib import Path

# Define the path to the configuration file.
# Path(__file__).parent ensures that we look for the file in the same directory as this script.
CONFIG_FILE_PATH = Path(__file__).parent / "config.yaml"

def load_config() -> dict:
    """
    Loads the YAML configuration file and returns it as a Python dictionary.
    """
    with open(CONFIG_FILE_PATH, "r") as f:
        config = yaml.safe_load(f)
    return config

# Load the configuration once when the module is imported.
# This makes it available to the rest of the application as `config`.
config = load_config()
