"""Shared guards for integer data returned by floating-point MILP backends.

Sage's GLPK mixed-integer backend returns objective and variable values as
floating-point numbers even when the mathematical model is integral.  These
helpers do not turn GLPK's branch-and-bound proof into an exact rational
certificate.  They do prevent silent rounding of visibly nonintegral output;
callers must still verify their extracted primal witnesses with exact integer
or representation-ring arithmetic.
"""

import math


DEFAULT_INTEGRAL_TOLERANCE = 1e-6


def checked_integer(
    value,
    description="MILP value",
    tolerance=DEFAULT_INTEGRAL_TOLERANCE,
):
    """Return the nearest integer after an explicit finite/drift check."""
    numerical = float(value)
    if not math.isfinite(numerical):
        raise ValueError(f"Expected finite {description}, obtained {value}")
    rounded = int(round(numerical))
    if abs(numerical - rounded) > tolerance:
        raise ValueError(
            f"Expected integral {description}, obtained {value} "
            f"(nearest integer {rounded})"
        )
    return rounded


def checked_value(values, key, description="MILP variable"):
    """Extract one integer variable value from a Sage solution dictionary."""
    return checked_integer(values.get(key, 0), f"{description} {key!r}")


def run_self_test():
    accepted = (
        checked_integer(3) == 3
        and checked_integer(2.0000001) == 2
        and checked_value({"x": 4.0}, "x") == 4
        and checked_value({}, "missing") == 0
    )
    rejected = 0
    for value in (1.01, float("inf"), float("nan")):
        try:
            checked_integer(value)
        except ValueError:
            rejected += 1
    return accepted and rejected == 3
