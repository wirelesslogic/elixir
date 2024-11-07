import os
from os import path
from os.path import (
    isdir,
    isfile,
)
import re
import yaml
from easydict import EasyDict

from . import log


# Constructor for including files
def include_constructor(loader, node):
    """Include file referenced at node."""
    filename = path.join(path.dirname(loader.name), loader.construct_scalar(node))
    with open(filename, "r") as f:
        return yaml.load(f, Loader=CustomLoader)


# Constructor for environment variable substitution
def env_constructor(loader, node):
    # Regex pattern for the environment variable substitution
    pattern = re.compile(r".*?\$\{([^}]+)\}.*?")

    value = loader.construct_scalar(node)
    matches = pattern.findall(value)

    for match in matches:
        env_var, default_value = re.match(r"(\w+)(?::(.*))?", match).groups()
        env_value = os.environ.get(env_var, default_value or "")
        value = value.replace(f"${{{match}}}", env_value)

    return value


def load_module_configs(directory, config):
    """
    Load config.yml files from direct subdirectories of the given directory
    and merges them under their respective module names in the main config.
    """
    log.warn(directory)
    for module_name in os.listdir(directory):
        module_path = path.join(directory, module_name)

        # Check if it's a directory
        if isdir(module_path):
            config_file_path = path.join(module_path, "config.yml")

            config[module_name] = {}

            # Check if config.yml exists in this module's directory
            if isfile(config_file_path):
                load_config_into(config, module_name, config_file_path)

            config_dir = path.join(module_path, "config")
            if isdir(config_dir):
                recursive_load(config[module_name], config_dir)

    return config


def load_config_into(sub_config, key, file):
    # Load and process the YAML file
    with open(file, "r") as conf_data:
        loaded_yaml = yaml.load(conf_data, Loader=CustomLoader)

        if loaded_yaml is not None:
            sub_config[key] = loaded_yaml


def get_file_type(input_path):
    _, extension = path.splitext(input_path)
    return extension.lower()


def get_base_name(input_path):
    filename, _ = path.splitext(path.basename(input_path))
    return filename.lower()


def recursive_load(sub_config, directory, parent_key=None):
    for config_path in os.listdir(directory):
        full_sub_path = path.join(directory, config_path)
        key = get_base_name(full_sub_path)

        target_config = sub_config

        if parent_key is not None:
            sub_config[parent_key] = {}
            target_config = sub_config[parent_key]

        # Check is sub_path contains file or directory.
        if isfile(full_sub_path) and get_file_type(full_sub_path) == ".yml":
            # Load config into key
            load_config_into(target_config, key, full_sub_path)
        # if file load into big config, use filename (without .yml) as key
        elif isdir(full_sub_path):
            # Recursively load configs from directory
            recursive_load(target_config, full_sub_path, key)
        else:
            # log.warn(f"unexpected file {config_path}")
            pass


class CustomLoader(yaml.SafeLoader):
    pass


CustomLoader.add_constructor("!include", include_constructor)
CustomLoader.add_constructor("!ENV", env_constructor)


def load_config(
    alternative_config_path: str | None = None,
    sub_configs: list[str] | None = None,
):
    try:
        # Load configuration file and substitute environment variables
        server = os.environ.get("SERVER", "development").lower()

        # Get root directory
        root_dir = path.dirname(path.dirname(path.abspath(__file__)))

        # Determine if alternative config is used
        config_path = (
            "config/config.yml"
            if alternative_config_path is None
            else alternative_config_path
        )

        # Get absolute path to the main config file
        config_file_path = path.join(root_dir, config_path)

        # Load and process the YAML file
        with open(config_file_path, "r") as conf_data:
            config_dict = yaml.load(conf_data, Loader=CustomLoader)[server]

        # Add the root directory to the config dict
        config_dict["root_dir"] = root_dir

        if sub_configs is None:
            sub_configs = ["components", "plugins"]

        # Load sub configs from components and plugins and merge with the main config
        for sub_dir in sub_configs:
            config_dict = load_module_configs(path.join(root_dir, sub_dir), config_dict)
    except Exception as e:
        print(
            "Unable to load config file. Make sure the `SERVER` environmental variable "
            "is set and that its value is also available in the config/config.yml file."
        )
        print(f"Exception: {e}")
        config_dict = {}

    return EasyDict(**config_dict)
