"""TK6B.6e: DDF/Koszul audit for the primitive-form inequality.

The scalar Bars correction has been reduced to

    pi_3(N) - pi_4(N-1) >= 0.

The shift suggests the ordinary Koszul differential associated with the
level-one transverse bosonic DDF creators.  This module records what that
interpretation proves exactly and where it stops:

* the relative D4/B4 Weyl Euler class, the compact scalar kernel at q=1,
  and the vector Koszul Euler class are the same D4 character;
* removing the genuine transverse level-one vector tower gives the
  pre-telescope series G = D_V(q) Res(Z_m), which is audited for positivity
  through a chosen finite degree;
* applying the inverse positive relative-Dirac half to G gives a canonical
  virtual B4 core Ghat.  Its coefficients are audited for positivity and its
  restriction back to D4 is checked exactly;
* the scalar functional on Ghat collapses at all orders to three tensor-hook
  trajectories.  Contraction plus exterior multiplication gives an injective
  stabilizer symbol from the middle hook to the two outer hooks for every
  first-row length;
* the raw middle Koszul map K_4 -> K_3 is not injective from the second
  relevant degree onward, because ker(d_4) = im(d_5);
* the only automatic injection is the induced map
  K_4 / im(d_5) -> K_3.  Identifying this primitive quotient with Pi_4,
  and making the map descend through massive-supermultiplet division,
  remain analytic tasks;
* relative Dirac descent maps the five low forms to a gamma-traceless tower.
  Explicit projected-wedge maps form an exact five-term polynomial free
  resolution with positive cokernel ``[n,0,3,0]`` in degree ``n``;
* the null fibre has nonzero homology, so truncated ``Tor_1`` vanishing is
  not the correct target.  Moving the complete resolution to the cumulative
  core gives the exact first-difference identity between the Bars margin,
  ``B_Gamma`` and ``H_4``.  After the required outer orientation, its prefix
  closes exactly onto the already-known virtual three-hook shell.  The
  physical derived action and its homology concentration are the sharpened
  remaining tasks.

The finite positivity and candidate-matching checks are diagnostics, not an
all-orders proof.  No protected SO(10) completion is imported.
"""

import argparse
import sys
import time
from math import comb

import hft_so9
from sage.all import WeylCharacterRing

from trajectory_kernel import hft_analytic_support
from trajectory_kernel import gamma_symbol_complex
from trajectory_kernel import scalar_boundary_functional


B4 = hft_so9.B4
D4 = hft_analytic_support.D4
V = hft_analytic_support.D4_VECTOR
S = hft_analytic_support.D4_OSCILLATOR_SPINOR
C = hft_analytic_support.D4_OTHER_SPINOR
ONE = D4(0, 0, 0, 0)
B3 = WeylCharacterRing("B3", style="coroots")


def character_inner_product(left, right):
    """Return the irreducible-character inner product in one Weyl ring."""
    right_coefficients = right.monomial_coefficients()
    return sum(
        coefficient * right_coefficients.get(highest_weight, 0)
        for highest_weight, coefficient in left.monomial_coefficients().items()
    )


def relative_euler_audit():
    """Check the three exact incarnations of the relative Euler class."""
    exterior = tuple(V.exterior_power(degree) for degree in range(9))
    vector_euler = sum(
        ((-1) ** degree * exterior[degree] for degree in range(9)),
        D4(0),
    )
    relative_denominator = S - C
    relative_square = relative_denominator ** 2

    compact_kernel = (
        character.branch(D4)
        for character in scalar_boundary_functional.b4_scalar_kernel_coefficients()
    )
    compact_at_one = sum(compact_kernel, D4(0))
    zq_restriction = hft_so9.Z_Q.branch(D4, rule="default")
    zq_factorization = (V + S) * (V + C)

    # Equal-rank Weyl integration inserts the relative Euler class and a
    # factor |W(D4)|/|W(B4)| = 1/2.  Avoid rational or floating arithmetic by
    # checking twice the B4 inner product against the D4 inner product.
    b4_samples = (
        B4(0, 0, 0, 0),
        B4(1, 0, 0, 0),
        B4(0, 1, 0, 0),
        B4(0, 0, 1, 0),
        B4(0, 0, 0, 1),
    )
    bridge_failures = []
    for left_index, left in enumerate(b4_samples):
        left_restriction = left.branch(D4, rule="default")
        for right_index, right in enumerate(b4_samples):
            right_restriction = right.branch(D4, rule="default")
            b4_value = character_inner_product(left, right)
            d4_value = character_inner_product(
                vector_euler * left_restriction,
                right_restriction,
            )
            if 2 * b4_value != d4_value:
                bridge_failures.append((left_index, right_index))

    return {
        "vector_euler": vector_euler,
        "relative_denominator": relative_denominator,
        "relative_square": relative_square,
        "compact_at_one": compact_at_one,
        "zq_restriction": zq_restriction,
        "zq_factorization": zq_factorization,
        "relative_euler_exact": (
            vector_euler == relative_square == compact_at_one
        ),
        "zq_factorization_exact": zq_restriction == zq_factorization,
        "weyl_bridge_failures": tuple(bridge_failures),
        "weyl_bridge_exact_on_fundamentals": not bridge_failures,
    }


def transverse_tower_audit(maximum_degree=12, compare_hft=False):
    """Audit ``G = D_V(q) Res(Z_m)`` and finite-degree positivity.

    ``G`` is obtained first from the exact Green--Schwarz telescope.  When
    ``compare_hft`` is true, the same coefficients are independently formed
    by restricting the baseline-free HFT primaries to D4 and convolving with
    the vector exterior polynomial.
    """
    maximum_degree = int(maximum_degree)
    if maximum_degree < 0:
        raise ValueError("maximum_degree must be nonnegative")

    telescope = scalar_boundary_functional.pre_telescoping_coefficients(
        maximum_degree
    )
    records = []
    positivity_failures = []
    for degree in range(maximum_degree + 1):
        coefficients = tuple(
            telescope[degree].monomial_coefficients().values()
        )
        record = {
            "degree": degree,
            "irreducible_terms": len(coefficients),
            "negative_coefficients": sum(value < 0 for value in coefficients),
            "minimum_coefficient": min(coefficients, default=0),
        }
        records.append(record)
        if record["negative_coefficients"]:
            positivity_failures.append(record)

    independent = None
    comparison_failures = []
    if compare_hft:
        _numerator, levels = hft_so9.derive_hft_spectrum(maximum_degree + 1)
        restricted = {
            degree: levels[degree + 1].branch(D4, rule="default")
            for degree in range(maximum_degree + 1)
        }
        exterior = tuple(V.exterior_power(degree) for degree in range(9))
        independent = {}
        for degree in range(maximum_degree + 1):
            independent[degree] = sum(
                (
                    (-1) ** exterior_degree
                    * exterior[exterior_degree]
                    * restricted[degree - exterior_degree]
                    for exterior_degree in range(min(8, degree) + 1)
                ),
                D4(0),
            )
            if independent[degree] != telescope[degree]:
                comparison_failures.append(degree)

    return {
        "maximum_degree": maximum_degree,
        "telescope": telescope,
        "independent": independent,
        "records": tuple(records),
        "positivity_failures": tuple(positivity_failures),
        "comparison_failures": tuple(comparison_failures),
        "positive_in_range": not positivity_failures,
        "independent_exact": not comparison_failures,
    }


def _d4_dynkin_label(highest_weight):
    """Recover a ``D4`` Dynkin label from an orthogonal-basis weight."""
    twice = tuple(int(2 * value) for value in highest_weight.to_vector())
    return hft_analytic_support.d4_dynkin_from_twice_orthogonal(twice)


