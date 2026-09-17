# NL1C7B4 pre-data — raw eta=0 initial-constraint certification

Status: **PRE-DATA / LOCKED BEFORE RADIAL CONSTRAINT EVALUATION**

Classification before evaluation: `NL1C7B4_PREDATA_RAW_INITIAL_CONSTRAINT_CERTIFICATION`.

## Purpose

NL1C7A now supplies a unique eta=0 growing-mode spherical initial state. NL1C7B1 supplies the action-derived pressureless-matter source, and NL1C7B3 Repair01 closes the homogeneous CLASS/AeST background at `a_i=0.02` to machine precision. The remaining prerequisite for nonlinear evolution is the original NL1C7 G3 gate: the unmodified growing-mode state must satisfy the retained Hamiltonian/lapse and radial-momentum/shift constraints.

This checkpoint evaluates those two constraints directly from the frozen spherical action. It does not solve, project, relax, refit, clip, smooth, or otherwise alter the C7A state.

## Frozen provenance

Branch parent before this preregistration: `aa7f6bd6580dd201009f3d8d1f7f3ba60eb20ad5` (`Freeze NL1C7B3 Repair01 direct background-point PASS`).

### C6 action and gauge

- C6 final classification: `NL1C6_SPHERICAL_SELF_GRAVITY_CLOSURE_PASS`.
- official G11 run: `35089436959`.
- official G11 head: `0f868057e788423b588cda5bc654287c784ebee7`.
- artifact: `10442933686`.
- artifact SHA256: `12b83f6f67f473937514005f6a87764646407e3b2141b4451d47bd92b62c6ddc`.
- frozen C6 G1-G10 source blob: `e3eeb820fa1826fb7ac29f3fce2fe0bdde8d564f`.
- frozen C6 G11 source blob: `970ccb164f8ab7d3de6681ff4af940b1638d1686`.
- gauge: proper-time, zero-shift, `N=1`, `b=0`.

### C7A growing-mode state

Final classification: `NL1C7A_REPAIR01_DENSE_TIME_SPHERICAL_BRIDGE_CERTIFIED`.

- official evaluator run: `35183893359`.
- head: `e650fcb2344813cc0e3c91a2f0ae99b9c7bf43ac`.
- artifact: `10481526695`.
- artifact SHA256: `c2ede2e602e35bbd52afdc0a5eee22cb1bf5c6efc2e1063bf8f2b91a0554fb6c`.
- retained dense trace run: `35149865129`.
- dense trace artifact: `10469031693`.
- dense trace SHA256: `193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70`.
- reconstruction source blob: `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`.
- evaluator source blob: `aa84b4892586a59455ec93b6dfdc0057adc20d38`.

The frozen scale ladder is exactly `R_sigma={5,10,20} h^-1 Mpc`, with `delta0=1e-3` and `a_i=0.02`. No scale may be selected after inspecting B4 results.

### Pressureless matter

Use only the NL1C7B1 variational dust action and source normalization. Frozen source blob: `485ed20a642ffe868b01c30196154b4834e18e10`.

The dust source is `varrho=8*pi*G*rho_phys`. On the future rapidity branch, its exact metric-source contributions are retained. In particular, the lapse source is `-2 L R^2 varrho cosh(v)^2` and the shift source is `+2 L^2 R^2 varrho cosh(v) sinh(v)` before setting the gauge.

### Homogeneous background

Use the certified B3 Repair01 common direct CLASS background point at `a_i=0.02`, run `35196289353`, head `03b8f454ed8749dcfb8185647bd78d85b3728578`, artifact `10486515383`, artifact SHA256 `12f3157fa05e7c0c4fc431005a506cbfa6347aa78dafd1a1dedf4328b193d3ec`.

The frozen direct C6-normalized background components are

- `3 H^2 = 0.006048695270400684 Mpc^-2`,
- `rhoA_C6 = 0.005009723008430343 Mpc^-2`,
- `varrho_b = 0.0009336821113982245 Mpc^-2`,
- `rho_std_C6 = 0.00010529015057211754 Mpc^-2`.

The standard sector is the already identified CLASS background content: photons, ultra-relativistic species, one non-cold species, and Lambda. No new species or fitted remainder is allowed. `rho_tot` is not an additional species.

For the AeST scalar background value `Q`, use the already certified stable Exp inversion from the retained C7A trace, `KQ/(4 K2 Z0)=Z exp(Z^2)`, followed by `Q=Q0+Z0 Z`. Do not reconstruct `Z` from the cancellation-limited difference `(Q-Q0)/Z0`.

## Frozen action for B4

The eta=0 radial constraints are generated from the same angularly reduced C6 action used in the C6 variational closure, with memory disabled:

`L_total = L_GR + L_AeST + L_dust + L_std,bg`.

The GR and AeST pieces retain the full C6 spherical variables and derivatives. Physical constants are fixed to the already frozen values

- `KB=0.0665`,
- `C=2-KB`,
- `Q0=1e-4 Mpc^-1`,
- `K2=9500`,
- `Z0=1e-17 Mpc^-1`,
- `a0_geo=4.1199352008117163e-5 Mpc^-1`.

The Q sector is the frozen Exp branch. The Y sector is **not selected after data**. All nine C6 co-primary combinations must be evaluated:

- `Simple`, `Exponential`, `Sharp`;
- `beta0={1,0.5,0.1}`.

For the Sharp branch, the exact piecewise low/high expression is evaluated pointwise from the local frozen `x=sqrt(Y)/a0_geo`; no smoothing of the kink is permitted.

