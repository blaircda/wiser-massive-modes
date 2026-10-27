"""TK6B.6c: closed ``D4`` boundary formula for the scalar tail.

Compose the equal-rank ``D4 -> B4`` Dirac fold with the six-ray one-row
coordinate of the all-chiral ``B4 -> D5`` section.  Although neither this
composition nor the Dirac fold is multiplicative, its value on a ``D4``
irrep is supported on only nine rays of the dominant chamber.  Away from
five low endpoints every value is a monomial times ``(1-x)^2``.

This module records the resulting all-label formula and verifies it directly
against the Weyl-alternant implementation.  It then applies the formula to
the Green--Schwarz telescope *before* its outer ``(1-q)`` factor.  Hence its
diagonal coefficients are the negatives of the proposed TK6B.6 scalar-tail
coefficients from degree nine onward.  A fixed-arm Plucker factorization and
bordered Weyl determinant subsequently collapse the infinite ray family to a
degree-seven character numerator.  Self-adjoint cancellation of the vector
tower and the relative ``D4/B4`` Weyl measure reduce the complete index once
more to six fixed low-form ``B4`` functionals.  Alternating inversion along
the five exterior powers then rewrites their sign as one short primitive-form
dominance inequality.

No protected ``SO(10)`` completion is imported.
"""

import argparse
import sys
import time
from functools import lru_cache
from itertools import product
from math import comb

from sage.all import PolynomialRing, QQ, ZZ, matrix

import hft_so9
from trajectory_kernel import cumulative_regge_uplift
from trajectory_kernel import hft_analytic_support
from trajectory_kernel import scalar_tail


D4 = hft_analytic_support.D4
B4 = hft_analytic_support.B4
POLYNOMIAL_RING = PolynomialRing(ZZ, names=("x",))
X = POLYNOMIAL_RING.gen()
ARM_POLYNOMIAL_RING = PolynomialRing(QQ, names=("L",))
L_VARIABLE = ARM_POLYNOMIAL_RING.gen()

RAY_GROUPS = {
    (0, 0, 0): "tensor",
    (1, 0, 0): "tensor",
    (2, 0, 0): "tensor",
    (0, 0, 2): "spinor_0",
    (0, 1, 1): "spinor_0",
    (1, 0, 2): "spinor_1",
    (1, 1, 1): "spinor_1",
    (0, 1, 3): "spinor_2",
    (0, 2, 2): "spinor_2",
}

# ``coefficient * x^(a + shift)`` before multiplication by ``(x - 1)^2``.
UNIFORM_RAY_DATA = {
    (0, 0, 0): ("tensor", 1, -2),
    (1, 0, 0): ("tensor", -2, -1),
    (2, 0, 0): ("tensor", 1, 0),
    (0, 0, 2): ("spinor_0", -3, -1),
    (0, 1, 1): ("spinor_0", 3, -1),
    (1, 0, 2): ("spinor_1", 2, 0),
    (1, 1, 1): ("spinor_1", -2, 0),
    (0, 1, 3): ("spinor_2", -1, 0),
    (0, 2, 2): ("spinor_2", 1, 0),
}

# Difference between the true endpoint polynomial and the uniform Laurent
# continuation ``coefficient*x^(a+shift)*(x-1)^2``.
ENDPOINT_CORRECTIONS = {
    (0, 0, 0, 0): {-2: -1, -1: 2},
    (1, 0, 0, 0): {-1: -1},
    (0, 1, 0, 0): {-1: 2, 0: -1},
    (0, 0, 0, 2): {-1: 3, 0: -2},
    (0, 0, 1, 1): {-1: -3, 0: 2},
}

# After removing the first (long) row, the nine stable rays are exactly nine
# of the ten Young diagrams contained in a 3-by-2 rectangle.  The missing
# tail is (2, 2, 2).  These coefficients are the transverse part of the
# Dirac/Mobius index at fixed first modified-Frobenius arm.
FROBENIUS_TAIL_COEFFICIENTS = {
    (): 1,
    (1,): -2,
    (2,): 1,
    (1, 1): 3,
    (1, 1, 1): -3,
    (2, 1): -2,
    (2, 1, 1): 2,
    (2, 2): 1,
    (2, 2, 1): -1,
}

# The ten partitions in the 3-by-2 rectangle index the standard basis of
# wedge^3(Z^5).  With the natural Hodge signs, the transverse coefficients
# are the complementary 2-by-2 minors of the following rank-two matrix.  Its
# first row is implicit; PLUCKER_GRADING is its second row.
PLUCKER_GRADING = (0, 0, 1, 2, 3)


def d4_tensor_partition(label):
    """Return the unsigned four-row tensor diagram of a ``D4`` label.

    All nine rays in this module are tensorial.  A nonzero fourth orthogonal
    coordinate distinguishes the two associated ``Spin(8)`` orientations;
    taking its absolute value deliberately forgets that orientation and
    retains the underlying Young diagram used by super-Howe duality.
    """
    a, b, c, d = map(int, label)
    if min(a, b, c, d) < 0 or (c + d) % 2:
        raise ValueError(f"Expected a tensorial D4 label: {label}")
    half_spin_sum = (c + d) // 2
    rows = (
        a + b + half_spin_sum,
        b + half_spin_sum,
        half_spin_sum,
        abs(d - c) // 2,
    )
    if not rows[0] >= rows[1] >= rows[2] >= rows[3] >= 0:
        raise ValueError(f"Invalid D4 tensor partition for {label}: {rows}")
    return rows


def frobenius_ray_table(first_arm=1):
    """Return the nine stable rays at one fixed first Frobenius arm.

    If the first modified-Frobenius arm is ``L``, every uniform monomial in
    the nine-ray formula is ``x^(L-1)``.  Thus the apparently unrelated rays
    form one finite transverse Euler index at each ``L >= 1``.
    """
    first_arm = int(first_arm)
    if first_arm < 1:
        raise ValueError("The stable Frobenius table requires first_arm >= 1")
    records = []
    for transverse, (group, coefficient, shift) in UNIFORM_RAY_DATA.items():
        # The first arm is affine in a with slope one.  Evaluate at a=0 to
        # recover its constant offset and then solve for a.
        trial_partition = d4_tensor_partition((0,) + transverse)
        trial_arms, _trial_heights = hft_analytic_support.modified_frobenius(
            trial_partition
        )
        arm_offset = trial_arms[0] if trial_arms else -1
        a = first_arm - arm_offset
        label = (a,) + transverse
        partition = d4_tensor_partition(label)
        arms, heights = hft_analytic_support.modified_frobenius(partition)
        tail = tuple(value for value in partition[1:] if value)
        records.append(
            {
                "label": label,
                "group": group,
                "coefficient": coefficient,
                "shift": shift,
                "partition": partition,
                "tail": tail,
                "arms": arms,
                "heights": heights,
                "monomial_exponent": a + shift,
            }
        )
    return tuple(records)