def inverse_relative_dirac_half(character):
    """Invert the positive relative-Dirac half on an outer-invariant character.

    If ``Y`` is invariant under the outer automorphism interchanging the two
    ``D4`` spinor nodes, then ``(S-C)Y`` is anti-invariant.  Its terms with
    third Dynkin label greater than the fourth have the unique form

        [a,b,c+d+1,c] = D^+ [a,b,c,d].

    Selecting that oriented half and undoing this label map gives the unique
    virtual ``B4`` character whose restriction is ``Y``.  The caller audits
    outer invariance and exact reconstruction separately.
    """
    relative_index = (S - C) * character
    core = B4(0)
    fixed_terms = []
    for highest_weight, coefficient in relative_index.monomial_coefficients().items():
        a, b, third, fourth = _d4_dynkin_label(highest_weight)
        if third == fourth:
            fixed_terms.append(((a, b, third, fourth), int(coefficient)))
        elif third > fourth:
            core += coefficient * B4(a, b, fourth, third - fourth - 1)
    return core, relative_index, tuple(fixed_terms)


def cumulative_koszul_kernel_audit():
    """Verify the exact ``B4`` kernel behind the oriented core.

    For the nine-dimensional vector ``W`` put

        E_W(q) = sum_j (-q)^j Lambda^j(W),
        K_W(q) = E_W(q)/(1-q).

    Odd-dimensional Hodge duality makes the division polynomial.  Its
    coefficient in degree ``r`` is the partial exterior Euler sum ``s_r``.
    Since ``W`` restricts to ``V+1``, ``K_W`` restricts to ``D_V(q)``.
    Consequently the canonical core is

        Ghat = K_W(q) Z_m,

    and ``Z_m/(1-q) = PE(qW) Ghat`` as a formal character identity.
    """
    vector_nine = B4(1, 0, 0, 0)
    exterior_nine = tuple(
        vector_nine.exterior_power(degree) for degree in range(10)
    )
    kernel = tuple(
        sum(
            (
                (-1) ** exterior_degree * exterior_nine[exterior_degree]
                for exterior_degree in range(degree + 1)
            ),
            B4(0),
        )
        for degree in range(9)
    )
    reconstructed_euler = tuple(
        (kernel[degree] if degree < 9 else B4(0))
        - (kernel[degree - 1] if degree else B4(0))
        for degree in range(10)
    )
    expected_euler = tuple(
        (-1) ** degree * exterior_nine[degree] for degree in range(10)
    )
    transverse_exterior = tuple(V.exterior_power(degree) for degree in range(9))
    expected_restriction = tuple(
        (-1) ** degree * transverse_exterior[degree] for degree in range(9)
    )
    observed_restriction = tuple(
        character.branch(D4, rule="default") for character in kernel
    )
    return {
        "kernel": kernel,
        "reconstructed_euler": reconstructed_euler,
        "expected_euler": expected_euler,
        "division_exact": reconstructed_euler == expected_euler,
        "palindromic": all(
            kernel[degree] == kernel[8 - degree] for degree in range(9)
        ),
        "observed_restriction": observed_restriction,
        "expected_restriction": expected_restriction,
        "restriction_exact": observed_restriction == expected_restriction,
        "all_exact": (
            reconstructed_euler == expected_euler
            and all(kernel[degree] == kernel[8 - degree] for degree in range(9))
            and observed_restriction == expected_restriction
        ),
    }


def cumulative_core_boundary_kernel_audit(maximum_degree=10):
    """Test the collapse of the scalar functional to three hook towers.

    Moving the factor ``(1-q) PE(qW)`` from

        Z_m = (1-q) PE(qW) Ghat

    through the self-dual character inner product replaces the six-term
    scalar kernel ``C`` by ``L = C (1-q) PE(qW)``.  The observed closed form is

        L_n = R_n - R_(n+1),
        R_n = [n,0,0,0] - [n-1,1,0,0] + [n-1,0,1,0],

    with negative leading labels omitted.  The three terms are the tensor
    hooks ``(n)``, ``(n,1)``, and ``(n,1,1)``.

    This finite calculation is an all-orders certificate once degrees zero
    through eight agree.  Indeed, the ``B4`` Weyl numerator for a family with
    fixed lower rows is a linear combination of ``z_i^n`` and ``z_i^-n``.
    It therefore obeys the order-eight recurrence with characteristic
    polynomial ``K_W = product_i (1-q z_i)(1-q/z_i)``.  All three hook
    families are in their dominant range in the recurrence from degree nine
    onward, while ``C`` has degree five.
    """
    maximum_degree = int(maximum_degree)
    if maximum_degree < 0:
        raise ValueError("maximum_degree must be nonnegative")

    vector_nine = B4(1, 0, 0, 0)
    scalar_kernel = scalar_boundary_functional.b4_scalar_kernel_coefficients()
    symmetric = tuple(
        vector_nine.symmetric_power(degree)
        for degree in range(maximum_degree + 1)
    )
    multiplier = tuple(
        symmetric[degree]
        - (symmetric[degree - 1] if degree else B4(0))
        for degree in range(maximum_degree + 1)
    )
    observed = tuple(
        sum(
            (
                scalar_kernel[kernel_degree]
                * multiplier[degree - kernel_degree]
                for kernel_degree in range(min(5, degree) + 1)
            ),
            B4(0),
        )
        for degree in range(maximum_degree + 1)
    )

    def hook_euler(degree):
        result = B4(degree, 0, 0, 0)
        if degree:
            result += (
                -B4(degree - 1, 1, 0, 0)
                + B4(degree - 1, 0, 1, 0)
            )
        return result

    expected = tuple(
        hook_euler(degree) - hook_euler(degree + 1)
        for degree in range(maximum_degree + 1)
    )
    failures = tuple(
        degree
        for degree in range(maximum_degree + 1)
        if observed[degree] != expected[degree]
    )
    return {
        "maximum_degree": maximum_degree,
        "observed": observed,
        "expected": expected,
        "failures": failures,
        "exact_in_range": not failures,
        "weyl_recurrence_start": 9,
        "all_orders_certified": maximum_degree >= 8 and not failures,
    }


def three_hook_symbol_audit(maximum_hook=6):
    """Audit the all-rank contraction/wedge symbol behind ``R_k``.

    Let ``H0(k)``, ``H1(k)``, and ``H2(k)`` be the ``B4`` tensor hooks
    ``(k)``, ``(k,1)``, and ``(k,1,1)``.  Under the stabilizer ``D4`` of a
    nonzero vector their restrictions are

        H0 = A0 + ... + Ak,
        H1 = A1 + ... + Ak + B0 + ... + B(k-1),
        H2 = B0 + ... + B(k-1) + C0 + ... + C(k-1),

    where ``Aj=[j,0,0,0]``, ``Bj=[j,1,0,0]`` and
    ``Cj=[j,0,1,1]`` in ``D4``.  The unique contraction and exterior
    projections evaluated at the stabilizing vector identify respectively
    the ``A`` and ``B`` summands.  Their direct sum is injective, with
    cokernel ``A0 + sum Cj``.

    The branching formulas themselves follow for every ``k`` from the
    multiplicity-free ``B4 -> D4`` interlacing rule; the finite loop is a
    convention and implementation audit.
    """
    maximum_hook = int(maximum_hook)
    if maximum_hook < 1:
        raise ValueError("maximum_hook must be positive")
    vector_nine = B4(1, 0, 0, 0)
    records = []
    failures = []
    for degree in range(1, maximum_hook + 1):
        hooks = (
            B4(degree, 0, 0, 0),
            B4(degree - 1, 1, 0, 0),
            B4(degree - 1, 0, 1, 0),
        )
        a_pieces = tuple(D4(index, 0, 0, 0) for index in range(degree + 1))
        b_pieces = tuple(D4(index, 1, 0, 0) for index in range(degree))
        c_pieces = tuple(D4(index, 0, 1, 1) for index in range(degree))
        expected = (
            sum(a_pieces, D4(0)),
            sum(a_pieces[1:], D4(0)) + sum(b_pieces, D4(0)),
            sum(b_pieces, D4(0)) + sum(c_pieces, D4(0)),
        )
        restrictions = tuple(
            character.branch(D4, rule="default") for character in hooks
        )
        contraction_multiplicity = int(
            character_inner_product(hooks[0], vector_nine * hooks[1])
        )
        exterior_multiplicity = int(
            character_inner_product(hooks[2], vector_nine * hooks[1])
        )
        cokernel = restrictions[0] - restrictions[1] + restrictions[2]
        expected_cokernel = D4(0, 0, 0, 0) + sum(c_pieces, D4(0))
        next_hooks = (
            B4(degree + 1, 0, 0, 0),
            B4(degree, 1, 0, 0),
            B4(degree, 0, 1, 0),
        )
        next_cokernel = (
            next_hooks[0].branch(D4, rule="default")
            - next_hooks[1].branch(D4, rule="default")
            + next_hooks[2].branch(D4, rule="default")
        )
        shell = next_cokernel - cokernel
        expected_shell = D4(degree, 0, 1, 1)
        record = {
            "hook": degree,
            "restrictions": restrictions,
            "expected_restrictions": expected,
            "contraction_multiplicity": contraction_multiplicity,
            "exterior_multiplicity": exterior_multiplicity,
            "cokernel": cokernel,
            "expected_cokernel": expected_cokernel,
            "shell": shell,
            "expected_shell": expected_shell,
            "exact": (
                restrictions == expected
                and contraction_multiplicity == 1
                and exterior_multiplicity == 1
                and cokernel == expected_cokernel
                and shell == expected_shell
            ),
        }
        records.append(record)
        if not record["exact"]:
            failures.append(record)
    return {
        "maximum_hook": maximum_hook,
        "records": tuple(records),
        "failures": tuple(failures),
        "all_exact": not failures,
        "all_orders_by_interlacing": not failures,
    }


