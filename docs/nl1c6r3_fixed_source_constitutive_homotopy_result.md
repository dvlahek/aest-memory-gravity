# NL1C6R3 result — fixed-source constitutive homotopy

## Status

Predata declaration: `docs/nl1c6r3_predata_fixed_source_constitutive_homotopy.md`

Predata commit: `c796b382b25278d14d5fbb65d91f756929ba3f02`

Production implementation commit: `b18179d53872bace7066025a6f64ff148f828919`

Workflow commit: `2f843fee204b0c426ed35e93d9a5d496cf889929`

Local reproducible runner commit: `e1a74869c3ad70140c9cfacd59455924ab3fb2aa`

Diagnostic geometry-map code commit: `5cac285f43b37e9bd01000e5ecd8deb961f97e79`

Decisive blocking-branch confirmation commit: `8303beb05121b92dd34b6621fd39e9f095503718`

Frozen NL1C5B input artifact ID: `10101422385`

Frozen NL1C5B input artifact SHA-256: `0ab60cbc32210ad3fb75c881f91a9db11148280e9223ea644680ed8cdfbaa590`

Final preregistered classification:

```text
NL1C6R3_FULL_J_BARYONIC_RECLOSURE_FAIL
```

This is a decisive numerical/static-snapshot reclosure FAIL under the frozen NL1C6R3 rules. It is not a CI failure, not a source-identity failure, and not evidence that the physical full-J AeST equations have no solution.

The full all-branch production run was intentionally not allowed to consume additional hours after a deterministic co-primary blocking snapshot was independently reproduced with the unchanged production solver. Because G3 requires every primary endpoint solution to converge and the predata rule declares a snapshot failed when neither constitutive anchor reaches a residual-valid theta=1 endpoint, one confirmed blocking co-primary snapshot is sufficient to make the global PASS classification impossible.

## Frozen physics and controls

NL1C6R3 retained the same NL1C5B baryonic source, physical full-J endpoint equations, constants, interpolation functions, co-primary beta0 values, periodic box, physical-coordinate derivatives, resolutions, and physical gates as NL1C6/NL1C6R/NL1C6R2.

The two continuation coordinates were numerical only:

```text
screened anchor: j_S(theta,x) = (1-theta)/beta0 + theta j_full(x)
mass anchor:     j_M(theta,x) = theta j_full(x)
```

Both reduce exactly to the unchanged physical full-J equation at `theta=1`.

The endpoint-identity smoke check passed exactly for both routes before the long run. No physical eta, retarded-memory forcing, matter re-evolution, observational likelihood, physical gate relaxation, endpoint-source change, or interpolation change was introduced.

## Runtime diagnostic

A local diagnostic-only geometry map was run at the first native snapshot,

```text
z = 6.000000000000045
Nx = 256
```

for all `3 x 3 x 2 = 18` combinations of interpolation family, beta0, and constitutive anchor. The diagnostic changed no production equation, tolerance, continuation rule, branch-selection rule, or physical gate.

It revealed two distinct numerical geometries.

### Screened-anchor behaviour

The screened route can reach the physical endpoint for several branches. In particular, all three interpolation families at `beta0=0.1` reached exact `theta=1` rapidly, and `sharp, beta0=0.5` also reached the endpoint after a stiff near-endpoint region.

Representative successful cases were:

| interpolation | beta0 | outcome | wall time |
|---|---:|---|---:|
| simple | 0.1 | `converged_theta1` | 3.73 s |
| exponential | 0.1 | `converged_theta1` | 3.12 s |
| sharp | 0.1 | `converged_theta1` | 2.07 s |
| sharp | 0.5 | `converged_theta1` | 129.97 s |

The slow screened cases were dominated by repeated augmented GMRES termination at the frozen `maxiter=600` near `theta ~= 1`, not by the small seed values. A separately traced `simple, beta0=1` screened route reached an exact residual-valid theta=1 endpoint after approximately 129 s, confirming that a 150 s parallel diagnostic timeout is not itself a physical or numerical branch failure.

### Mass-anchor behaviour

The mass anchor showed a different pathology. Its pseudo-arclength tangent commonly became almost orthogonal to the theta direction, so the solver moved rapidly in field space while making essentially no progress toward `theta=1`.

Examples include:

| interpolation | beta0 | final reason | theta_max | min abs(t_theta) |
|---|---:|---|---:|---:|
| simple | 1.0 | `arclength_max_accepted_points` | 0.00390625 | 9.279e-8 |
| exponential | 0.5 | `arclength_max_accepted_points` | 0.0009765625 | 1.622e-8 |
| sharp | 1.0 | `arclength_max_accepted_points` | 0.00493447 | 4.008e-8 |
| sharp | 0.5 | `arclength_max_accepted_points` | 0.0009765625 | 1.625e-8 |