def frobenius_ray_audit(maximum_first_arm=8):
    """Check the fixed-arm Young-diagram organization of all nine rays."""
    maximum_first_arm = int(maximum_first_arm)
    records = []
    failures = []
    expected_tails = set(FROBENIUS_TAIL_COEFFICIENTS)
    for first_arm in range(1, maximum_first_arm + 1):
        table = frobenius_ray_table(first_arm)
        observed_tails = {record["tail"] for record in table}
        for record in table:
            exact = (
                record["arms"][0] == first_arm
                and len(record["arms"]) <= 2
                and record["monomial_exponent"] == first_arm - 1
                and FROBENIUS_TAIL_COEFFICIENTS.get(record["tail"])
                == record["coefficient"]
            )
            checked = dict(record, first_arm=first_arm, exact=exact)
            records.append(checked)
            if not exact:
                failures.append(checked)
        if observed_tails != expected_tails:
            failures.append(
                {
                    "first_arm": first_arm,
                    "expected_tails": expected_tails,
                    "observed_tails": observed_tails,
                    "exact": False,
                }
            )
    return {
        "maximum_first_arm": maximum_first_arm,
        "records": tuple(records),
        "failures": tuple(failures),
        "all_exact": not failures,
    }


def tail_plucker_data(tail):
    """Return the Grassmannian subset and decomposable-minor coefficient.

    A partition ``tail`` in the 3-by-2 rectangle maps to the three-subset

        I = {tail_3 + 1, tail_2 + 2, tail_1 + 3} of {1,...,5}.

    If ``J=(j_1,j_2)`` is its complement, the coefficient is the Hodge sign
    times ``v[j_2]-v[j_1]`` for ``v=(0,0,1,2,3)``.  These are the Plucker
    coordinates of the row span of ``(1,1,1,1,1)`` and ``v``.
    """
    tail = tuple(map(int, tail))
    padded = tail + (0,) * (3 - len(tail))
    if (
        len(tail) > 3
        or any(value < 0 or value > 2 for value in padded)
        or not padded[0] >= padded[1] >= padded[2]
    ):
        raise ValueError(f"Expected a partition in the 3-by-2 rectangle: {tail}")
    subset = tuple(padded[2 - index] + index + 1 for index in range(3))
    complement = tuple(value for value in range(1, 6) if value not in subset)
    concatenated = subset + complement
    inversions = sum(
        concatenated[left] > concatenated[right]
        for left in range(5)
        for right in range(left + 1, 5)
    )
    hodge_sign = -1 if inversions % 2 else 1
    first, second = (value - 1 for value in complement)
    minor = PLUCKER_GRADING[second] - PLUCKER_GRADING[first]
    return {
        "tail": tail,
        "subset": subset,
        "complement": complement,
        "hodge_sign": hodge_sign,
        "minor": minor,
        "coefficient": hodge_sign * minor,
    }


def transverse_plucker_audit():
    """Verify all ten complementary minors, including the missing zero."""
    tails = tuple(FROBENIUS_TAIL_COEFFICIENTS) + ((2, 2, 2),)
    records = tuple(tail_plucker_data(tail) for tail in tails)
    failures = tuple(
        record
        for record in records
        if record["coefficient"]
        != FROBENIUS_TAIL_COEFFICIENTS.get(record["tail"], 0)
    )
    return {
        "matrix_rows": ((1, 1, 1, 1, 1), PLUCKER_GRADING),
        "records": records,
        "failures": failures,
        "all_exact": not failures,
    }


def _d4_determinant_component(exponents, variables, sign):
    """Evaluate one of the two determinant components of a D-type alternant."""
    return matrix(
        QQ,
        4,
        4,
        lambda row, column: (
            variables[row] ** exponents[column]
            + sign * variables[row] ** (-exponents[column])
        ),
    ).det()


def _d4_alternant_value(exponents, variables):
    """Evaluate the even-sign ``D4`` Weyl alternant at rational points."""
    return (
        _d4_determinant_component(exponents, variables, 1)
        + _d4_determinant_component(exponents, variables, -1)
    ) / 2


def _bordered_determinant(first_exponent, variables, sign):
    """Evaluate the six-column determinant supplied by the Plucker factor."""
    exponents = (int(first_exponent), 0, 1, 2, 3, 4)
    first_row = (0, 1, 1, 1, 1, 1)
    second_row = (0,) + PLUCKER_GRADING
    return matrix(
        QQ,
        6,
        6,
        lambda row, column: (
            variables[row] ** exponents[column]
            + sign * variables[row] ** (-exponents[column])
            if row < 4
            else (first_row[column] if row == 4 else second_row[column])
        ),
    ).det()


def bordered_weyl_audit(maximum_first_arm=5):
    """Check the bordered-determinant form of the nine Weyl numerators.

    This is only a finite convention audit.  The identity for arbitrary
    first arm is the Laplace expansion of the displayed determinant, using
    the all-arm Plucker formula checked above.
    """
    variables = tuple(map(QQ, (2, 3, 5, 7)))
    records = []
    failures = []
    for first_arm in range(1, int(maximum_first_arm) + 1):
        direct = QQ.zero()
        for record in frobenius_ray_table(first_arm):
            a, b, c, d = record["label"]
            exponents = (
                a + b + (c + d) // 2 + 3,
                b + (c + d) // 2 + 2,
                (c + d) // 2 + 1,
                (d - c) // 2,
            )
            direct += record["coefficient"] * _d4_alternant_value(
                exponents, variables
            )
        bordered = -(
            _bordered_determinant(first_arm + 4, variables, 1)
            + _bordered_determinant(first_arm + 4, variables, -1)
        ) / 2
        record = {
            "first_arm": first_arm,
            "direct": direct,
            "bordered": bordered,
            "exact": direct == bordered,
        }
        records.append(record)
        if not record["exact"]:
            failures.append(record)
    return {
        "records": tuple(records),
        "failures": tuple(failures),
        "all_exact": not failures,
    }