def _b4_tensor_hook(exterior_depth, first_row):
    """Return ``(first_row, 1^exterior_depth)`` for depths zero, one or two."""
    exterior_depth = int(exterior_depth)
    first_row = int(first_row)
    if first_row < 0 or exterior_depth not in (0, 1, 2):
        return B4(0)
    if exterior_depth == 0:
        return B4(first_row, 0, 0, 0)
    if first_row == 0:
        return B4(0)
    if exterior_depth == 1:
        return B4(first_row - 1, 1, 0, 0)
    return B4(first_row - 1, 0, 1, 0)


def three_hook_diagonal_audit(cores):
    """Split the finite scalar margin into two supplies and one demand."""
    maximum_degree = max(map(int, cores), default=-1)
    records = []
    diagonal_difference_failures = []
    shell_pairing_negatives = []
    for core_degree, core in sorted(cores.items()):
        for first_row in range(maximum_degree - core_degree + 1):
            shell = sum(
                (
                    (-1) ** exterior_depth
                    * (
                        _b4_tensor_hook(exterior_depth, first_row + 1)
                        - _b4_tensor_hook(exterior_depth, first_row)
                    )
                    for exterior_depth in range(3)
                ),
                B4(0),
            )
            value = int(character_inner_product(shell, core))
            if value < 0:
                shell_pairing_negatives.append(
                    {
                        "core_degree": core_degree,
                        "first_row": first_row,
                        "total_degree": core_degree + first_row,
                        "value": value,
                    }
                )
    for total_degree in range(maximum_degree + 1):
        births = []
        for exterior_depth in range(3):
            value = 0
            for core_degree in range(total_degree + 1):
                first_row = total_degree - core_degree
                shell = (
                    _b4_tensor_hook(exterior_depth, first_row + 1)
                    - _b4_tensor_hook(exterior_depth, first_row)
                )
                value += int(
                    character_inner_product(shell, cores[core_degree])
                )
            births.append(value)
        records.append(
            {
                "degree": total_degree,
                "one_row_supply": births[0],
                "middle_hook_demand": births[1],
                "three_row_supply": births[2],
                "margin": births[0] - births[1] + births[2],
            }
        )
        for exterior_depth in range(3):
            present_diagonal = sum(
                int(
                    character_inner_product(
                        _b4_tensor_hook(
                            exterior_depth, total_degree - core_degree
                        ),
                        cores[core_degree],
                    )
                )
                for core_degree in range(total_degree + 1)
            )
            next_diagonal_without_endpoint = sum(
                int(
                    character_inner_product(
                        _b4_tensor_hook(
                            exterior_depth,
                            total_degree - core_degree + 1,
                        ),
                        cores[core_degree],
                    )
                )
                for core_degree in range(total_degree + 1)
            )
            if births[exterior_depth] != (
                next_diagonal_without_endpoint - present_diagonal
            ):
                diagonal_difference_failures.append(
                    (total_degree, exterior_depth)
                )
    tail = tuple(record for record in records if record["degree"] >= 9)
    return {
        "maximum_degree": maximum_degree,
        "records": tuple(records),
        "tail_records": tail,
        "births_nonnegative_in_tail": all(
            record["one_row_supply"] >= 0
            and record["middle_hook_demand"] >= 0
            and record["three_row_supply"] >= 0
            for record in tail
        ),
        "margin_nonnegative_in_tail": all(
            record["margin"] >= 0 for record in tail
        ),
        "shell_pairing_negatives": tuple(shell_pairing_negatives),
        "termwise_shell_positivity": not shell_pairing_negatives,
        "diagonal_difference_failures": tuple(
            diagonal_difference_failures
        ),
        "diagonal_difference_exact": not diagonal_difference_failures,
    }


def three_hook_translation_audit(cores, tail_start=9):
    """Separate three distinct translation tests for the hook multiplicities.

    Write

        m_p(d,k) = <H_k^(p), Ghat_d>.

    The shell formula uses the first-row difference
    ``m_p(d,k+1)-m_p(d,k)``.  A literal Regge-direction injection would force
    every such difference to be nonnegative.  The audit records the failures
    in the finite triangle ``d+k <= maximum_degree``.

    Two other inequalities are useful necessary conditions for the proposed
    diagonal construction, but are not existence proofs:

    * a Lorentz-scalar level translation would require
      ``m_p(d+1,k) >= m_p(d,k)``;
    * the oriented vector symbol could only inject a middle hook at ``(d,k)``
      into the two outer hooks at ``(d+1,k)`` if their total multiplicity is
      at least as large.

    Keeping these tests separate prevents a dimension coincidence from being
    mistaken for an actual module map.
    """
    maximum_degree = max(map(int, cores), default=-1)
    tail_start = int(tail_start)
    regge_failures = []
    level_failures = []
    vector_rank_failures = []

    def multiplicity(exterior_depth, core_degree, first_row):
        return int(
            character_inner_product(
                _b4_tensor_hook(exterior_depth, first_row),
                cores[core_degree],
            )
        )

    for exterior_depth in range(3):
        for core_degree in range(maximum_degree + 1):
            for first_row in range(maximum_degree - core_degree + 1):
                source = multiplicity(
                    exterior_depth, core_degree, first_row
                )
                regge_target = multiplicity(
                    exterior_depth, core_degree, first_row + 1
                )
                if regge_target < source:
                    regge_failures.append(
                        {
                            "exterior_depth": exterior_depth,
                            "core_degree": core_degree,
                            "first_row": first_row,
                            "total_degree": core_degree + first_row,
                            "source": source,
                            "target": regge_target,
                            "margin": regge_target - source,
                        }
                    )
                if core_degree < maximum_degree:
                    level_target = multiplicity(
                        exterior_depth, core_degree + 1, first_row
                    )
                    if level_target < source:
                        level_failures.append(
                            {
                                "exterior_depth": exterior_depth,
                                "core_degree": core_degree,
                                "first_row": first_row,
                                "total_degree": core_degree + first_row,
                                "source": source,
                                "target": level_target,
                                "margin": level_target - source,
                            }
                        )

    for core_degree in range(maximum_degree):
        for first_row in range(1, maximum_degree - core_degree + 1):
            middle = multiplicity(1, core_degree, first_row)
            one_row = multiplicity(0, core_degree + 1, first_row)
            three_row = multiplicity(2, core_degree + 1, first_row)
            if one_row + three_row < middle:
                vector_rank_failures.append(
                    {
                        "core_degree": core_degree,
                        "first_row": first_row,
                        "total_degree": core_degree + first_row,
                        "middle": middle,
                        "one_row": one_row,
                        "three_row": three_row,
                        "margin": one_row + three_row - middle,
                    }
                )

    def in_tail(record):
        return record["total_degree"] >= tail_start

    return {
        "maximum_degree": maximum_degree,
        "tail_start": tail_start,
        "regge_failures": tuple(regge_failures),
        "regge_failures_in_tail": tuple(filter(in_tail, regge_failures)),
        "level_failures": tuple(level_failures),
        "level_failures_in_tail": tuple(filter(in_tail, level_failures)),
        "vector_rank_failures": tuple(vector_rank_failures),
        "vector_rank_failures_in_tail": tuple(
            filter(in_tail, vector_rank_failures)
        ),
        "termwise_regge_injection_refuted_in_tail": any(
            map(in_tail, regge_failures)
        ),
        "level_translation_dimension_compatible_in_tail": not any(
            map(in_tail, level_failures)
        ),
        "vector_symbol_dimension_compatible_in_tail": not any(
            map(in_tail, vector_rank_failures)
        ),
    }


