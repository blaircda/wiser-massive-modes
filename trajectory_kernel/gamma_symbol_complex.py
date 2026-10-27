"""Exact Clifford audit of the Dirac-oriented five-term symbol.

The five ``Spin(8)`` representations occurring after positive relative
Dirac orientation can be realized as gamma-traceless spinor-valued forms

    U_p = ker(gamma contraction:
              Lambda^p(V) tensor S+ -> Lambda^(p-1)(V) tensor S-),
    0 <= p <= 4.

Branching to the stabilizer of a nonzero vector shows that adjacent vector
couplings have the dimensions required by an exact symbol sequence, but it
does not check that consecutive symbols compose to zero.  This module makes
the adjacent maps explicitly.  It uses the split eight-dimensional Clifford
model on ``Lambda^*(QQ^4)`` and projects exterior multiplication back to the
gamma-traceless summand.  All ranks and compositions are computed over the
rationals.

This is a derivation/obstruction audit.  It does not import the protected
SO(10) baseline and it does not assume that the symbols act on the HFT
massive-primary multiplicity module.  It also constructs the complete
gamma-trace triangle, proves the universal Clifford-valued Cartan identity,
and factors the failure of a projected mixed-chirality map through an
explicit invertible trace Laplacian.  That local transfer formula sharpens,
but does not prove, the required global HFT homology concentration.
"""

import argparse
import sys

from sage.all import QQ, WeylCharacterRing, matrix

from trajectory_kernel.hft_analytic_support import (
    D4,
    D4_VECTOR,
    d4_dynkin_from_twice_orthogonal,
)


VECTOR_DIMENSION = 8
HALF_SPIN_DIMENSION = 8
B3 = WeylCharacterRing("B3", style="coroots")


def _d4_dynkin_label(highest_weight):
    """Recover a ``D4`` Dynkin label from an orthogonal-basis weight."""
    twice = tuple(int(2 * value) for value in highest_weight.to_vector())
    return d4_dynkin_from_twice_orthogonal(twice)


def positive_outer_orientation(character):
    """Keep the ``D4`` terms whose third Dynkin label exceeds the fourth."""
    result = D4(0)
    fixed = []
    for highest_weight, coefficient in character.monomial_coefficients().items():
        label = _d4_dynkin_label(highest_weight)
        if label[2] > label[3]:
            result += coefficient * D4(*label)
        elif label[2] == label[3]:
            fixed.append((label, int(coefficient)))
    return result, tuple(fixed)


def _subsets_of_parity(parity):
    """Return the four-bit spinor basis with the requested parity."""
    return tuple(
        bits
        for bits in range(1 << 4)
        if bits.bit_count() % 2 == parity
    )


SPIN_BASES = {
    0: _subsets_of_parity(0),
    1: _subsets_of_parity(1),
}


def _form_basis(degree):
    """Return the increasing tuples forming the exterior basis of ``V``."""
    from itertools import combinations

    return tuple(combinations(range(VECTOR_DIMENSION), degree))


def _tensor_basis(form_degree, spin_parity):
    return tuple(
        (form, spin)
        for form in _form_basis(form_degree)
        for spin in SPIN_BASES[spin_parity]
    )


def _exterior_sign(form, vector_index):
    """Return the sign for wedging ``vector_index`` on the left."""
    if vector_index in form:
        return 0
    return -1 if sum(entry < vector_index for entry in form) % 2 else 1


def _wedge_basis_vector(form, vector_index):
    sign = _exterior_sign(form, vector_index)
    if not sign:
        return None
    return tuple(sorted((vector_index,) + form)), sign


def _gamma_basis_vector(vector_index, spin):
    """Act in the split Clifford model.

    The first four vector basis elements act by exterior multiplication on
    ``Lambda^*(QQ^4)``.  The final four act by twice contraction.  Hence

        gamma(a_i) gamma(b_j) + gamma(b_j) gamma(a_i) = 2 delta_ij.
    """
    if vector_index < 4:
        position = vector_index
        if spin & (1 << position):
            return None
        sign = -1 if (spin & ((1 << position) - 1)).bit_count() % 2 else 1
        return spin | (1 << position), QQ(sign)

    position = vector_index - 4
    if not spin & (1 << position):
        return None
    sign = -1 if (spin & ((1 << position) - 1)).bit_count() % 2 else 1
    return spin & ~(1 << position), QQ(2 * sign)


def _dual_vector_index(vector_index):
    """Return the metric-dual split basis index."""
    return vector_index + 4 if vector_index < 4 else vector_index - 4


def gamma_contraction_matrix(form_degree, spin_parity=0):
    """Matrix of gamma contraction on spinor-valued forms."""
    if form_degree == 0:
        return matrix(QQ, 0, HALF_SPIN_DIMENSION)
    source = _tensor_basis(form_degree, spin_parity)
    target = _tensor_basis(form_degree - 1, 1 - spin_parity)
    target_index = {entry: index for index, entry in enumerate(target)}
    entries = {}
    for column, (form, spin) in enumerate(source):
        for position, vector_index in enumerate(form):
            gamma = _gamma_basis_vector(vector_index, spin)
            if gamma is None:
                continue
            new_spin, gamma_coefficient = gamma
            new_form = form[:position] + form[position + 1 :]
            coefficient = ((-1) ** position) * gamma_coefficient
            row = target_index[(new_form, new_spin)]
            entries[(row, column)] = entries.get((row, column), QQ(0)) + coefficient
    return matrix(QQ, len(target), len(source), entries, sparse=True)


def gamma_wedge_matrix(form_degree, spin_parity=1):
    """Matrix of invariant gamma exterior multiplication.

    This is the map from degree ``form_degree`` and parity ``spin_parity``
    to degree ``form_degree + 1`` and the opposite spin parity.
    """
    source = _tensor_basis(form_degree, spin_parity)
    target = _tensor_basis(form_degree + 1, 1 - spin_parity)
    target_index = {entry: index for index, entry in enumerate(target)}
    entries = {}
    for column, (form, spin) in enumerate(source):
        for vector_index in range(VECTOR_DIMENSION):
            wedge = _wedge_basis_vector(form, vector_index)
            if wedge is None:
                continue
            new_form, wedge_coefficient = wedge
            gamma = _gamma_basis_vector(_dual_vector_index(vector_index), spin)
            if gamma is None:
                continue
            new_spin, gamma_coefficient = gamma
            row = target_index[(new_form, new_spin)]
            coefficient = wedge_coefficient * gamma_coefficient
            entries[(row, column)] = entries.get((row, column), QQ(0)) + coefficient
    return matrix(QQ, len(target), len(source), entries, sparse=True)