def virtual_dimension_polynomial():
    """Return the all-arm Weyl dimension of the nine-term virtual character."""
    rho = (3, 2, 1, 0)
    denominator = 1
    for left in range(4):
        for right in range(left + 1, 4):
            denominator *= rho[left] ** 2 - rho[right] ** 2
    result = ARM_POLYNOMIAL_RING.zero()
    for record in frobenius_ray_table(1):
        a, b, c, d = record["label"]
        exponents = (
            L_VARIABLE + 4,
            b + (c + d) // 2 + 2,
            (c + d) // 2 + 1,
            (d - c) // 2,
        )
        numerator = ARM_POLYNOMIAL_RING.one()
        for left in range(4):
            for right in range(left + 1, 4):
                numerator *= exponents[left] ** 2 - exponents[right] ** 2
        result += record["coefficient"] * numerator / denominator
    return ARM_POLYNOMIAL_RING(result)


@lru_cache(maxsize=None)
def stable_virtual_character(first_arm):
    """Return the nine-term virtual ``D4`` character at fixed stable arm."""
    return sum(
        (
            record["coefficient"] * D4(*record["label"])
            for record in frobenius_ray_table(int(first_arm))
        ),
        D4(0),
    )


def stable_ray_numerator_audit(maximum_degree=10):
    """Audit the finite numerator of the all-arm character series.

    If ``D_V(t)=sum_j (-t)^j wedge^j(V)``, the bordered determinant proves

        D_V(t) sum_{L>=1} t^(L-1) K_L = N(t),

    with ``deg N <= 7``.  The finite computation below checks the character
    coefficients and their dimensions across and just beyond that boundary.
    """
    maximum_degree = max(8, int(maximum_degree))
    exterior = tuple(
        hft_analytic_support.D4_VECTOR.exterior_power(degree)
        for degree in range(9)
    )
    coefficients = []
    for degree in range(maximum_degree + 1):
        value = D4(0)
        for exterior_degree in range(min(8, degree) + 1):
            value += (
                (-1) ** exterior_degree
                * exterior[exterior_degree]
                * stable_virtual_character(degree - exterior_degree + 1)
            )
        coefficients.append(value)
    finite_degree_seven = all(
        coefficients[degree] == D4(0)
        for degree in range(8, maximum_degree + 1)
    )
    dimension_exact = all(
        int(coefficients[degree].degree())
        == 15 * ((-1) ** degree) * comb(7, degree)
        for degree in range(8)
    )
    return {
        "maximum_degree": maximum_degree,
        "coefficients": tuple(coefficients),
        "finite_degree_seven": finite_degree_seven,
        "dimension_exact": dimension_exact,
        "all_exact": finite_degree_seven and dimension_exact,
    }


def d4_outer_swap(character):
    """Exchange the two ``D4`` spinor nodes in a virtual character."""
    result = D4(0)
    for highest_weight, coefficient in character.monomial_coefficients().items():
        twice = tuple(int(2 * value) for value in highest_weight.to_vector())
        a, b, c, d = hft_analytic_support.d4_dynkin_from_twice_orthogonal(
            twice
        )
        result += coefficient * D4(a, b, d, c)
    return result


def b4_scalar_kernel_coefficients():
    """Return the six fixed ``B4`` coefficients of the scalar index."""
    exterior = tuple(B4(1, 0, 0, 0).exterior_power(degree) for degree in range(5))
    partial = tuple(
        sum(
            ((-1) ** degree * exterior[degree] for degree in range(stop + 1)),
            B4(0),
        )
        for stop in range(5)
    )
    return (
        partial[3],
        partial[4] + partial[2],
        partial[3] + partial[1],
        partial[2] + partial[0],
        partial[1],
        partial[0],
    )


def finite_b4_kernel_audit(numerator_audit=None):
    """Reduce the scalar index to six fixed ``B4`` character functionals.

    Moving the self-dual symmetric-vector tower through the representation
    inner product cancels the vector-exterior factor in ``G``.  The remaining
    stable curvature plus actual endpoint contribution is a finite ``D4``
    polynomial.  Its outer-symmetric part is one half of the square of the
    relative Weyl denominator times the restriction of the six ``B4``
    characters returned above.
    """
    if numerator_audit is None:
        numerator_audit = stable_ray_numerator_audit(9)
    numerator = numerator_audit["coefficients"][:8]
    vector = D4(1, 0, 0, 0)
    adjoint = D4(0, 1, 0, 0)
    four_form = D4(0, 0, 0, 2)
    three_form = D4(0, 0, 1, 1)
    endpoint_kernel = (
        D4(0, 0, 0, 0)
        - 2 * vector
        + 3 * adjoint
        + 4 * four_form
        - 4 * three_form,
        vector - 2 * adjoint - 3 * four_form + 3 * three_form,
    )
    exterior = tuple(
        (-1) ** degree
        * hft_analytic_support.D4_VECTOR.exterior_power(degree)
        for degree in range(9)
    )
    final_kernel = []
    for degree in range(10):
        value = D4(0)
        if degree < len(numerator):
            value += numerator[degree]
        if 0 <= degree - 1 < len(numerator):
            value -= 2 * numerator[degree - 1]
        if 0 <= degree - 2 < len(numerator):
            value += numerator[degree - 2]
        for exterior_degree, exterior_character in enumerate(exterior):
            endpoint_degree = degree - exterior_degree
            if 0 <= endpoint_degree < len(endpoint_kernel):
                value += (
                    exterior_character * endpoint_kernel[endpoint_degree]
                )
        final_kernel.append(value)

    b4_kernel = b4_scalar_kernel_coefficients()
    d4_exterior = tuple(
        hft_analytic_support.D4_VECTOR.exterior_power(degree)
        for degree in range(5)
    )
    expected_restrictions = (
        -d4_exterior[3],
        d4_exterior[4] + d4_exterior[2],
        -d4_exterior[3] - d4_exterior[1],
        d4_exterior[2] + d4_exterior[0],
        -d4_exterior[1],
        d4_exterior[0],
    )
    koszul_restriction_exact = all(
        b4_kernel[degree].branch(D4) == expected_restrictions[degree]
        for degree in range(6)
    )
    relative_denominator = (
        hft_analytic_support.D4_OSCILLATOR_SPINOR
        - hft_analytic_support.D4_OTHER_SPINOR
    )
    records = []
    failures = []
    for degree, b4_character in enumerate(b4_kernel):
        symmetric_part = (
            final_kernel[degree]
            + d4_outer_swap(final_kernel[degree])
        ) / 2
        expected = (
            relative_denominator ** 2
            * b4_character.branch(D4)
            / 2
        )
        record = {
            "degree": degree,
            "symmetric_part": symmetric_part,
            "expected": expected,
            "exact": symmetric_part == expected,
        }
        records.append(record)
        if not record["exact"]:
            failures.append(record)
    closes_at_five = all(
        final_kernel[degree] == D4(0)
        for degree in range(6, len(final_kernel))
    )
    return {
        "numerator_audit": numerator_audit,
        "final_d4_kernel": tuple(final_kernel),
        "b4_kernel": b4_kernel,
        "expected_restrictions": expected_restrictions,
        "koszul_restriction_exact": koszul_restriction_exact,
        "records": tuple(records),
        "failures": tuple(failures),
        "closes_at_five": closes_at_five,
        "all_exact": (
            not failures and closes_at_five and koszul_restriction_exact
        ),
    }


