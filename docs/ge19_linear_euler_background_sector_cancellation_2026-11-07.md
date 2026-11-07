# GE19 — exact GE06+Lambda / GE07 homogeneous lapse cancellation

**Date:** 2026-11-07  
**Scope/classification:** `GE19_ANALYTIC_GE06_LAMBDA_GE07_LAPSE_BALANCE_DERIVED_FULL_CMAT_OPEN`  
**Branch:** `physics-first-gravitational-elasticity`.  
**Purpose:** Identify a *nontrivial necessary prerequisite* for testing the complete canonical `Cmat` Ward operator. No H4 source, parent arrays, FD4/FD8 budget, Z21 science solve or lensing run.

## 1. Exact original action dictionary

Pinned action generators:

- GE06 Einstein+AeST: `ge06/analytic_aest_directional_source_generator.py` (blob `a7afe0035054a9dca55d74a6497c081422114b4c`).
- GE07 dust: `ge07/pressureless_matter_directional_source_generator.py` (blob `cde8da77a80799cef00fc7c09c3633310fc9e3d4`).
- Lambda: `ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py` (blob `dbfa43ae11dbd3cfeeb1994a30237e9374dbb3e7`), with `L_lambda=-6 rho_lambda N L R^2`.
- Repair13 on-shell Friedmann: `ge19/repair13_self_consistent_reduced_background_h1_reclosure.py` (blob `362d63d03d7b850fceae393f535353ded79aeea7`).
- Repair07 canonical source convention: `ge19/repair07_window_retarded_reduced_h3_z20_particular.py` (blob `e34d28a2062c748f48bc82fa928844b02631de25`), `rhob=3*C_VALUES[tag]/a^3`.
- H4F3D1 original shift / independent L projection: `ge19/h4f3d1_frozen_canonical_operator_ward.py`.

The homogeneous GE06+Lambda action, retaining lapse `N` **until after varying**, is

```text
L_g+Lambda,hom(N)
  = a^3[-6 H^2/N + 2 N K(Q/N) - 6 rho_lambda N].
```

Here `H=dot(a)/a` and `Q=dot(phi0)` are fixed coordinate-time background rates during the variation `d/dN`. The `K(Q)` function is the original GE06 exponential AeST scalar action, not a substitute parametrization. Differentiating before setting `N=1` gives

```text
E_N00^{GE06+Lambda}
 = 6 a^3 H^2 + 2 a^3(K - Q K_Q) - 6 rho_lambda a^3.
```

The **frozen Repair13** homogeneous relation is

```text
H^2 = (Q K_Q-K)/3 + C/a^3 + rho_lambda,
```

hence, exactly,

```text
E_N00^{GE06+Lambda} = +6 C.
```

The frozen GE07 dust action is

```text
L_d = N L R^2 varrho[ ((T_t-b T_x)/N)^2 - (T_x/L)^2 -1 ].
```

On comoving FLRW `L=R=a, N=1, b=0, T_t=1, T_x=0`, the **action density** is `varrho0=3C/a^3`, not `C/a^3` in the raw GE07 conventions. Defining `D=a^3 varrho0=3C` (constant), the source-derived Euler derivative is

```text
E_N00^{GE07} = -2D = -6 C.
```

Therefore `E_N00^{GE06+Lambda+GE07}=0` **exactly** on the original Repair13 background. The reduced GE05 bath has vanishing regular homogeneous `q0=Xphi0=0` and supplies no background lapse term; the corresponding restricted background conditions were already treated in D12R2. This audit isolates the *lapse* balance, not every background Euler component.

## 2. Explicit exact GE07 linear Euler Ward identity

The full reduced spatial Ward identity for GE07 alone is off-shell, with `T` and `varrho` transforming as spatial **scalars**, not densities. In canonical Euler sign convention:

```text
W_GE07 =
  E_N N_x+E_L L_x+E_R R_x+E_b b_x
  +E_T T_x + E_varrho varrho_x
  -d_x(L E_L-b E_b)-d_t E_b = 0.
```

