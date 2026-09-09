# NL1C6D1 result — dynamical formulation audit

## Status

Predata declaration: `docs/nl1c6d1_predata_dynamical_formulation_audit.md`

D1A predata commit: `354af396d082a1204f3171bbec804847ba827a92`

D1A implementation commit: `20f9e1f387d405101fe5132c478353a7871479d8`

D1A local runner commit: `422ae986b09443f622d763e4e8ca641613b74bcc`

D1B implementation commit: `82a64385c2139c304967a3c710bd502856c0336e`

D1CDE predata commit: `fc5f0360cac796c08e652b6b4b59f2830a4d2efa`

D1CDE local runner commit: `3a182148e32479acf602f09fe179719f7f31f7ca`

Final preregistered classification:

```text
NL1C6D1_DYNAMICAL_FORMULATION_AUDIT_PASS
```

This PASS applies to the repository's one-dimensional periodic longitudinal weak-field gravitational formulation. It establishes a traceable AeST dynamical reduction, the published scalar propagating mode, scalar constraints, the exact full-J quasistatic reduction, the high-gradient regression, and the absence of an omitted curl contribution in this 1D geometry. It is not a nonlinear cosmological branch-selection result and it does not establish the time-dependent baryonic matter sector required for D2.

No ad hoc relaxation, damping, pseudo-time, arclength-as-time, or branch-selection term was introduced.

## D1A — longitudinal weak-field reduction

Classification:

```text
NL1C6D1A_LONGITUDINAL_WEAKFIELD_REDUCTION_AUDIT_PASS
```

Frozen reduced variables are

```text
E = dot(alpha) + Psi
U = dot(chi) - Q0 E
Y = |grad chi|^2
```

with canonical quantities

```text
P_Phi   = -12 dot(Phi)
P_chi   = 4 K2 U
P_alpha = -4 K2 Q0 U - 2 K_B lap(E) - 2(2-K_B) lap(chi)
```

and scalar constraint

```text
4 lap(Phi) + P_alpha - 16 pi G_tilde rho_b = 0.
```

The local audit returned:

| gate | maximum normalized discrepancy | outcome |
|---|---:|---|
| published canonical identity | `1.52227038634057e-16` | PASS |
| 1D vector/curl completeness | `0.0` | PASS |
| static full-J reduction | `1.4747800630706163e-15` | PASS |
| tracking dispersion identity | `3.966415482397415e-16` | PASS |

The finite vector-sector scale is

```text
m_cross = 3.8128196895424266e-4 Mpc^-1
m_cross^-1 = 2622.730895832132 Mpc.
```

For the repository ansatz `chi=chi(x)`, `U=(d_x chi,0,0)`, the spectral curl and double curl vanish identically. The extra finite-`m_cross` quasistatic curl sector therefore does not contribute in the geometry used by NL1C6/R3. No claim is made for general 2D/3D sources.

The zero-time-derivative limit reproduces the frozen R3 full-J operator to `1.4747800630706163e-15`. Thus the R3 numerical/static branch pathology is not attributable to an identified mismatch between the audited 1D weak-field dynamics and the frozen quasistatic equations.

## D1B — propagating scalar-mode regression

Classification:

```text
NL1C6D1B_LINEAR_SCALAR_MODE_REGRESSION_PASS
```

All `3 x 6 = 18` preregistered combinations of `beta0 in {1.0,0.5,0.1}` and `k in {0.03,0.05,0.08,0.10,0.15,0.20} h/Mpc` passed the published dispersion target

```text
omega^2 = c_s^2 k^2 + M^2
```

with primary relative error in `omega^2` approximately

```text
5.144617e-4
```

against the frozen gate `5e-3`.

The six convergence controls gave approximately

```text
p_40_80  = 2.002838
p_80_160 = 2.000738
```

and therefore passed the second-order gate `p >= 1.8`.

The static mass scale `mu^2 = 2 K2 Q0^2/(2-K_B)` was kept distinct from the propagating normal-mode mass `M^2`; no silent identification was made.

## D1CDE — constraints, quasistatic identity, high-gradient limit

Classification:

```text
NL1C6D1CDE_CONSTRAINT_QS_REGRESSION_PASS
```

The exact first-class scalar-constraint reconstruction gave

```text
max initial normalized constraint residual   = 8.271806125530277e-17
max evolution normalized constraint residual = 8.271806125530277e-17
```

against gates `1e-10` and `1e-7`, respectively.

The independent full-J quasistatic operator comparison gave

```text
max relative discrepancy = 0.0
```

against the frozen `1e-12` gate across the deterministic manufactured-state matrix of scale factors, beta0 values and interpolation families.

The independent saturated/high-gradient regression on the frozen NL1C5B baryon source gave

```text
max relative error = 4.400287801142642e-14
```

against the `1e-10` gate across the eight native evaluation snapshots.

## Interpretation

The combined D1A, D1B and D1CDE results satisfy the frozen D1 PASS rule for the one-dimensional longitudinal gravitational formulation. In particular:

1. the retained nonlinear spatial constitutive term is traceable to AeST rather than introduced as a numerical relaxation;
2. the reduced system reproduces the published healthy scalar propagating mode;
3. the retained scalar constraints are satisfied and preserved in the linear regression;
4. the exact static limit returns the same full-J equations used by NL1C6R3;
5. the known high-gradient Helmholtz limit remains intact;
6. the additional transverse curl sector is exactly inactive for the repository's strict 1D longitudinal ansatz.

This does not reverse or reinterpret the historical

```text
NL1C6R3_FULL_J_BARYONIC_RECLOSURE_FAIL
```

which remains a numerical/static-snapshot reclosure FAIL under its own frozen rules.

## D2 boundary

D1 does not permit an arbitrary time-dependent external `rho_b(t,x)` to be inserted into the fixed-source alpha equation. The D1A fixed-source relation `dot(P_alpha)=0` is not the complete matter-coupled statement for an evolving cosmological source. A D2 branch-selection calculation must first establish a constraint-consistent baryonic density and momentum/velocity history from the same frozen cosmological model.

The next permitted stage is therefore a separately preregistered D2A matter-sector audit. D2A must establish source identity, baryon velocity/momentum identity, and continuity consistency before any nonlinear full-J branch evolution is interpreted physically.

NL1C7 causal-memory physics remains blocked until a later D2 phase establishes a self-consistent nonlinear full-J trajectory under separately frozen gates.