def character_inner_product(left, right):
    """Return the irreducible-character inner product in one Weyl ring."""
    right_coefficients = right.monomial_coefficients()
    return sum(
        coefficient * right_coefficients.get(highest_weight, 0)
        for highest_weight, coefficient in left.monomial_coefficients().items()
    )


def b4_scalar_convolution(maximum_degree):
    """Evaluate the six-term kernel on independently derived HFT primaries."""
    maximum_degree = int(maximum_degree)
    _numerator, levels = hft_so9.derive_hft_spectrum(maximum_degree + 1)
    primaries = {
        degree: levels[degree + 1]
        for degree in range(maximum_degree + 1)
    }
    kernel = b4_scalar_kernel_coefficients()
    coefficients = []
    for degree in range(maximum_degree + 1):
        coefficients.append(
            sum(
                character_inner_product(
                    kernel[kernel_degree],
                    primaries[degree - kernel_degree],
                )
                for kernel_degree in range(min(5, degree) + 1)
            )
        )
    return {
        "maximum_degree": maximum_degree,
        "kernel": kernel,
        "primaries": primaries,
        "coefficients": tuple(map(int, coefficients)),
    }


def primitive_form_dominance_audit(maximum_degree, convolution=None):
    """Rewrite the six-term index as one primitive-form dominance.

    Put ``e_j = exterior^j(9)`` and

        h_k(d) = (-1)^k <sum_{j=0}^k (-1)^j e_j, Q_d>.

    If ``H_k(q)`` is the corresponding scalar series, define

        D = H_3 - q H_2 + q^2 H_1 - q^3 H_0.

    Direct algebra in the ``B4`` representation ring gives

        <C(q), Z_m(q)> = -(1+q^2) D(q) + q H_4(q).

    A second alternating inversion

        Pi_k = H_k - q H_(k-1) + ... + (-q)^k H_0

    has ``Pi_3 = D`` and turns the desired correction into the adjacent
    dominance ``Pi_3(N) - Pi_4(N-1)``.

    Equivalently, if ``x`` marks exterior degree, the complete kernel is

        [x^4] Lambda_x(9) / ((1+x)(1+qx)) * (q-x).

    The function verifies this identity independently from the six-term
    convolution and records finite-degree sign evidence.  It does not treat
    that evidence as an all-orders positivity proof.
    """
    maximum_degree = int(maximum_degree)
    if convolution is None:
        convolution = b4_scalar_convolution(maximum_degree)
    if int(convolution["maximum_degree"]) != maximum_degree:
        raise ValueError("Convolution cutoff does not match maximum_degree")

    primaries = convolution["primaries"]
    exterior = tuple(
        B4(1, 0, 0, 0).exterior_power(degree)
        for degree in range(5)
    )
    partial = tuple(
        sum(
            (
                (-1) ** exterior_degree * exterior[exterior_degree]
                for exterior_degree in range(stop + 1)
            ),
            B4(0),
        )
        for stop in range(5)
    )

    low_form_multiplicities = tuple(
        tuple(
            int(character_inner_product(form, primaries[degree]))
            for form in exterior
        )
        for degree in range(maximum_degree + 1)
    )
    primitive_series = tuple(
        tuple(
            int(
                (-1) ** stop
                * character_inner_product(partial[stop], primaries[degree])
            )
            for degree in range(maximum_degree + 1)
        )
        for stop in range(5)
    )

    def coefficient(series, degree):
        return series[degree] if 0 <= degree <= maximum_degree else 0

    dominance_base = tuple(
        coefficient(primitive_series[3], degree)
        - coefficient(primitive_series[2], degree - 1)
        + coefficient(primitive_series[1], degree - 2)
        - coefficient(primitive_series[0], degree - 3)
        for degree in range(maximum_degree + 1)
    )
    double_primitive_series = tuple(
        tuple(
            sum(
                (-1) ** shift
                * coefficient(
                    primitive_series[exterior_degree - shift],
                    degree - shift,
                )
                for shift in range(exterior_degree + 1)
            )
            for degree in range(maximum_degree + 1)
        )
        for exterior_degree in range(5)
    )
    negated_index = tuple(
        coefficient(dominance_base, degree)
        + coefficient(dominance_base, degree - 2)
        - coefficient(primitive_series[4], degree - 1)
        for degree in range(maximum_degree + 1)
    )
    adjacent_difference = tuple(
        coefficient(double_primitive_series[3], degree)
        - coefficient(double_primitive_series[4], degree - 1)
        for degree in range(maximum_degree + 1)
    )
    reconstructed_index = tuple(-value for value in negated_index)

    # Verify the reorganization before applying it to any spectrum.
    reconstructed_kernel = []
    for degree in range(6):
        value = B4(0)
        if 0 <= degree <= 3:
            value += partial[3 - degree]
        if 0 <= degree - 2 <= 3:
            value += partial[3 - (degree - 2)]
        if degree == 1:
            value += partial[4]
        reconstructed_kernel.append(value)
    kernel_identity_exact = (
        tuple(reconstructed_kernel) == b4_scalar_kernel_coefficients()
    )
    primitive_characters = tuple(
        (-1) ** degree * partial[degree]
        for degree in range(5)
    )
    compact_kernel = []
    for degree in range(6):
        value = B4(0)
        # q Pi_4 contributes at q^(shift+1).
        shift = degree - 1
        if 0 <= shift <= 4:
            value += (-1) ** shift * primitive_characters[4 - shift]
        # -Pi_3 contributes at q^shift.
        shift = degree
        if 0 <= shift <= 3:
            value -= (-1) ** shift * primitive_characters[3 - shift]
        compact_kernel.append(value)
    compact_kernel_exact = (
        tuple(compact_kernel) == b4_scalar_kernel_coefficients()
    )
    convolution_identity_exact = (
        reconstructed_index == convolution["coefficients"]
    )
    double_primitive_identity_exact = (
        double_primitive_series[3] == dominance_base
        and adjacent_difference == negated_index
    )
    evidence_start = min(6, maximum_degree + 1)
    tail_start = min(9, maximum_degree + 1)
    return {
        "maximum_degree": maximum_degree,
        "low_form_multiplicities": low_form_multiplicities,
        "primitive_series": primitive_series,
        "double_primitive_series": double_primitive_series,
        "dominance_base": dominance_base,
        "negated_index": negated_index,
        "adjacent_difference": adjacent_difference,
        "reconstructed_index": reconstructed_index,
        "kernel_identity_exact": kernel_identity_exact,
        "compact_kernel": tuple(compact_kernel),
        "compact_kernel_exact": compact_kernel_exact,
        "convolution_identity_exact": convolution_identity_exact,
        "double_primitive_identity_exact": double_primitive_identity_exact,
        "primitive_nonnegative_from_six_in_range": all(
            primitive_series[stop][degree] >= 0
            for stop in range(5)
            for degree in range(evidence_start, maximum_degree + 1)
        ),
        "base_nonnegative_from_six_in_range": all(
            dominance_base[degree] >= 0
            for degree in range(evidence_start, maximum_degree + 1)
        ),
        "adjacent_series_nonnegative_from_six_in_range": all(
            double_primitive_series[exterior_degree][degree] >= 0
            for exterior_degree in (3, 4)
            for degree in range(evidence_start, maximum_degree + 1)
        ),
        "dominance_from_nine_in_range": all(
            negated_index[degree] >= 0
            for degree in range(tail_start, maximum_degree + 1)
        ),
        "all_exact": (
            kernel_identity_exact
            and compact_kernel_exact
            and convolution_identity_exact
            and double_primitive_identity_exact
        ),
    }


