# GE19 H4 structural audit — Stage A source-row ledger and proven row0 lemma

## Status

**STAGE A SOURCE-ROW INVENTORY COMPLETE; FULL H4 NOETHER CERTIFICATE NOT YET ESTABLISHED.**

This is an analytical/source-code traceability result under the post-Repair44
structural stop gate. It is not another H4 numerical repair, not an H4 science
PASS, and not proof that the six-piece source satisfies the complete
off-shell or on-shell H4 Noether identity.

Parent:
`docs/ge19_h4_source_constraint_noether_structural_stop_gate.md`.

Frozen diagnostic:
`docs/ge19_repair44_valid_shift_row0_localization_freeze.md`.

## Frozen row convention

The GE19 canonical source vector is

`s = (N, L+R, u, phi, T, rho, b, L - R/2)`,

in this exact order. In particular:

- main row0: lapse `N`;
- main row1: isotropic `L+R`;
- main row2: aether `u`;
- main row3: scalar `phi`;
- main row4: dust potential `T`;
- main row5: dust density `rho`;
- constraint row0, source vector index6: independent shift `b`;
- constraint row1, source vector index7: anisotropy `L-R/2`.

Source: `ge19/repair07_window_retarded_reduced_h3_z20_particular.py`,
`main_and_constraints` and `_canonical_operator_matrices`.

This same row convention MUST be used for every source piece.
Physical interpretation and relative normalization must not be inferred
solely from array position.

## Exact six-piece source dictionary

Repair37 forms each beta's total source by summing the following pieces
at their frozen time nodes, separately for the six main rows and two
constraint rows:

| Frozen piece | Direct generating function | Nonzero row family established by code | Important convention |
|---|---|---|---|
| `2Q_GE06_cross` | `q_cross_direct` -> `assemble_ga_local` -> `main_and_constraints` | GE06 lapse/isotropic/aether/scalar plus shift/anisotropy | direct mixed bilinear, `-2*fft_low`, GE06 raw convention |
| `2Q_GE07_cross` | `q_cross_direct` -> `assemble_m_local` -> `main_and_constraints` | dust lapse/isotropic/potential/density plus shift/anisotropy | direct mixed dust bilinear, `-2*fft_low` |
| `2Q_Lambda_cross` | `lambda_cross_direct` | lapse/isotropic; both constraint rows identically zero | direct Lambda mixed quadratic with `-2` source sign included |
| `2DY2` | `dy2_real` and `assemble_nonmemory` | scalar main row3 only; both constraint rows zero | nonanalytic Y2 directional derivative and `-2` source sign |
| `2M1_GE05_mapped` | `m1_mapped_fourier` | aether main row2 and scalar main row3 only; constraints zero | exact GE05-to-GE06 factor-two mapping in Repair32A |
| `2M2_GE05_mapped` | `memory_m2_chunk` -> `reconstruct_m2_source` | GE05 metric lapse/isotropic, aether/scalar plus shift/anisotropy; dust rows zero | second memory variation, quadrature sum and `-2*fft_low` |

Code anchors:

- `ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py`:
  `q_cross_direct`, `lambda_cross_direct`, `dy2_real`,
  `m1_mapped_fourier`, `memory_m2_chunk`,
  `reconstruct_m2_source`, `assemble_nonmemory`,
  `build_source_config`.
- `ge19/repair07_window_retarded_reduced_h3_z20_particular.py`:
  `main_and_constraints`, `assemble_ga_local`,
  `assemble_m_local`.
- `ge19/repair32a_ge06_ge05_raw_residual_normalization_dictionary_audit.py`:
  exact `GE05_M1_to_GE06_raw_residual_scale=2`.

**Important exclusion:** M1 has zero shift and anisotropy source in this
dictionary, but that does NOT imply total memory has zero metric
constraint source: M2 has both constraint rows.

