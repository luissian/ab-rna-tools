#!/usr/bin/env python
from Bio.Blast.Applications import NcbiblastnCommandline
import os
import sys
import subprocess


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
        try:
            with subprocess.Popen(
                blastn_db,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ) as proc:
                stderr.print("Successful creation of blast database")
        except subprocess.CalledProcessError:
            log.error("Unable to create blast database. Error %s ", proc.returncode)
            stderr.print(f"[red] Unable to create blast database {proc.stderr}")
            sys.exit(1)

    def collect_data(self, out_lines):
        matches_found = []
        for out_line in out_lines:
            matches_found.append(out_line.split("\t"))
        return matches_found

    def run_blast(query_file, match):
        blast_parameters = '"6 , qseqid , sseqid , pident ,  qlen , length , mismatch , gapopen , evalue , bitscore , sstart , send , qstart , qend , sseq , qseq"'
        result = {}
        cline = NcbiblastnCommandline(
            db=self.db_folder,
            task=self.task,
            evalue=self.evalue,
            perc_identity=self.perc_identity,
            outfmt=blast_parameters,
            max_target_seqs=50,
            max_hsps=20,
            num_threads=4,
            query=query_file,
        )
        out, err = cline()
        out_lines = out.splitlines()

        if match:
            if len(out_lines) > 0:
                result["match"] = self.collect_data(out_lines)
        else:
            if len(out_lines) == 0:
                result["not_match"] = query_file
        import pdb

        pdb.set_trace()
        return result