def closed_irrep_polynomial(label):
    """Return the nine-ray formula for one ``D4`` Dynkin label.

    The output is

    ``sum_l Phi_l(V_label) x^l``,

    where ``Phi_l`` is the one-row coordinate after Dirac folding.  The
    exceptional formulas are exactly the endpoints at which a formal
    negative power of ``x`` would cross the dominant wall.
    """
    a, b, c, d = map(int, label)
    if min(a, b, c, d) < 0:
        raise ValueError(f"Invalid D4 Dynkin label: {label}")

    transverse = (b, c, d)
    if transverse == (0, 0, 0):
        if a == 0:
            return POLYNOMIAL_RING.one()
        if a == 1:
            return X - 2
        return X ** (a - 2) * (X - 1) ** 2
    if transverse == (1, 0, 0):
        if a == 0:
            return -2 * X + 3
        return -2 * X ** (a - 1) * (X - 1) ** 2
    if transverse == (2, 0, 0):
        return X ** a * (X - 1) ** 2
    if transverse == (0, 0, 2):
        if a == 0:
            return -3 * X + 4
        return -3 * X ** (a - 1) * (X - 1) ** 2
    if transverse == (0, 1, 1):
        if a == 0:
            return 3 * X - 4
        return 3 * X ** (a - 1) * (X - 1) ** 2
    interior_rays = {
        (1, 0, 2): 2,
        (1, 1, 1): -2,
        (0, 1, 3): -1,
        (0, 2, 2): 1,
    }
    coefficient = interior_rays.get(transverse)
    if coefficient is not None:
        return coefficient * X ** a * (X - 1) ** 2
    return POLYNOMIAL_RING.zero()


def alternant_irrep_polynomial(label):
    """Evaluate the same functional through the independent Weyl fold."""
    table = hft_analytic_support.d4_dirac_dominant_table(D4(*label))
    maximum_ell = max((entry[0] for entry in table), default=0) + 2
    return sum(
        cumulative_regge_uplift.one_row_chiral_coordinate(table, ell)
        * X ** ell
        for ell in range(maximum_ell + 1)
    )


def formula_audit(maximum_label_sum=7):
    """Compare the closed formula with Weyl alternants on a finite simplex."""
    maximum_label_sum = int(maximum_label_sum)
    records = []
    failures = []
    for label in product(range(maximum_label_sum + 1), repeat=4):
        if sum(label) > maximum_label_sum:
            continue
        closed = closed_irrep_polynomial(label)
        alternant = alternant_irrep_polynomial(label)
        record = {
            "label": label,
            "closed": closed,
            "alternant": alternant,
            "exact": closed == alternant,
        }
        records.append(record)
        if not record["exact"]:
            failures.append(record)
    return {
        "maximum_label_sum": maximum_label_sum,
        "records": tuple(records),
        "failures": tuple(failures),
        "all_exact": not failures,
    }


def character_polynomial(character):
    """Apply the closed boundary functional to a virtual ``D4`` character."""
    result = POLYNOMIAL_RING.zero()
    for highest_weight, coefficient in character.monomial_coefficients().items():
        twice = tuple(int(2 * value) for value in highest_weight.to_vector())
        label = hft_analytic_support.d4_dynkin_from_twice_orthogonal(twice)
        result += int(coefficient) * closed_irrep_polynomial(label)
    return result