def oriented_b4_core_audit(transverse, direct_branch_degrees=(0, 4)):
    """Audit the canonical ``B4`` core underlying the transverse series ``G``.

    The inverse is exact for any outer-invariant ``D4`` character, but its
    coefficients need not be nonnegative.  Positivity is therefore recorded
    only as finite evidence.  Exact outer symmetry, the Dirac-index identity,
    and reconstruction of the supplied ``G`` are checked degree by degree.

    Reconstruction follows algebraically from the relative-Dirac identity:
    ``delta Res(core) = delta G``, and the character ring is an integral
    domain, so the nonzero ``delta`` cancels.  A few degrees are also branched
    directly as an independent implementation check; branching every large
    core is needlessly expensive.
    """
    records = []
    cores = {}
    outer_symmetry_failures = []
    fixed_support_failures = []
    dirac_identity_failures = []
    reconstruction_failures = []
    direct_branch_failures = []
    direct_branch_degrees = set(map(int, direct_branch_degrees))
    positivity_failures = []

    for degree in sorted(transverse):
        character = transverse[degree]
        outer_symmetric = (
            scalar_boundary_functional.d4_outer_swap(character) == character
        )
        if not outer_symmetric:
            outer_symmetry_failures.append(degree)

        core, relative_index, fixed_terms = inverse_relative_dirac_half(character)
        cores[degree] = core
        if fixed_terms:
            fixed_support_failures.append((degree, fixed_terms))

        positive_half = relative_dirac_positive_half(core)
        dirac_exact = (
            positive_half
            - scalar_boundary_functional.d4_outer_swap(positive_half)
            == relative_index
        )
        if not dirac_exact:
            dirac_identity_failures.append(degree)

        reconstructs = outer_symmetric and not fixed_terms and dirac_exact
        if not reconstructs:
            reconstruction_failures.append(degree)

        direct_branch_exact = None
        if degree in direct_branch_degrees:
            direct_branch_exact = core.branch(D4, rule="default") == character
            if not direct_branch_exact:
                direct_branch_failures.append(degree)

        coefficients = tuple(core.monomial_coefficients().values())
        negative_coefficients = sum(value < 0 for value in coefficients)
        record = {
            "degree": degree,
            "irreducible_terms": len(coefficients),
            "negative_coefficients": negative_coefficients,
            "minimum_coefficient": min(coefficients, default=0),
            "outer_symmetric": outer_symmetric,
            "dirac_identity_exact": dirac_exact,
            "reconstructs": reconstructs,
            "direct_branch_exact": direct_branch_exact,
        }
        records.append(record)
        if negative_coefficients:
            positivity_failures.append(record)

    return {
        "cores": cores,
        "records": tuple(records),
        "outer_symmetry_failures": tuple(outer_symmetry_failures),
        "fixed_support_failures": tuple(fixed_support_failures),
        "dirac_identity_failures": tuple(dirac_identity_failures),
        "reconstruction_failures": tuple(reconstruction_failures),
        "direct_branch_degrees": tuple(
            degree for degree in sorted(transverse) if degree in direct_branch_degrees
        ),
        "direct_branch_failures": tuple(direct_branch_failures),
        "positivity_failures": tuple(positivity_failures),
        "positive_in_range": not positivity_failures,
        "all_exact": not (
            outer_symmetry_failures
            or fixed_support_failures
            or dirac_identity_failures
            or reconstruction_failures
            or direct_branch_failures
        ),
    }


def _symmetric_power_dimension(degree, rank=8):
    """Dimension of ``Sym^degree`` of a vector space of the given rank."""
    degree = int(degree)
    rank = int(rank)
    if degree < 0:
        return 0
    return comb(degree + rank - 1, rank - 1)


def middle_koszul_rank_audit(maximum_target_level=8):
    """Compute the exact ranks around the middle of the vector Koszul complex.

    The desired bidegree map has the form

        d_4: Lambda^4(V) tensor Sym^(N-1)(V)
             -> Lambda^3(V) tensor Sym^N(V).

    It belongs to the homogeneous Koszul strand of total degree ``N+3``.
    Exactness of the ordinary polynomial Koszul complex gives

        ker(d_4) = im(d_5).

    Ranks are obtained recursively from exactness, beginning at the top of
    the eight-variable strand.  This is an exact dimension calculation, not
    a numerical matrix-rank estimate.
    """
    maximum_target_level = int(maximum_target_level)
    if maximum_target_level < 1:
        raise ValueError("maximum_target_level must be positive")

    records = []
    failures = []
    for target_level in range(1, maximum_target_level + 1):
        total_degree = target_level + 3
        dimensions = {
            exterior_degree: (
                comb(8, exterior_degree)
                * _symmetric_power_dimension(
                    total_degree - exterior_degree, rank=8
                )
            )
            for exterior_degree in range(9)
        }
        ranks = {9: 0}
        for exterior_degree in range(8, -1, -1):
            ranks[exterior_degree] = (
                dimensions[exterior_degree] - ranks[exterior_degree + 1]
            )

        domain_dimension = dimensions[4]
        image_dimension = ranks[4]
        kernel_dimension = ranks[5]
        exact_dimension_identity = (
            domain_dimension == image_dimension + kernel_dimension
        )
        record = {
            "target_level": target_level,
            "domain_dimension": domain_dimension,
            "image_dimension": image_dimension,
            "kernel_dimension": kernel_dimension,
            "raw_map_injective": kernel_dimension == 0,
            "primitive_quotient_dimension": image_dimension,
            "exact_dimension_identity": exact_dimension_identity,
        }
        records.append(record)
        if not exact_dimension_identity:
            failures.append(record)

    return {
        "maximum_target_level": maximum_target_level,
        "records": tuple(records),
        "failures": tuple(failures),
        "all_exact": not failures,
        "raw_injectivity_fails_from_two": all(
            record["raw_map_injective"] == (record["target_level"] == 1)
            for record in records
        ),
    }


def compact_super_koszul_mismatch_audit():
    """Record the first-degree obstruction to a literal super-Koszul match.

    Supersymmetry pairs the bosonic DDF vector creators with spinorial
    fermionic creators.  A full super-Koszul completion therefore introduces
    a spinor ghost already in auxiliary degree one.  The compact primitive
    kernel instead divides by ``1+qx`` and hence introduces a shifted scalar.
    These cannot be the same equivariant complex at its first page.
    """
    scalar_spinor_hom = character_inner_product(ONE, S)
    return {
        "compact_shifted_character": ONE,
        "super_koszul_character": S,
        "scalar_spinor_hom_dimension": int(scalar_spinor_hom),
        "first_auxiliary_degree_matches": ONE == S,
        "no_equivariant_linear_identification": scalar_spinor_hom == 0,
    }