def exterior_multiplication_matrix(form_degree, vector, spin_parity=0):
    """Matrix of exterior multiplication by one vector on fixed-chirality spinors."""
    vector = tuple(QQ(value) for value in vector)
    if len(vector) != VECTOR_DIMENSION:
        raise ValueError("Expected an eight-component vector")
    source = _tensor_basis(form_degree, spin_parity)
    target = _tensor_basis(form_degree + 1, spin_parity)
    target_index = {entry: index for index, entry in enumerate(target)}
    entries = {}
    for column, (form, spin) in enumerate(source):
        for vector_index, value in enumerate(vector):
            if not value:
                continue
            wedge = _wedge_basis_vector(form, vector_index)
            if wedge is None:
                continue
            new_form, coefficient = wedge
            row = target_index[(new_form, spin)]
            entries[(row, column)] = (
                entries.get((row, column), QQ(0)) + value * coefficient
            )
    return matrix(QQ, len(target), len(source), entries, sparse=True)


def gamma_traceless_decomposition(form_degree, spin_parity=0):
    """Return an exact basis and projection for the gamma-traceless summand."""
    contraction = gamma_contraction_matrix(
        form_degree, spin_parity=spin_parity
    )
    ambient_dimension = contraction.ncols()
    if form_degree == 0:
        kernel_columns = matrix.identity(QQ, ambient_dimension)
        projection = matrix.identity(QQ, ambient_dimension)
        return {
            "contraction": contraction,
            "kernel_columns": kernel_columns,
            "gamma_wedge_columns": matrix(QQ, ambient_dimension, 0),
            "projection_coordinates": projection,
            "gamma_wedge_coordinates": matrix(QQ, 0, ambient_dimension),
            "ambient_dimension": ambient_dimension,
            "kernel_dimension": ambient_dimension,
        }

    kernel_rows = contraction.right_kernel().basis_matrix()
    kernel_columns = kernel_rows.transpose()
    gamma_wedge = gamma_wedge_matrix(
        form_degree - 1, spin_parity=1 - spin_parity
    )
    decomposition = kernel_columns.augment(gamma_wedge)
    if decomposition.nrows() != decomposition.ncols():
        raise AssertionError(
            "Gamma-traceless plus gamma-wedge dimensions do not fill the ambient space"
        )
    if decomposition.rank() != ambient_dimension:
        raise AssertionError("Gamma-wedge is not a complementary summand")
    inverse = decomposition.inverse()
    kernel_dimension = kernel_columns.ncols()
    projection = inverse[:kernel_dimension, :]
    gamma_wedge_coordinates = inverse[kernel_dimension:, :]
    return {
        "contraction": contraction,
        "kernel_columns": kernel_columns,
        "gamma_wedge_columns": gamma_wedge,
        "projection_coordinates": projection,
        "gamma_wedge_coordinates": gamma_wedge_coordinates,
        "ambient_dimension": ambient_dimension,
        "kernel_dimension": kernel_dimension,
    }


def projected_wedge_symbol(
    form_degree, vector, decompositions=None, spin_parity=0
):
    """Return ``U_p -> U_(p+1)`` induced by projected exterior product."""
    if decompositions is None:
        decompositions = tuple(
            gamma_traceless_decomposition(
                degree, spin_parity=spin_parity
            )
            for degree in range(5)
        )
    source = decompositions[form_degree]
    target = decompositions[form_degree + 1]
    wedge = exterior_multiplication_matrix(
        form_degree, vector, spin_parity=spin_parity
    )
    return (
        target["projection_coordinates"]
        * wedge
        * source["kernel_columns"]
    )


def clifford_multiplication_matrix(form_degree, vector, spin_parity=0):
    """Act by ``gamma(vector)`` on the spinor factor of a fixed form degree."""
    vector = tuple(QQ(value) for value in vector)
    if len(vector) != VECTOR_DIMENSION:
        raise ValueError("Expected an eight-component vector")
    source = _tensor_basis(form_degree, spin_parity)
    target = _tensor_basis(form_degree, 1 - spin_parity)
    target_index = {entry: index for index, entry in enumerate(target)}
    entries = {}
    for column, (form, spin) in enumerate(source):
        for vector_index, value in enumerate(vector):
            if not value:
                continue
            gamma = _gamma_basis_vector(vector_index, spin)
            if gamma is None:
                continue
            new_spin, coefficient = gamma
            row = target_index[(form, new_spin)]
            entries[(row, column)] = (
                entries.get((row, column), QQ(0)) + value * coefficient
            )
    return matrix(QQ, len(target), len(source), entries, sparse=True)


def projected_clifford_symbol(
    form_degree,
    vector,
    source_decompositions=None,
    target_decompositions=None,
    spin_parity=0,
):
    """Project ``gamma(vector)`` between opposite gamma-traceless towers."""
    if source_decompositions is None:
        source_decompositions = tuple(
            gamma_traceless_decomposition(
                degree, spin_parity=spin_parity
            )
            for degree in range(5)
        )
    if target_decompositions is None:
        target_decompositions = tuple(
            gamma_traceless_decomposition(
                degree, spin_parity=1 - spin_parity
            )
            for degree in range(5)
        )
    source = source_decompositions[form_degree]
    target = target_decompositions[form_degree]
    clifford = clifford_multiplication_matrix(
        form_degree, vector, spin_parity=spin_parity
    )
    return (
        target["projection_coordinates"]
        * clifford
        * source["kernel_columns"]
    )


def split_quadratic_form(vector):
    """Return the quadratic form compatible with the split Clifford action."""
    vector = tuple(QQ(value) for value in vector)
    return sum(vector[index] * vector[index + 4] for index in range(4))


def mixed_chirality_symbol_audit(vector):
    """Test the projected Clifford action against both chiral complexes.

    This is the literal symbol-level candidate suggested by the Ramond
    operator ``gamma . alpha_(-1)``.  The audit deliberately records both
    commutators and anticommutators: only a zero relation would make the
    projected Clifford maps act on the homology of the projected-wedge
    complex without an additional homotopy correction.
    """
    vector = tuple(QQ(value) for value in vector)
    decompositions = {
        parity: tuple(
            gamma_traceless_decomposition(degree, spin_parity=parity)
            for degree in range(5)
        )
        for parity in (0, 1)
    }
    wedges = {
        parity: tuple(
            projected_wedge_symbol(
                degree,
                vector,
                decompositions=decompositions[parity],
                spin_parity=parity,
            )
            for degree in range(4)
        )
        for parity in (0, 1)
    }
    clifford = {
        parity: tuple(
            projected_clifford_symbol(
                degree,
                vector,
                source_decompositions=decompositions[parity],
                target_decompositions=decompositions[1 - parity],
                spin_parity=parity,
            )
            for degree in range(5)
        )
        for parity in (0, 1)
    }
    relations = {}
    for parity in (0, 1):
        commutator_ranks = []
        anticommutator_ranks = []
        for degree in range(4):
            left = clifford[parity][degree + 1] * wedges[parity][degree]
            right = wedges[1 - parity][degree] * clifford[parity][degree]
            commutator_ranks.append((left - right).rank())
            anticommutator_ranks.append((left + right).rank())
        square_ranks = tuple(
            (
                clifford[1 - parity][degree] * clifford[parity][degree]
            ).rank()
            for degree in range(5)
        )
        relations[parity] = {
            "commutator_ranks": tuple(commutator_ranks),
            "anticommutator_ranks": tuple(anticommutator_ranks),
            "square_ranks": square_ranks,
        }
    return {
        "vector": vector,
        "quadratic_form": split_quadratic_form(vector),
        "wedge_ranks": {
            parity: tuple(item.rank() for item in wedges[parity])
            for parity in (0, 1)
        },
        "clifford_ranks": {
            parity: tuple(item.rank() for item in clifford[parity])
            for parity in (0, 1)
        },
        "relations": relations,
    }


