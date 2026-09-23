"""Generic character-valued plethystic series operations.

This module contains only formal representation-ring recurrences. It imports no
project spectrum and no protected baseline. Callers supply truncated series
whose coefficients belong to a Sage Weyl character ring over QQ.
"""

from sage.all import Rational, divisors, moebius


def compute_log_coefficients(series, max_degree):
    """Return coefficients of ``log(series)`` through ``max_degree``."""
    logarithm = {}
    for n in range(1, max_degree + 1):
        term = series[n]
        for j in range(1, n):
            term -= Rational((j, n)) * logarithm[j] * series[n - j]
        logarithm[n] = term
    return logarithm


def compute_plethystic_log(logarithm, max_degree):
    """Apply Möbius inversion and Adams operations to a formal logarithm."""
    parent = logarithm[1].parent()
    result = {}
    for n in range(1, max_degree + 1):
        value = parent(0)
        for k in divisors(n):
            value += Rational((moebius(k), k)) * logarithm[n // k].adams_operator(k)
        result[n] = value
    return result


def compute_plethystic_exp(plethystic_logarithm, max_degree):
    """Reconstruct a series from its plethystic logarithm."""
    parent = plethystic_logarithm[1].parent()
    rank = parent.cartan_type().rank()
    ordinary_logarithm = {}
    result = {0: parent(*([0] * rank))}

    for n in range(1, max_degree + 1):
        value = parent(0)
        for k in divisors(n):
            value += Rational((1, k)) * plethystic_logarithm[n // k].adams_operator(k)
        ordinary_logarithm[n] = value

        coefficient = value
        for j in range(1, n):
            coefficient += Rational((j, n)) * ordinary_logarithm[j] * result[n - j]
        result[n] = coefficient
    return result


def plethystic_log(series, max_degree):
    """Convenience wrapper returning ``PL[series]``."""
    return compute_plethystic_log(
        compute_log_coefficients(series, max_degree),
        max_degree,
    )
