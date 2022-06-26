#!/usr/bin/env python
import os
import sys
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
    def __init__(self, seq_file=None, out_folder=None, out_format=None):
        if seq_file is None:
            seq_file = s_rna_tools.utils.prompt_path(
                msg="Select the fasta file to group sequences"
            )
        self.seq_file = seq_file
        if not os.path.isfile(self.seq_file):
            log.error("fasta file %s does not exist ", self.seq_file)
            stderr.print(f"[red] fasta data file {self.seq_file} does not exist")
            sys.exit(1)
        if out_folder is None:
            out_folder = s_rna_tools.utils.prompt_path(
                msg="Select the folder to save results"
            )
        return
