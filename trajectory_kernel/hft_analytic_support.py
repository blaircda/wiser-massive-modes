"""Analytic support reduction for the HFT virtual remainder.

The successful route uses the Green--Schwarz ``D4`` oscillator product.  If
``E(u)`` is the spinor exterior polynomial and ``D(u)`` the alternating
vector exterior polynomial, triality gives the exact finite identity

    E(u) - D(u) = u (V + S) B(u).

It telescopes the division by the universal ground multiplet and rewrites the
level-one-vector remainder as

    F(q) = (1-q) sum_{n>=1} q^(n-1) B(q^n)
             prod_{m<n} E(q^m) / prod_{2<=m<=n} D(q^m).

The infinite tail is controlled by uniform Lipschitz bounds for the seven
support walls.  Only fermion modes one through four, vector modes two and
three, and three pivot classes remain.  Those are finite exact character-ring
certificates, independent of a string-level cutoff.

The older principal-embedding/Koszul route is retained as an obstruction
diagnostic.  It fails term by term because the virtual Koszul sum needs
cancellation; it is not part of the proof reduction.

No protected SO(10) completion is imported.
"""

import argparse
import sys
import time
from functools import lru_cache
from itertools import permutations, product

from sage.all import QQ, ZZ, WeylCharacterRing

import hft_so9
from trajectory_kernel import hft_pieri_hazard
from trajectory_kernel import regge_factorization


B4 = hft_so9.B4
D4 = WeylCharacterRing("D4", base_ring=QQ, style="coroots")
D4_VECTOR = D4(1, 0, 0, 0)
D4_OSCILLATOR_SPINOR = D4(0, 0, 1, 0)
D4_OTHER_SPINOR = D4(0, 0, 0, 1)
D4_SCALAR = D4(0, 0, 0, 0)

# The finite quotient in the one-mode supersymmetric identity
#
#   E(u) - D(u) = u (V + S) B(u),
#
# where E is the exterior polynomial of S and D the alternating exterior
# polynomial of V.  Triality gives the compact coefficient formula below.
D4_B_POLYNOMIAL = {
    0: D4_SCALAR,
    2: D4_OTHER_SPINOR - D4_SCALAR,
    3: D4_VECTOR - D4_OSCILLATOR_SPINOR,
    4: D4_OTHER_SPINOR - D4_SCALAR,
    6: D4_SCALAR,
}

# Maximizing a Pieri-polytope relaxation of the seven support walls after
# tensoring by a D4 harmonic H_k and charging degree 2k gives these seven
# affine upper bounds.  Repeating the optimization for mode three adds only
# the final eighth piece.  They are analytic support bounds, not fits to the
# HFT level data; exact products attain them throughout the regression sample.
MODE_TWO_HAZARD_FORMS = (
    ((2, 3, 8, 5), 7),
    ((2, 4, 6, 4), 3),
    ((2, 4, 6, 3), 2),
    ((2, 3, 0, 2), 0),
    ((3, 5, 6, 3), 4),
    ((3, 5, 7, 4), 5),
    ((3, 7, 9, 5), 9),
)
MODE_TWO_THREE_HAZARD_FORMS = MODE_TWO_HAZARD_FORMS + (
    ((4, 7, 9, 5), 9),
)


def tensor_partition(label):
    """Return the four integral row lengths of a tensorial B4 label."""
    ell, middle, rank_three, spin = map(int, label)
    if spin % 2:
        raise ValueError(f"Expected a tensorial B4 label: {label}")
    half_spin = spin // 2
    return (
        ell + middle + rank_three + half_spin,
        middle + rank_three + half_spin,
        rank_three + half_spin,
        half_spin,
    )


def tensor_spinor_partition(label):
    """Remove the basic spinor and return its integral tensor diagram."""
    ell, middle, rank_three, spin = map(int, label)
    if spin % 2 != 1:
        raise ValueError(f"Expected a spinorial B4 label: {label}")
    half_spin = (spin - 1) // 2
    return (
        ell + middle + rank_three + half_spin,
        middle + rank_three + half_spin,
        rank_three + half_spin,
        half_spin,
    )


def modified_frobenius(partition):
    """Return the modified Frobenius data ``(ell_i | h_i)``.

    Here ``ell_i`` counts boxes to the right of the ith diagonal box and
    ``h_i`` is the height of its column including that diagonal box.
    """
    rows = tuple(int(value) for value in partition)
    if len(rows) != 4 or not rows[0] >= rows[1] >= rows[2] >= rows[3] >= 0:
        raise ValueError(f"Expected a four-row partition: {partition}")
    diagonal = sum(rows[index] >= index + 1 for index in range(4))
    arms = tuple(rows[index] - index - 1 for index in range(diagonal))
    heights = tuple(
        sum(row >= index + 1 for row in rows) - index
        for index in range(diagonal)
    )
    return arms, heights