def weyl_numerator_table(character):
    """Return the doubled-weight table of ``A_rho * character``.

    This is the constant-term bridge to the oscillator product: a dominant
    coefficient at ``lambda + rho`` is exactly the multiplicity of
    ``V_lambda``.  It avoids any conceptual dependence on irreducible
    decomposition when the input character is supplied as a weight product.
    """
    weights = hft_analytic_support._twice_weight_table(character)
    alternant = hft_analytic_support.d4_weyl_orbit_with_sign((6, 4, 2, 0))
    result = {}
    for rho_weight, sign in alternant:
        for weight, multiplicity in weights.items():
            exponent = tuple(
                rho_weight[index] + weight[index]
                for index in range(4)
            )
            result[exponent] = (
                result.get(exponent, 0) + sign * multiplicity
            )
    return {exponent: value for exponent, value in result.items() if value}


def weyl_numerator_audit(maximum_degree=4):
    """Check dominant ray extraction from the weight numerator of ``G``."""
    characters = pre_telescoping_coefficients(maximum_degree)
    records = []
    failures = []
    for degree, character in characters.items():
        numerator = weyl_numerator_table(character)
        for highest_weight, coefficient in character.monomial_coefficients().items():
            highest = tuple(
                int(2 * value) for value in highest_weight.to_vector()
            )
            shifted = tuple(
                highest[index] + (6, 4, 2, 0)[index]
                for index in range(4)
            )
            record = {
                "degree": degree,
                "shifted_weight": shifted,
                "expected": int(coefficient),
                "observed": int(numerator.get(shifted, 0)),
            }
            records.append(record)
            if record["expected"] != record["observed"]:
                failures.append(record)
    return {
        "maximum_degree": int(maximum_degree),
        "records": tuple(records),
        "failures": tuple(failures),
        "all_exact": not failures,
    }


def pre_telescoping_coefficients(maximum_degree):
    """Return coefficients of ``G(q)=F(q)/(1-q)`` in the ``D4`` ring."""
    maximum_degree = int(maximum_degree)
    terms = hft_analytic_support.d4_telescoping_terms(maximum_degree)
    f_coefficients = {degree: D4(0) for degree in range(maximum_degree + 1)}
    for series in terms.values():
        for degree, character in series.items():
            f_coefficients[degree] += character
    running = D4(0)
    result = {}
    for degree in range(maximum_degree + 1):
        running += f_coefficients[degree]
        result[degree] = running
    return result


def diagonal_from_pre_telescope(maximum_degree):
    """Compute ``[q^N] Phi_q(G(q))`` from the nine-ray formula."""
    maximum_degree = int(maximum_degree)
    coefficients = [0] * (maximum_degree + 1)
    characters = pre_telescoping_coefficients(maximum_degree)
    polynomials = {}
    for degree, character in characters.items():
        polynomial = character_polynomial(character)
        polynomials[degree] = polynomial
        for exponent, coefficient in polynomial.dict().items():
            ell = int(exponent[0] if isinstance(exponent, tuple) else exponent)
            if degree + ell <= maximum_degree:
                coefficients[degree + ell] += int(coefficient)
    return {
        "maximum_degree": maximum_degree,
        "characters": characters,
        "polynomials": polynomials,
        "diagonal": tuple(coefficients),
    }


def grouped_pre_telescoping_diagonal(maximum_degree):
    """Split the nine-ray index into its four natural transverse pairs."""
    maximum_degree = int(maximum_degree)
    characters = pre_telescoping_coefficients(maximum_degree)
    groups = {
        name: [0] * (maximum_degree + 1)
        for name in set(RAY_GROUPS.values())
    }
    for degree, character in characters.items():
        for highest_weight, coefficient in character.monomial_coefficients().items():
            twice = tuple(int(2 * value) for value in highest_weight.to_vector())
            label = hft_analytic_support.d4_dynkin_from_twice_orthogonal(twice)
            group = RAY_GROUPS.get(label[1:])
            if group is None:
                continue
            polynomial = closed_irrep_polynomial(label)
            for exponent, value in polynomial.dict().items():
                ell = int(
                    exponent[0] if isinstance(exponent, tuple) else exponent
                )
                if degree + ell <= maximum_degree:
                    groups[group][degree + ell] += (
                        int(coefficient) * int(value)
                    )
    grouped = {name: tuple(values) for name, values in groups.items()}
    demand = tuple(
        grouped["tensor"][degree] + grouped["spinor_2"][degree]
        for degree in range(maximum_degree + 1)
    )
    supply = tuple(
        -grouped["spinor_0"][degree] - grouped["spinor_1"][degree]
        for degree in range(maximum_degree + 1)
    )
    margin = tuple(
        supply[degree] - demand[degree]
        for degree in range(maximum_degree + 1)
    )
    return {
        "groups": grouped,
        "demand": demand,
        "supply": supply,
        "margin": margin,
        "tail_dominance": all(
            margin[degree] >= 0
            for degree in range(9, maximum_degree + 1)
        ),
    }