For arbitrary perturbations `N=1+eps n`, `T=t+eps tau` and arbitrary other GE07 first-order variables, the *actual frozen action derivatives* imply

```text
E_N00^d = -2D,
E_L10^d = (2D/a)(partial_t tau - n),
E_b10^d = -2D partial_x tau.
```

The background dust current is `J_T^t=2D`, and `partial_t D=0` on comoving dust.

Taking the first epsilon derivative of the full off-shell Ward gives

```text
W_GE07,10
  = (-2D) partial_x n
    -a partial_x[(2D/a)(partial_t tau-n)]
    -partial_t[-2D partial_x tau]
  = 0,
```

by commutativity of `partial_t partial_x tau` for sufficiently regular fields. This was checked **symbolically**, and also follows from the previously frozen H4F2A off-shell GE07 spatial covariance.

**Critical negative control:** Dropping `E_N00^d partial_x n` from the GE07-only identity produces

```text
  -partial_t E_b10^d -a partial_x E_L10^d
  = +2D partial_x n = +6C partial_x n,
```

which is NOT identically zero. Thus **the short linear syzygy does not hold sector-by-sector** on the *total on-shell* background. The GE06+Lambda sector carries the opposite background term. Only after summing sectors, using the **same Euler normalization and before** discarding `E_i00`, is the total background-free linear syzygy justified.

## 3. What this resolves and what remains

**Resolved as algebra:**
- Exact source-based GE06+Lambda/GE07 lapse background cancellation, including the frozen `3C/a^3` raw dust normalization.
- Exact off-shell Euler GE07 identity and explicit first-order dust Euler shift/longitudinal rows.
- Explicit negative control against the tempting but invalid sector-wise `E00=0` assumption.
- Existing H4F1 (reduced GE05 spatial covariance), H4F2F (GE06 coframe covariance), H4F2A (GE07 off-shell covariance), H4F3D4 formal mixed all-sector Ward, and D12R2 other background Euler reductions remain the frozen parent proof chain; none is silently replaced.

**Not proven here:**
- Exact arbitrary-jet `D_W L_total=0` **for the actual GE19 gauge-restricted 16x10 production Cmat**, including all field/jet consistency conditions, derivatives of background coefficients and independent L momentum; check it on physical time not merely `ln(a)` and handle the GE05 eta convention at mixed H4.
- G1 actual-grid all-parent Euler and lower-boundary closure, including all bath nodes.
- G3 original FD4/FD8 physical derivative/zero-set/roundoff bounds and frozen `B_total`; **local D12R9 audits still require direct frozen evidence review**.
- Full actual all-cohort H4 Ward, the final action-completed Z21 or gauge-invariant lensing.

## 4. Independent implementation and execution policy

The read-only source-bound symbolic script `ge19/h4f3d_linear_sector_background_lapse_audit.py` extracts original GE06/GE07 action AST assignments rather than importing generator modules with side effects; checks Git blobs, exact off-shell GE07 Euler Ward, first-order GE07 Euler rows, GE06+Lambda background lapse and the repaired Repair13 `C` normalization. It produces no physical H4 residual, does not overwrite old outputs and does not run the Z21 solver.

Independent local SymPy checks of these equations **passed on the same action expressions reproduced from the pinned sources**. The newly added repository script still requires its **own execution on the actual checkout**; do not label it a frozen CI or all-sector science PASS merely because it was committed.

Safe local command (no GitHub Actions consumption):

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
export PYTHONPATH="$PWD"
python3 -u -m ge19.h4f3d_linear_sector_background_lapse_audit \
  --json-out results/ge19_h4f3d_linear_sector_background_lapse_audit_20261107.json
```

The next proof gate is an independent arbitrary-jet **combined** GE06+GE07+Lambda production `Cmat` linear syzygy, with no assumption that sector-wise background Euler factors are zero. A formally valid continuum syzygy must not be silently promoted to a discrete FD4/FD8 physical tolerance.

**Unchanged:** `full_H4_Ward_certified=false`, `Z21_certified=false`, `lensing_licensed=false`; original active shift `<=1e-6`, original temporal order `>=2.5`, and all historical FAIL classifications remain frozen.