def ns_minimum_mass_level(partition):
    """Return the lowest NS mass level for a tensor Young diagram.

    Basile--Markou's oscillator level is

        sum_i i ell_i + (i-1/2) h_i.

    The HFT physical mass-level convention subtracts the NS intercept 1/2.
    """
    arms, heights = modified_frobenius(partition)
    oscillator_level = sum(
        (index + 1) * arms[index]
        + (QQ(index + 1) - QQ(1) / 2) * heights[index]
        for index in range(len(arms))
    )
    mass_level = oscillator_level - QQ(1) / 2
    # Some principal embeddings lie in the GSO-projected half-integral mass
    # levels.  A surviving physical state with this diagram must then occur at
    # an integral level no smaller than the ceiling of the unprojected bound.
    return int(mass_level.ceil())


def ramond_minimum_mass_level(partition):
    """Return the lowest R mass level for a tensor-spinor diagram."""
    arms, heights = modified_frobenius(partition)
    mass_level = sum(
        (index + 1) * (arms[index] + heights[index])
        for index in range(len(arms))
    )
    return int(mass_level)


def cartan_physical_bounds(label):
    """Return principal-embedding bounds from the three Cartan components.

    If ``V_label`` occurs in the massive-primary coefficient ``R_d``, every
    Cartan component obtained by adding one of the three highest weights in
    ``Z_Q`` occurs among physical states at mass level ``d+1``.  Its principal
    embedding therefore gives a necessary lower bound on ``d``.
    """
    label = tuple(map(int, label))
    cartan_labels = (
        (label[0] + 2, label[1], label[2], label[3]),
        (label[0], label[1], label[2] + 1, label[3]),
        (label[0] + 1, label[1], label[2], label[3] + 1),
    )
    records = []
    for physical_label in cartan_labels:
        if physical_label[3] % 2:
            sector = "R"
            partition = tensor_spinor_partition(physical_label)
            mass_level = ramond_minimum_mass_level(partition)
        else:
            sector = "NS"
            partition = tensor_partition(physical_label)
            mass_level = ns_minimum_mass_level(partition)
        records.append(
            {
                "physical_label": physical_label,
                "sector": sector,
                "partition": partition,
                "minimum_mass_level": mass_level,
                "minimum_primary_degree": mass_level - 1,
            }
        )
    return tuple(records)


def primary_degree_lower_bound(label):
    """Take the strongest of the three principal-embedding bounds."""
    return max(
        record["minimum_primary_degree"]
        for record in cartan_physical_bounds(tuple(label))
    )


def physical_degree_lower_bound(physical_label):
    """Return the principal-embedding lower bound for one physical irrep."""
    physical_label = tuple(map(int, physical_label))
    if physical_label[3] % 2:
        mass_level = ramond_minimum_mass_level(
            tensor_spinor_partition(physical_label)
        )
    else:
        mass_level = ns_minimum_mass_level(tensor_partition(physical_label))
    return mass_level - 1


@lru_cache(maxsize=None)
def full_supermultiplet_degree_lower_bound(label):
    """Use every physical constituent of ``Z_Q tensor V_label``.

    Every constituent occurs at the same physical mass level if ``V_label``
    labels a massive supermultiplet.  Hence the maximum of their individual
    principal-embedding lower bounds is still a necessary bound.
    """
    label = tuple(map(int, label))
    table = regge_factorization.character_table(hft_so9.Z_Q * B4(*label))
    return max(
        physical_degree_lower_bound(physical_label)
        for physical_label in table
    )


def global_seven_wall_degree(label):
    """Return the uniform maximum of all seven TK6B.5e affine walls."""
    label = tuple(map(int, label))
    return max(
        hft_pieri_hazard.stable_pieri.exterior_cost(label) - 1,
        *(
            hft_pieri_hazard.linear_form(label, coefficients) - shift
            for coefficients, shift in hft_pieri_hazard.WALL_HAZARD_FORMS
        ),
    )


def folded_b4_label_from_d4_weight(weight):
    """Fold a dominant D4 weight to the dominant B4 chamber."""
    first, second, third, fourth = map(QQ, weight.to_vector())
    fourth = abs(fourth)
    dynkin = (
        first - second,
        second - third,
        third - fourth,
        2 * fourth,
    )
    if any(value not in ZZ or value < 0 for value in dynkin):
        raise ValueError(f"Cannot fold the D4 weight {weight}")
    return tuple(int(value) for value in dynkin)


def folded_wall_degree(weight):
    """Evaluate the uniform seven-wall degree after D4 chirality folding."""
    return global_seven_wall_degree(folded_b4_label_from_d4_weight(weight))


def affine_maximum(label, forms):
    """Evaluate a maximum of integral affine forms on a Dynkin label."""
    label = tuple(map(int, label))
    return max(
        sum(coefficient * value for coefficient, value in zip(coefficients, label))
        - shift
        for coefficients, shift in forms
    )


def closed_mode_two_hazard(weight):
    """Evaluate the closed piecewise-affine mode-two hazard upper bound."""
    return affine_maximum(
        folded_b4_label_from_d4_weight(weight), MODE_TWO_HAZARD_FORMS
    )


def closed_two_low_vector_mode_hazard(weight):
    """Evaluate the joint mode-two/mode-three hazard upper bound."""
    return affine_maximum(
        folded_b4_label_from_d4_weight(weight),
        MODE_TWO_THREE_HAZARD_FORMS,
    )


