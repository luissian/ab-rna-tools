#!/usr/bin/env python

from setuptools import setup, find_packages

version = "0.0.1"

with open("README.md") as f:
    readme = f.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="s-rna_tools",
    version=version,
    description="Tools for handling Small RNA sequences.",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords=[
        "RNA",
        "bioinformatics",
        "pipeline",
        "sequencing",
        "NGS",
        "next generation sequencing",
    ],
    author="Luis Chapado",
    author_email="chapado.l@gmail.com",
    url="https://github.com/luissian/s-rna-tools",
    license="GNU GENERAL PUBLIC LICENSE v.3",
    entry_points={
        "console_scripts": ["s-rna-tools=s_rna_tools.__main__:run_s_rna_tools"]
    },
    install_requires=required,
    packages=find_packages(exclude=("docs")),
    include_package_data=True,
    zip_safe=False,
)
