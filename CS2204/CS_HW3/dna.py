#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DNA Analysis"""

__author__ = ""


class Codon:
    """Amino-acid encoding with three nucleotides"""

    def __init__(self, bases):
        pass

    def __str__(self):
        """Convert to string enclosed in square brackets.
        E.g. [GCT]
        """
        pass

    def __eq__(self, other):
        """Compare if two Codon objects are equal (same sequence of bases)"""
        pass

    def transcribe(self):
        """Return a string of transcribed bases enclosed in angle brackets.

        E.g. <GCU>
        """
        pass


class Gene:
    """Protein encoding with a sequence of codons"""

    def __init__(self, seq):
        pass

    def __str__(self):
        """Convert to string using a sequence of codons (in square brackets).

        E.g. [GCT][GGC]...
        """
        pass

    def transcribe(self):
        """Return a string of transcribed codons (in anle brackets).

        E.g. <GCU><GGC>...
        """
        pass

    def __contains__(self, codon):
        """Check if the gene seuence contains the given codon"""
        pass

    def gc_content(self):
        """Return the fraction of G and C bases relative to all bases"""
        pass


if __name__ == "__main__":

    # Read DNA sample file (ignore comments and newlines)
    dna_lines = []
    with open("dna_sample.txt") as datafile:
        for line in datafile:
            line = line.strip()
            if not line.startswith("#"):
                dna_lines.append(line)
    dna_sample = "".join(dna_lines)

    gene = Gene(dna_sample)

    # Feel free to change, delete or add to this testing code below
    # This part of your code and the printed outputs below will not be graded
    print(Codon("act") in gene)
    print(gene.gc_content())