def d4_dynkin_from_twice_orthogonal(twice_weight):
    """Convert doubled dominant D4 orthogonal coordinates to Dynkin labels."""
    first, second, third, fourth = map(int, twice_weight)
    values = (
        QQ(first - second) / 2,
        QQ(second - third) / 2,
        QQ(third - fourth) / 2,
        QQ(third + fourth) / 2,
    )
    if any(value not in ZZ or value < 0 for value in values):
        raise ValueError(f"Invalid dominant D4 doubled weight: {twice_weight}")
    return tuple(int(value) for value in values)


def twice_orthogonal_highest(character):
    """Return doubled orthogonal coordinates of a D4 irreducible."""
    return tuple(
        int(2 * value) for value in character.highest_weight().to_vector()
    )


@lru_cache(maxsize=None)
def d4_harmonic_product(source_twice_weight, degree):
    """Return highest weights in a D4 product with the harmonic one-row."""
    source = D4(*d4_dynkin_from_twice_orthogonal(source_twice_weight))
    product_character = source * D4(int(degree), 0, 0, 0)
    return tuple(product_character.monomial_coefficients())


@lru_cache(maxsize=None)
def mode_two_hazard(source_twice_weight):
    """Return the exact mode-two one-row hazard.

    Orthogonal Pieri stability implies that the value of
    ``K(target)-2*k`` is constant after ``k=2*source_1``.  It is therefore
    enough to inspect the displayed finite interval.
    """
    maximum_degree = int(source_twice_weight[0])
    values = []
    for degree in range(maximum_degree + 1):
        values.extend(
            folded_wall_degree(target) - 2 * degree
            for target in d4_harmonic_product(source_twice_weight, degree)
        )
    return max(values)


@lru_cache(maxsize=None)
def two_low_vector_mode_hazard(source_twice_weight):
    """Return the exact joint hazard of vector modes two and three.

    For mode three, the stable translated tail loses one unit of margin per
    additional first-row box.  The maximum is therefore attained for
    ``s <= 2*source_1``.  For every intermediate irrep the mode-two maximum
    is the finite hazard above.
    """
    maximum_mode_three_degree = int(source_twice_weight[0])
    values = []
    for degree in range(maximum_mode_three_degree + 1):
        for intermediate in d4_harmonic_product(
            source_twice_weight, degree
        ):
            intermediate_twice = tuple(
                int(2 * value) for value in intermediate.to_vector()
            )
            values.append(
                mode_two_hazard(intermediate_twice) - 3 * degree
            )
    return max(values)


def low_vector_hazard_formula_audit(maximum_label_sum=2):
    """Compare the closed Pieri hazards with direct D4 tensor products."""
    records = []
    failures = []
    for label in _d4_labels_up_to_sum(maximum_label_sum):
        character = D4(*label)
        highest_weight = character.highest_weight()
        twice_weight = tuple(
            int(2 * value) for value in highest_weight.to_vector()
        )
        exact_mode_two = mode_two_hazard(twice_weight)
        closed_mode_two = closed_mode_two_hazard(highest_weight)
        exact_joint = two_low_vector_mode_hazard(twice_weight)
        closed_joint = closed_two_low_vector_mode_hazard(highest_weight)
        record = {
            "source": label,
            "exact_mode_two": exact_mode_two,
            "closed_mode_two": closed_mode_two,
            "exact_joint": exact_joint,
            "closed_joint": closed_joint,
            "matches": (
                exact_mode_two == closed_mode_two
                and exact_joint == closed_joint
            ),
        }
        records.append(record)
        if not record["matches"]:
            failures.append(record)
    return {
        "maximum_label_sum": int(maximum_label_sum),
        "records": tuple(records),
        "failures": tuple(failures),
        "all_match": not failures,
    }


def d4_fermion_factors(maximum_mode):
    """Return the finite product of spinor exterior factors through a mode."""
    exterior = tuple(
        D4_OSCILLATOR_SPINOR.exterior_power(degree)
        for degree in range(9)
    )
    series = {0: D4_SCALAR}
    maximum_degree = 8 * sum(range(1, int(maximum_mode) + 1))
    for mode in range(1, int(maximum_mode) + 1):
        series = _multiply_d4_series(
            series,
            {mode * degree: exterior[degree] for degree in range(9)},
            maximum_degree,
        )
    return series


def minimum_fermion_degrees(maximum_mode):
    """Return the first degree of every D4 irrep in a finite fermion core."""
    first_degrees = {}
    for degree, character in d4_fermion_factors(maximum_mode).items():
        for highest_weight in character.monomial_coefficients():
            twice_weight = tuple(
                int(2 * value) for value in highest_weight.to_vector()
            )
            first_degrees[twice_weight] = min(
                first_degrees.get(twice_weight, degree), degree
            )
    return first_degrees


