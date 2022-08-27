#!/usr/bin/env python
import os
import sys
import logging
import rich.console
import s_rna_tools.utils
from collections import OrderedDict

log = logging.getLogger(__name__)
stderr = rich.console.Console(
    stderr=True,
    style="dim",
    highlight=False,
    force_terminal=s_rna_tools.utils.rich_force_colors(),
)


class JoinDuplicates:
    def __init__(self, input=None, position=None):
        if input is None:
            input = s_rna_tools.utils.prompt_path(
                msg="Select the file which have a key colunm with duplicated values"
            )
        if not s_rna_tools.utils.file_exists(input):
            log.error("file  %s does not exist ", self.input)
            stderr.print(f"[red] file {self.folder} does not exist")
            sys.exit(1)
        self.input = input
        if position is None:
            position = s_rna_tools.utils.prompt_message(
                msg="Select the position where checking duplicates"
            )
        try:
            self.position = int(position)
        except ValueError:
            log.error("Position value  %s is not a integer ", position)
            stderr.print(f"[red] Position value {position} is not a integer")
            sys.exit(1)

    def join_lines(self, old_line, new_split_line):
        s_old_line = old_line.split()
        j_values = []
        for idx in range(len(s_old_line)):
            if idx <= self.position:
                j_values.append(s_old_line[idx])
                continue
            try:
                sum_values = int(s_old_line[idx]) + int(new_split_line[idx])
                j_values.append(str(sum_values))
            except ValueError:
                j_values.append(s_old_line)
        return "\t".join(j_values)

    def write_join(self, data_dict):
        f_name = os.path.join(os.path.dirname(self.input), "without_duplicated.tsv")
        with open(f_name, "w") as fh:
            for key, value in data_dict.items():
                fh.write(value + "\n")
        return

    def make_unique(self):
        with open(self.input, "r") as fh:
            lines = fh.readlines()
        s_rna_dict = OrderedDict()
        for line in lines:
            line = line.strip()
            l_split = line.split("\t")
            c_value = l_split[self.position]
            if c_value not in s_rna_dict:
                s_rna_dict[c_value] = line
            else:
                s_rna_dict[c_value] = self.join_lines(s_rna_dict[c_value], l_split)
        return s_rna_dict
