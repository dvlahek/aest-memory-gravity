# NL1C6D2C6D pre-data — finite-positive-eta retained scalar-current continuation

## License and purpose

This stage is licensed only by the formal D2C6C R7 PASS on commit `a6c61e275ce2ab949dd108ac2b326a4ed617ebcc`, Actions run `34502078991`, which passed all frozen C1-C8 gates on all 27 members and reported `FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=True`.

D2C6D is the first finite **physical** positive-eta continuation of the already certified D2C6B/D2C6C retained scalar-current system. It is a controlled finite-eta numerical continuation with external CLASS metric/matter histories held fixed, exactly as in the parent retained system. It is **not** labelled a full nonlinear AeST+memory simulation: the covariant NL0B completion has direct memory Einstein stress beginning at second perturbative order, and nonlinear metric/matter evolution is outside the D2C6B retained scalar-current scope.

Historical D2C6C FAIL runs and all earlier classifications remain immutable. R7 remains the formal eta=0 certification.

## Frozen physical family

The 27 co-primary nonlinear members are unchanged:

- `sigma in {-1,0,+1}`,
- `kind in {simple, exponential, sharp}`,
- `beta0 in {1,0.5,0.1}`,
- `epsilon_mix=0.25`.

The AeST background, `K_B=0.0665`, corrected Exp branch, six seeded modes/phases, periodic box, redshift interval `z=6..0.2`, nine checkpoints, external CLASS metric/matter histories, and D2C6B constitutive functions are frozen unchanged.

The memory bath is the D2C6C positive Drude design:

- `tau H0 = 1`,
- primary order 39,
- order-47 bath control,
- same positive nodes/weights,
- no memory background correction.

No likelihood, observation, parameter refit, or member selection is allowed.

## Frozen physical eta ladder

Before any finite-eta output, freeze

`eta in {2^-8, 2^-7, 2^-6}`

that is

`eta in {0.00390625, 0.0078125, 0.015625}`.

All are physical positive couplings of the NL0B action. The numerical tangent amplifier `lambda` is absent. The dyadic ladder is chosen only to provide a small one-sided eta->0 continuation and a distinct finite endpoint for convergence controls. It is not tuned to produce a desired response.

No desired response sign, ordering, monotonicity, or minimum amplitude is preregistered.

## Exact retained finite-eta equations

The stable canonical state remains

`y=(alpha, chi, P_chi, S_c)`, with `S_c=P_alpha+Q P_chi`,

and

`E=[invLap(-S_c/(2a))-(2-K_B) chi]/K_B`.

Let `F_member(y,tau)` be exactly the frozen D2C6B nonlinear memory-off RHS for one of the 27 members. For finite eta, the order-N bath coordinates obey the already certified real-space representation

`z_j'' + 2 Hconf z_j' + a^2 omega_j^2 z_j = a omega_j^2 chi_eta`,

with

`B_eta = chi_eta - a sum_j w_j z_j`,

`M_eta = a^2 Lap(B_eta)`.

The NL0B completed-square action fixes the retained scalar-current backreaction to be linear in physical eta. Therefore the finite-eta retained RHS is

`y_eta' = F_member(y_eta,tau) + eta (0,0,M_eta,Q M_eta)`.

The bath itself is driven by the **current finite-eta** `chi_eta`, so the full trajectory is not obtained by multiplying the eta=0 tangent by eta.

For numerical conditioning the implementation evolves the same memory-off base `y0` and the difference

`d = y_eta - y0`

with

`y0' = F_member(y0,tau)`,

`d' = F_member(y0+d,tau)-F_member(y0,tau) + eta (0,0,M_eta,Q M_eta)`.

This difference-state formulation is algebraically identical to the finite-eta retained system and avoids cancellation between two large full states.

## Retarded prehistory

Finite eta is not switched on at z=6.

For each of the same six frozen linear CLASS modes, start at that mode's already frozen valid `tau_lo` with the regular bath state and finite-eta difference equal to zero. Propagate independently to z=6 using the frozen external linear CLASS background/metric/matter history, the exact homogeneous stable-canonical linear operator for the difference, and the finite-eta memory source evaluated on `chi_CLASS + d_chi`. The bath is driven by the same full finite-eta `chi_CLASS + d_chi`.

Sum the six mode contributions at z=6 and initialize

`y_eta(z=6) = y_D2C6B(z=6) + d(z=6)`.

