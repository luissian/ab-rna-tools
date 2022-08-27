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


def write_seq_file(data, out_file, heading, seq_name, format):
    """write the sequence data dict to text file"""
    counter = 1
    with open(out_file, "w") as fh:
        if format == "summary":
            fh.write(heading + "\n")
            for key, value in data.items():
                fh.write(
                    seq_name + str(counter) + "\t" + key + "\t" + str(value) + "\n"
                )
                counter += 1
        elif format == "fasta":
            for key, value in data.items():
                fh.write("> " + seq_name + str(counter) + "_x" + str(value) + "\n")
                fh.write(key + "\n")
                counter += 1
        else:
            pass
    return


def write_unique_seq(data, out_file):
    """write the unique sequences to fasta file"""
    with open(out_file, "w") as fh:
        for key, value in data.items():
            fh.write("> " + value + "\n")
            fh.write(key + "\n")
    return


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


def prompt_message(msg):
    value = questionary.text(msg).unsafe_ask()
    return value