def uniform_curvature_decomposition(maximum_degree):
    """Split the index into uniform second differences and wall endpoints.

    The nine interior formulas are Laurent monomials times ``(1-q)^2``.
    Their monomial coefficients are *signed*, so they are not Hilbert series
    and do not by themselves support a literal injection of state sets.  This
    routine exposes the correct target: a discrete-curvature inequality plus
    five explicit endpoint series.
    """
    maximum_degree = int(maximum_degree)
    minimum_degree = -2
    # The uniform Laurent continuation contains powers down to q^(-2).
    # Two look-ahead coefficients are therefore needed to separate curvature
    # and wall terms without a cutoff artefact at the last two degrees.
    characters = pre_telescoping_coefficients(maximum_degree + 2)
    group_names = set(RAY_GROUPS.values())
    raw_groups = {
        name: {
            degree: 0
            for degree in range(minimum_degree, maximum_degree + 1)
        }
        for name in group_names
    }
    wall = {
        degree: 0
        for degree in range(minimum_degree, maximum_degree + 1)
    }
    stable_raw = {degree: 0 for degree in range(maximum_degree + 1)}
    actual_wall = {degree: 0 for degree in range(maximum_degree + 1)}

    for degree, character in characters.items():
        for highest_weight, multiplicity in character.monomial_coefficients().items():
            twice = tuple(int(2 * value) for value in highest_weight.to_vector())
            label = hft_analytic_support.d4_dynkin_from_twice_orthogonal(twice)
            ray = UNIFORM_RAY_DATA.get(label[1:])
            if ray is not None:
                group, coefficient, shift = ray
                monomial_exponent = label[0] + shift
                target_degree = degree + monomial_exponent
                if minimum_degree <= target_degree <= maximum_degree:
                    raw_groups[group][target_degree] += (
                        int(multiplicity) * coefficient
                    )
                if (
                    monomial_exponent >= 0
                    and 0 <= target_degree <= maximum_degree
                ):
                    stable_raw[target_degree] += int(multiplicity) * coefficient
            endpoint = ENDPOINT_CORRECTIONS.get(label)
            if endpoint is not None:
                for shift, coefficient in endpoint.items():
                    target_degree = degree + shift
                    if minimum_degree <= target_degree <= maximum_degree:
                        wall[target_degree] += int(multiplicity) * coefficient
                polynomial = closed_irrep_polynomial(label)
                for exponent, coefficient in polynomial.dict().items():
                    ell = int(
                        exponent[0]
                        if isinstance(exponent, tuple)
                        else exponent
                    )
                    target_degree = degree + ell
                    if 0 <= target_degree <= maximum_degree:
                        actual_wall[target_degree] += (
                            int(multiplicity) * int(coefficient)
                        )

    raw_total = {
        degree: sum(group[degree] for group in raw_groups.values())
        for degree in range(minimum_degree, maximum_degree + 1)
    }
    curvature = {}
    reconstructed = {}
    stable_curvature = {}
    stable_reconstructed = {}
    for degree in range(0, maximum_degree + 1):
        curvature[degree] = (
            raw_total.get(degree, 0)
            - 2 * raw_total.get(degree - 1, 0)
            + raw_total.get(degree - 2, 0)
        )
        reconstructed[degree] = curvature[degree] + wall.get(degree, 0)
        stable_curvature[degree] = (
            stable_raw.get(degree, 0)
            - 2 * stable_raw.get(degree - 1, 0)
            + stable_raw.get(degree - 2, 0)
        )
        stable_reconstructed[degree] = (
            stable_curvature[degree] + actual_wall[degree]
        )
    return {
        "minimum_degree": minimum_degree,
        "raw_groups": {
            name: tuple(
                values[degree]
                for degree in range(minimum_degree, maximum_degree + 1)
            )
            for name, values in raw_groups.items()
        },
        "raw_total": tuple(
            raw_total[degree]
            for degree in range(minimum_degree, maximum_degree + 1)
        ),
        "curvature": tuple(
            curvature[degree] for degree in range(maximum_degree + 1)
        ),
        "wall": tuple(wall[degree] for degree in range(maximum_degree + 1)),
        "reconstructed": tuple(
            reconstructed[degree] for degree in range(maximum_degree + 1)
        ),
        "stable_raw": tuple(
            stable_raw[degree] for degree in range(maximum_degree + 1)
        ),
        "stable_curvature": tuple(
            stable_curvature[degree]
            for degree in range(maximum_degree + 1)
        ),
        "actual_wall": tuple(
            actual_wall[degree] for degree in range(maximum_degree + 1)
        ),
        "stable_reconstructed": tuple(
            stable_reconstructed[degree]
            for degree in range(maximum_degree + 1)
        ),
        "raw_groups_nonnegative": {
            name: all(value >= 0 for value in values.values())
            for name, values in raw_groups.items()
        },
    }


