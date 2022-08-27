#!/usr/bin/env python
from Bio.Blast.Applications import NcbiblastnCommandline
import os
import sys
import subprocess
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


class RnaBlast:
    def __init__(self, blast_fasta, task, perc_identity, evalue, out_dir):
        self.blast_db = blast_fasta
        self.task = task
        self.perc_identity = perc_identity
        self.evalue = evalue
        db_name = os.path.basename(self.blast_db).split(".")[0]
        self.db_folder = os.path.join(out_dir, db_name, db_name)
        blastn_db = (
            "makeblastdb -in "
            + blast_fasta
            + " -dbtype nucl -input_type fasta -out "
            + self.db_folder
        )
        # stderr.print("Starting blast index generation. Please wait")

        proc = subprocess.Popen(
            blastn_db,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        proc.wait()
        if proc.returncode == 0:
            stderr.print("\nSuccessful creation of blast database")
        else:
            log.error("Unable to create blast database. Error %s ", proc.returncode)
            log.error("running the following parameters %s", proc.args)
            stderr.print(f"\n[red] Unable to create blast database {proc.returncode}")
            stderr.print(f"[red] running the following parameters {proc.args}")
            sys.exit(1)

    def collect_data(self, out_lines):
        matches_found = []
        for out_line in out_lines:
            matches_found.append(out_line.split("\t"))
        return matches_found

    def run_blast(self, query_file):
        blast_parameters = '"6 , qseqid , sseqid , pident ,  qlen , length , mismatch , gapopen , evalue , bitscore , sstart , send , qstart , qend , sseq , qseq"'
        result = {}
        cline = NcbiblastnCommandline(
            db=self.db_folder,
            task=self.task,
            evalue=self.evalue,
            penalty=-2,
            perc_identity=self.perc_identity,
            outfmt=blast_parameters,
            max_target_seqs=200,
            max_hsps=20,
            num_threads=8,
            query=query_file,
        )
        out, err = cline()
        out_lines = out.splitlines()
        if len(out_lines) > 0:
            result["match"] = self.collect_data(out_lines)
        else:
            result["not_match"] = query_file

        return result

    def write_to_file(self, data, file_name):
        match_heading = "Sample\tmiRNA Name\tcontig\tpident\tmiRNA\tlength\tmismatch\tgapopen\tevalue\tbitscore\tSample start\tSample end\tmiRNA start\tmiRNA end\tSample Sequence\tmiRNA Sequence"
        with open(file_name, "w") as fh:
            fh.write(match_heading + "\n")
            for key, values in data.items():
                for value in values:
                    fh.write(key + "\t" + "\t".join(value) + "\n")
        return
