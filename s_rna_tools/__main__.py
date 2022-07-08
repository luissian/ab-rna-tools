#!/usr/bin/env python
import logging
import emoji

# from rich.prompt import Confirm
import click
import rich.console
import rich.logging
import rich.traceback

import s_rna_tools.utils
import s_rna_tools.group_sequences
import s_rna_tools.create_unique
import s_rna_tools.find_unknown

log = logging.getLogger()


def run_s_rna_tools():
    # Set up rich stderr console
    stderr = rich.console.Console(
        stderr=True, force_terminal=s_rna_tools.utils.rich_force_colors()
    )

    # Set up the rich traceback
    rich.traceback.install(console=stderr, width=200, word_wrap=True, extra_lines=1)
    stderr.print(
        "[yellow]    ____            ___                            ",
        highlight=False,
    )
    stderr.print(
        "[yellow]   /      [blue]__  __ [yellow]  |   \ |\   |    /\ ", highlight=False
    )
    stderr.print(
        "[yellow]   \___   [red]  \/   [yellow]  |__ / | \  |   /  \ ", highlight=False
    )
    stderr.print(
        "[yellow]       \  [blue]__/\__ [yellow]  |  \  |  \ |  /____\ ",
        highlight=False,
    )
    stderr.print(
        "[yellow]   ____/         [yellow]  |   \ |   \| /      \ ", highlight=False
    )

    __version__ = "0.0.1"
    stderr.print()
    stderr.print(
        "       ",
        emoji.emojize(":dna:"),
        "[bold grey39] s-rna-tools version {}".format(__version__),
        highlight=False,
    )
    stderr.print()

    # Lanch the click cli
    s_rna_tools_cli()


# Customise the order of subcommands for --help
class CustomHelpOrder(click.Group):
    def __init__(self, *args, **kwargs):
        self.help_priorities = {}
        super(CustomHelpOrder, self).__init__(*args, **kwargs)

    def get_help(self, ctx):
        self.list_commands = self.list_commands_for_help
        return super(CustomHelpOrder, self).get_help(ctx)

    def list_commands_for_help(self, ctx):
        """reorder the list of commands when listing the help"""
        commands = super(CustomHelpOrder, self).list_commands(ctx)
        return (
            c[1]
            for c in sorted(
                (self.help_priorities.get(command, 1000), command)
                for command in commands
            )
        )

    def command(self, *args, **kwargs):
        """Behaves the same as `click.Group.command()` except capture
        a priority for listing command names in help.
        """
        help_priority = kwargs.pop("help_priority", 1000)
        help_priorities = self.help_priorities

        def decorator(f):
            cmd = super(CustomHelpOrder, self).command(*args, **kwargs)(f)
            help_priorities[cmd.name] = help_priority
            return cmd

        return decorator


@click.group(cls=CustomHelpOrder)
@click.version_option(s_rna_tools.__version__)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="Print verbose output to the console.",
)
@click.option(
    "-l", "--log-file", help="Save a verbose log to a file.", metavar="<filename>"
)
def s_rna_tools_cli(verbose, log_file):

    # Set the base logger to output DEBUG
    log.setLevel(logging.DEBUG)

    # Set up logs to a file if we asked for one
    if log_file:
        log_fh = logging.FileHandler(log_file, encoding="utf-8")
        log_fh.setLevel(logging.DEBUG)
        log_fh.setFormatter(
            logging.Formatter(
                "[%(asctime)s] %(name)-20s [%(levelname)-7s]  %(message)s"
            )
        )
        log.addHandler(log_fh)


@s_rna_tools_cli.command(help_priority=1)
@click.option("-i", "--infile", help="fasta input file with sequences")
@click.option("-o", "--out_folder", help="Path to save generated ouput files")
@click.option("-f", "--out_format", type=click.Choice(["summary", "fasta"]), help = "Select format for output file")
def group_sequences(infile, out_folder, out_format):
    """Group small RNA sequences."""
    new_s_group = s_rna_tools.group_sequences.GroupSequences(infile, out_folder, out_format)
    counter = new_s_group.counter_seq()
    # print(counter)


@s_rna_tools_cli.command(help_priority=2)
@click.option("-d", "--directory", type=click.Path(), help="Folder with processed count files")
@click.option("-m", "--mirna", type=click.Path(), help="miRNA fasta file to exclude them in unique sequences")
@click.option("-o", "--out_file", help="file name to save fata file for unique sequences")
@click.option("-f", "--out_format", type=click.Choice(["summary", "fasta"]), help = "Select format for output file")
def create_unique(directory, mirna, out_file, out_format):
    """Create a file which has only the unique samples"""
    unique_seq = s_rna_tools.create_unique.CreateUnique(directory, mirna, out_file, out_format)
    unique_seq.collect_unique()


@s_rna_tools_cli.command(help_priority=3)
@click.option("-i", "--in_seq", type=click.Path(), help="file having the unique reads")
@click.option("-m", "--match_to_file", type=click.Path(), help="file with the sequences to discard")
@click.option("-o", "--outdir", type=click.Path(), help="output directory to save result")
def find_unknown(in_seq, match_to_file, outdir):
    new_findings = s_rna_tools.find_unknown.FindUnknown(in_seq, match_to_file, outdir)
    new_findings.get_unknow_sequences()
