# GE19 — H4 action/Noether shift-constraint propagation and initial-condition compatibility

**Date:** 2026-11-08. **Branch:** `physics-first-gravitational-elasticity`.  
**Status:** **ANALYTICAL CONSEQUENCE OF SOURCE-FROZEN ACTION LEDGER; CONDITIONAL BOUNDARY MECHANISM, NOT AN ATTRIBUTED CAUSE OF D55Cr12ad FAIL.**  
**Local independent SymPy study:** `ge19_h4_action_constraint_propagation.py`; 12/12 exact symbolic checks PASS (SHA256 `5caabc65ba4d0028a507539b1a8b17a47a9cc6a2c54fbe3bee56673afbac8d7c`), JSON SHA256 `6a93ef68cb240ad6e349fc07edf291cdff9316636f6732e44483d49f4c7f1cb2`. It does **not** independently vary the entire covariant Einstein+AeST+GE05+dust action. It uses the existing original complete mixed action Noether identity, and independently checks the coefficient expansion, the Fourier and boundary transport, and the canonical algebraic-initial compatibility theorem.

## 1. Actual source lineage and frozen negative science gate

Original `ge19/h4f3d4_complete_eta_regularized_mixed_ward_ledger.py` (blob `87d8be9ec44ecb099feecbaf59a904bd989da2fb`) is the exact frozen off-shell spatial-diffeomorphism action ledger. Original `ge19/h4f3d12r2_exact_background_onshell_elimination.py` (blob `df5d0b384747edefaab2878e1a9fe6d174d2da29`) eliminates only background-multiplied mixed unknowns, not first-order parent Euler errors. `ge19/h4f3d1_frozen_canonical_operator_ward.py` (blob `60786ac14c9478801c5df9ccf458ead9a34ac827`) supplies the correct original momentum time derivative and `E_L=(E_iso+2 E_aniso)/3` projection. Original canonical source `ge19/repair07_window_retarded_reduced_h3_z20_particular.py` (blob `e34d28a2062c748f48bc82fa928844b02631de25`) specifies all 16 Cmat rows, local Noether algebraic partition, separate initial canonical solver and original shift constraint.

Actual audited D55Cr12ad closed-campaign science result was **`H4_REPAIR_CAMPAIGN_CLOSED_MODEL_LEVEL_REDERIVATION_REQUIRED_FOR_ANY_NEW_ATTEMPT`**: lowest tested coherent M2 Cstar `H4_active_shift_Linf=1.2175965417947408e-6`, above the original `1e-6` criterion by `21.76%`, with sub12/sub24/sub48 robustness. This is a robust negative **numerical acceptance result for a frozen formulation**, not an analytic proof of a mathematical inconsistency of every solution of the covariant action. D55Cr11f independently certified the Cstar primary six-mode GE05 bath H-channel; don't undo its PASS.

## 2. Independent analytical H4 Ward coefficient re-expansion

Use the frozen original convention `F=F00+eps(F10+eta F11)+eps²(F20+eta F21)/2`, with the same expansion for signed Euler components, and the **physical eta-regularized** bath `2eta E_q d_chi q`, NOT naive `eta E_q d_chi q`.

The complete mixed spatial Noether coefficient at `d_eta d_eps²`, on the independently background-on-shell D12R2 equations, is

```text
0 = R_parent - d_chi (a E_L21 + B_parent) - d_t E_b21

R_parent =
    2 sum_{i in {N,L,R,b,u,phi,T,rho}}
      (E_i10 d_chi F_i11 + E_i11 d_chi F_i10)
    + 4 sum_j E_qj10,GE05 d_chi q_j10

B_parent =
    2 L10 E_L11 + 2 L11 E_L10
    - 2 b10 E_b11 - 2 b11 E_b10 .
```

Here `t` is **physical time**, `chi` the periodic spatial coordinate, and `x=ln a` is the numerical clock; do not mix them. The 12/12 independent SymPy exact symbolic tests include the factor-2 nonbath coefficient, physical factor-4 bath parent (deliberately wrong factor rejected), the complete signed L-minus-b boundary coefficient, the exact D12R2 reduced boundary flux, and the time/Fourier identity.