def mixed_chirality_defect_factorization_audit(vector):
    """Factor the projected Clifford defect through gamma-trace complements.

    Write ``I_p P_p`` for the ambient projector onto the gamma-traceless
    summand and ``G_p H_p`` for its gamma-wedge complement.  The exact
    decomposition constructed above gives

        1 = I_p P_p + G_p H_p.

    Exterior multiplication ``E`` and Clifford multiplication ``C`` commute
    on the ambient spinor-valued form spaces.  After projection to the two
    opposite-chirality gamma-traceless rows, however, the induced maps need
    not commute.  Their defect has the exact factorization

        q_(p+1) sigma_p - sigma'_p q_p
          = - P' C (G H) E I + P' E (G' H') C I.

    Thus every part of the defect passes through a discarded gamma-trace
    summand.  This is the finite-dimensional algebraic datum needed before a
    homological-transfer construction can be attempted; it does not by
    itself prove that the transferred map exists on the HFT quotient.
    """
    vector = tuple(QQ(value) for value in vector)
    decompositions = {
        parity: tuple(
            gamma_traceless_decomposition(degree, spin_parity=parity)
            for degree in range(5)
        )
        for parity in (0, 1)
    }

    def gamma_traceless_projector(decomposition):
        return (
            decomposition["kernel_columns"]
            * decomposition["projection_coordinates"]
        )

    def complement_projector(decomposition):
        return (
            decomposition["gamma_wedge_columns"]
            * decomposition["gamma_wedge_coordinates"]
        )

    projector_decomposition = {}
    for parity in (0, 1):
        checks = []
        for degree, decomposition in enumerate(decompositions[parity]):
            identity = matrix.identity(QQ, decomposition["ambient_dimension"])
            traceless = gamma_traceless_projector(decomposition)
            complement = complement_projector(decomposition)
            checks.append(
                {
                    "degree": degree,
                    "sum_is_identity": traceless + complement == identity,
                    "cross_products_zero": (
                        traceless * complement == 0
                        and complement * traceless == 0
                    ),
                    "complement_rank": complement.rank(),
                    "gamma_wedge_rank": decomposition[
                        "gamma_wedge_columns"
                    ].rank(),
                }
            )
        projector_decomposition[parity] = tuple(checks)

    records = {}
    for parity in (0, 1):
        opposite = 1 - parity
        parity_records = []
        for degree in range(4):
            source = decompositions[parity][degree]
            same_target = decompositions[parity][degree + 1]
            opposite_source = decompositions[opposite][degree]
            opposite_target = decompositions[opposite][degree + 1]

            exterior = exterior_multiplication_matrix(
                degree, vector, spin_parity=parity
            )
            opposite_exterior = exterior_multiplication_matrix(
                degree, vector, spin_parity=opposite
            )
            clifford_source = clifford_multiplication_matrix(
                degree, vector, spin_parity=parity
            )
            clifford_target = clifford_multiplication_matrix(
                degree + 1, vector, spin_parity=parity
            )

            sigma = (
                same_target["projection_coordinates"]
                * exterior
                * source["kernel_columns"]
            )
            opposite_sigma = (
                opposite_target["projection_coordinates"]
                * opposite_exterior
                * opposite_source["kernel_columns"]
            )
            q_source = (
                opposite_source["projection_coordinates"]
                * clifford_source
                * source["kernel_columns"]
            )
            q_target = (
                opposite_target["projection_coordinates"]
                * clifford_target
                * same_target["kernel_columns"]
            )
            defect = q_target * sigma - opposite_sigma * q_source

            same_target_complement = complement_projector(same_target)
            opposite_source_complement = complement_projector(opposite_source)
            first_trace_term = (
                -opposite_target["projection_coordinates"]
                * clifford_target
                * same_target_complement
                * exterior
                * source["kernel_columns"]
            )
            second_trace_term = (
                opposite_target["projection_coordinates"]
                * opposite_exterior
                * opposite_source_complement
                * clifford_source
                * source["kernel_columns"]
            )
            reconstructed = first_trace_term + second_trace_term
            ambient_commutator = (
                clifford_target * exterior
                - opposite_exterior * clifford_source
            )
            one_sided_transfer = (
                -2
                * opposite_target["projection_coordinates"]
                * opposite_exterior
                * same_target["gamma_wedge_coordinates"]
                * exterior
                * source["kernel_columns"]
            )
            trace_laplacian = (
                gamma_contraction_matrix(degree + 1, spin_parity=parity)
                * same_target["gamma_wedge_columns"]
            )
            laplacian_transfer = (
                -2
                * opposite_target["projection_coordinates"]
                * opposite_exterior
                * trace_laplacian.inverse()
                * clifford_source
                * source["kernel_columns"]
            )

            # Repeat the two trace factors without multiplying G H together.
            # This explicitly certifies passage through the lower-degree
            # spinor-form spaces which parametrize the trace complements.
            first_through_coordinates = (
                -opposite_target["projection_coordinates"]
                * clifford_target
                * same_target["gamma_wedge_columns"]
                * same_target["gamma_wedge_coordinates"]
                * exterior
                * source["kernel_columns"]
            )
            second_through_coordinates = (
                opposite_target["projection_coordinates"]
                * opposite_exterior
                * opposite_source["gamma_wedge_columns"]
                * opposite_source["gamma_wedge_coordinates"]
                * clifford_source
                * source["kernel_columns"]
            )
            first_trace_coordinates = (
                same_target["gamma_wedge_coordinates"]
                * exterior
                * source["kernel_columns"]
            )
            second_trace_coordinates = (
                opposite_source["gamma_wedge_coordinates"]
                * clifford_source
                * source["kernel_columns"]
            )

            parity_records.append(
                {
                    "degree": degree,
                    "defect_rank": defect.rank(),
                    "first_trace_term_rank": first_trace_term.rank(),
                    "second_trace_term_rank": second_trace_term.rank(),
                    "first_trace_coordinate_rank": (
                        first_trace_coordinates.rank()
                    ),
                    "second_trace_coordinate_rank": (
                        second_trace_coordinates.rank()
                    ),
                    "ambient_commutator_rank": ambient_commutator.rank(),
                    "factorization_exact": defect == reconstructed,
                    "second_trace_term_zero": second_trace_term == 0,
                    "one_sided_transfer_exact": defect == one_sided_transfer,
                    "laplacian_transfer_exact": defect == laplacian_transfer,
                    "first_coordinate_factor_exact": (
                        first_trace_term == first_through_coordinates
                    ),
                    "second_coordinate_factor_exact": (
                        second_trace_term == second_through_coordinates
                    ),
                }
            )
        records[parity] = tuple(parity_records)

    all_projector_decompositions_exact = all(
        record["sum_is_identity"] and record["cross_products_zero"]
        for parity_records in projector_decomposition.values()
        for record in parity_records
    )
    all_factorizations_exact = all(
        record["factorization_exact"]
        and record["second_trace_term_zero"]
        and record["one_sided_transfer_exact"]
        and record["laplacian_transfer_exact"]
        and record["first_coordinate_factor_exact"]
        and record["second_coordinate_factor_exact"]
        and record["ambient_commutator_rank"] == 0
        for parity_records in records.values()
        for record in parity_records
    )
    return {
        "vector": vector,
        "quadratic_form": split_quadratic_form(vector),
        "projector_decomposition": projector_decomposition,
        "projector_decompositions_exact": (
            all_projector_decompositions_exact
        ),
        "records": records,
        "all_factorizations_exact": all_factorizations_exact,
    }