def _b4_dynkin_label(highest_weight):
    """Recover a ``B4`` Dynkin label from an orthogonal-basis weight."""
    twice = tuple(int(2 * value) for value in highest_weight.to_vector())
    differences = tuple(twice[index] - twice[index + 1] for index in range(3))
    if any(value % 2 for value in differences):
        raise ValueError(f"Nonintegral B4 Dynkin conversion: {highest_weight}")
    return (
        differences[0] // 2,
        differences[1] // 2,
        differences[2] // 2,
        twice[3],
    )


def relative_dirac_positive_half(character):
    """Return the positive half of the relative ``B4/D4`` Dirac index.

    On irreducibles the equal-rank Dirac identity is

        (S-C) Res[a,b,c,d]
          = [a,b,c+d+1,c] - [a,b,c,c+d+1].

    This function returns the first term and extends additively.
    """
    result = D4(0)
    for highest_weight, coefficient in character.monomial_coefficients().items():
        a, b, c, d = _b4_dynkin_label(highest_weight)
        result += coefficient * D4(a, b, c + d + 1, c)
    return result


def relative_dirac_half_audit(maximum_label_sum=3):
    """Verify the relative Dirac identity and its low-form compact kernel."""
    maximum_label_sum = int(maximum_label_sum)
    identity_failures = []
    for a in range(maximum_label_sum + 1):
        for b in range(maximum_label_sum + 1 - a):
            for c in range(maximum_label_sum + 1 - a - b):
                for d in range(maximum_label_sum + 1 - a - b - c):
                    label = (a, b, c, d)
                    character = B4(*label)
                    positive = D4(a, b, c + d + 1, c)
                    expected = positive - scalar_boundary_functional.d4_outer_swap(
                        positive
                    )
                    observed = (S - C) * character.branch(D4, rule="default")
                    if observed != expected:
                        identity_failures.append(label)

    vector_nine = B4(1, 0, 0, 0)
    low_forms = tuple(vector_nine.exterior_power(degree) for degree in range(5))
    gamma_traceless = tuple(
        relative_dirac_positive_half(character) for character in low_forms
    )
    expected_labels = (
        (0, 0, 1, 0),
        (1, 0, 1, 0),
        (0, 1, 1, 0),
        (0, 0, 2, 1),
        (0, 0, 3, 0),
    )
    expected_tower = tuple(D4(*label) for label in expected_labels)

    # After relative Dirac insertion, the compact scalar denominator becomes
    # a spinorial index.  Verify the coefficient identity through x-degree 4:
    #
    #   delta Lambda_x(V)/(1+qx)
    #     = U^Delta(x)/((1+x)(1+qx)),
    #
    # where U^Delta_j = U_j - tau(U_j).
    compact_failures = []
    exterior = tuple(V.exterior_power(degree) for degree in range(5))
    oriented = tuple(
        character - scalar_boundary_functional.d4_outer_swap(character)
        for character in gamma_traceless
    )
    for x_degree in range(5):
        direct = {
            q_degree: ((-1) ** q_degree) * (S - C) * exterior[x_degree - q_degree]
            for q_degree in range(x_degree + 1)
        }
        through_dirac = {}
        for form_degree in range(x_degree + 1):
            remaining = x_degree - form_degree
            sign = (-1) ** remaining
            for q_degree in range(remaining + 1):
                through_dirac[q_degree] = (
                    through_dirac.get(q_degree, D4(0))
                    + sign * oriented[form_degree]
                )
        if direct != through_dirac:
            compact_failures.append(x_degree)

    return {
        "maximum_label_sum": maximum_label_sum,
        "identity_failures": tuple(identity_failures),
        "relative_dirac_exact": not identity_failures,
        "gamma_traceless": gamma_traceless,
        "expected_tower": expected_tower,
        "tower_exact": gamma_traceless == expected_tower,
        "tower_dimensions": tuple(int(character.degree()) for character in gamma_traceless),
        "compact_failures": tuple(compact_failures),
        "compact_dirac_identity_exact": not compact_failures,
    }


def gamma_traceless_symbol_audit():
    """Audit the exact symbol data of the five-term Dirac tower.

    The stabilizer in ``Spin(8)`` of a nonzero vector is ``Spin(7)``.  The
    restrictions of the five gamma-traceless modules telescope as

        A0, A0+A1, A1+A2, A2+A3, A3.

    Together with the multiplicity-one adjacent ``Spin(8)`` vector couplings,
    this is the symbol data for an exact complex.  In particular the reverse
    top symbol ``U4 -> U3`` is injective.  This does not yet prove that the
    supermultiplet-reduced DDF action realizes that symbol on HFT multiplicity
    spaces.
    """
    dirac = relative_dirac_half_audit()
    tower = dirac["gamma_traceless"]
    stabilizer_pieces = (
        B3(0, 0, 1),
        B3(1, 0, 1),
        B3(0, 1, 1),
        B3(0, 0, 3),
    )
    expected_restrictions = (
        stabilizer_pieces[0],
        stabilizer_pieces[0] + stabilizer_pieces[1],
        stabilizer_pieces[1] + stabilizer_pieces[2],
        stabilizer_pieces[2] + stabilizer_pieces[3],
        stabilizer_pieces[3],
    )
    restrictions = tuple(
        character.branch(B3, rule="default") for character in tower
    )
    adjacency = tuple(
        int(character_inner_product(tower[index + 1], V * tower[index]))
        for index in range(4)
    )
    nonadjacent_couplings = []
    for source in range(5):
        for target in range(5):
            multiplicity = int(
                character_inner_product(tower[target], V * tower[source])
            )
            if multiplicity and abs(source - target) != 1:
                nonadjacent_couplings.append((source, target, multiplicity))
    alternating_restriction = sum(
        ((-1) ** index * restrictions[index] for index in range(5)),
        B3(0),
    )
    explicit_complex = gamma_symbol_complex.symbol_audit(maximum_degree=6)
    return {
        "tower": tower,
        "restrictions": restrictions,
        "expected_restrictions": expected_restrictions,
        "restriction_telescope_exact": restrictions == expected_restrictions,
        "alternating_restriction": alternating_restriction,
        "alternating_restriction_zero": alternating_restriction == B3(0),
        "adjacent_vector_multiplicities": adjacency,
        "adjacent_vector_couplings_unique": adjacency == (1, 1, 1, 1),
        "nonadjacent_couplings": tuple(nonadjacent_couplings),
        "path_only": not nonadjacent_couplings,
        "top_symbol_source": stabilizer_pieces[3],
        "top_symbol_target_multiplicity": int(
            character_inner_product(
                stabilizer_pieces[3], restrictions[3]
            )
        ),
        "top_symbol_injective_data": (
            restrictions[4] == stabilizer_pieces[3]
            and character_inner_product(stabilizer_pieces[3], restrictions[3]) == 1
            and adjacency[3] == 1
        ),
        "explicit_complex": explicit_complex,
        "projected_wedge_complex_exact": explicit_complex[
            "polynomial_complex_exact"
        ],
        "resolved_positive_tower_exact_in_range": explicit_complex[
            "positive_tower_exact_in_range"
        ],
        "prefix_kernel_exact_in_range": explicit_complex[
            "prefix_kernel_exact_in_range"
        ],
        "prefix_kernel_branches_positive": explicit_complex[
            "prefix_kernel"
        ]["branches_positive"],
        "prefix_kernel_d4_virtual": explicit_complex[
            "prefix_kernel"
        ]["prefix_virtual_from_degree_zero"],
    }


