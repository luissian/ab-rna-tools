#!/usr/bin/env python
import os
import sys
import logging
import rich.console
from Bio import SeqIO
import glob
import s_rna_tools.utils

log = logging.getLogger(__name__)
stderr = rich.console.Console(
    stderr=True,
    style="dim",
    highlight=False,
    force_terminal=s_rna_tools.utils.rich_force_colors(),
)


class CreateUnique:
    def __init__(self, folder=None, mirna=None, out_file=None, in_format=None):
        if folder is None:
            folder = s_rna_tools.utils.prompt_path(
                msg="Select the fasta file to group sequences"
            )
        self.folder = folder
        if not os.path.dirname(self.folder):
            log.error("folder  %s does not exist ", self.folder)
            stderr.print(f"[red] Folder for input files {self.folder} does not exist")
            sys.exit(1)
        if mirna:
            if not s_rna_tools.utils.file_exists(mirna):
                log.error("miRNA file  %s does not exist ", mirna)
                stderr.print(f"[red] miRNA file  {mirna} does not exist")
                sys.exit(1)
        self.mirna = mirna

        if out_file is None:
            out_file = s_rna_tools.utils.prompt_path(
                msg="Select the file to save results"
            )
        self.out_file = out_file

        if in_format is None:
            in_format = s_rna_tools.utils.prompt_selection(
                "Define the input format", ["summary", "fasta"]
            )
        self.in_format = in_format
        return

    def find_unique_in_file(self, f_name, unique_seq):
        """Find new unique sequences"""
        if self.in_format == "summary":
            with open(f_name, "r") as fh:
                lines = fh.readlines()
            for line in lines:
                seq = line.split("\t")[1]
                if seq not in unique_seq:
                    unique_seq[seq] = line.split("\t")[0]
        elif self.in_format == "fasta":
            for seq_record in SeqIO.parse(f_name, "fasta"):
                if str(seq_record.seq) not in unique_seq:
                    unique_seq[str(seq_record.seq)] = str(seq_record.id)
        return unique_seq

    def read_mirna_file(self):
        """Read the miRNA file, collecting the unique sequences and convert RNA to DNA sequences"""
        mirna_unique = {}
        for seq_record in SeqIO.parse(self.mirna, "fasta"):
            seq = str(seq_record.seq.back_transcribe())
            if seq not in mirna_unique:
                mirna_unique[seq] = str(seq_record.id)
        return mirna_unique

    def remove_mirna_seq(self, sequences, mirna):
        """Remove in the unique sequences the miRNAs. miRNAs harpins are also
        discarded"""
        return

    def collect_unique(self):
        """Collect the unique sequences"""
        if self.in_format == "summary":
            file_list = glob.glob(self.folder + "*.tsv")
            if len(file_list) == 0:
                log.error("There is not valid files on folder  %s ", self.folder)
                stderr.print(f"[red] There is not valid files on folder {self.folder}")
                sys.exit(1)
        else:
            file_list = glob.glob(self.folder + "*.fa")
            if len(file_list) == 0:
                file_list = glob(self.folder, "/*.fasta")
                if len(file_list) == 0:
                    log.error("There is not valid files on folder  %s ", self.folder)
                    stderr.print(
                        f"[red] There is not valid files on folder {self.folder}"
                    )
                    sys.exit(1)

        unique_seq = {}
        for f_name in file_list:
            unique_seq = self.find_unique_in_file(f_name, unique_seq)
        if self.mirna:
            pass
        s_rna_tools.utils.write_unique_seq(unique_seq, self.out_file)
