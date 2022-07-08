#!/usr/bin/env python
import os
import sys
import logging
import rich.console
from Bio import SeqIO
import glob
import s_rna_tools.utils
from s_rna_tools.rna_blast import RnaBlast

log = logging.getLogger(__name__)
stderr = rich.console.Console(
    stderr=True,
    style="dim",
    highlight=False,
    force_terminal=s_rna_tools.utils.rich_force_colors(),
)


class FindUnknown:
    def __init__(self, in_file=None, m_file=None, out_folder=None):
        if in_file is None:
            in_file = s_rna_tools.utils.prompt_path(
                msg="Select the fasta file with the sequences"
            )
        self.in_file = in_file
        if not os.path.isfile(self.in_file):
            log.error("fasta file %s does not exist ", self.in_file)
            stderr.print(f"[red] fasta data file {self.in_file} does not exist")
            sys.exit(1)
        if m_file is None:
            m_file = s_rna_tools.utils.prompt_path(
                msg="Select the file to match against the sequences"
            )
        self.m_file = m_file
        if not os.path.isfile(self.m_file):
            log.error("matching file %s does not exist ", self.m_file)
            stderr.print(f"[red] matching file {self.m_file} does not exist")
            sys.exit(1)
        if out_folder is None:
            out_folder = s_rna_tools.utils.prompt_path(
                msg="Select the folder to save results"
            )
        self.out_folder = out_folder

    def find_blast_match(self):
        return RnaBlast(self.in_file, "blastn-short", 90, 0.05, self.out_folder)


    def get_unknow_sequences(self):
        blast_db_obj= self.find_blast_match()