The homogeneous standard sector contributes only its frozen background energy density to the lapse constraint and zero radial momentum. C7A did not certify radial photon/UR/ncdm/Lambda perturbation profiles. They must not be invented. If their absence prevents the raw G3 gate from closing, the appropriate outcome is an explicit standard-sector radial-closure incompleteness, not a fitted correction.

## Frozen reconstruction and grids

The B4 implementation must reconstruct the state from the retained dense C7A trace using the exact frozen C7A methods and normalization. It must also load the official C7A primary-state NPZ and verify reproduction before constraint evaluation.

Primary radial grid: `Nr=256`.
Control radial grid: `Nr=512`.

Both use the same dimensionless domain `x in [0,8]`, with `r=x R_sigma/h`. No radial-domain change, filtering, smoothing, clipping, extrapolation, profile renormalization, or boundary fitting is allowed.

The full initial variables are formed only by adding the certified perturbations to the certified homogeneous background:

- `L = a_i + (L-a_i)`,
- `R = a_i r + (R-a_i r)`,
- `Ldot = a_i H + (Ldot-a_i H)`,
- `Rdot = a_i H r + (Rdot-a_i H r)`,
- `u = u_C7A`, `udot = udot_C7A`,
- `phi = delta phi_C7A`,
- `phidot = Q + (phidot-Q)_C7A`,
- `varrho = varrho_b (1+delta_b)`,
- dust rapidity is `v=atanh(v_r)` using the frozen C7A radial velocity and no fitted velocity normalization.

The implementation must terminate as an interface/normalization failure if the velocity representation is not subluminal or if the official primary state cannot be reproduced to relative L2 error `<=1e-12` for every nonzero stored state array.

## Constraint construction

Before imposing `N=1,b=0`, derive the two retained constraints from the frozen action:

- Hamiltonian/lapse: `C_H = dL_total/dN - d_r[dL_total/d(N_r)]`;
- radial momentum/shift: `C_M = dL_total/db - d_r[dL_total/d(b_r)]`.

No evolution equation may be substituted for either constraint.

For numerical differentiation on the uniform radial grid, use a fixed 9-point, eighth-order polynomial finite-difference derivative, centered where possible and one-sided near boundaries. The same derivative operator must be used for all radial first derivatives and for the radial derivative in the Euler-Lagrange constraint. The analytically regular center point `r=0` is the only point excluded from the G3 maximum, exactly as in the original C7 preregistration.

## Frozen normalization

The raw constraint is not normalized by itself. For each action term `j`, derive its own Euler-Lagrange contribution `C_H,j` or `C_M,j` before summing. At each radius define

`D_H = sum_j |C_H,j| + F_H`,

`D_M = sum_j |C_M,j| + F_M`,

with fixed nonzero numerical floors

`F_H = 1e-14 * max_{r>0}(sum_j |C_H,j|)`,

`F_M = 1e-14 * max_{r>0}(sum_j |C_M,j|)`.

If the maximum pre-floor denominator of a constraint is exactly zero or non-finite, classify the implementation as incomplete rather than redefining the normalization.

The normalized pointwise residuals are

`epsilon_H(r)=|C_H(r)|/D_H(r)`,

`epsilon_M(r)=|C_M(r)|/D_M(r)`.

This is an action-term normalization only. No residual-dependent rescaling is allowed.

## Pre-registered gates

### B4-G1 — provenance and state reproduction

All frozen parent run/head/artifact digests and source blobs must match. The official C7A `Nr=256` primary state must be reproduced at relative L2 error `<=1e-12` for every nonzero state array.

### B4-G2 — exact action/source structure

The implementation must regenerate the C6 lapse and shift Euler-Lagrange constraints from the frozen reduced action and add only the B1 action-derived dust source plus the B3 frozen homogeneous standard-sector lapse source. No Poisson replacement, shell force, drag, artificial pressure, viscosity, fitted source, constraint projection, or post-result correction is permitted.

### B4-G3 — original NL1C7 initial constraints

For **every** frozen scale, **every** one of the nine Y branches, and **both** `Nr=256` and `Nr=512`, after excluding only `r=0`, require

`max epsilon_H <= 1e-7`

and

`max epsilon_M <= 1e-7`.

This is the unchanged NL1C7 G3 threshold.

### B4-G4 — grid control

For each scale and Y branch, the primary/control RMS normalized residuals for each constraint must agree within a factor of 2 when both are nonzero. The control grid must not convert a failing `>1e-7` maximum into a PASS by averaging.

### B4-G5 — no state modification

The evaluated state must remain exactly the reconstructed C7A growing mode. No constraint solve or projection is executed in B4. No field, profile, amplitude, phase, background component, Y branch, scale, or radial interval may be selected after inspecting residuals.

## Classification

If all B4-G1 through B4-G5 pass for all `9 x 3 x 2` cases:

`NL1C7B4_RAW_INITIAL_CONSTRAINT_PASS`.

If the frozen state is finite and correctly reproduced but the raw Hamiltonian or momentum residual exceeds `1e-7`:

`NL1C7B4_RAW_INITIAL_CONSTRAINT_FAIL`.

If the failure can be localized to the absence of radial standard-sector perturbations that are not present in the certified C7A state, with the action/interface otherwise consistent:

`NL1C7B4_STANDARD_SECTOR_RADIAL_CLOSURE_INCOMPLETE`.

If the constraint cannot be generated or evaluated without adding a new physical prescription:

`NL1C7B4_CONSTRAINT_IMPLEMENTATION_INCOMPLETE`.

A B4 PASS licenses a separate preregistered short eta=0 evolution/constraint-propagation checkpoint. It does not itself license a long collapse trajectory, finite eta, lensing, or an observational claim.