# -*- coding:utf-8 -*-
from __future__ import division
from __future__ import print_function

import os
import re
import yaml

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
LOG_PATH = os.path.join(ROOT_PATH, "logs/")
BOOTSTRAP_CONFIG_FILE = os.path.join(ROOT_PATH, "bootstrap.yml")
LOGGING_CONFIG_FILE = os.path.join(ROOT_PATH, "logging.yml")
DEFAULT_CONFIG_FILE = os.path.join(ROOT_PATH, "application.yml")
DEFAULT_MESSAGE_FILE = os.path.join(ROOT_PATH, "messages.properties")

__all__ = [
    "ROOT_PATH",
    "LOG_PATH",
    "BOOTSTRAP_CONFIG_FILE",
    "LOGGING_CONFIG_FILE",
    "DEFAULT_CONFIG_FILE",
    "DEFAULT_MESSAGE_FILE"
]

path_matcher = re.compile(r'.*\$\{([^}^{]+)\}.*')


def path_constructor(loader, node):
    return os.path.expandvars(node.value)


class EnvVarLoader(yaml.SafeLoader):
    pass


EnvVarLoader.add_implicit_resolver('!path', path_matcher, None)
EnvVarLoader.add_constructor('!path', path_constructor)