Thus the mass route can remain residual-valid along its local branch while never approaching the physical endpoint. A small field residual away from theta=1 must not be interpreted as an endpoint solution.

## Decisive blocking snapshot

The geometry map identified the co-primary branch

```text
z = 6.000000000000045
interpolation = sharp
beta0 = 1.0
```

as a candidate global blocker. It was then rerun by a dedicated local confirmation script using the unchanged NL1C6R3 production solver, with no diagnostic wall timeout.

Git state for the confirmation:

```text
commit = 8303beb05121b92dd34b6621fd39e9f095503718
branch = v053-model-freeze-planck
```

### Screened route

The screened continuation crossed the neighbourhood of the physical endpoint:

```text
seed_theta      = 0.00390625
theta_max       = 1.011354093571781
accepted_points = 16
rejected_points = 0
fold_count      = 0
```

However, the required exact-theta endpoint correction failed under the frozen fixed-theta solver:

```text
reason = theta1_gmres_failed_300
final_solver_relative_residual = 0.05794504649617346
endpoint_valid = false
wall_seconds = 13.1128
```

The residual is many orders of magnitude above the frozen fixed-theta tolerance `2e-10`. Therefore the screened route does not supply a valid physical endpoint for this snapshot.

### Mass route

The mass continuation remained far from the endpoint and exhausted the preregistered arclength budget:

```text
reason          = arclength_max_accepted_points
seed_theta      = 0.00390625
accepted_points = 1200
rejected_points = 0
fold_count      = 0
theta_max       = 0.004934468552216773
endpoint_valid  = false
wall_seconds    = 8.0999
```

The reported final solver-relative residual `8.938542358970198e-12` is a residual on the local mass-anchor branch near theta of order `5e-3`; it is not a residual at the physical `theta=1` endpoint.

The dedicated confirmation therefore returned

```text
BLOCKING_SNAPSHOT=True
```

with total wall time approximately 21.2 s.

## Gate consequence

The NL1C6R3 predata rule states that if neither constitutive anchor reaches a residual-valid theta=1 endpoint, the snapshot fails. The physical G3 gate additionally requires every primary endpoint solution to converge and remain finite.

For the confirmed `sharp, beta0=1, z=6` snapshot:

```text
screened anchor: FAIL at exact theta=1 endpoint correction
mass anchor:     FAIL to approach theta=1 before arclength budget exhaustion
```

Therefore

```text
G3_all_primary_solutions_converged = FAIL
```

is already forced, and the global preregistered PASS classification is impossible regardless of uncomputed later snapshots or controls. The appropriate final classification is consequently

```text
NL1C6R3_FULL_J_BARYONIC_RECLOSURE_FAIL
```

No zeros or missing aggregate residual/resolution values from the stopped full production run may be interpreted as passing G3 or G4.

## Interpretation

NL1C6R3 materially changes the numerical picture relative to NL1C6R2. Holding the physical baryonic source fixed and continuing the constitutive law can reach valid full-J theta=1 states on multiple screened-anchor branches. Therefore the R2 source-amplitude fold at lambda of order `1e-7` was not evidence that all physical-source full-J states are inaccessible.

At the same time, the two exact constitutive anchors expose two different static-snapshot branch-selection problems:

1. screened routes can become strongly stiff or singular in the augmented/fixed-theta Jacobian near the physical endpoint for larger beta0;
2. mass routes can turn almost completely into the field direction, with `t_theta -> 0`, and follow a residual-valid branch that does not approach theta=1.

The decisive `sharp, beta0=1, z=6` case fails through both mechanisms under the frozen R3 solver and continuation rules.

This remains a numerical/static-snapshot result. It does not prove non-existence of a physical full-J AeST solution at that source, and it does not select a preferred physical branch.

## Consequence

NL1C7 causal-memory response must not be started from NL1C6R3 because the required self-consistent full-J native-time trajectory has not been established for all co-primary branches.

Per the R3 predata declaration, the next scientific step is not an `R4` obtained by increasing GMRES iteration limits, reducing `ds_min`, increasing the arclength budget, or relaxing endpoint/physical gates. Those would continue an open-ended static-solver repair sequence after the preregistered stopping condition has been met.

The next phase must instead address physical time evolution and branch selection from the dynamical AeST equations. Any such phase must be separately preregistered and must first demonstrate that its dynamical formulation is derived from the AeST action, reproduces the known linear propagating-mode limit, and reduces to the frozen full-J quasistatic equations in the appropriate zero-time-derivative limit before it is used for nonlinear science output.
