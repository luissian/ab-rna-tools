#!/usr/bin/env python
import os
import sys
import re
import logging
import rich.console
from glob import glob
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


class Countifier:
    def __init__(self, sample_files=None, unique_seq=None, out_folder=None):
        if sample_files is None:
            sample_files =  s_rna_tools.utils.prompt_path(
                msg="Select the sample file or directory with the count reads"
            )
        if os.path.isdir(sample_files):
            file_list = glob(sample_files + "/*.fa")
            if len(file_list) == 0:
                file_list = glob(sample_files + "/*.fasta")
                if len(file_list) == 0:
                    log.error("folder  %s does not contain any fasta file", self.sample_files)
                    stderr.print(f"[red] Folder  {self.sample_files} does not contain any fasta file")
                    sys.exit(1)
            self.file_list = file_list
        elif os.path.isfile(sample_files):
            self.file_list = [sample_files]
        else:
            log.error(" %s does not exist", self.sample_files)
            stderr.print(f"[red] {self.sample_files} does not exist")
            sys.exit(1)
        if unique_seq is None:
            unique_seq =  s_rna_tools.utils.prompt_path(
                msg="Select the file which contains the unique sequences"
            )
        if not os.path.isfile(unique_seq):
            log.error(" %s does not exist", self.unique_seq)
            stderr.print(f"[red] {self.unique_seq} does not exist")
            sys.exit(1)
        self.unique_seq = unique_seq
        if out_folder is None:
            out_folder = s_rna_tools.utils.prompt_path(
                msg="Select the directory to save results"
            )
        self.out_folder = out_folder

    def parse_seq(self, fasta_file):
        """Read the unique sequence file and return a dictonary with the sequences"""
        seq_dict = {}
        for seq_record in SeqIO.parse(fasta_file, "fasta"):
            id_match = re.search(r'.*_x(\d+)$', str(seq_record.id))
            if id_match:
                seq_dict[str(seq_record.seq)] = id_match.group(1)
            else:
                seq_dict[str(seq_record.seq)]  = 0
        return seq_dict

    def fetch_sample_counts(self, s_file, seq_master):
        """Fetch the sequence and the count for sample, using as unique_seq
        as reference
        """
        seq_sample = self.parse_seq(s_file)
        count_seq = {}
        for seq in seq_master.keys():
            if seq in seq_sample:
                count_seq[seq] = seq_sample[seq]
            else:
                count_seq[seq] = "0"
        return count_seq

    def create_counter_file(self, samples_dict, seq_master):
        """Create the tab file with sequences  and the counter"""
        sample_list = list(samples_dict.keys())
        heading = "Sequence\tTotal Counts\t" + "\t".join(sample_list)
        f_name = os.path.join(self.out_folder, "sample_cuantifier.tsv")
        with open(f_name, "w") as fh:
            fh.write(heading + "\n")
            for seq in seq_master.keys():
                count = 0
                value_list = []
                for sample in sample_list:
                    value = samples_dict[sample][seq]
                    value_list.append(value)
                    count += int(value)
                fh.write(seq + "\t" + str(count) + "\t" + "\t".join(value_list) + "\n")
        return


    def split_files(self):
        """Read the unique sequence file, find the sequence in the sample count
        reads and create a file having the number that the sequence was found
        """
        seq_master = self.parse_seq(self.unique_seq)
        samples_dict = {}
        for s_file in self.file_list:
            f_name = os.path.basename(s_file).split(".")[0]
            f_match = re.search(r'(.*)_count_reads.*', f_name)
            if f_match:
                s_name = f_match.group(1)
            else:
                s_name = f_name
            samples_dict[s_name] = self.fetch_sample_counts(s_file, seq_master)
        self.create_counter_file(samples_dict, seq_master)