def oriented_three_hook_symbol_audit(maximum_hook=6):
    """Lift the complete three-hook symbol through the positive Dirac half.

    For ``H_k^(p) = (k,1^p)``, ``p=0,1,2``, put

        U_k^(p) = D^+(H_k^(p)).

    These are the three ``D4`` gamma-traceless families

        [k,0,1,0], [k-1,1,1,0], [k-1,0,2,1].

    Their restrictions to the stabilizer ``B3`` of a nonzero transverse
    vector have the same interlacing telescope as the un-oriented hooks,
    with pieces

        A_j=[j,0,1], B_j=[j,1,1], C_j=[j,0,3].

    The two adjacent vector couplings are unique.  Evaluating them at the
    stabilizing vector therefore injects the middle family into the two
    outer families.  Since one full-rank specialization gives a nonzero
    maximal minor, the corresponding degree-one map of free
    ``Sym(V)``-modules is injective over the polynomial ring.  Tensoring that
    sequence with a physical multiplicity module can nevertheless create a
    kernel; algebraically that kernel is ``Tor_1`` of the cokernel.  This
    routine certifies the universal symbol, not the required Tor vanishing.
    """
    maximum_hook = int(maximum_hook)
    if maximum_hook < 1:
        raise ValueError("maximum_hook must be positive")

    records = []
    failures = []
    for first_row in range(1, maximum_hook + 1):
        hooks = tuple(
            _b4_tensor_hook(exterior_depth, first_row)
            for exterior_depth in range(3)
        )
        oriented = tuple(
            relative_dirac_positive_half(character) for character in hooks
        )
        expected_oriented = (
            D4(first_row, 0, 1, 0),
            D4(first_row - 1, 1, 1, 0),
            D4(first_row - 1, 0, 2, 1),
        )

        a_pieces = tuple(
            B3(index, 0, 1) for index in range(first_row + 1)
        )
        b_pieces = tuple(
            B3(index, 1, 1) for index in range(first_row)
        )
        c_pieces = tuple(
            B3(index, 0, 3) for index in range(first_row)
        )
        expected_restrictions = (
            sum(a_pieces, B3(0)),
            sum(a_pieces[1:], B3(0)) + sum(b_pieces, B3(0)),
            sum(b_pieces, B3(0)) + sum(c_pieces, B3(0)),
        )
        restrictions = tuple(
            character.branch(B3, rule="default") for character in oriented
        )
        vector_multiplicities = (
            int(character_inner_product(oriented[0], V * oriented[1])),
            int(character_inner_product(oriented[2], V * oriented[1])),
        )
        cokernel = restrictions[0] - restrictions[1] + restrictions[2]
        expected_cokernel = B3(0, 0, 1) + sum(c_pieces, B3(0))

        next_hooks = tuple(
            _b4_tensor_hook(exterior_depth, first_row + 1)
            for exterior_depth in range(3)
        )
        next_oriented = tuple(
            relative_dirac_positive_half(character)
            for character in next_hooks
        )
        next_cokernel = sum(
            (
                (-1) ** exterior_depth
                * next_oriented[exterior_depth].branch(B3, rule="default")
                for exterior_depth in range(3)
            ),
            B3(0),
        )
        shell = next_cokernel - cokernel
        expected_shell = B3(first_row, 0, 3)
        exact = (
            oriented == expected_oriented
            and restrictions == expected_restrictions
            and vector_multiplicities == (1, 1)
            and cokernel == expected_cokernel
            and shell == expected_shell
        )
        record = {
            "first_row": first_row,
            "oriented_hooks": oriented,
            "expected_oriented_hooks": expected_oriented,
            "restrictions": restrictions,
            "expected_restrictions": expected_restrictions,
            "vector_multiplicities": vector_multiplicities,
            "cokernel": cokernel,
            "expected_cokernel": expected_cokernel,
            "shell": shell,
            "expected_shell": expected_shell,
            "exact": exact,
        }
        records.append(record)
        if not exact:
            failures.append(record)

    return {
        "maximum_hook": maximum_hook,
        "records": tuple(records),
        "failures": tuple(failures),
        "all_exact": not failures,
        "all_orders_by_interlacing": not failures,
        "free_polynomial_symbol_injective": not failures,
        "truncated_tensor_descent_has_tor_obstruction": True,
        "full_five_term_resolution_required": True,
    }


def gamma_resolution_core_pairing_audit(cores, maximum_degree=13):
    """Move the five-term resolution from ``Z_m`` to the positive core.

    Let ``M=D^+(Z_m)``, ``P=D^+(Ghat)`` and

        N(q) = U_4 - q U_3 + q^2 U_2 - q^3 U_1 + q^4 U_0,
        T(q) = PE(q V) N(q) = sum_n q^n [n,0,3,0].

    Outer antisymmetrization and ``D_V Res(Z_m)=Res(Ghat)`` imply

        <N,M> = <T,P>.

    The common scalar series is denoted ``B_Gamma`` in the report.  If ``H_4`` is
    the fourth primitive series and ``a`` the three-hook margin, then

        a_N-a_(N-1) = B_Gamma_N+B_Gamma_(N-2)-h_4(N)-h_4(N-1).

    Outer antisymmetrization is essential when converting this
    first-difference relation into a prefix kernel on ``P``.  With the
    correct orientation, that prefix is exactly the previously derived
    three-hook shell and its convolution with ``P`` reproduces ``a``.

    The audit reconstructs ``Z_m`` from the cumulative core identity, so it
    neither imports the protected uplift nor performs circular HFT seeding.
    """
    available_degree = max(map(int, cores), default=-1)
    maximum_degree = min(int(maximum_degree), available_degree)
    if maximum_degree < 0:
        raise ValueError("A nonempty cumulative core is required")

    vector_nine = B4(1, 0, 0, 0)
    cumulative = {}
    massive = {}
    for degree in range(maximum_degree + 1):
        cumulative[degree] = sum(
            (
                vector_nine.symmetric_power(vector_degree)
                * cores[degree - vector_degree]
                for vector_degree in range(degree + 1)
            ),
            B4(0),
        )
        massive[degree] = cumulative[degree] - (
            cumulative[degree - 1] if degree else B4(0)
        )

    multiplicity_module = {
        degree: relative_dirac_positive_half(massive[degree])
        for degree in range(maximum_degree + 1)
    }
    positive_core = {
        degree: relative_dirac_positive_half(cores[degree])
        for degree in range(maximum_degree + 1)
    }
    tower = relative_dirac_half_audit()["gamma_traceless"]
    numerator = (tower[4], -tower[3], tower[2], -tower[1], tower[0])
    primitive_four_kernel = sum(
        ((-1) ** degree * tower[degree] for degree in range(5)),
        D4(0),
    )

    left = []
    right = []
    primitive_four = []
    for degree in range(maximum_degree + 1):
        left.append(
            int(
                sum(
                    character_inner_product(
                        numerator[shift], multiplicity_module[degree - shift]
                    )
                    for shift in range(min(4, degree) + 1)
                )
            )
        )
        right.append(
            int(
                sum(
                    character_inner_product(
                        D4(tower_degree, 0, 3, 0),
                        positive_core[degree - tower_degree],
                    )
                    for tower_degree in range(degree + 1)
                )
            )
        )
        primitive_four.append(
            int(
                character_inner_product(
                    primitive_four_kernel, multiplicity_module[degree]
                )
            )
        )

    hook_records = three_hook_diagonal_audit(
        {degree: cores[degree] for degree in range(maximum_degree + 1)}
    )["records"]
    margins = tuple(record["margin"] for record in hook_records)
    difference_failures = []
    for degree in range(maximum_degree + 1):
        observed = margins[degree] - (margins[degree - 1] if degree else 0)
        expected = (
            left[degree]
            + (left[degree - 2] if degree >= 2 else 0)
            - primitive_four[degree]
            - (primitive_four[degree - 1] if degree else 0)
        )
        if observed != expected:
            difference_failures.append((degree, observed, expected))

    prefix_kernel = gamma_symbol_complex.prefix_kernel_audit(maximum_degree)
    prefix_pairing = tuple(
        int(
            sum(
                character_inner_product(
                    prefix_kernel["prefixes"][degree - core_degree],
                    positive_core[core_degree],
                )
                for core_degree in range(degree + 1)
            )
        )
        for degree in range(maximum_degree + 1)
    )
    prefix_pairing_failures = tuple(
        degree
        for degree in range(maximum_degree + 1)
        if prefix_pairing[degree] != margins[degree]
    )

    return {
        "maximum_degree": maximum_degree,
        "massive": massive,
        "multiplicity_module": multiplicity_module,
        "positive_core": positive_core,
        "resolution_numerator": numerator,
        "left_pairing": tuple(left),
        "positive_core_pairing": tuple(right),
        "pairing_failures": tuple(
            degree
            for degree in range(maximum_degree + 1)
            if left[degree] != right[degree]
        ),
        "pairing_exact": left == right,
        "primitive_four": tuple(primitive_four),
        "margins": margins,
        "difference_failures": tuple(difference_failures),
        "difference_identity_exact": not difference_failures,
        "prefix_kernel": prefix_kernel,
        "prefix_pairing": prefix_pairing,
        "prefix_pairing_failures": prefix_pairing_failures,
        "prefix_pairing_exact": not prefix_pairing_failures,
    }