def recursive_gamma_triangle_decompositions(maximum_degree=4):
    """Split every spinor-form space into all gamma-traceless diagonals.

    Recursively applying

        A_p^s = U_p^s direct-sum gamma-wedge(A_(p-1)^(1-s))

    gives a triangular decomposition

        A_p^s = U_p^s direct-sum U_(p-1)^(1-s)
                direct-sum ... direct-sum U_0^(s+p).

    The returned change-of-basis matrices are exact over ``QQ``.  This is the
    finite algebraic version of the spinor-form triangle used by higher-spin
    Dirac complexes.
    """
    maximum_degree = int(maximum_degree)
    if maximum_degree < 0 or maximum_degree > VECTOR_DIMENSION:
        raise ValueError("maximum_degree must lie between zero and eight")

    basic = {
        (degree, parity): gamma_traceless_decomposition(
            degree, spin_parity=parity
        )
        for degree in range(maximum_degree + 1)
        for parity in (0, 1)
    }
    result = {}
    for degree in range(maximum_degree + 1):
        for parity in (0, 1):
            decomposition = basic[(degree, parity)]
            kernel_columns = decomposition["kernel_columns"]
            if degree == 0:
                change_of_basis = kernel_columns
                block_dimensions = (decomposition["kernel_dimension"],)
            else:
                lower = result[(degree - 1, 1 - parity)]
                trace_columns = (
                    decomposition["gamma_wedge_columns"]
                    * lower["change_of_basis"]
                )
                change_of_basis = kernel_columns.augment(trace_columns)
                block_dimensions = (
                    decomposition["kernel_dimension"],
                ) + lower["block_dimensions"]
            if change_of_basis.nrows() != change_of_basis.ncols():
                raise AssertionError("Recursive gamma triangle is not square")
            if change_of_basis.rank() != change_of_basis.nrows():
                raise AssertionError("Recursive gamma triangle is singular")
            result[(degree, parity)] = {
                "change_of_basis": change_of_basis,
                "inverse_change_of_basis": change_of_basis.inverse(),
                "block_dimensions": block_dimensions,
                "basic_decomposition": decomposition,
            }
    return result


def _block_rank_table(linear_map, target_dimensions, source_dimensions):
    """Return the ranks of all blocks of a matrix in triangular coordinates."""
    target_offsets = [0]
    for dimension in target_dimensions:
        target_offsets.append(target_offsets[-1] + dimension)
    source_offsets = [0]
    for dimension in source_dimensions:
        source_offsets.append(source_offsets[-1] + dimension)
    return tuple(
        tuple(
            linear_map[
                target_offsets[row] : target_offsets[row + 1],
                source_offsets[column] : source_offsets[column + 1],
            ].rank()
            for column in range(len(source_dimensions))
        )
        for row in range(len(target_dimensions))
    )