def finite_low_mode_case(pivot_class, progress=False):
    """Audit one of the pivot 3, pivot 4, or universal pivot >=5 cores."""
    pivot_class = int(pivot_class)
    if pivot_class not in (3, 4, 5):
        raise ValueError("The low-mode case must be 3, 4, or 5")
    maximum_fermion_mode = pivot_class - 1
    base_degree = pivot_class - 1
    first_degrees = minimum_fermion_degrees(maximum_fermion_mode)
    records = []
    for index, (twice_weight, fermion_degree) in enumerate(
        sorted(first_degrees.items()), start=1
    ):
        highest_weight = D4(
            *d4_dynkin_from_twice_orthogonal(twice_weight)
        ).highest_weight()
        hazard = closed_two_low_vector_mode_hazard(highest_weight)
        margin = base_degree + fermion_degree - hazard
        records.append(
            {
                "pivot_class": pivot_class,
                "fermion_degree": fermion_degree,
                "source": twice_weight,
                "hazard": hazard,
                "margin": margin,
            }
        )
        if progress and (index % 10 == 0 or index == len(first_degrees)):
            print(
                f"pivot {pivot_class}: {index}/{len(first_degrees)} "
                f"low-mode weights certified",
                flush=True,
            )
    failures = tuple(record for record in records if record["margin"] < 0)
    return {
        "pivot_class": pivot_class,
        "sources": len(first_degrees),
        "records": tuple(records),
        "minimum_margin": min(
            (record["margin"] for record in records), default=None
        ),
        "failures": failures,
        "all_pass": not failures,
    }


def finite_low_mode_core_audit(core_pivots=(3, 4, 5), progress=False):
    """Check the finite cores left after the analytic tail estimates.

    Pivots three and four, and every pivot at least five, reduce respectively
    to the finite fermion products through modes two, three and four, followed
    by the two exceptional vector modes.  Pivot two includes its finite B
    polynomial and only mode two.  Pivot one is completely finite.
    """
    records = []
    failures = []

    core_pivots = tuple(sorted(set(map(int, core_pivots))))
    if any(pivot not in (3, 4, 5) for pivot in core_pivots):
        raise ValueError("Core pivots must be selected from 3, 4, and 5")
    core_cases = tuple(
        finite_low_mode_case(pivot, progress=progress)
        for pivot in core_pivots
    )
    for case in core_cases:
        records.extend(case["records"])
        failures.extend(case["failures"])

    # Pivot two: q * B(q^2) * E(q) / D(q^2).
    exterior = tuple(
        D4_OSCILLATOR_SPINOR.exterior_power(degree)
        for degree in range(9)
    )
    for b_degree, b_character in D4_B_POLYNOMIAL.items():
        for exterior_degree, exterior_character in enumerate(exterior):
            source = b_character * exterior_character
            for highest_weight, coefficient in source.monomial_coefficients().items():
                twice_weight = tuple(
                    int(2 * value) for value in highest_weight.to_vector()
                )
                hazard = closed_mode_two_hazard(highest_weight)
                degree = 1 + 2 * b_degree + exterior_degree
                margin = degree - hazard
                record = {
                    "pivot_class": 2,
                    "fermion_degree": exterior_degree,
                    "b_degree": b_degree,
                    "source": twice_weight,
                    "coefficient": int(coefficient),
                    "hazard": hazard,
                    "margin": margin,
                }
                records.append(record)
                if margin < 0:
                    failures.append(record)

    # Pivot one: (1-q) B(q).  The extra -q term only improves the degree.
    for b_degree, character in D4_B_POLYNOMIAL.items():
        for highest_weight, coefficient in character.monomial_coefficients().items():
            hazard = folded_wall_degree(highest_weight)
            margin = b_degree - hazard
            record = {
                "pivot_class": 1,
                "b_degree": b_degree,
                "source": tuple(
                    int(2 * value) for value in highest_weight.to_vector()
                ),
                "coefficient": int(coefficient),
                "hazard": hazard,
                "margin": margin,
            }
            records.append(record)
            if margin < 0:
                failures.append(record)

    return {
        "requested_core_pivots": core_pivots,
        "core_cases": core_cases,
        "records": tuple(records),
        "minimum_margin": min(
            (record["margin"] for record in records), default=None
        ),
        "failures": tuple(failures),
        "all_pass": not failures,
        "complete": set(core_pivots) == {3, 4, 5} and not failures,
    }


def d4_one_mode_divisibility_audit():
    """Verify the finite triality identity underlying telescoping."""
    exterior_vector = tuple(
        D4_VECTOR.exterior_power(degree) for degree in range(9)
    )
    exterior_spinor = tuple(
        D4_OSCILLATOR_SPINOR.exterior_power(degree)
        for degree in range(9)
    )
    ground = D4_VECTOR + D4_OSCILLATOR_SPINOR
    failures = []
    for degree in range(9):
        left = exterior_spinor[degree] - ((-1) ** degree) * exterior_vector[degree]
        right = (
            D4(0)
            if degree == 0
            else ground * D4_B_POLYNOMIAL.get(degree - 1, D4(0))
        )
        if left != right:
            failures.append({"degree": degree, "left": left, "right": right})
    return {
        "failures": tuple(failures),
        "all_match": not failures,
    }


def _multiply_d4_series(left, right, maximum_degree):
    """Multiply two truncated D4 character series."""
    result = {}
    for left_degree, left_character in left.items():
        for right_degree, right_character in right.items():
            degree = left_degree + right_degree
            if degree > maximum_degree:
                continue
            result[degree] = (
                result.get(degree, D4(0))
                + left_character * right_character
            )
    return {
        degree: character
        for degree, character in result.items()
        if character != D4(0)
    }