For each Fourier wave number `k` (including full spatial convolutions in products entering `R_parent,k` and `B_parent,k`),

```text
d_t E_b21,k
    = R_parent,k - i k (a E_L21,k + B_parent,k).       (A)

E_b21,k(t)
    = E_b21,k(t0)
      + integral_{t0}^t [ R_parent,k
                         - i k (a E_L21,k + B_parent,k) ] ds.  (B)
```

For the expanding original action `H=dx/dt>0`, the equivalent exact identity is

```text
d_x E_b21,k
    = [R_parent,k - i k (a E_L21,k + B_parent,k)] / H.  (C)
```

A correct conditional absolute bound is

```text
|E_b21,k(t)|
 <= |E_b21,k(t0)|
    + integral_t0^t (|R_parent,k|
                     + |k| a |E_L21,k|
                     + |k| |B_parent,k|) ds.
```

In the **exact first-order-parent on-shell and longitudinal on-shell limit** `R_parent=B_parent=E_L21=0`, equation (A) states that `E_b21,k` is **constant, not automatically zero**. A nonzero initial shift residual can survive arbitrarily accurate time integration if the relevant exact premises hold. Therefore, a stable full-window shift residual can be boundary/initial-constraint related **rather than a missing source coefficient**. This is a *candidate explanation only*. If any of `R_parent,B_parent,E_L21` remain nonzero or distributional, they can produce, cancel or amplify the shift residual and must be accounted for. Spatial zero-mode `k=0` obeys `d_t E_b21,0=R_parent,0`, not automatically zero without parent on-shell.

**Crucial distinction:** the original acceptance monitor is a **cancellation-safe normalized** `|row@w-source|/max(|lhs|,|source|,sum|row*w|,...)` on the original ACTIVE mask, **not the raw absolute `|E_b|`**. A bound for raw E_b does not by itself prove the fixed `<=1e-6` normalized gate; it also requires lower bounds for the normalization scale and the original active mask plus derivative/B_total budgets. Never change the threshold to accommodate this reasoning.

## 3. No-go for a purported 'homogeneous fix' of the shift row

For the **entire** original linearized Euler operator including **all** independent constraint rows, let

```text
L_total w_p = S + residual,
L_total w_h = 0  (ALL Euler + shift/constraint rows).
```

Then by linearity

```text
E_b(w_p+w_h)
    = [L_b w_p + L_b w_h - S_b]
    = E_b(w_p)
```

exactly. **No genuinely full homogeneous solution can repair the residual of an inhomogeneous shift equation.** An 'evolution-only homogeneous' response that does change the shift residual necessarily violates at least a constraint row; it is not a homogeneous solution of the full action Euler system. Thus solving for a primordial homogeneous H4 mode must not be advertised as a means to fit away the frozen Cr12ad shift failure.

A physically derived change in initial conditions *before the full constraint solve* is a different question: it must satisfy the complete source-frozen first-order/mixed constraints and original primordial conditions and cannot be chosen by optimizing the observed H4 failure.

## 4. NEW exact local initial-data compatibility formula from the original canonical solver

Original `repair07._initial_canonical_state(mod6,mod7,bg,tag,k,x0,q0,v0,rhs0)` starts from four physical fields `q0=(S,u,phi,T)` and four velocities `v0=(Sdot,udot,phidot,Tdot)`; it solves `Cmat[[4,5]][:,[0,1]]` for lapse and dust density using **lapse+density** RHS `rhs0[[0,5]]`, then defines the canonical momenta `p=Cmat[0:4]@w_trial`. This function has **no separate anisotropy/shift RHS argument**, so it does not itself certify that the trial physical state obeys the initial H4 anisotropy or shift source equations. That is an implementation/contract observation, not proof that actual frozen initial conditions violate them.

For canonical propagation, the original source-locked Noether partition instead solves

```text
Calg = vstack(Cmat[0:4], Cmat[5:6],
              Cmat[12:13]+Cmat[13:14])
Az = Calg[:,(0,1,6,7,8,9)]
Aq = Calg[:,(2,3,4,5)] .
```