def gamma_triangle_audit(vector):
    """Audit exterior and Clifford actions on the full spinor-form triangle.

    The projected gamma-traceless row alone is not preserved by the joint
    exterior/Clifford action.  In recursive triangular coordinates the full
    ambient identities are restored.  The top-left block relation writes the
    failed projected commutator as a finite sum of paths through lower
    gamma-trace diagonals, making the needed transfer correction explicit.
    """
    vector = tuple(QQ(value) for value in vector)
    triangle = recursive_gamma_triangle_decompositions(4)
    exterior_actions = {}
    clifford_actions = {}

    for parity in (0, 1):
        for degree in range(4):
            source = triangle[(degree, parity)]
            target = triangle[(degree + 1, parity)]
            ambient = exterior_multiplication_matrix(
                degree, vector, spin_parity=parity
            )
            exterior_actions[(degree, parity)] = (
                target["inverse_change_of_basis"]
                * ambient
                * source["change_of_basis"]
            )
        for degree in range(5):
            source = triangle[(degree, parity)]
            target = triangle[(degree, 1 - parity)]
            ambient = clifford_multiplication_matrix(
                degree, vector, spin_parity=parity
            )
            clifford_actions[(degree, parity)] = (
                target["inverse_change_of_basis"]
                * ambient
                * source["change_of_basis"]
            )

    records = {}
    all_exterior_compositions_zero = True
    all_clifford_squares_exact = True
    all_mixed_relations_exact = True
    all_top_block_transfers_exact = True
    quadratic_scalar = 2 * split_quadratic_form(vector)
    for parity in (0, 1):
        parity_records = []
        for degree in range(4):
            source_dimensions = triangle[(degree, parity)]["block_dimensions"]
            target_dimensions = triangle[(degree + 1, parity)][
                "block_dimensions"
            ]
            opposite_source_dimensions = triangle[
                (degree, 1 - parity)
            ]["block_dimensions"]
            opposite_target_dimensions = triangle[
                (degree + 1, 1 - parity)
            ]["block_dimensions"]
            exterior = exterior_actions[(degree, parity)]
            opposite_exterior = exterior_actions[(degree, 1 - parity)]
            clifford_source = clifford_actions[(degree, parity)]
            clifford_target = clifford_actions[(degree + 1, parity)]

            mixed_left = clifford_target * exterior
            mixed_right = opposite_exterior * clifford_source
            mixed_exact = mixed_left == mixed_right
            all_mixed_relations_exact &= mixed_exact

            first_target = target_dimensions[0]
            first_source = source_dimensions[0]
            direct_defect = (
                clifford_target[:first_target, :first_target]
                * exterior[:first_target, :first_source]
                - opposite_exterior[
                    : opposite_target_dimensions[0],
                    : opposite_source_dimensions[0],
                ]
                * clifford_source[
                    : opposite_source_dimensions[0], :first_source
                ]
            )
            left_trace_paths = sum(
                (
                    clifford_target[
                        :first_target,
                        sum(target_dimensions[:trace_depth]) : sum(
                            target_dimensions[: trace_depth + 1]
                        ),
                    ]
                    * exterior[
                        sum(target_dimensions[:trace_depth]) : sum(
                            target_dimensions[: trace_depth + 1]
                        ),
                        :first_source,
                    ]
                    for trace_depth in range(1, len(target_dimensions))
                ),
                matrix(QQ, first_target, first_source),
            )
            right_trace_paths = sum(
                (
                    opposite_exterior[
                        : opposite_target_dimensions[0],
                        sum(opposite_source_dimensions[:trace_depth]) : sum(
                            opposite_source_dimensions[: trace_depth + 1]
                        ),
                    ]
                    * clifford_source[
                        sum(opposite_source_dimensions[:trace_depth]) : sum(
                            opposite_source_dimensions[: trace_depth + 1]
                        ),
                        :first_source,
                    ]
                    for trace_depth in range(
                        1, len(opposite_source_dimensions)
                    )
                ),
                matrix(QQ, first_target, first_source),
            )
            transferred_correction = right_trace_paths - left_trace_paths
            top_block_transfer_exact = direct_defect == transferred_correction
            all_top_block_transfers_exact &= top_block_transfer_exact

            parity_records.append(
                {
                    "degree": degree,
                    "exterior_block_ranks": _block_rank_table(
                        exterior, target_dimensions, source_dimensions
                    ),
                    "clifford_source_block_ranks": _block_rank_table(
                        clifford_source,
                        opposite_source_dimensions,
                        source_dimensions,
                    ),
                    "direct_defect_rank": direct_defect.rank(),
                    "left_trace_path_rank": left_trace_paths.rank(),
                    "right_trace_path_rank": right_trace_paths.rank(),
                    "transferred_correction_rank": (
                        transferred_correction.rank()
                    ),
                    "mixed_relation_exact": mixed_exact,
                    "top_block_transfer_exact": top_block_transfer_exact,
                }
            )
        for degree in range(3):
            composition = (
                exterior_actions[(degree + 1, parity)]
                * exterior_actions[(degree, parity)]
            )
            all_exterior_compositions_zero &= composition == 0
        for degree in range(5):
            clifford_square = (
                clifford_actions[(degree, 1 - parity)]
                * clifford_actions[(degree, parity)]
            )
            identity = matrix.identity(QQ, clifford_square.nrows())
            all_clifford_squares_exact &= (
                clifford_square == quadratic_scalar * identity
            )
        records[parity] = tuple(parity_records)

    decomposition_dimensions_exact = all(
        sum(data["block_dimensions"])
        == data["change_of_basis"].nrows()
        for data in triangle.values()
    )
    return {
        "vector": vector,
        "quadratic_form": split_quadratic_form(vector),
        "triangle_block_dimensions": {
            key: data["block_dimensions"] for key, data in triangle.items()
        },
        "decomposition_dimensions_exact": decomposition_dimensions_exact,
        "records": records,
        "exterior_compositions_zero": all_exterior_compositions_zero,
        "clifford_squares_exact": all_clifford_squares_exact,
        "mixed_relations_exact": all_mixed_relations_exact,
        "top_block_transfers_exact": all_top_block_transfers_exact,
        "all_exact": (
            decomposition_dimensions_exact
            and all_exterior_compositions_zero
            and all_clifford_squares_exact
            and all_mixed_relations_exact
            and all_top_block_transfers_exact
        ),
    }


