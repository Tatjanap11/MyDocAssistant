"""Util function to load configuration from a YAML file"""
import yaml


def load_yaml_configuration(file_path: str) -> dict:
    """Load configuration from a YAML file.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        dict: The configuration as a dictionary.
    """
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
    return config