**Important exclusion:** Lambda and DY2 have zero constraint rows in
their implemented H4 source, but their contributions to the full
Noether relation can involve other equations, derivatives and parent
residuals. It is invalid to infer termwise identity from a zero
constraint-source array.

## Exact operator lemma explaining Repair44

Let `y=(S,u,phi,T,pS,pu,pphi,pT)` and let the frozen canonical affine
system and algebraic reconstruction be

`y' = M y + F s`,  `w = WY y + WR s`.

In the frozen Repair07 construction:

`Rr[4,5]=1`, `Rr[5,7]=1`, and every other `Rr` entry is zero.

In particular `Rr[:,6]=0`. Since
`ZR = Az^{-1}Rr` on the solved regular domain, it follows exactly that

`ZR[:,6]=0`, `WR[:,6]=0`, `F[:,6]=0`.

Consequently, with the SAME initial canonical state and all other
source components frozen,

`delta s = e_6 delta s_shift` implies `delta y=0` and
`delta w=0`; in particular `delta Z21=0`.

The independent shift constraint is checked as

`r_shift = (Cmat[10]+Cmat[11]) w - s_shift`.

With fixed `w`, its exact source response is

`delta r_shift = - delta s_shift`.

Repair44's observed bitwise Z21 equality and registered complex
constraint identity with reported defects 0.0 are the expected
consequences of these two exact operator facts. They show that the
selective source intervention does not test a self-consistent new
physical solution.

**This lemma is not the full Noether identity.** In particular the
right null direction of the old algebraic partition in Repair06 is a
property of the linear operator, not a demonstration that an arbitrary
inhomogeneous H4 source obeys the corresponding on-shell
differential compatibility relation.

## Discrete-versus-continuum compatibility risk to check

Repair37's direct GE06/GE07 cross terms use its exact finite-difference
FD8 time assembly (`q_cross_direct`). GE05 M2's independently
reconstructed raw memory scalar source uses the frozen FD4 time
derivative in `memory_m2_chunk`, plus the full-history bath/quadrature
realization. DY2 uses its specified spatial Fourier derivative.

This is an implementation fact, not an established source bug.
Nevertheless, even if the **continuum** H4 Ward/Noether identity
holds for all six pieces, mixing different discrete derivative
operators can create a nonzero **discrete** identity residual.
A common time-node array is therefore necessary but not sufficient:
time-derivative, spatial derivative, bath and boundary conventions
must also be examined together.

Do not silently replace the frozen FD4/FD8 operators or alter the
quadrature. First derive the analytic identity and evaluate the
identity defect under the *existing* frozen discrete realization.

## Open proof obligations: do not promote to PASS yet

1. Derive the precise reduced H4 diffeomorphism/Noether identity from
   the same frozen Einstein+AeST, dust, Lambda, Y2 and covariant GE05
   memory action, including bath equations, field transformation
   conventions, factor-two dictionary and boundary terms. Existing
   GE19 Repair06 Noether-regularized algebraic rank diagnostics do
   NOT discharge this obligation.
2. Expand the identity through the required mixed H4 coefficient and
   express its source side in the six-piece dictionary, explicitly
   separating terms proportional to certified H1/H2/background/bath
   parent equations and gauge or boundary terms.
3. Decide from the derived identity which **complete** H4 source
   rows must be compared, and establish a signed residual
   formula without fitting an offset to the numerical result.
4. Evaluate that signed formula independently at the registered
   C_max/beta0=1/m8/it3 hotspot and on the frozen active window,
   using one common parent/time realization. Report absolute
   complex defect and the original local backward-error scale,
   not only aggregate relative L2.
5. Only after the structural audit has a frozen outcome, determine
   if one separately preregistered integrated science Z21 reclosure
   is licensed. Otherwise report an explicit localized structural
   FAIL or unresolved identity, without inventing a numerical
   Repair45 patch.

## Next deliverable

The next deliverable is a signed, independently checkable reduced H4
Noether source identity and parent-residual dictionary. It is **not**
a new interpolated source or a relabelled Repair37.
