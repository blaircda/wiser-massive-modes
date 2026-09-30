# Code to compute the massive states of the IIA superstring
# in either left or right moving sector
# firstly as SO8 states F^l in lightcone gauge
# then factoring out the common massive supermultiplet ( 44 + 84 + 128 )
# so the state at level l is:
# F_l = r_l^9 otimes ( 44 + 84 + 128 )
# we are interested in the r_l
# we find an uplift
# r_l^8 -> r_l^9
# where R^l are SO9 states
# as required by the fact SO9 is the little group for massive states in 10d
#
# then we want to verify that the representations
# R_l^9 = sum_{i = 1}^l r_i^9
# form SO(10) multiplets
# i.e. there exists
# R_n^10 s.t. R_n^10 -> R_n^9 under branching
# this code verifies this using a previously found set of SO(10) multiplets up to level 10

from sage.all import *
from massive_SO8_construct import (
    fock_series, factor_susy_d4, susy_factor
)
from massive_SO8_to_SO9 import greedy_so8_to_so9
from massive_SO10 import (
    SO10_SUPERMULTIPLETS_DYNKIN, get_so10_character
)
D5 = WeylCharacterRing("D5", style="coroots")
D4 = WeylCharacterRing("D4", style="coroots")
B4 = WeylCharacterRing("B4", style="coroots")

# ------------------------------------------------------------
# Calculate first N levels of the massive state SO8 Fock space
# ------------------------------------------------------------

N = 11

F = fock_series(N)

for n in range(N+1):
    print()
    print("F_%d =" % n)
    print(F[n])
    print("dimension =", F[n].degree())
    
# ------------------------------------------------------------
# factor out SUSY multiplet
# ------------------------------------------------------------
r_list = []

for n in range(1, N):
    r = factor_susy_d4(F[n])
    r_list.append(r)

    print(f"r_{n} =", r)
    print("reconstruction:", susy_factor * r == F[n])
    print()

# ------------------------------------------------------------
# SO9 -> SO10
# ------------------------------------------------------------

R_list = []

for n, r in enumerate(r_list, start=1):

    print()
    print("==============================")
    print("LEVEL", n)
    print("==============================")
    print("r =", r)

    R = greedy_so8_to_so9(r)

    print("R =", R)
    print("degree =", R.degree())
    print("branch =", R.branch(D4))
    print("reconstruction =", R.branch(D4) == r)

    R_list.append(R)

# ------------------------------------------------------------
# SO10 -> SO9
# ------------------------------------------------------------

proposed_SO10 = [ get_so10_character(n) for n in range(1,N) ]
proposed_SO9 = [ sum(R_list[:n]) for n in range(1,N) ]

for i, S in enumerate(proposed_SO10):
    R = S.branch(B4, rule="default")
    target = proposed_SO9[i]
    print(f"Level {i+1}")
    print(R)
    print(target)
    print(R == target)
