"""Baseline-free oscillator-count refinement of chiral string primaries.

At fixed string level ``ell = sum n N_n`` this module retains the unweighted
oscillator count ``nu = sum N_n``.  Each positive SO(8) Fock coefficient is
divided by the common ``8_v + 8_s`` massive supersymmetry factor while the
original value of ``nu`` is retained.  Fermion parity is then restored as the
standard SO(8) supercharacter sign.

No protected SO(10) completion is imported.
"""

from functools import lru_cache

from sage.all import QQ, ZZ, WeylCharacterRing


D4 = WeylCharacterRing("D4", base_ring=QQ, style="coroots")
ONE = D4(0, 0, 0, 0)
V8 = D4(1, 0, 0, 0)
S8 = D4(0, 0, 0, 1)
QS_POSITIVE = V8 + S8


def _integer(value, description):
    if value not in ZZ:
        raise ValueError(f"Non-integral {description}: {value}")
    return int(value)


def d4_weight_to_dynkin(weight):
    x1, x2, x3, x4 = weight.to_vector()
    return (
        _integer(x1 - x2, "D4 label a1"),
        _integer(x2 - x3, "D4 label a2"),
        _integer(x3 - x4, "D4 label a3"),
        _integer(x3 + x4, "D4 label a4"),
    )


def d4_coefficients(character):
    return {
        d4_weight_to_dynkin(weight): _integer(coefficient, "D4 coefficient")
        for weight, coefficient in character.monomial_coefficients().items()
        if coefficient
    }


def d4_parity(label):
    """Return +1 on tensor representations and -1 on spinor representations."""
    return -1 if (label[2] + label[3]) % 2 else 1


def signed_supercharacter(character):
    result = D4(0)
    for label, coefficient in d4_coefficients(character).items():
        result += d4_parity(label) * coefficient * D4(*label)
    return result


def _dominant(weight):
    x1, x2, x3, x4 = weight.to_vector()
    return x1 >= x2 >= x3 and x3 >= abs(x4)


def divide_by_positive_qs(target):
    """Divide a positive D4 character by ``8_v + 8_s`` exactly."""
    remainder = target
    quotient = D4(0)
    omega_v = V8.highest_weight()
    omega_s = S8.highest_weight()

    while remainder != D4(0):
        coefficients = remainder.monomial_coefficients()
        dominant = [
            weight
            for weight, coefficient in coefficients.items()
            if coefficient > 0 and _dominant(weight)
        ]
        if not dominant:
            raise ValueError(f"No positive dominant weight in remainder: {remainder}")
        highest = max(dominant, key=lambda weight: tuple(weight.to_vector()))
        multiplicity = coefficients[highest]
        candidates = []
        for omega in (omega_v, omega_s):
            candidate_weight = highest - omega
            if not _dominant(candidate_weight):
                continue
            try:
                candidate = D4(candidate_weight)
            except (TypeError, ValueError):
                continue
            trial = remainder - multiplicity * QS_POSITIVE * candidate
            if all(value >= 0 for value in trial.monomial_coefficients().values()):
                candidates.append(candidate)
        if len(candidates) != 1:
            raise ValueError(
                "Oscillator-count quotient is not uniquely positive: "
                f"highest={highest}, candidates={candidates}"
            )
        quotient += multiplicity * candidates[0]
        remainder -= multiplicity * QS_POSITIVE * candidates[0]
    return quotient


@lru_cache(maxsize=None)
def oscillator_factor(mode, max_level):
    """Return ``{(ell,nu): character}`` for one oscillator mode."""
    factor = {(0, 0): ONE}
    for occupation in range(1, max_level // mode + 1):
        coefficient = D4(0)
        for bosons in range(occupation + 1):
            fermions = occupation - bosons
            if fermions <= 8:
                coefficient += (
                    V8.symmetric_power(bosons)
                    * S8.exterior_power(fermions)
                )
        factor[mode * occupation, occupation] = coefficient
    return factor


def _multiply(left, right, max_level):
    result = {}
    for (ell_left, nu_left), char_left in left.items():
        for (ell_right, nu_right), char_right in right.items():
            level = ell_left + ell_right
            if level > max_level:
                continue
            key = (level, nu_left + nu_right)
            result[key] = result.get(key, D4(0)) + char_left * char_right
    return result


def refined_fock_space(max_level):
    result = {(0, 0): ONE}
    for mode in range(1, max_level + 1):
        result = _multiply(result, oscillator_factor(mode, max_level), max_level)
    return result


def derive_refined_primaries(max_level):
    """Return positive and signed primary characters indexed by ``(ell,nu)``."""
    fock = refined_fock_space(max_level)
    positive = {}
    signed = {}
    for level in range(1, max_level + 1):
        for excitation_number in range(1, level + 1):
            target = fock.get((level, excitation_number), D4(0))
            if target == D4(0):
                continue
            quotient = divide_by_positive_qs(target)
            if QS_POSITIVE * quotient != target:
                raise ValueError(
                    f"Failed refined quotient at ell={level}, nu={excitation_number}"
                )
            positive[level, excitation_number] = quotient
            signed[level, excitation_number] = signed_supercharacter(quotient)
    return {
        "fock": fock,
        "positive": positive,
        "signed": signed,
    }


def level_character(table, level):
    return sum(
        (
            character
            for (candidate_level, _nu), character in table.items()
            if candidate_level == level
        ),
        D4(0),
    )