def gamma_trace_transfer_identity_audit():
    """Certify the universal gamma-trace homotopy and transfer formulas.

    For every vector ``v`` and spinor-valued ``p``-form, the ambient maps
    obey

        Gamma_(p+1) E_v + E_v Gamma_p = C_v,

    while gamma contraction and gamma wedge obey

        Gamma_(p+1) G_p - G_(p-1) Gamma_p = (8 - 2p) identity.

    Both are checked on all eight vector-basis elements, hence for every
    vector by linearity.  On degrees ``p <= 3`` the trace Laplacian
    ``Gamma_(p+1) G_p`` is invertible.  Consequently the discarded trace
    coordinate of ``E_v`` on a gamma-traceless source is explicitly

        H_(p+1) E_v I_p
          = (Gamma_(p+1) G_p)^(-1) C_v I_p.

    This is the local transfer formula suggested by the spinor-form triangle;
    it is not yet the global homology-concentration theorem for the HFT
    multiplicity module.
    """
    triangle = recursive_gamma_triangle_decompositions(4)
    basis_vectors = tuple(
        tuple(1 if index == basis_index else 0 for index in range(8))
        for basis_index in range(8)
    )
    records = {}
    all_gamma_wedge_identities = True
    all_trace_spectra_exact = True
    all_complement_formulas_exact = True
    all_homotopy_identities_exact = True
    all_leakage_formulas_exact = True
    all_exterior_wedge_identities_exact = True
    all_clifford_wedge_identities_exact = True

    for parity in (0, 1):
        parity_records = []
        for degree in range(5):
            contraction_after_wedge = (
                gamma_contraction_matrix(degree + 1, 1 - parity)
                * gamma_wedge_matrix(degree, parity)
            )
            if degree:
                wedge_after_contraction = (
                    gamma_wedge_matrix(degree - 1, 1 - parity)
                    * gamma_contraction_matrix(degree, parity)
                )
            else:
                wedge_after_contraction = matrix(
                    QQ,
                    contraction_after_wedge.nrows(),
                    contraction_after_wedge.ncols(),
                )
            identity = matrix.identity(
                QQ, contraction_after_wedge.nrows()
            )
            gamma_wedge_identity_exact = (
                contraction_after_wedge
                - wedge_after_contraction
                == (VECTOR_DIMENSION - 2 * degree) * identity
            )
            all_gamma_wedge_identities &= gamma_wedge_identity_exact

            homotopy_vector_checks = []
            exterior_wedge_checks = []
            clifford_wedge_checks = []
            for vector in basis_vectors:
                contraction_after_exterior = (
                    gamma_contraction_matrix(degree + 1, parity)
                    * exterior_multiplication_matrix(
                        degree, vector, spin_parity=parity
                    )
                )
                if degree:
                    exterior_after_contraction = (
                        exterior_multiplication_matrix(
                            degree - 1,
                            vector,
                            spin_parity=1 - parity,
                        )
                        * gamma_contraction_matrix(degree, parity)
                    )
                else:
                    exterior_after_contraction = matrix(
                        QQ,
                        contraction_after_exterior.nrows(),
                        contraction_after_exterior.ncols(),
                    )
                clifford = clifford_multiplication_matrix(
                    degree, vector, spin_parity=parity
                )
                homotopy_vector_checks.append(
                    contraction_after_exterior
                    + exterior_after_contraction
                    == clifford
                )
                if degree <= 3:
                    exterior_wedge_checks.append(
                        exterior_multiplication_matrix(
                            degree + 1,
                            vector,
                            spin_parity=1 - parity,
                        )
                        * gamma_wedge_matrix(degree, parity)
                        + gamma_wedge_matrix(degree + 1, parity)
                        * exterior_multiplication_matrix(
                            degree, vector, spin_parity=parity
                        )
                        == 0
                    )
                    clifford_wedge_checks.append(
                        clifford_multiplication_matrix(
                            degree + 1,
                            vector,
                            spin_parity=1 - parity,
                        )
                        * gamma_wedge_matrix(degree, parity)
                        + gamma_wedge_matrix(degree, 1 - parity)
                        * clifford_multiplication_matrix(
                            degree, vector, spin_parity=parity
                        )
                        == 2
                        * exterior_multiplication_matrix(
                            degree, vector, spin_parity=parity
                        )
                    )
            homotopy_identity_exact = all(homotopy_vector_checks)
            all_homotopy_identities_exact &= homotopy_identity_exact
            exterior_wedge_identity_exact = (
                all(exterior_wedge_checks)
                if exterior_wedge_checks
                else None
            )
            clifford_wedge_identity_exact = (
                all(clifford_wedge_checks)
                if clifford_wedge_checks
                else None
            )
            if exterior_wedge_identity_exact is not None:
                all_exterior_wedge_identities_exact &= (
                    exterior_wedge_identity_exact
                )
                all_clifford_wedge_identities_exact &= (
                    clifford_wedge_identity_exact
                )

            trace_spectrum_exact = None
            complement_formula_exact = None
            leakage_formula_exact = None
            trace_eigenvalues = None
            if degree <= 3:
                # Here ``degree`` is the source degree of gamma wedge, so the
                # relevant target decomposition has degree ``degree + 1`` and
                # chirality ``1 - parity``.
                target_decomposition = gamma_traceless_decomposition(
                    degree + 1, spin_parity=1 - parity
                )
                trace_laplacian = contraction_after_wedge
                if trace_laplacian.rank() != trace_laplacian.nrows():
                    raise AssertionError(
                        "Trace Laplacian unexpectedly singular below middle degree"
                    )
                trace_laplacian_inverse = trace_laplacian.inverse()
                complement_formula_exact = (
                    target_decomposition["gamma_wedge_coordinates"]
                    == trace_laplacian_inverse
                    * gamma_contraction_matrix(degree + 1, 1 - parity)
                )
                all_complement_formulas_exact &= complement_formula_exact

                triangular = triangle[(degree, parity)]
                conjugated_laplacian = (
                    triangular["inverse_change_of_basis"]
                    * trace_laplacian
                    * triangular["change_of_basis"]
                )
                trace_eigenvalues = tuple(
                    (depth + 1)
                    * (VECTOR_DIMENSION - 2 * degree + depth)
                    for depth in range(degree + 1)
                )
                expected_laplacian = matrix(
                    QQ,
                    conjugated_laplacian.nrows(),
                    conjugated_laplacian.ncols(),
                )
                offset = 0
                for dimension, eigenvalue in zip(
                    triangular["block_dimensions"], trace_eigenvalues
                ):
                    expected_laplacian[
                        offset : offset + dimension,
                        offset : offset + dimension,
                    ] = eigenvalue * matrix.identity(QQ, dimension)
                    offset += dimension
                trace_spectrum_exact = (
                    conjugated_laplacian == expected_laplacian
                )
                all_trace_spectra_exact &= trace_spectrum_exact

                leakage_source_parity = 1 - parity
                source_decomposition = gamma_traceless_decomposition(
                    degree, spin_parity=leakage_source_parity
                )
                leakage_checks = []
                for vector in basis_vectors:
                    leakage = (
                        target_decomposition["gamma_wedge_coordinates"]
                        * exterior_multiplication_matrix(
                            degree,
                            vector,
                            spin_parity=leakage_source_parity,
                        )
                        * source_decomposition["kernel_columns"]
                    )
                    expected_leakage = (
                        trace_laplacian_inverse
                        * clifford_multiplication_matrix(
                            degree,
                            vector,
                            spin_parity=leakage_source_parity,
                        )
                        * source_decomposition["kernel_columns"]
                    )
                    leakage_checks.append(leakage == expected_leakage)
                leakage_formula_exact = all(leakage_checks)
                all_leakage_formulas_exact &= leakage_formula_exact

            parity_records.append(
                {
                    "degree": degree,
                    "gamma_wedge_identity_exact": (
                        gamma_wedge_identity_exact
                    ),
                    "homotopy_identity_exact_on_vector_basis": (
                        homotopy_identity_exact
                    ),
                    "exterior_wedge_identity_exact_on_vector_basis": (
                        exterior_wedge_identity_exact
                    ),
                    "clifford_wedge_identity_exact_on_vector_basis": (
                        clifford_wedge_identity_exact
                    ),
                    "trace_eigenvalues": trace_eigenvalues,
                    "trace_spectrum_exact": trace_spectrum_exact,
                    "complement_formula_exact": complement_formula_exact,
                    "leakage_formula_exact_on_vector_basis": (
                        leakage_formula_exact
                    ),
                }
            )
        records[parity] = tuple(parity_records)

    return {
        "records": records,
        "gamma_wedge_identities_exact": all_gamma_wedge_identities,
        "trace_spectra_exact": all_trace_spectra_exact,
        "complement_formulas_exact": all_complement_formulas_exact,
        "homotopy_identities_exact": all_homotopy_identities_exact,
        "leakage_formulas_exact": all_leakage_formulas_exact,
        "exterior_wedge_identities_exact": (
            all_exterior_wedge_identities_exact
        ),
        "clifford_wedge_identities_exact": (
            all_clifford_wedge_identities_exact
        ),
        "all_exact": (
            all_gamma_wedge_identities
            and all_trace_spectra_exact
            and all_complement_formulas_exact
            and all_homotopy_identities_exact
            and all_leakage_formulas_exact
            and all_exterior_wedge_identities_exact
            and all_clifford_wedge_identities_exact
        ),
    }


