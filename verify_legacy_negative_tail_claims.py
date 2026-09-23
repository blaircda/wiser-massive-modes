#!/usr/bin/env python3
"""Reconstruct the old negative-tail tables from the protected SO(10) data.

The missing ``test_neg_analysis.py`` cannot be audited.  This replacement makes
the provenance explicit: it defines the virtual single-level character by the
consecutive difference of the already known positive cumulative characters,

    r_n^10 := R_n^10 - R_{n-1}^10,

and decomposes that difference into positive and negative irreducible parts.
Consequently ``neg_n <= R_{n-1}`` is a restatement of the known positivity of
``R_n`` for this baseline-defined difference, not an independent derivation.
"""

import argparse
import sys

from sage.all import QQ, WeylCharacterRing

from massive_SO10 import SO10_SUPERMULTIPLETS_DYNKIN


D5 = WeylCharacterRing("D5", base_ring=QQ, style="coroots")


def baseline_character(level):
    """Return the preserved cumulative character at one level."""
    result = D5(0)
    data = SO10_SUPERMULTIPLETS_DYNKIN[level]
    for multiplicity, _dimension, dynkin in data["bosons"]:
        result += multiplicity * D5(*dynkin)
    for multiplicity, _dimension, dynkin in data["fermions"]:
        result += multiplicity * D5(*dynkin)
    return result


def dynkin_labels(weight):
    """Convert a D5 ambient highest weight to Dynkin labels."""
    x1, x2, x3, x4, x5 = weight.to_vector()
    return tuple(
        int(value)
        for value in (
            x1 - x2,
            x2 - x3,
            x3 - x4,
            x4 - x5,
            x4 + x5,
        )
    )


def positive_and_negative(character):
    """Return positive and negative parts of a virtual D5 character."""
    positive = D5(0)
    negative = D5(0)
    positive_terms = []
    negative_terms = []
    for weight, coefficient in character.monomial_coefficients().items():
        labels = dynkin_labels(weight)
        if coefficient > 0:
            positive += coefficient * D5(*labels)
            positive_terms.append((labels, int(coefficient)))
        elif coefficient < 0:
            negative -= coefficient * D5(*labels)
            negative_terms.append((labels, int(-coefficient)))
    return positive, negative, tuple(positive_terms), tuple(negative_terms)


def run_audit(max_level=10, verbose=False):
    cumulative = {
        level: baseline_character(level)
        for level in range(1, max_level + 1)
    }
    zero = D5(0)

    print("=" * 106)
    print("RECONSTRUCTION OF LEGACY NEGATIVE-TAIL TABLES (BASELINE-DEPENDENT)")
    print("=" * 106)
    print(
        f"{'Level':<7}{'dim R_n':<13}{'dim R_(n-1)':<16}{'dim neg_n':<14}"
        f"{'Dominated':<12}{'Surplus dim':<14}{'Identity R_n=R_(n-1)+r_n'}"
    )
    print("-" * 106)

    all_pass = True
    results = {}
    for level in range(1, max_level + 1):
        previous = cumulative[level - 1] if level > 1 else zero
        single = cumulative[level] - previous
        positive, negative, positive_terms, negative_terms = positive_and_negative(single)
        surplus = previous - negative

        identity = previous + positive - negative == cumulative[level]
        dominated = all(
            coefficient >= 0
            for coefficient in surplus.monomial_coefficients().values()
        )
        level_pass = identity and dominated
        all_pass = all_pass and level_pass
        results[level] = {
            "single": single,
            "positive": positive,
            "negative": negative,
            "positive_terms": positive_terms,
            "negative_terms": negative_terms,
            "surplus": surplus,
        }

        print(
            f"{level:<7}{int(cumulative[level].degree()):<13}"
            f"{int(previous.degree()):<16}{int(negative.degree()):<14}"
            f"{str(dominated):<12}{int(surplus.degree()):<14}{str(identity)}"
        )
        if verbose:
            print(f"      negative terms: {negative_terms}")

    print("-" * 106)
    print("Provenance: r_n^10 was defined from consecutive protected baseline differences.")
    print("Logical status: domination is equivalent here to the already known positivity of R_n.")
    print(f"Reconstruction result: {'[PASSED]' if all_pass else '[FAILED]'}")
    return all_pass, results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Reconstruct legacy negative-tail claims from protected baseline data"
    )
    parser.add_argument("--max-level", type=int, default=10)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    passed, _results = run_audit(args.max_level, args.verbose)
    sys.exit(0 if passed else 1)
