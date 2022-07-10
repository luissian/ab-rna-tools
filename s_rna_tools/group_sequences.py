#!/usr/bin/env python
import os
import sys
import logging
import rich.console
from halo import Halo
from Bio import SeqIO
import s_rna_tools.utils

log = logging.getLogger(__name__)
stderr = rich.console.Console(
    stderr=True,
    style="dim",
    highlight=False,
    force_terminal=s_rna_tools.utils.rich_force_colors(),
)


class GroupSequences:
    def __init__(self, seq_file=None, out_folder=None, out_format=None, threshold=None):
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
        self.out_folder = out_folder

        if out_format is None:
            out_format = s_rna_tools.utils.prompt_selection(
                "Define the output format", ["summary", "fasta"]
            )
        self.out_format = out_format
        if threshold is None:
            threshold = 10
        try:
            self.threshold = int(threshold)
        except ValueError:
            log.error(
                "%s is not a valid value for threshold. Integer value must be set",
                threshold,
            )
            stderr.print(
                f"[red] {threshold} is not a valid value for threshold. Integer value must be set"
            )
            sys.exit(1)

        return

    def filter_seq(self, seqs):
        f_seqs = {}
        for seq, counter in seqs.items():
            if counter >= self.threshold:
                f_seqs[seq] = counter
        return f_seqs

    def counter_seq(self):
        seq_counter = {}
        spinner = Halo(text="Searching for repeated contings", spinner="dots")
        spinner.start()
        for seq_record in SeqIO.parse(self.seq_file, "fasta"):
            str_seq = str(seq_record.seq)
            if str_seq not in seq_counter:
                seq_counter[str_seq] = 0
            seq_counter[str_seq] += 1
        spinner.succeed("Processed sequence file")

        if self.threshold != 0:
            spinner.start("filtering sequences for removing low values")
            seq_counter = self.filter_seq(seq_counter)
            spinner.succeed("Filter done")
        heading = "SRNA\tSequence\tCounts"
        seq_id = os.path.basename(self.seq_file).split(".")[0] + "_RNA_"
        count_f_name = os.path.join(
            self.out_folder,
            os.path.basename(self.seq_file).split(".")[0] + "_count_reads",
        )
        if self.out_format == "summary":
            count_f_name += ".tsv"
        else:
            count_f_name += ".fa"
        stderr.print(f"[green] Saving data to file")
        s_rna_tools.utils.write_seq_file(
            seq_counter, count_f_name, heading, seq_id, self.out_format
        )
        spinner.stop()
        stderr.print(
            f"[green] Processing file {os.path.basename(self.seq_file)} completed"
        )
        return
