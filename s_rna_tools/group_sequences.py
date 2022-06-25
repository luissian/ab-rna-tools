#!/usr/bin/env python
import logging
import rich.console
import s_rna_tools.utils

log = logging.getLogger(__name__)
stderr = rich.console.Console(
    stderr=True,
    style="dim",
    highlight=False,
    force_terminal=s_rna_tools.utils.rich_force_colors(),
)


class GroupSequences:
    def __init__(self, file=None, out_folder=None):
        return