No bath or finite-eta response is reset at z=6. This is the finite-eta counterpart of the R3/R7 modewise full-prehistory convention.

## Frozen numerical scheme

Use the same stage-consistent partitioned RK4/analytic-bath convention as D2C6C. At every RK4 stage the nonlinear base/difference RHS and the analytic bath advance use the same stage value of the full finite-eta source `chi_eta/a`.

Primary finite-eta trajectories:

- order 39,
- `Nx=128`,
- `Nstep=4096`,
- all 27 members,
- all three frozen eta values.

Controls at the largest eta `2^-6`:

- bath order: order 47 at `Nx=128`, `Nstep=4096`,
- time: order 39 at `Nx=128`, `Nstep=8192`,
- space: order 39 at `Nx=256`, `Nstep=4096`, with the same spectral resampling rule as D2C6B/D2C6C.

The eta=0 tangent reference used for the one-sided continuation gate is the already certified R7 D2C6C implementation, not a refitted or newly normalized tangent.

## Locked gates

D2C6D PASS requires all of the following.

**D1 — provenance and exact coverage.** R7 provenance is the locked PASS above. All `27 x 3 = 81` primary finite-positive-eta trajectories are present exactly once, with no member or eta removed.

**D2 — finite-eta source identity.** A deterministic algebraic audit must verify that the finite memory increment in stable canonical variables is exactly `eta (0,0,M,Q M)` and reconstructs the retained elliptic forcing `delta E' = -eta a Q B/(2 K_B)` with relative L2 error `<=1e-10`.

**D3 — eta->0 tangent continuation.** At the smallest frozen eta `2^-8`, for every one of the 27 members, the one-sided quotient of the finite displacement relative to the same memory-off trajectory must reproduce the certified R7 eta=0 tangent over the nine checkpoints in `alpha`, `E`, and `chi`. The maximum relative L2 error over all members and these three fields must be `<=5e-3`. Canonical momentum quotient errors are reported diagnostically but do not gate.

**D4 — all finite-eta health.** Every primary finite-eta trajectory is finite. At every primary checkpoint the full stable-canonical constraint residual is `<=1e-10` and `min(1+j_eff)>0`.

**D5 — bath-order convergence.** At eta=`2^-6`, the maximum relative L2 difference between order-39 and order-47 finite memory displacement canonical checkpoint states `(d_alpha,d_chi,d_Pchi,d_Palpha)` over all 27 members is `<=1e-2`.

**D6 — time convergence.** At eta=`2^-6`, the maximum relative L2 difference between the 4096-step and 8192-step order-39 finite memory displacement canonical checkpoint states over all 27 members is `<=2e-3`.

**D7 — spatial convergence.** At eta=`2^-6`, after the frozen spectral resampling, the maximum relative L2 difference between Nx=128 and Nx=256 order-39 finite memory displacement canonical checkpoint states over all 27 members is `<=5e-3`.

**D8 — scope clean.** Physical eta is strictly positive and only the frozen three-value ladder is used. External metric/matter histories remain frozen. No direct nonlinear memory Einstein stress, nonlinear matter evolution, likelihood, observation, refit, response-sign gate, response-amplitude gate, post-data eta change, or member removal is allowed.

## Non-gating diagnostics

For every member and eta report finite displacements in `alpha`, `E`, and `chi`, signed projections onto the certified eta=0 tangent, and the nonlinear remainder after subtracting `eta * tangent`. Also report the dyadic quotient changes between the three eta values. These diagnostics may show any sign or ordering and cannot change PASS/FAIL.

## Classification and continuation

All D1-D8 gates pass:

`NL1C6D2C6D_FINITE_POSITIVE_ETA_RETAINED_SCALAR_CURRENT_PASS`.

Any frozen numerical/physics gate fails after a valid run:

`NL1C6D2C6D_FINITE_POSITIVE_ETA_RETAINED_SCALAR_CURRENT_FAIL`.

A technical failure before the frozen diagnostics are evaluated is

`NL1C6D2C6D_FINITE_POSITIVE_ETA_RETAINED_SCALAR_CURRENT_INCOMPLETE`.

A PASS licenses only a separately preregistered larger-amplitude retained finite-eta response study or the next theory-complete nonlinear step. It does **not** by itself license an observational claim or a claim of full nonlinear AeST+memory structure formation.