def primitive_tower_comparison(maximum_degree=10):
    """Test whether Pi_3 or Pi_4 is a raw exterior-form multiplicity.

    Both the transverse ``D4`` series ``G`` and its canonical ``B4`` core are
    tested.  This finite scan only rules out the simplest identification.  It
    does not rule out a quotient, homology, or filtered spectral-sequence
    realization.
    """
    maximum_degree = int(maximum_degree)
    if maximum_degree < 8:
        raise ValueError("Use maximum_degree >= 8 for a meaningful comparison")

    convolution = scalar_boundary_functional.b4_scalar_convolution(
        maximum_degree
    )
    primitive = scalar_boundary_functional.primitive_form_dominance_audit(
        maximum_degree, convolution=convolution
    )
    pi_series = {
        3: primitive["double_primitive_series"][3],
        4: primitive["double_primitive_series"][4],
    }

    transverse = scalar_boundary_functional.pre_telescoping_coefficients(
        maximum_degree
    )
    core = oriented_b4_core_audit(
        transverse, direct_branch_degrees=()
    )["cores"]
    exterior = tuple(V.exterior_power(degree) for degree in range(9))
    form_series = {
        exterior_degree: tuple(
            int(character_inner_product(exterior[exterior_degree], transverse[degree]))
            for degree in range(maximum_degree + 1)
        )
        for exterior_degree in range(9)
    }
    b4_exterior = tuple(
        B4(1, 0, 0, 0).exterior_power(degree) for degree in range(5)
    )
    core_form_series = {
        exterior_degree: tuple(
            int(character_inner_product(b4_exterior[exterior_degree], core[degree]))
            for degree in range(maximum_degree + 1)
        )
        for exterior_degree in range(5)
    }

    comparison_start = 6
    def find_matches(candidates):
        matches = []
        for primitive_degree, series in pi_series.items():
            for exterior_degree, candidate in candidates.items():
                for shift in range(-2, 3):
                    exact = True
                    tested = 0
                    for degree in range(comparison_start, maximum_degree + 1):
                        candidate_degree = degree + shift
                        if not 0 <= candidate_degree <= maximum_degree:
                            continue
                        tested += 1
                        if series[degree] != candidate[candidate_degree]:
                            exact = False
                            break
                    if exact and tested >= 3:
                        matches.append(
                            {
                                "primitive_degree": primitive_degree,
                                "exterior_degree": exterior_degree,
                                "shift": shift,
                                "tested": tested,
                            }
                        )
        return tuple(matches)

    raw_matches = find_matches(form_series)
    core_raw_matches = find_matches(core_form_series)
    core_boundary = cumulative_core_boundary_kernel_audit(maximum_degree)
    core_index = tuple(
        int(
            sum(
                character_inner_product(
                    core_boundary["observed"][kernel_degree],
                    core[degree - kernel_degree],
                )
                for kernel_degree in range(degree + 1)
            )
        )
        for degree in range(maximum_degree + 1)
    )
    core_index_failures = tuple(
        degree
        for degree in range(maximum_degree + 1)
        if core_index[degree] != convolution["coefficients"][degree]
    )
    accidental_core_candidate = all(
        pi_series[4][degree] == core_form_series[3][degree - 1]
        for degree in range(6, 11)
    )
    accidental_candidate_breaks_at_eleven = (
        maximum_degree >= 11
        and pi_series[4][11] != core_form_series[3][10]
    )

    return {
        "maximum_degree": maximum_degree,
        "comparison_start": comparison_start,
        "pi_series": pi_series,
        "form_series": form_series,
        "core_form_series": core_form_series,
        "raw_matches": raw_matches,
        "core_raw_matches": core_raw_matches,
        "core_index": core_index,
        "core_index_failures": core_index_failures,
        "core_index_exact": not core_index_failures,
        "accidental_core_candidate": accidental_core_candidate,
        "accidental_candidate_breaks_at_eleven": (
            accidental_candidate_breaks_at_eleven
        ),
        "no_raw_form_match_in_scan": not raw_matches,
        "no_core_raw_form_match_in_scan": not core_raw_matches,
        "pi3_not_global_hilbert_series": pi_series[3][0] < 0,
    }