Let `w_trial` satisfy the *same four momenta and dust-density source* as the reconstructed state (true by construction when these inputs are consistent) and let its residual in the **last, anisotropy** algebraic row be

```text
r_aniso0=(Cmat[12]+Cmat[13])w_trial - s_aniso0 .
```

If `Az` is invertible at x0, the canonical reconstructed state from the **same** q0,p0 and the physical source satisfies the exact algebraic mismatch formula

```text
z_rec-z_trial = -Az^{-1} e_6 r_aniso0,
z=(N,delta_rho,Sdot,udot,phidot,Tdot),
e_6=(0,0,0,0,0,1)^T.

E_b(rec)-E_b(trial)
 = -(Cmat[10]+Cmat[11])_Z Az^{-1} e_6 r_aniso0.      (D)
```

This result is **conditional on exact consistency of the other five algebraic rows**, and does not assume any actual numerical value of `r_aniso0`. It is not a first-order lapse constraint identity and not evidence that the original Noether algebraic block is singular. If `r_aniso0=0`, the reclosure difference in (D) vanishes; the separate initial shift residual `E_b(trial)` may still be nonzero. If `r_aniso0!=0`, an initial source/boundary compatibility mismatch can change the reconstructed shift even before propagation; it must be evaluated from the original frozen H4 source and primordial data, not changed post hoc.

The independent symbolic proof checks this formula exactly on a rational nonsingular manufactured 6x6 block, with explicit negative controls; that is **an algebraic theorem demonstration**, not an execution on original H4 Cmat/NPZ physical parents.

## 5. The ONE physically discriminating next step (no new ODE or source repair)

The present frozen D55Cr12ad report contains only *whole-window* normalized active shift extrema and step-refinement robustness, not enough initial and parent-flow information to attribute the failing `1.2176e-6` to (A) or (D). Its closeout says `primordial_homogeneous_Z21_certified=false`, and Cr12j explicitly reports `projected_p0_recomputed=false` and `projected_p0_inherited_exactly=true`.

Before considering any new action or H4 simulation, inspect **original existing** Cstar coherent M2 `Cr12abr2` data and exact source code at its initial time and the active-mask hotspot, without rerunning a solver:

1. At initial original x0, reconstruct original `w_trial`, full **both shift and anisotropy** Euler source rows, original `Cmat` and `Az`, and calculate `r_aniso0`, `E_b(trial)_0`, `E_b(rec)_0`, exact transfer predicted by (D), original raw absolute residual and cancellation-safe normalized active-mask value. Check whether the frozen Cr12abr2 baseline inherited the same `p0` and trial-source values.
2. From the **same original parent** arrays, evaluate the original full `E_L21,k`, `R_parent,k`, `B_parent,k` including bath, dust, corrected Y and all physical action boundary/interface terms. Compare direct frozen `E_b,k(t)-E_b,k(t0)` to the independently integrated RHS of (B), with an **independent FD4/FD8+roundoff error envelope**. Never infer original continuum PASS from sampled data alone.
3. Report which of these four cases is true: (i) initial shift/anisotropy incompatible; (ii) parent/boundary Ward source still nonzero; (iii) action constraint propagation closes but original discrete normalized acceptance remains above target; (iv) missing provenance/regularity prevents attribution. No source coefficient or threshold is adjusted in any case.

If (i) occurs, this is an **initial-value/constraint-completion** issue to be independently reconciled with the physics of primordial data, not a fitted homogeneous fix. If (ii), restore a mathematically justified omitted physical term **only after independent covariant action variation and preregistration**. If (iii), retain the frozen H4 numerical science FAIL without claiming a model-level contradiction. If (iv), retain missing-evidence status.

Original `1e-6` active-shift and temporal convergence order `>=2.5` unchanged. **No full covariant rederivation or final original Ward test is claimed by this note.** No `Z21` or gauge-invariant lensing license. Preserve original prior negative results and D55Cr11f positive GE05 bath proof.