def d4_telescoping_terms(maximum_degree):
    """Return the exact Green--Schwarz telescoping summands for ``F``.

    Put ``A(u)=E(u)/D(u)``, with spinor exterior numerator ``E`` and
    vector symmetric denominator ``1/D``.  The elementary identity above
    gives

        (prod_{m>=1} A(q^m)-1)/(q(V+S))
          = sum_{n>=1} q^(n-1) B(q^n)/D(q^n)
              prod_{m<n} A(q^m).

    Multiplication by ``PE(-q(V+1))=(1-q)D(q)`` removes the level-one
    B4 vector tower and yields the summands constructed here.
    """
    maximum_degree = int(maximum_degree)
    exterior_spinor = tuple(
        D4_OSCILLATOR_SPINOR.exterior_power(degree)
        for degree in range(9)
    )
    terms = {}
    for pivot in range(1, maximum_degree + 2):
        series = {pivot - 1: D4_SCALAR}
        b_factor = {
            pivot * degree: character
            for degree, character in D4_B_POLYNOMIAL.items()
            if pivot * degree <= maximum_degree
        }
        series = _multiply_d4_series(series, b_factor, maximum_degree)

        for mode in range(1, pivot):
            exterior_factor = {
                mode * degree: exterior_spinor[degree]
                for degree in range(9)
                if mode * degree <= maximum_degree
            }
            series = _multiply_d4_series(
                series, exterior_factor, maximum_degree
            )
        for mode in range(2, pivot + 1):
            symmetric_factor = {
                mode * degree: D4_VECTOR.symmetric_power(degree)
                for degree in range(maximum_degree // mode + 1)
            }
            series = _multiply_d4_series(
                series, symmetric_factor, maximum_degree
            )
        series = _multiply_d4_series(
            series,
            {0: D4_SCALAR, 1: -D4_SCALAR},
            maximum_degree,
        )
        terms[pivot] = series
    return terms


def _twice_weight_table(character):
    """Convert a Weyl character into a doubled orthogonal-weight table."""
    result = {}
    parent = character.parent()
    for highest_weight, irrep_coefficient in character.monomial_coefficients().items():
        irreducible = parent(highest_weight)
        for weight, weight_multiplicity in irreducible.weight_multiplicities().items():
            exponent = tuple(int(2 * value) for value in weight.to_vector())
            result[exponent] = (
                result.get(exponent, 0)
                + int(irrep_coefficient) * int(weight_multiplicity)
            )
    return {exponent: value for exponent, value in result.items() if value}


def _permutation_sign(permutation):
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(4)
        for right in range(left + 1, 4)
    )
    return -1 if inversions % 2 else 1


def b4_rho_orbit():
    """Return the doubled B4 Weyl alternant orbit of rho."""
    rho = (7, 5, 3, 1)
    result = []
    for permutation in permutations(range(4)):
        permutation_sign = _permutation_sign(permutation)
        permuted = tuple(rho[index] for index in permutation)
        for signs in product((-1, 1), repeat=4):
            exponent = tuple(
                signs[index] * permuted[index] for index in range(4)
            )
            determinant = permutation_sign
            for sign in signs:
                determinant *= sign
            result.append((exponent, determinant))
    return tuple(result)


B4_RHO_ORBIT = b4_rho_orbit()


def d4_weyl_orbit_with_sign(twice_weight):
    """Return the signed D4 Weyl orbit of a doubled regular weight."""
    result = []
    for permutation in permutations(range(4)):
        determinant = _permutation_sign(permutation)
        permuted = tuple(twice_weight[index] for index in permutation)
        for signs in product((-1, 1), repeat=4):
            if signs[0] * signs[1] * signs[2] * signs[3] != 1:
                continue
            result.append(
                (
                    tuple(
                        signs[index] * permuted[index]
                        for index in range(4)
                    ),
                    determinant,
                )
            )
    return tuple(result)


def d4_dirac_dominant_table(character):
    """Compute dominant terms of ``A_rho(B4) * character`` finitely.

    The Weyl denominators obey

        A_rho(B4) / A_rho(D4)
          = product_i (exp(e_i/2) - exp(-e_i/2)).

    Combining this with the D4 Weyl character formula replaces a potentially
    huge weight expansion by at most ``192 * 16`` alternant terms per D4
    irreducible, independently of the size of its highest weight.  This is the
    equal-rank Dirac-induction calculation appropriate to ``D4 in B4``.
    """
    result = {}
    rho_d4 = (6, 4, 2, 0)
    rho_b4 = (7, 5, 3, 1)
    for highest_weight, irrep_coefficient in character.monomial_coefficients().items():
        highest = tuple(int(2 * value) for value in highest_weight.to_vector())
        shifted_highest = tuple(
            highest[index] + rho_d4[index] for index in range(4)
        )
        alternant = d4_weyl_orbit_with_sign(shifted_highest)
        for d4_weight, d4_sign in alternant:
            for short_signs in product((-1, 1), repeat=4):
                shifted = tuple(
                    d4_weight[index] + short_signs[index]
                    for index in range(4)
                )
                if not shifted[0] > shifted[1] > shifted[2] > shifted[3] > 0:
                    continue
                unshifted = tuple(
                    QQ(shifted[index] - rho_b4[index]) / 2
                    for index in range(4)
                )
                dynkin = (
                    unshifted[0] - unshifted[1],
                    unshifted[1] - unshifted[2],
                    unshifted[2] - unshifted[3],
                    2 * unshifted[3],
                )
                if any(value not in ZZ or value < 0 for value in dynkin):
                    continue
                label = tuple(int(value) for value in dynkin)
                coefficient = int(irrep_coefficient) * d4_sign
                for sign in short_signs:
                    coefficient *= sign
                result[label] = result.get(label, 0) + coefficient
    return {label: coefficient for label, coefficient in result.items() if coefficient}