def resolution_character_audit(maximum_degree=12):
    """Audit the positive tower resolved by the five symbol modules.

    With

        (U_0,...,U_4) =
        ([0,0,1,0], [1,0,1,0], [0,1,1,0],
         [0,0,2,1], [0,0,3,0]),

    the proposed free resolution has degree-``n`` Euler character

        sum_j (-1)^j Sym^(n-j)(V) U_(4-j).

    The result is the single positive gamma-traceless trajectory
    ``[n,0,3,0]``.  Its restriction to ``Spin(7)`` is the cumulative shell
    ``sum_(r=0)^n [r,0,3]``.  The implementation checks full characters, not
    only dimensions.  The accompanying report derives the all-degree
    identity from the Weyl recurrence and interlacing.
    """
    maximum_degree = int(maximum_degree)
    if maximum_degree < 0:
        raise ValueError("maximum_degree must be nonnegative")
    modules = (
        D4(0, 0, 1, 0),
        D4(1, 0, 1, 0),
        D4(0, 1, 1, 0),
        D4(0, 0, 2, 1),
        D4(0, 0, 3, 0),
    )
    records = []
    failures = []
    for degree in range(maximum_degree + 1):
        observed = sum(
            (
                (-1) ** homological_degree
                * D4_VECTOR.symmetric_power(degree - homological_degree)
                * modules[4 - homological_degree]
                for homological_degree in range(min(4, degree) + 1)
            ),
            D4(0),
        )
        expected = D4(degree, 0, 3, 0)
        observed_branch = expected.branch(B3, rule="default")
        expected_branch = sum(
            (B3(shell, 0, 3) for shell in range(degree + 1)),
            B3(0),
        )
        record = {
            "degree": degree,
            "observed": observed,
            "expected": expected,
            "character_exact": observed == expected,
            "dimension": int(expected.degree()),
            "branch": observed_branch,
            "expected_branch": expected_branch,
            "branch_exact": observed_branch == expected_branch,
        }
        records.append(record)
        if not record["character_exact"] or not record["branch_exact"]:
            failures.append(record)
    return {
        "maximum_degree": maximum_degree,
        "modules": modules,
        "records": tuple(records),
        "failures": tuple(failures),
        "all_exact": not failures,
    }


def prefix_kernel_audit(maximum_degree=12):
    """Audit the correctly oriented prefix of the first-difference kernel.

    Put ``J=N(1)`` and ``T=PE(q V) N(q)`` for the five-term resolution
    numerator.  Moving ``<J,M>`` to the cumulative core requires outer
    antisymmetrization before taking the positive orientation.  It is *not*
    legitimate to replace it by ``PE(q V) J`` directly.  If ``S+`` denotes
    the positive orientation of

        PE(q V) (J - tau(J)),

    then the physical first-difference kernel and its prefix are

        K(q) = (1+q^2) T(q) - (1+q) S+(q),
        L(q) = K(q)/(1-q).

    Define

        E_n = [n+1,0,1,0] - [n,1,1,0] + [n,0,2,1],
        E_(-1) = [0,0,1,0].

    The exact answer is ``L_n=E_n-E_(n-1)``.  Its restriction to ``B3`` is
    the single positive shell ``[n,0,3]``, but ``L_n`` is virtual in ``D4``.
    Thus the five-term resolution closes back onto the previously known
    three-hook shell; it does not create a coefficientwise-positive shortcut.
    """
    maximum_degree = int(maximum_degree)
    if maximum_degree < 0:
        raise ValueError("maximum_degree must be nonnegative")

    modules = (
        D4(0, 0, 1, 0),
        D4(1, 0, 1, 0),
        D4(0, 1, 1, 0),
        D4(0, 0, 2, 1),
        D4(0, 0, 3, 0),
    )
    primitive_four = sum(
        ((-1) ** degree * modules[degree] for degree in range(5)),
        D4(0),
    )

    def outer_swap(character):
        result = D4(0)
        for highest_weight, coefficient in character.monomial_coefficients().items():
            a, b, third, fourth = _d4_dynkin_label(highest_weight)
            result += coefficient * D4(a, b, fourth, third)
        return result

    def trajectory(degree):
        return D4(degree, 0, 3, 0) if degree >= 0 else D4(0)

    def hook_euler(degree):
        if degree == -1:
            return modules[0]
        if degree < -1:
            return D4(0)
        return (
            D4(degree + 1, 0, 1, 0)
            - D4(degree, 1, 1, 0)
            + D4(degree, 0, 2, 1)
        )

    primitive_four_antisymmetric = primitive_four - outer_swap(primitive_four)
    prefix = D4(0)
    records = []
    failures = []
    for degree in range(maximum_degree + 1):
        symmetric, symmetric_fixed = positive_outer_orientation(
            D4_VECTOR.symmetric_power(degree) * primitive_four_antisymmetric
        )
        if degree:
            previous_symmetric, previous_fixed = positive_outer_orientation(
                D4_VECTOR.symmetric_power(degree - 1)
                * primitive_four_antisymmetric
            )
        else:
            previous_symmetric = D4(0)
            previous_fixed = ()
        first_difference_kernel = (
            trajectory(degree)
            + trajectory(degree - 2)
            - symmetric
            - previous_symmetric
        )
        prefix += first_difference_kernel
        expected_prefix = hook_euler(degree) - hook_euler(degree - 1)
        expected_branch = B3(degree, 0, 3)
        prefix_coefficients = tuple(prefix.monomial_coefficients().values())
        exact = (
            not symmetric_fixed
            and not previous_fixed
            and prefix == expected_prefix
            and prefix.branch(B3, rule="default") == expected_branch
        )
        record = {
            "degree": degree,
            "first_difference_kernel": first_difference_kernel,
            "prefix": prefix,
            "expected_prefix": expected_prefix,
            "symmetric_fixed_terms": symmetric_fixed,
            "previous_symmetric_fixed_terms": previous_fixed,
            "negative_coefficients": sum(
                coefficient < 0 for coefficient in prefix_coefficients
            ),
            "branch": prefix.branch(B3, rule="default"),
            "expected_branch": expected_branch,
            "exact": exact,
        }
        records.append(record)
        if not exact:
            failures.append(record)

    return {
        "maximum_degree": maximum_degree,
        "primitive_four": primitive_four,
        "records": tuple(records),
        "failures": tuple(failures),
        "all_exact": not failures,
        "prefixes": tuple(record["prefix"] for record in records),
        "prefix_virtual_from_degree_zero": all(
            record["negative_coefficients"] > 0 for record in records
        ),
        "branches_positive": all(
            all(
                coefficient > 0
                for coefficient in record["branch"].monomial_coefficients().values()
            )
            for record in records
        ),
        "closes_to_three_hook_shell": not failures,
    }


