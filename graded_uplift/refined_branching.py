"""Exact SO(10) -> SO(8) x SO(2)_J branching with Delta-J grading."""

from collections import defaultdict
from functools import lru_cache

from sage.all import QQ, ZZ, WeylCharacterRing

from graded_uplift import refined_spectrum


D5 = WeylCharacterRing("D5", base_ring=QQ, style="coroots")
D4 = refined_spectrum.D4


def _integer(value, description):
    if value not in ZZ:
        raise ValueError(f"Non-integral {description}: {value}")
    return int(value)


def d5_parity(label):
    return -1 if (label[3] + label[4]) % 2 else 1


@lru_cache(maxsize=None)
def branch_irrep_with_charge(label):
    """Return a dictionary ``2J -> D4 character`` for one D5 irrep."""
    grouped_weights = defaultdict(dict)
    for weight, multiplicity in D5(*label).weight_multiplicities().items():
        coordinates = weight.to_vector()
        twice_charge = _integer(2 * coordinates[4], "twice SO(2) charge")
        d4_weight = D4.space()(tuple(coordinates[:4]))
        grouped_weights[twice_charge][d4_weight] = multiplicity
    return {
        twice_charge: D4.char_from_weights(weights)
        for twice_charge, weights in grouped_weights.items()
    }


def delta_nu_image(label, twice_delta):
    """Apply ``nu = Delta-J`` and return ``nu -> D4 character``."""
    result = {}
    for twice_charge, character in branch_irrep_with_charge(tuple(label)).items():
        twice_nu = int(twice_delta) - twice_charge
        if twice_nu % 2:
            raise ValueError(
                f"Non-integral nu for label={label}, 2Delta={twice_delta}, 2J={twice_charge}"
            )
        nu = twice_nu // 2
        result[nu] = result.get(nu, D4(0)) + character
    return result


def axial_delta_nu_image(label, twice_delta):
    """Apply ``nu = Delta+J`` and return ``nu -> D4 character``.

    This is the right-moving form of the grading after the Type-IIA
    chirality reversal.  Equivalently, one may outer-conjugate the D5 label
    and retain ``nu = Delta-J``.
    """
    result = {}
    for twice_charge, character in branch_irrep_with_charge(tuple(label)).items():
        twice_nu = int(twice_delta) + twice_charge
        if twice_nu % 2:
            raise ValueError(
                f"Non-integral axial nu for label={label}, "
                f"2Delta={twice_delta}, 2J={twice_charge}"
            )
        nu = twice_nu // 2
        result[nu] = result.get(nu, D4(0)) + character
    return result


def add_graded(left, right, scale=1):
    result = dict(left)
    for grade, character in right.items():
        result[grade] = result.get(grade, D4(0)) + scale * character
        if result[grade] == D4(0):
            result.pop(grade)
    return dict(sorted(result.items()))


def image_of_terms(terms, signed=True):
    """Refine a sequence of ``(2Delta, coefficient, D5 label)`` terms."""
    result = {}
    for twice_delta, coefficient, label in terms:
        scale = int(coefficient)
        if signed:
            scale *= d5_parity(label)
        result = add_graded(
            result,
            delta_nu_image(tuple(label), int(twice_delta)),
            scale=scale,
        )
    return result


def axial_image_of_terms(terms, signed=True):
    """Refine terms using the Type-IIA right-moving relation ``nu=Delta+J``."""
    result = {}
    for twice_delta, coefficient, label in terms:
        scale = int(coefficient)
        if signed:
            scale *= d5_parity(label)
        result = add_graded(
            result,
            axial_delta_nu_image(tuple(label), int(twice_delta)),
            scale=scale,
        )
    return result
