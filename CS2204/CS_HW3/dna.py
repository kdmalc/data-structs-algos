#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DNA Analysis"""

__author__ = "malcolkd"


from math import floor


class Codon:
    """Amino-acid encoding with three nucleotides"""

    def __init__(self, bases):
        assert len(bases) == 3
        assert type(bases) is str
        for base in bases:
            assert base.upper() in ['A', 'C', 'G', 'T']

        self.bases = bases.upper()

    def __str__(self):
        """Convert to string enclosed in square brackets.
        E.g. [GCT]
        """
        return f"[{self.bases}]"

    def __eq__(self, other):
        """Compare if two Codon objects are equal (same sequence of bases)"""
        return self.bases == other.bases

    def transcribe(self):
        """Return a string of transcribed bases enclosed in angle brackets.

        E.g. <GCU>
        """

        trans_bases = ["U" if base == "T" else base for base in self.bases]
        for idx in range(len(trans_bases)):
            bases_hold = "".join(str(ele) for ele in trans_bases)
        if (len(bases_hold) is None) or (len(bases_hold) == 0):
            return ""
        else:
            return f"<{bases_hold}>"


class Gene:
    """Protein encoding with a sequence of codons"""

    def __init__(self, seq):
        self.seq = seq.upper()
        while len(self.seq) % 3 > 0:
            self.seq = self.seq[0:-1]

        seq_hold = []
        for idx in range(floor(len(self.seq) / 3)):
            codon_str = ((self.seq[3*idx]) + (self.seq[3*idx + 1])
                         + (self.seq[3*idx + 2]))
            seq_hold.append(Codon(codon_str).bases)

        self.seq = seq_hold

    def __str__(self):
        """Convert to string using a sequence of codons (in square brackets).

        E.g. [GCT][GGC]...
        """

        seq_hold = "".join(f"[{str(ele)}]" for ele in self.seq)
        return seq_hold

    def transcribe(self):
        """Return a string of transcribed codons (in angle brackets).

        E.g. <GCU><GGC>...
        """
        trans_codons = [Codon(codon).transcribe() for codon in self.seq]
        codons_hold = ""
        for idx in range(len(trans_codons)):
            codons_hold = "".join(str(ele) for ele in trans_codons)
        if (len(codons_hold) is None) or (len(codons_hold) == 0):
            return ""
        else:
            return f"{codons_hold}"

    def __contains__(self, codon):
        """Check if the gene seuence contains the given codon"""
        return (True if sum([1 for ele in self.seq
                             if codon.bases.upper() == ele]) > 0 else False)

    def gc_content(self):
        """Return the fraction of G and C bases relative to all bases"""

        my_c = sum([codon.upper().count('C') for codon in self.seq])
        my_g = sum([codon.upper().count('G') for codon in self.seq])

        return (my_c + my_g)/(3*len(self.seq))


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

    # My additions
    print("Codon Testing")
    # Test Codon init and str
    try:
        print(Codon("ac1t"))
        print("------- 0Error passed through -------")
    except AssertionError:
        print("Successful error catch")

    try:
        print(Codon("ac "))
        print("------- 1Error passed through -------")
    except AssertionError:
        print("Successful error catch")

    # Test Codon eq
    try:
        print(Codon("act") == Codon("ACT"))
        print(Codon("ac ") == Codon("ACT"))
        print("------- 2Error passed through -------")
    except AssertionError:
        print("Succssful error catch")

    try:
        print(Codon("aCt") == Codon("aTT"))
    except AssertionError:
        print("Succssful error catch")

    print("Gene Testing:")
    # test Gene init and str
    try:
        print(Gene("aCt"))
        print(Gene("aCt"))
        print(Gene("actuttta"))
        print("------- 3Error passed through -------")
    except AssertionError:
        print("Succssful error catch")
    # test Gene transcribe
    try:
        print(Gene("aCtaTTTCCTCTCTATATTAAAGGTGTGTG").transcribe())
        print(Gene("aCtaTTTCCTCTCTATATTA123AGGTGTGTG").transcribe())
        print("------- 4Error passed through -------")
    except AssertionError:
        print("Succssful error catch")

    try:
        print(Gene("aCtaTTTCCTCT ATATTAAAGGTGTGTG").transcribe())
        print("------- 5Error passed through -------")
    except AssertionError:
        print("Succssful error catch")
    print("All tests complete")