def _d4_labels_up_to_sum(maximum_label_sum):
    """Enumerate dominant D4 Dynkin labels in a finite regression simplex."""
    maximum_label_sum = int(maximum_label_sum)
    return tuple(
        label
        for label in product(range(maximum_label_sum + 1), repeat=4)
        if sum(label) <= maximum_label_sum
    )


def dirac_fold_audit(maximum_label_sum=4):
    """Audit the finite Weyl/Dirac folding support inequality.

    For a D4 highest weight ``lambda``, every dominant B4 term produced by
    ``A_rho(B4) chi_lambda`` must have seven-wall degree no larger than the
    degree of the chirality-folded highest weight.  The accompanying proof is
    a finite Weyl-chamber argument; this enumeration is its regression test.
    """
    records = []
    failures = []
    empty = []
    for label in _d4_labels_up_to_sum(maximum_label_sum):
        character = D4(*label)
        source_label = folded_b4_label_from_d4_weight(
            character.highest_weight()
        )
        source_bound = global_seven_wall_degree(source_label)
        table = d4_dirac_dominant_table(character)
        if not table:
            empty.append(label)
        for target, coefficient in table.items():
            target_bound = global_seven_wall_degree(target)
            record = {
                "source": label,
                "folded_source": source_label,
                "source_bound": source_bound,
                "target": target,
                "coefficient": coefficient,
                "target_bound": target_bound,
                "margin": source_bound - target_bound,
            }
            records.append(record)
            if record["margin"] < 0:
                failures.append(record)
    return {
        "maximum_label_sum": int(maximum_label_sum),
        "sources": len(_d4_labels_up_to_sum(maximum_label_sum)),
        "empty_sources": tuple(empty),
        "records": tuple(records),
        "minimum_margin": min(
            (record["margin"] for record in records), default=None
        ),
        "failures": tuple(failures),
        "all_pass": not failures,
    }


def tail_lipschitz_audit(maximum_label_sum=3):
    """Audit the vector and spinor increments used to close the mode tail.

    A vector tensor factor can raise the folded seven-wall degree by at most
    four, and a spinor tensor factor by at most five.  These constants follow
    directly from the seven affine forms in orthogonal coordinates; the
    finite check here protects the implementation against convention errors.
    """
    factors = (
        ("vector", D4_VECTOR, 4),
        ("spinor", D4_OSCILLATOR_SPINOR, 5),
    )
    records = []
    failures = []
    for label in _d4_labels_up_to_sum(maximum_label_sum):
        source = D4(*label)
        source_bound = folded_wall_degree(source.highest_weight())
        for name, factor, allowed_increment in factors:
            for target in (source * factor).monomial_coefficients():
                target_bound = folded_wall_degree(target)
                record = {
                    "factor": name,
                    "source": label,
                    "source_bound": source_bound,
                    "target": d4_dynkin_from_twice_orthogonal(
                        tuple(int(2 * value) for value in target.to_vector())
                    ),
                    "target_bound": target_bound,
                    "increment": target_bound - source_bound,
                    "allowed_increment": allowed_increment,
                }
                records.append(record)
                if record["increment"] > allowed_increment:
                    failures.append(record)
    return {
        "maximum_label_sum": int(maximum_label_sum),
        "records": tuple(records),
        "maximum_vector_increment": max(
            (
                record["increment"]
                for record in records
                if record["factor"] == "vector"
            ),
            default=None,
        ),
        "maximum_spinor_increment": max(
            (
                record["increment"]
                for record in records
                if record["factor"] == "spinor"
            ),
            default=None,
        ),
        "failures": tuple(failures),
        "all_pass": not failures,
    }


def dominant_weyl_numerator_table(character):
    """Project ``A_rho * character`` onto the shifted B4 chamber.

    The input need only be a character on the common D4/B4 torus.  When it is
    B4 invariant, the result is exactly its B4 irreducible coefficient table.
    For an individual telescoping summand it remains a useful sufficient
    support diagnostic: summing the displayed dominant monomials gives the
    exact table of the total B4-invariant series.
    """
    weights = _twice_weight_table(character)
    result = {}
    for weight, coefficient in weights.items():
        for rho_weight, sign in B4_RHO_ORBIT:
            shifted = tuple(
                weight[index] + rho_weight[index] for index in range(4)
            )
            if not shifted[0] > shifted[1] > shifted[2] > shifted[3] > 0:
                continue
            unshifted = tuple(
                QQ(shifted[index] - (7, 5, 3, 1)[index]) / 2
                for index in range(4)
            )
            dynkin = (
                unshifted[0] - unshifted[1],
                unshifted[1] - unshifted[2],
                unshifted[2] - unshifted[3],
                2 * unshifted[3],
            )
            if any(value not in ZZ or value < 0 for value in dynkin):
                continue
            label = tuple(int(value) for value in dynkin)
            result[label] = result.get(label, 0) + sign * coefficient
    return {label: coefficient for label, coefficient in result.items() if coefficient}