def run_analysis(maximum_degree=10, compare_hft=False):
    """Run the DDF/Koszul obstruction and finite diagnostic audits."""
    started = time.time()
    relative = relative_euler_audit()
    cumulative_kernel = cumulative_koszul_kernel_audit()
    core_boundary = cumulative_core_boundary_kernel_audit(
        max(8, int(maximum_degree))
    )
    hook_symbol = three_hook_symbol_audit()
    transverse = transverse_tower_audit(
        maximum_degree, compare_hft=compare_hft
    )
    oriented_core = oriented_b4_core_audit(transverse["telescope"])
    hook_diagonal = three_hook_diagonal_audit(oriented_core["cores"])
    hook_translation = three_hook_translation_audit(oriented_core["cores"])
    koszul = middle_koszul_rank_audit(maximum_degree)
    mismatch = compact_super_koszul_mismatch_audit()
    dirac = relative_dirac_half_audit()
    symbol = gamma_traceless_symbol_audit()
    oriented_hook_symbol = oriented_three_hook_symbol_audit()
    gamma_pairing = gamma_resolution_core_pairing_audit(
        oriented_core["cores"], maximum_degree=min(13, int(maximum_degree))
    )
    # The five-point window 6--10 has one accidental core match:
    # Pi_4(N) agrees there with the Lambda^3(W) multiplicity in Ghat_(N-1).
    # Degree 11 refutes it, so keep six stable coefficients while avoiding an
    # unnecessarily large B4 convolution at the transverse-positivity cutoff.
    primitive = primitive_tower_comparison(11)

    print("=" * 100)
    print("TK6B.6e — DDF / CUMULATIVE CORE / PRIMITIVE KOSZUL AUDIT")
    print("=" * 100)
    print(
        "Relative Weyl square = vector Euler class = compact kernel at q=1: "
        f"{relative['relative_euler_exact']}"
    )
    print(
        "Restricted universal supermultiplet factorization exact: "
        f"{relative['zq_factorization_exact']}"
    )
    print(
        "Relative Weyl inner-product bridge exact on fundamentals: "
        f"{relative['weyl_bridge_exact_on_fundamentals']}"
    )
    print(
        "Cumulative B4 Koszul kernel and D4 restriction exact: "
        f"{cumulative_kernel['all_exact']}"
    )
    print(
        "Scalar kernel collapses to three cumulative-core hook towers in range: "
        f"{core_boundary['all_orders_certified']}"
    )
    print(
        "Three-hook contraction/wedge symbol is injective by interlacing: "
        f"{hook_symbol['all_orders_by_interlacing']}"
    )
    print(
        "Positive-Dirac three-hook symbol and free polynomial injection exact: "
        f"{oriented_hook_symbol['all_orders_by_interlacing'] and oriented_hook_symbol['free_polynomial_symbol_injective']}"
    )
    print(
        f"Transverse quotient G positive through degree {int(maximum_degree)}: "
        f"{transverse['positive_in_range']}"
    )
    print(
        "Canonical oriented B4 core positive in the same range: "
        f"{oriented_core['positive_in_range']}"
    )
    print(
        "Oriented core reconstructs G exactly under restriction: "
        f"{oriented_core['all_exact']}"
    )
    if int(maximum_degree) >= 9:
        print(
            "Three-hook births and supply-demand margin nonnegative from degree 9: "
            f"{hook_diagonal['births_nonnegative_in_tail'] and hook_diagonal['margin_nonnegative_in_tail']}"
        )
        print(
            "Individual hook-shell pairings are signed (cross-degree map required): "
            f"{bool(hook_diagonal['shell_pairing_negatives'])}"
        )
        print(
            "Termwise first-row/Regge injection refuted in the tail: "
            f"{hook_translation['termwise_regge_injection_refuted_in_tail']} "
            f"({len(hook_translation['regge_failures_in_tail'])} failures)"
        )
        print(
            "Level-shift and oriented-vector rank tests remain dimension-compatible "
            "in the finite tail: "
            f"{hook_translation['level_translation_dimension_compatible_in_tail'] and hook_translation['vector_symbol_dimension_compatible_in_tail']}"
        )
    print(f"Independent HFT comparison requested: {bool(compare_hft)}")
    if compare_hft:
        print(
            "Green--Schwarz and independently restricted HFT quotients agree: "
            f"{transverse['independent_exact']}"
        )
    print(
        "Raw K_4 -> K_3 injectivity fails from target level 2: "
        f"{koszul['raw_injectivity_fails_from_two']}"
    )
    print("Middle Koszul dimensions (target: domain / image / kernel):")
    for record in koszul["records"]:
        print(
            f"  {record['target_level']}: {record['domain_dimension']} / "
            f"{record['image_dimension']} / {record['kernel_dimension']}"
        )
    print(
        "Compact shifted scalar is not the spinorial super-Koszul ghost: "
        f"{mismatch['no_equivariant_linear_identification']}"
    )
    print(
        "Relative Dirac half and compact-kernel transform exact: "
        f"{dirac['relative_dirac_exact'] and dirac['tower_exact'] and dirac['compact_dirac_identity_exact']}"
    )
    print(
        "Gamma-traceless tower dimensions: "
        f"{dirac['tower_dimensions']}"
    )
    print(
        "Explicit projected-wedge complex and positive tower resolution exact: "
        f"{symbol['projected_wedge_complex_exact'] and symbol['resolved_positive_tower_exact_in_range']}"
    )
    print(
        "Gamma-resolution pairing moves exactly to the positive cumulative core: "
        f"{gamma_pairing['pairing_exact']}"
    )
    print(
        "Bars-margin first-difference identity from B_Gamma and H_4 exact: "
        f"{gamma_pairing['difference_identity_exact']}"
    )
    print(
        "Outer-oriented gamma-prefix kernel reproduces the full Bars margin: "
        f"{gamma_pairing['prefix_pairing_exact']}"
    )
    print(
        "It closes to the positive B3 hook shell but remains virtual in D4: "
        f"{gamma_pairing['prefix_kernel']['branches_positive'] and gamma_pairing['prefix_kernel']['prefix_virtual_from_degree_zero']}"
    )
    print(
        "Pi_3/Pi_4 equal no raw transverse/core exterior-form multiplicity in scan: "
        f"{primitive['no_raw_form_match_in_scan'] and primitive['no_core_raw_form_match_in_scan']}"
    )
    print(
        "Short Pi_4/core Lambda^3 match through 10 breaks at degree 11: "
        f"{primitive['accidental_core_candidate'] and primitive['accidental_candidate_breaks_at_eleven']}"
    )
    print(
        "Three-hook core functional reproduces the original scalar index: "
        f"{primitive['core_index_exact']}"
    )
    print("Protected SO(10) baseline imported: NO")
    print(f"Runtime: {time.time() - started:.3f}s")

    return {
        "relative": relative,
        "cumulative_kernel": cumulative_kernel,
        "core_boundary": core_boundary,
        "hook_symbol": hook_symbol,
        "transverse": transverse,
        "oriented_core": oriented_core,
        "hook_diagonal": hook_diagonal,
        "hook_translation": hook_translation,
        "koszul": koszul,
        "mismatch": mismatch,
        "dirac": dirac,
        "symbol": symbol,
        "oriented_hook_symbol": oriented_hook_symbol,
        "gamma_pairing": gamma_pairing,
        "primitive": primitive,
        "all_exact": (
            relative["relative_euler_exact"]
            and relative["zq_factorization_exact"]
            and relative["weyl_bridge_exact_on_fundamentals"]
            and cumulative_kernel["all_exact"]
            and core_boundary["all_orders_certified"]
            and hook_symbol["all_exact"]
            and transverse["independent_exact"]
            and oriented_core["all_exact"]
            and hook_diagonal["diagonal_difference_exact"]
            and koszul["all_exact"]
            and koszul["raw_injectivity_fails_from_two"]
            and mismatch["no_equivariant_linear_identification"]
            and dirac["relative_dirac_exact"]
            and dirac["tower_exact"]
            and dirac["compact_dirac_identity_exact"]
            and symbol["restriction_telescope_exact"]
            and symbol["alternating_restriction_zero"]
            and symbol["adjacent_vector_couplings_unique"]
            and symbol["path_only"]
            and symbol["top_symbol_injective_data"]
            and symbol["projected_wedge_complex_exact"]
            and symbol["resolved_positive_tower_exact_in_range"]
            and oriented_hook_symbol["all_exact"]
            and oriented_hook_symbol["free_polynomial_symbol_injective"]
            and gamma_pairing["pairing_exact"]
            and gamma_pairing["difference_identity_exact"]
            and gamma_pairing["prefix_kernel"]["all_exact"]
            and gamma_pairing["prefix_pairing_exact"]
            and primitive["core_index_exact"]
        ),
    }


def run_self_test():
    """Exercise every exact identity and a short independent comparison."""
    result = run_analysis(maximum_degree=8, compare_hft=True)
    if not result["all_exact"]:
        raise AssertionError("An exact DDF/Koszul audit failed")
    if not result["transverse"]["positive_in_range"]:
        raise AssertionError("The transverse quotient has a negative coefficient")
    if not result["oriented_core"]["positive_in_range"]:
        raise AssertionError("The canonical oriented B4 core has a negative coefficient")
    if not result["primitive"]["no_raw_form_match_in_scan"]:
        raise AssertionError("Unexpected raw-form match; inspect the candidate")
    if not result["primitive"]["no_core_raw_form_match_in_scan"]:
        raise AssertionError("Unexpected raw core-form match; inspect the candidate")
    if not result["primitive"]["accidental_core_candidate"]:
        raise AssertionError("Expected short core candidate changed")
    if not result["primitive"]["accidental_candidate_breaks_at_eleven"]:
        raise AssertionError("Short core candidate did not break at degree 11")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Audit the cumulative core and DDF/Koszul interpretation of "
            "primitive dominance"
        )
    )
    parser.add_argument("--maximum-degree", type=int, default=10)
    parser.add_argument("--compare-hft", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            return 0 if run_self_test() else 1
        result = run_analysis(
            maximum_degree=args.maximum_degree,
            compare_hft=args.compare_hft,
        )
    except Exception as error:
        print(f"TK6B.6e FAILED: {error}", file=sys.stderr)
        return 1
    return 0 if result["all_exact"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