def symbol_audit(maximum_degree=12):
    """Compute exact dimensions, ranks, compositions and resolution data."""
    decompositions = tuple(
        gamma_traceless_decomposition(degree) for degree in range(5)
    )
    dimensions = tuple(item["kernel_dimension"] for item in decompositions)
    expected_dimensions = (8, 56, 160, 224, 112)

    vectors = {
        "nonnull": (1, 0, 0, 0, 1, 0, 0, 0),
        "null": (1, 0, 0, 0, 0, 0, 0, 0),
    }
    records = {}
    for name, vector in vectors.items():
        symbols = tuple(
            projected_wedge_symbol(degree, vector, decompositions)
            for degree in range(4)
        )
        compositions = tuple(
            symbols[degree + 1] * symbols[degree]
            for degree in range(3)
        )
        ranks = tuple(symbol.rank() for symbol in symbols)
        composition_ranks = tuple(item.rank() for item in compositions)
        exact_rank_pattern = (
            ranks == (8, 48, 112, 112)
            and all(
                ranks[degree - 1] + ranks[degree] == dimensions[degree]
                for degree in range(1, 4)
            )
        )
        records[name] = {
            "vector": vector,
            "quadratic_form": split_quadratic_form(vector),
            "ranks": ranks,
            "composition_ranks": composition_ranks,
            "compositions_zero": not any(composition_ranks),
            "exact_rank_pattern": exact_rank_pattern,
        }

    # Over the algebraic closure there are only three relevant vector
    # strata: the origin, the punctured null cone, and the non-null orbit.
    # The exact ranks at representatives therefore determine the rank-drop
    # loci.  Number the maps from the right of the free resolution.  The
    # Buchsbaum--Eisenbud grade requirements are 1,2,3,4, while the observed
    # codimensions are 1,8,8,8 respectively.
    expected_ranks = (8, 48, 112, 112)
    grade_requirements_from_right = (1, 2, 3, 4)
    degeneracy_codimensions_from_right = (1, 8, 8, 8)
    grade_conditions = tuple(
        codimension >= requirement
        for codimension, requirement in zip(
            degeneracy_codimensions_from_right,
            grade_requirements_from_right,
        )
    )
    resolution = resolution_character_audit(maximum_degree)
    prefix_kernel = prefix_kernel_audit(maximum_degree)
    polynomial_complex_exact = (
        dimensions == expected_dimensions
        and records["nonnull"]["ranks"] == expected_ranks
        and records["null"]["ranks"][:3] == expected_ranks[:3]
        and records["nonnull"]["compositions_zero"]
        and records["null"]["compositions_zero"]
        and all(grade_conditions)
    )
    return {
        "dimensions": dimensions,
        "expected_dimensions": expected_dimensions,
        "dimensions_exact": dimensions == expected_dimensions,
        "records": records,
        "expected_ranks": expected_ranks,
        "grade_requirements_from_right": grade_requirements_from_right,
        "degeneracy_codimensions_from_right": (
            degeneracy_codimensions_from_right
        ),
        "grade_conditions": grade_conditions,
        "polynomial_complex_exact": polynomial_complex_exact,
        "resolution": resolution,
        "positive_tower_exact_in_range": resolution["all_exact"],
        "prefix_kernel": prefix_kernel,
        "prefix_kernel_exact_in_range": prefix_kernel["all_exact"],
    }


def run_self_test():
    result = symbol_audit()
    if not result["dimensions_exact"]:
        raise AssertionError("Gamma-traceless dimensions do not match the Dirac tower")
    if not result["polynomial_complex_exact"]:
        raise AssertionError("The projected-wedge free complex failed exactness")
    if not result["positive_tower_exact_in_range"]:
        raise AssertionError("The free-resolution character identity failed")
    if not result["prefix_kernel_exact_in_range"]:
        raise AssertionError("The gamma prefix-kernel identity failed")
    if not result["prefix_kernel"]["prefix_virtual_from_degree_zero"]:
        raise AssertionError("The prefix-kernel obstruction changed")
    if not result["prefix_kernel"]["branches_positive"]:
        raise AssertionError("A prefix kernel has a signed B3 branch")
    mixed_factorizations = {
        name: mixed_chirality_defect_factorization_audit(vector)
        for name, vector in {
            "nonnull": (1, 0, 0, 0, 1, 0, 0, 0),
            "null": (1, 0, 0, 0, 0, 0, 0, 0),
        }.items()
    }
    for name, audit in mixed_factorizations.items():
        if not audit["projector_decompositions_exact"]:
            raise AssertionError(
                f"The gamma-trace projector decomposition failed at {name}"
            )
        if not audit["all_factorizations_exact"]:
            raise AssertionError(
                f"The mixed-chirality defect factorization failed at {name}"
            )
    result["mixed_chirality_defect_factorizations"] = mixed_factorizations
    triangle_audits = {
        name: gamma_triangle_audit(vector)
        for name, vector in {
            "nonnull": (1, 0, 0, 0, 1, 0, 0, 0),
            "null": (1, 0, 0, 0, 0, 0, 0, 0),
        }.items()
    }
    for name, audit in triangle_audits.items():
        if not audit["all_exact"]:
            raise AssertionError(f"The full gamma triangle failed at {name}")
    result["gamma_triangle_audits"] = triangle_audits
    trace_transfer = gamma_trace_transfer_identity_audit()
    if not trace_transfer["all_exact"]:
        raise AssertionError("The universal gamma-trace transfer identities failed")
    result["gamma_trace_transfer_identity"] = trace_transfer
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Audit the exact gamma-traceless projected-wedge symbols"
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    result = run_self_test() if args.self_test else symbol_audit()
    print("Gamma-traceless dimensions:", result["dimensions"])
    for name, record in result["records"].items():
        print(
            f"{name}: q={record['quadratic_form']}, ranks={record['ranks']}, "
            f"composition ranks={record['composition_ranks']}, "
            f"complex={record['compositions_zero']}, "
            f"exact-rank-pattern={record['exact_rank_pattern']}"
        )
    print("Buchsbaum--Eisenbud grade conditions:", result["grade_conditions"])
    print("Polynomial free complex exact:", result["polynomial_complex_exact"])
    print(
        "Resolved positive tower through degree "
        f"{result['resolution']['maximum_degree']}: "
        f"{result['positive_tower_exact_in_range']}"
    )
    print(
        "Outer-oriented prefix closes to the positive B3 hook shell: "
        f"{result['prefix_kernel_exact_in_range'] and result['prefix_kernel']['branches_positive']}"
    )
    print(
        "Coefficientwise D4 prefix positivity refuted: "
        f"{result['prefix_kernel']['prefix_virtual_from_degree_zero']}"
    )
    if "mixed_chirality_defect_factorizations" in result:
        for name, audit in result[
            "mixed_chirality_defect_factorizations"
        ].items():
            defect_ranks = {
                parity: tuple(
                    record["defect_rank"]
                    for record in audit["records"][parity]
                )
                for parity in (0, 1)
            }
            print(
                f"{name} mixed defect ranks={defect_ranks}, "
                "trace-complement factorization="
                f"{audit['all_factorizations_exact']}"
            )
    if "gamma_triangle_audits" in result:
        for name, audit in result["gamma_triangle_audits"].items():
            trace_path_ranks = {
                parity: tuple(
                    (
                        record["direct_defect_rank"],
                        record["left_trace_path_rank"],
                        record["right_trace_path_rank"],
                    )
                    for record in audit["records"][parity]
                )
                for parity in (0, 1)
            }
            print(
                f"{name} full gamma triangle trace-path ranks="
                f"{trace_path_ranks}, exact={audit['all_exact']}"
            )
    if "gamma_trace_transfer_identity" in result:
        transfer = result["gamma_trace_transfer_identity"]
        spectra = tuple(
            record["trace_eigenvalues"]
            for record in transfer["records"][0]
            if record["trace_eigenvalues"] is not None
        )
        print(
            "Universal gamma-trace homotopy and leakage transfer exact: "
            f"{transfer['all_exact']}; trace spectra={spectra}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
