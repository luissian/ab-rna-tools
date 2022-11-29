#!/usr/bin/env python
import os
import sys
import logging
import rich.console
from Bio import SeqIO
import s_rna_tools.utils
from s_rna_tools.rna_blast import RnaBlast
from halo import Halo

log = logging.getLogger(__name__)
stderr = rich.console.Console(
    stderr=True,
    style="dim",
    highlight=False,
    force_terminal=s_rna_tools.utils.rich_force_colors(),
)


class MatchAllSmrna:
    def __init__(
        self,
        grep_result=None,
        sample_file=None,
        out_folder=None
    ):
        if grep_result is None:
            grep_result = s_rna_tools.utils.prompt_path(
                msg="Select the file with the grep result"
            )
        self.grep_result = grep_result
        if not os.path.isfile(self.grep_result):
            log.error("grep result file %s does not exist ", self.grep_result)
            stderr.print(f"[red] grep result file {self.grep_result} does not exist")
            sys.exit(1)

        if sample_file is None:
            sample_file = s_rna_tools.utils.prompt_path(
                msg="Select the file to match against the sequences"
            )
        self.sample_file = sample_file
        if not os.path.isfile(self.sample_file):
            log.error("matching file %s does not exist ", self.sample_file)
            stderr.print(f"[red] matching file {self.sample_file} does not exist")
            sys.exit(1)
        if out_folder is None:
            out_folder = s_rna_tools.utils.prompt_path(
                msg="Select the folder to save results"
            )
        self.out_folder = out_folder

    def _split_matched_annotation(self):
        """Read the file from the grep result and split between matched and
        not matched
        """
        with open (self.grep_result, "r") as fh:
            lines = fh.readlines()
        smrna_annot = {"match": {}, "not_match": []}
        for line in lines:
            line = line.strip()
            line_split = line.split(",")
            if "Not match" in line_split[1]:
                smrna_annot["not_match"].append(line_split[0])
            else:
                smrna_annot["match"][line_split[0]] = line_split[2]
        return smrna_annot

    def _replace_match(self, s_annot):
        """Read the sample file and replace sequence by annotations"""
        with open(self.sample_file, "r") as fh:
            lines = fh.readlines()
        mapped_list =  []
        unmapped_list = []
        mapped_list.append(lines[0])
        unmapped_list.append(lines[0])
        for line in lines[1:]:
            line_split = line.split("\t")
            if line_split[0] in s_annot:
                line_split[0] = s_annot[line_split[0]]
                mapped_list.append(",".join(line_split))
            else:
                unmapped_list.append(line)

        return mapped_list, unmapped_list

    def _write_files(self, mapped, unmapped):
        map_file = os.path.join(self.out_folder, "mapped_results.csv")
        unmap_file = os.path.join(self.out_folder, "unmapped_results.csv")
        with open (map_file, "w") as fh:
            for line in mapped:
                fh.write(line)

        with open(unmap_file, "w") as fh:
            for line in unmapped:
                fh.write(line)
        return

    def get_match_sequences(self):
        smrna_annot = self._split_matched_annotation()
        mapped, unmapped = self._replace_match(smrna_annot["match"])
        self._write_files(mapped, unmapped)


        import pdb; pdb.set_trace()
