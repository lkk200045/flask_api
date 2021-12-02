# -*- coding: utf-8 -*-

import os
import re
from datetime import datetime
from subprocess import Popen
from setuptools import Command

VERSION_RE = re.compile('^__version__\s*=\s*"(.*?)"$', re.MULTILINE)


def current_version_from_version_file(version_file):
    """
    Extract the current version from `version_file`.

    Args:
        version_file (str): A path to a Python file with a version specifier

    Returns:
        The current version specifier
    """
    with open(version_file, "r") as infile:
        contents = infile.read()

    m = VERSION_RE.search(contents)
    try:
        version = m.group(1)
    except:
        raise IOError(
            "Unable to find __version__ variable defined in {}".format(version_file))

    return version


def update_version_file(filename, new_version):
    """
    Update the version file at the path specified by `filename`.

    Args:
        filename (str): The path to the version file
        new_version (str): The new version specifier

    Returns:
        The new version specifier
    """

    with open(filename, "r") as infile:
        contents = infile.read()

    contents = VERSION_RE.sub('__version__ = "{}"'.format(new_version), contents)

    with open(filename, "w") as outfile:
        outfile.write(contents)

    return new_version

def bump_patch_version(version):
    """
    Increment the patch version.

    Args:
        version (str): The version to bump
    """
    parts = [int(x) for x in version.split('.')]
    parts[2] += 1

    return '.'.join([str(x) for x in parts])

def build():
    """
    Build a wheel distribution.
    """
    # code = Popen(["python", "setup.py", "clean", "bdist_wheel"]).wait()
    code = Popen(["python", "setup.py", "clean"]).wait()
    if code:
        raise RuntimeError("Error building wheel")

    code = Popen(["python", "setup.py", "sdist"]).wait()
    if code:
        raise RuntimeError("Error building wheel")


def publish_to_nexus():
    """
    Publish the distribution to nexus.
    """
    code = Popen(["twine", "upload", "-r", "nexus", "dist/*"]).wait()
    if code:
        raise RuntimeError("Error publishing to nexus")


class SnapshotCommand(Command):
    user_options = [
        ("version=", "v", "new version number")
    ]

    def initialize_options(self):
        self.project_name = None
        self.old_version = None  # the previous version
        self.version = None  # the new version
        self.version_file = None  # the version file

    def finalize_options(self):
        if not os.path.exists(self.version_file):
            raise IOError(
                "Specified version file ({}) does not exist".format(self.version_file))

        self.old_version = current_version_from_version_file(self.version_file)
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        new_version = "{}.snapshot.{}".format(bump_patch_version(self.old_version), date)
        self.version = self.version or new_version

    def run(self):
        print(self.project_name)
        update_version_file(self.version_file, self.version)
        build()
        publish_to_nexus()
        update_version_file(self.version_file, self.old_version)
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')
