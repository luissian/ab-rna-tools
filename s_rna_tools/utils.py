#!/usr/bin/env python
"""
Common utility function for relecov_tools package.
"""
import os
import logging
from rich.console import Console
import questionary


log = logging.getLogger(__name__)


def file_exists(file_to_check):
    """
    Input:
        file_to_check   # file name to check if exists
    Return:
        True if exists
    """
    if os.path.isfile(file_to_check):
        return True
    return False


def rich_force_colors():
    """
    Check if any environment variables are set to force Rich to use coloured output
    """
    if (
        os.getenv("GITHUB_ACTIONS")
        or os.getenv("FORCE_COLOR")
        or os.getenv("PY_COLORS")
    ):
        return True
    return None


stderr = Console(
    stderr=True, style="dim", highlight=False, force_terminal=rich_force_colors()
)


def prompt_tmp_dir_path():
    stderr.print("Temporal directory destination to execute service")
    source = questionary.path("Source path").unsafe_ask()
    return source


def prompt_selection(msg, choices):
    selection = questionary.select(msg, choices=choices).unsafe_ask()
    return selection


def prompt_path(msg):
    source = questionary.path(msg).unsafe_ask()
    return source