def telescoping_support_audit(maximum_degree=8):
    """Test seven-wall support before summing telescoping pivots."""
    terms = d4_telescoping_terms(maximum_degree)
    records = []
    failures = []
    total = {degree: D4(0) for degree in range(maximum_degree + 1)}
    for pivot, series in terms.items():
        for degree, character in series.items():
            total[degree] += character
            table = d4_dirac_dominant_table(character)
            for label, coefficient in table.items():
                record = {
                    "pivot": pivot,
                    "degree": degree,
                    "label": label,
                    "coefficient": coefficient,
                    "bound": global_seven_wall_degree(label),
                }
                records.append(record)
                if degree < record["bound"]:
                    failures.append(record)
    return {
        "terms": terms,
        "total": total,
        "records": tuple(records),
        "failures": tuple(failures),
        "all_termwise": not failures,
    }


def telescoping_reconstruction_audit(maximum_degree=5):
    """Compare the D4 telescope with the independently derived B4 remainder."""
    maximum_degree = int(maximum_degree)
    terms = d4_telescoping_terms(maximum_degree)
    total = {degree: D4(0) for degree in range(maximum_degree + 1)}
    for series in terms.values():
        for degree, character in series.items():
            total[degree] += character

    _numerator, single_levels = hft_so9.derive_hft_spectrum(
        maximum_degree + 1
    )
    factorization = regge_factorization.factor_symmetric_vector_tower(
        single_levels, maximum_degree + 1
    )
    records = []
    failures = []
    for degree in range(maximum_degree + 1):
        telescope_weights = _twice_weight_table(total[degree])
        remainder_weights = _twice_weight_table(
            factorization["remainder"][degree]
        )
        record = {
            "degree": degree,
            "telescope_weight_terms": len(telescope_weights),
            "remainder_weight_terms": len(remainder_weights),
            "matches": telescope_weights == remainder_weights,
        }
        records.append(record)
        if not record["matches"]:
            failures.append(record)
    return {
        "maximum_degree": maximum_degree,
        "records": tuple(records),
        "failures": tuple(failures),
        "all_match": not failures,
    }


def actual_support_audit(max_level=13):
    """Compare the analytic input bounds with exact HFT coefficients."""
    _numerator, single_levels = hft_so9.derive_hft_spectrum(int(max_level))
    factorization = regge_factorization.factor_symmetric_vector_tower(
        single_levels, int(max_level)
    )
    primary_records = []
    remainder_records = []
    for degree, character in factorization["primaries"].items():
        for label, coefficient in regge_factorization.character_table(character).items():
            cartan_bound = primary_degree_lower_bound(label)
            bound = full_supermultiplet_degree_lower_bound(tuple(label))
            primary_records.append(
                {
                    "degree": degree,
                    "label": label,
                    "coefficient": coefficient,
                    "cartan_bound": cartan_bound,
                    "bound": bound,
                    "margin": degree - bound,
                }
            )
    for degree, character in factorization["remainder"].items():
        for label, coefficient in regge_factorization.character_table(character).items():
            bound = global_seven_wall_degree(label)
            remainder_records.append(
                {
                    "degree": degree,
                    "label": label,
                    "coefficient": coefficient,
                    "bound": bound,
                    "margin": degree - bound,
                }
            )
    return {
        "single_levels": single_levels,
        "factorization": factorization,
        "primary_records": tuple(primary_records),
        "primary_failures": tuple(
            record for record in primary_records if record["margin"] < 0
        ),
        "remainder_records": tuple(remainder_records),
        "remainder_failures": tuple(
            record for record in remainder_records if record["margin"] < 0
        ),
    }


def koszul_transition_audit(maximum_label_sum=5):
    """Test whether the principal bounds imply every seven-wall transition.

    This audit is deliberately independent of the observed HFT spectrum.  It
    enumerates arbitrary dominant source labels, all exterior degrees
    ``0 <= j <= 9``, and every constituent of ``Lambda^j(V) tensor V_source``.
    """
    maximum_label_sum = int(maximum_label_sum)
    labels = tuple(
        label
        for label in product(range(maximum_label_sum + 1), repeat=4)
        if sum(label) <= maximum_label_sum
    )
    records = []
    failures = []
    for source in labels:
        source_bound = full_supermultiplet_degree_lower_bound(source)
        for exterior_degree, exterior_character in enumerate(hft_so9._WEDGE_9):
            table = regge_factorization.character_table(
                B4(*source) * exterior_character
            )
            for target, multiplicity in table.items():
                target_bound = global_seven_wall_degree(target)
                margin = source_bound + exterior_degree - target_bound
                record = {
                    "source": source,
                    "source_bound": source_bound,
                    "exterior_degree": exterior_degree,
                    "target": target,
                    "multiplicity": multiplicity,
                    "target_bound": target_bound,
                    "margin": margin,
                }
                records.append(record)
                if margin < 0:
                    failures.append(record)
    return {
        "maximum_label_sum": maximum_label_sum,
        "sources": len(labels),
        "records": tuple(records),
        "minimum_margin": min(
            (record["margin"] for record in records), default=None
        ),
        "failures": tuple(failures),
        "all_implied": not failures,
    }


