#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DNA Analysis"""

__author__ = "malcolkd"


from math import floor


class Codon:
    """Amino-acid encoding with three nucleotides"""

    def __init__(self, bases):
        self.bases = bases.upper()
        # Something about raising exceptions if you get bad input
        """
        try:
            assert len(bases) == 3
            assert type(bases) ==  str
            acceptable_bases = ['A', 'C', 'G', 'T']
            assert bases[0].upper() in acceptable_bases

        except TypeError:
            print("Error: bases is NoneType")
        """

    def __str__(self):
        """Convert to string enclosed in square brackets.
        E.g. [GCT]
        """
        return self.bases

    def __eq__(self, other):
        """Compare if two Codon objects are equal (same sequence of bases)"""
        return self.bases == other.bases

    def transcribe(self):
        """Return a string of transcribed bases enclosed in angle brackets.

        E.g. <GCU>
        """
        return f"<{self.bases}>"


class Gene:
    """Protein encoding with a sequence of codons"""

    def __init__(self, seq):
        self.seq = seq.upper()
        while len(self.seq) % 3 > 0:
            self.seq = self.seq[0:-1]

        third_length = floor(len(self.seq)/3)
        seq_hold = [0] * third_length
        for idx in range(third_length):
            seq_hold[idx] = (str(self.seq[3*idx]) + str(self.seq[3*idx+1])
                             + str(self.seq[3*idx+2]))
        self.seq = seq_hold

    def __str__(self):
        """Convert to string using a sequence of codons (in square brackets).

        E.g. [GCT][GGC]...
        """
        # Double check that this string doesn't start/end with "[[...]]"
        # Return this as a string...
        return [f"[{str(ele)}]" for ele in self.seq]

    def transcribe(self):
        """Return a string of transcribed codons (in angle brackets).

        E.g. <GCU><GGC>...
        """
        # Double check that this string doesn't start/end with "[[...]]"
        # Return this as a string...
        return [f"<{str(ele)}>" for ele in self.seq]

    def __contains__(self, codon):
        """Check if the gene seuence contains the given codon"""
        return (True if sum([1 for ele in self.seq
                             if str(codon).upper() == ele]) > 0 else False)

    def gc_content(self):
        """Return the fraction of G and C bases relative to all bases"""
        # This is not good enough, as a codon could be just G/Cs
        return ((sum([1 for codon in self.seq if "GC" in codon.upper()]) > 0)
                / len(self.seq))


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