def run_analysis(maximum_degree=12, audit_label_sum=7, weight_audit_degree=4):
    """Audit the ray theorem and compare it with the scalar-tail series."""
    started = time.time()
    audit = formula_audit(audit_label_sum)
    frobenius_audit = frobenius_ray_audit(audit_label_sum + 1)
    plucker_audit = transverse_plucker_audit()
    bordered_audit = bordered_weyl_audit(audit_label_sum + 1)
    dimension_polynomial = virtual_dimension_polynomial()
    numerator_audit = stable_ray_numerator_audit(9)
    b4_kernel_audit = finite_b4_kernel_audit(numerator_audit)
    weight_audit = weyl_numerator_audit(
        min(int(weight_audit_degree), int(maximum_degree))
    )
    pre = diagonal_from_pre_telescope(maximum_degree)
    b4_convolution = b4_scalar_convolution(maximum_degree)
    primitive_dominance = primitive_form_dominance_audit(
        maximum_degree, convolution=b4_convolution
    )
    grouped = grouped_pre_telescoping_diagonal(maximum_degree)
    curvature = uniform_curvature_decomposition(maximum_degree)
    tail = scalar_tail.green_schwarz_scalar_tail(maximum_degree, tail_start=9)
    prefix = tuple(
        sum(tail["total_diagonal"][: degree + 1])
        for degree in range(maximum_degree + 1)
    )
    pre_matches_prefix = pre["diagonal"] == prefix
    b4_convolution_exact = (
        b4_convolution["coefficients"] == pre["diagonal"]
    )
    correction_match = all(
        tail["total_correction"][degree] == -pre["diagonal"][degree]
        for degree in range(9, maximum_degree + 1)
    )
    group_sum = tuple(
        sum(values[degree] for values in grouped["groups"].values())
        for degree in range(maximum_degree + 1)
    )
    group_sum_exact = group_sum == pre["diagonal"]
    curvature_exact = curvature["reconstructed"] == pre["diagonal"]
    stable_curvature_exact = (
        curvature["stable_reconstructed"] == pre["diagonal"]
    )
    wall_dominance = all(
        -curvature["wall"][degree] >= curvature["curvature"][degree]
        for degree in range(9, maximum_degree + 1)
    )
    wall_margin_matches_correction = all(
        -curvature["wall"][degree] - curvature["curvature"][degree]
        == tail["total_correction"][degree]
        for degree in range(9, maximum_degree + 1)
    )
    stable_wall_dominance = all(
        -curvature["actual_wall"][degree]
        >= curvature["stable_curvature"][degree]
        for degree in range(9, maximum_degree + 1)
    )
    stable_wall_margin_matches_correction = all(
        -curvature["actual_wall"][degree]
        - curvature["stable_curvature"][degree]
        == tail["total_correction"][degree]
        for degree in range(9, maximum_degree + 1)
    )
    margin_matches_correction = all(
        grouped["margin"][degree] == tail["total_correction"][degree]
        for degree in range(9, maximum_degree + 1)
    )

    print("=" * 100)
    print("TK6B.6c — NINE-RAY D4 / SIX-TERM B4 SCALAR FUNCTIONAL")
    print("=" * 100)
    print(
        f"Closed formula audit through label sum {int(audit_label_sum)}: "
        f"{audit['all_exact']} ({len(audit['records'])} irreps)"
    )
    print(
        "Fixed-arm modified-Frobenius organization exact: "
        f"{frobenius_audit['all_exact']}"
    )
    print(
        "Transverse coefficients form one decomposable Plucker vector: "
        f"{plucker_audit['all_exact']}"
    )
    print(
        "Bordered-determinant Weyl numerator exact: "
        f"{bordered_audit['all_exact']}"
    )
    print(
        "Nine-term virtual dimension is identically 15: "
        f"{dimension_polynomial == 15}"
    )
    print(
        "All-arm character numerator closes at degree 7: "
        f"{numerator_audit['all_exact']}"
    )
    print(
        "Complete scalar index reduces to six fixed B4 functionals: "
        f"{b4_kernel_audit['all_exact']}"
    )
    print(
        "Their B4-to-D4 restriction is the truncated Koszul top homology: "
        f"{b4_kernel_audit['koszul_restriction_exact']}"
    )
    print(
        "Weyl-numerator/constant-term bridge exact through degree "
        f"{weight_audit['maximum_degree']}: {weight_audit['all_exact']}"
    )
    print(f"Degrees: 0 through {int(maximum_degree)}")
    print(f"Pre-telescope diagonal: {pre['diagonal']}")
    print(f"Equals prefix sum of C: {pre_matches_prefix}")
    print(
        "Six-term B4 convolution equals the D4 boundary index: "
        f"{b4_convolution_exact}"
    )
    print(
        "Primitive-form dominance reorganization exact: "
        f"{primitive_dominance['all_exact']}"
    )
    print(
        "Double-Koszul adjacent-degree form exact: "
        f"{primitive_dominance['double_primitive_identity_exact'] and primitive_dominance['compact_kernel_exact']}"
    )
    print(
        "Primitive H_0,...,H_4 nonnegative from degree 6 in range: "
        f"{primitive_dominance['primitive_nonnegative_from_six_in_range']}"
    )
    print(
        "Pi_3(N) >= Pi_4(N-1) from degree 9 in range: "
        f"{primitive_dominance['dominance_from_nine_in_range']}"
    )
    print(f"Negative equals A from degree 9: {correction_match}")
    print(f"Four-group sum exact: {group_sum_exact}")
    print(
        "Legacy signed-sector regrouping has the observed tail sign: "
        f"{grouped['tail_dominance']}"
    )
    print(f"Legacy regrouping margin equals A: {margin_matches_correction}")
    print(f"Uniform-curvature plus wall decomposition exact: {curvature_exact}")
    print(
        "Laurent wall correction dominates full curvature from degree 9: "
        f"{wall_dominance}"
    )
    print(
        "Wall-minus-curvature margin equals A: "
        f"{wall_margin_matches_correction}"
    )
    print(
        "Stable-arm curvature plus actual endpoints exact: "
        f"{stable_curvature_exact}"
    )
    print(
        "Actual wall dominates stable-arm curvature from degree 9: "
        f"{stable_wall_dominance}"
    )
    print(
        "Actual-wall-minus-stable-curvature margin equals A: "
        f"{stable_wall_margin_matches_correction}"
    )
    print(
        "Raw Euler sectors are Hilbert series: "
        f"{curvature['raw_groups_nonnegative']}"
    )
    print("Protected SO(10) baseline imported: NO")
    print(f"Runtime: {time.time() - started:.3f}s")
    return {
        "audit": audit,
        "frobenius_audit": frobenius_audit,
        "plucker_audit": plucker_audit,
        "bordered_audit": bordered_audit,
        "dimension_polynomial": dimension_polynomial,
        "numerator_audit": numerator_audit,
        "b4_kernel_audit": b4_kernel_audit,
        "weight_audit": weight_audit,
        "pre_telescope": pre,
        "b4_convolution": b4_convolution,
        "primitive_dominance": primitive_dominance,
        "scalar_tail": tail,
        "grouped": grouped,
        "curvature": curvature,
        "prefix": prefix,
        "pre_matches_prefix": pre_matches_prefix,
        "b4_convolution_exact": b4_convolution_exact,
        "correction_match": correction_match,
        "group_sum_exact": group_sum_exact,
        "curvature_exact": curvature_exact,
        "stable_curvature_exact": stable_curvature_exact,
        "wall_dominance": wall_dominance,
        "wall_margin_matches_correction": wall_margin_matches_correction,
        "stable_wall_dominance": stable_wall_dominance,
        "stable_wall_margin_matches_correction": (
            stable_wall_margin_matches_correction
        ),
        "margin_matches_correction": margin_matches_correction,
        "all_checks": (
            audit["all_exact"]
            and frobenius_audit["all_exact"]
            and plucker_audit["all_exact"]
            and bordered_audit["all_exact"]
            and dimension_polynomial == 15
            and numerator_audit["all_exact"]
            and b4_kernel_audit["all_exact"]
            and weight_audit["all_exact"]
            and pre_matches_prefix
            and b4_convolution_exact
            and primitive_dominance["all_exact"]
            and correction_match
            and group_sum_exact
            and curvature_exact
            and stable_curvature_exact
            and wall_margin_matches_correction
            and stable_wall_margin_matches_correction
            and margin_matches_correction
        ),
    }


def run_self_test():
    """Exercise the closed formula and pre-telescope identity at low degree."""
    result = run_analysis(maximum_degree=10, audit_label_sum=5)
    if not result["all_checks"]:
        raise AssertionError("The nine-ray scalar-boundary audit failed")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Audit the nine-ray D4 formula for the TK6B.6 scalar tail"
    )
    parser.add_argument("--maximum-degree", type=int, default=12)
    parser.add_argument("--audit-label-sum", type=int, default=7)
    parser.add_argument("--weight-audit-degree", type=int, default=4)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            return 0 if run_self_test() else 1
        result = run_analysis(
            maximum_degree=args.maximum_degree,
            audit_label_sum=args.audit_label_sum,
            weight_audit_degree=args.weight_audit_degree,
        )
    except Exception as error:
        print(f"TK6B.6c FAILED: {error}", file=sys.stderr)
        return 1
    return 0 if result["all_checks"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