def run_analysis(
    max_level=13,
    maximum_label_sum=2,
    telescoping_degree=5,
    core_pivots=(),
    progress=False,
):
    """Run exact identities, regressions, and selected finite certificates."""
    started = time.time()
    one_mode = d4_one_mode_divisibility_audit()
    reconstruction = telescoping_reconstruction_audit(telescoping_degree)
    telescoping = telescoping_support_audit(telescoping_degree)
    dirac_fold = dirac_fold_audit(maximum_label_sum)
    tail = tail_lipschitz_audit(maximum_label_sum)
    low_vector = low_vector_hazard_formula_audit(maximum_label_sum)
    actual = actual_support_audit(max_level)
    transitions = koszul_transition_audit(maximum_label_sum)
    finite_core = None
    if core_pivots:
        finite_core = finite_low_mode_core_audit(
            core_pivots, progress=progress
        )

    expected_koszul_obstruction = bool(transitions["failures"])
    diagnostics_pass = (
        one_mode["all_match"]
        and reconstruction["all_match"]
        and telescoping["all_termwise"]
        and dirac_fold["all_pass"]
        and tail["all_pass"]
        and low_vector["all_match"]
        and not actual["primary_failures"]
        and not actual["remainder_failures"]
        and expected_koszul_obstruction
        and (finite_core is None or finite_core["all_pass"])
    )
    proof_complete = bool(
        finite_core and finite_core["complete"] and diagnostics_pass
    )

    print("=" * 100)
    print("TK6B.5f — ANALYTIC HFT SUPPORT REDUCTION")
    print("=" * 100)
    print(
        "One-mode triality divisibility failures: "
        f"{len(one_mode['failures'])}"
    )
    print(
        "Telescoping reconstruction degrees/failures: "
        f"{len(reconstruction['records'])}/{len(reconstruction['failures'])}"
    )
    print(
        "Telescoping support terms/failures: "
        f"{len(telescoping['records'])}/{len(telescoping['failures'])}"
    )
    print(
        "Dirac-fold support terms/failures: "
        f"{len(dirac_fold['records'])}/{len(dirac_fold['failures'])}"
    )
    print(
        "Tail Lipschitz maxima (vector/spinor): "
        f"{tail['maximum_vector_increment']}/"
        f"{tail['maximum_spinor_increment']}"
    )
    print(
        "Closed low-vector hazard cases/failures: "
        f"{len(low_vector['records'])}/{len(low_vector['failures'])}"
    )
    print(f"Physical HFT levels: 1 through {int(max_level)}")
    print(
        "Massive-primary principal-bound terms/failures: "
        f"{len(actual['primary_records'])}/{len(actual['primary_failures'])}"
    )
    print(
        "Uniform seven-wall remainder terms/failures: "
        f"{len(actual['remainder_records'])}/{len(actual['remainder_failures'])}"
    )
    print(
        "Generic Koszul transition cases/expected obstructions: "
        f"{len(transitions['records'])}/{len(transitions['failures'])}"
    )
    print(f"Generic transition minimum margin: {transitions['minimum_margin']}")
    if finite_core is None:
        print("Finite low-mode core: not requested")
    else:
        print(
            "Finite low-mode pivots/sources/failures: "
            f"{finite_core['requested_core_pivots']}/"
            f"{sum(case['sources'] for case in finite_core['core_cases'])}/"
            f"{len(finite_core['failures'])}"
        )
        print(f"Finite core minimum margin: {finite_core['minimum_margin']}")
    print(f"Complete finite certificate: {proof_complete}")
    print("Protected SO(10) baseline imported: NO")
    print(f"Runtime: {time.time() - started:.3f}s")
    return {
        "one_mode_identity": one_mode,
        "telescoping_reconstruction": reconstruction,
        "telescoping_support": telescoping,
        "dirac_fold": dirac_fold,
        "tail_lipschitz": tail,
        "low_vector_hazard": low_vector,
        "actual_support": actual,
        "koszul_transitions": transitions,
        "expected_koszul_obstruction": expected_koszul_obstruction,
        "finite_core": finite_core,
        "proof_complete": proof_complete,
        "all_checks": diagnostics_pass,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Reduce the HFT seven-wall theorem to a finite low-mode core"
    )
    parser.add_argument("--max-level", type=int, default=13)
    parser.add_argument("--maximum-label-sum", type=int, default=2)
    parser.add_argument("--telescoping-degree", type=int, default=5)
    parser.add_argument(
        "--core-pivot",
        type=int,
        choices=(3, 4, 5),
        action="append",
        default=[],
        help="run an expensive finite low-mode certificate; repeat as needed",
    )
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = run_analysis(
            max_level=args.max_level,
            maximum_label_sum=args.maximum_label_sum,
            telescoping_degree=args.telescoping_degree,
            core_pivots=args.core_pivot,
            progress=args.progress,
        )
    except Exception as error:
        print(f"TK6B.5f analytic support FAILED: {error}", file=sys.stderr)
        return 1
    return 0 if result["all_checks"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
