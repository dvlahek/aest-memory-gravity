# Stable AeST growth–Weyl memory R4 — common-mode mechanism audit

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

This declaration is fixed after the completed R3 result and its post-data checkpoint and before any R4 mechanism result is generated.

## Parent chain

Immediate formal parent:

`STABLE_AEST_GROWTH_WEYL_MEMORY_R3_SCALE_GENERALITY_CERTIFIED`.

R3 post-data checkpoint commit:

`8094cf2a3a40659419e64ea0c45fd27491decae3`.

R2e remains:

`STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_ABSOLUTE_COMMON_MODE_CERTIFIED`.

Historical R1/R1b/R2/R2a/R2b/R2c/R2d classifications remain unchanged and cannot be retroactively reclassified by R4.

## Question

R2e and R3 established that the first-order finite-memory response of CLASS total matter and the Weyl combination is common-mode to the preregistered one-percent bound over ten tested stable scales in the locked long-relaxation regime.

R4 tests the mechanism behind this result. The working mechanism is that physical memory enters the stable AeST perturbation system through one direct first-order forcing channel in the scalar closure variable `E_aest`. If the subsequent linear metric/matter response is dominated by one transfer-amplitude direction, then `d_m`, `phi`, and `psi` should acquire nearly the same fractional memory response. In that case the metric slip and the Weyl-to-matter ratio remain nearly unchanged even though the common amplitude changes.

R4 does not assume this outcome. It distinguishes a single-amplitude mechanism from a Weyl-only cancellation or an unresolved mechanism.

## Frozen physical regime

Use the already certified stable-AeST regime:

- `tau H0 = 10`
- `memory_order = 20`
- `tol_perturbations_integration = 3e-8`
- physical `aest_eta in {0, 0.005, 0.01}`
- stable residual `s = a theta/k^2 + alpha`
- `chi = Q s`
- redshifts `z = [6,5,4,3,2,1.5,1,0.5,0.2]`
- CLASS transfer observables `d_m`, `phi`, and `psi`
- no diagnostic variational forcing in the science runs.

Use the seven held-out scales already certified by R3:

`k_h = {0.10000, 0.10125, 0.10250, 0.10375, 0.16500, 0.19750, 0.19875}`.

These scales are used because they are direct physical finite-eta R3 scales and are independent of the original three R2e anchors.

## Exact source-topology statement to audit

The stabilized AeST source must retain:

`dy[alpha_aest] = a (E_aest - psi_aest)`

and

`s' = 3 c_a^2 H (s-alpha) + a [Pi/(1+w) + E]`.

The physical finite-memory feedback enters through

`Bchi_aest *= aest_eta`

followed by

`E_rhs_aest -= 0.5 Q_aest Bchi_aest`.

R4 source audit tests that the physical `aest_eta` multiplication appears exactly once in the perturbation RHS memory closure, that the closure appears exactly once, and that there is no other direct physical `aest_eta` forcing of the metric or matter variables in the same RHS block.

Passing this source audit licenses the statement that first-order memory enters the perturbation dynamics through one direct physical forcing channel in `E_aest`. It does not by itself prove common-mode propagation to observables.

## Observable tangents

For X in `{D,P,S,W}` define

- `D = d_m`
- `P = phi`
- `S = psi`
- `W = phi + psi`.

For eta in `{0.005,0.01}` define the matched fractional tangent

`T_X(eta) = [X(eta)-X(0)] / [eta X(0)]`.

Denominators must be finite and nonzero on the evaluated redshift vector. If either `phi` or `psi` violates this requirement at an anchor, that anchor cannot pass the individual-potential mechanism gate.

The primary estimate is eta=0.01. Eta=0.005 is used for tangent consistency.

## Mechanism metrics

### Individual tangent consistency

For each X in `{D,P,S,W}` and anchor:

`E_X = relL2(T_X(0.005), T_X(0.01))`

`C_X = cosine(T_X(0.005), T_X(0.01))`.

Strict consistency requires `E_X <= 0.02` and `C_X >= 0.999` for all four channels.

Loose consistency requires `E_X <= 0.05` and `C_X >= 0.995` for all four channels.

### Single-amplitude mismatch

Using eta=0.01 define

`B_phiD = ||T_phi-T_D|| / max(||T_phi||,||T_D||)`

`B_psiD = ||T_psi-T_D|| / max(||T_psi||,||T_D||)`

`B_WD = ||T_W-T_D|| / max(||T_W||,||T_D||)`.

A strict single-amplitude anchor requires all three values `<= 0.01`.

A loose single-amplitude anchor requires all three values `<= 0.05`.

### Metric-slip response

Define

`B_slip = ||T_phi-T_psi|| / max(||T_phi||,||T_psi||)`.

A strict slip-invariant anchor requires `B_slip <= 0.01`.

A loose slip-invariant anchor requires `B_slip <= 0.05`.

This is preferred to directly differentiating `phi/psi` because it avoids introducing an additional ratio singularity while testing the same first-order statement.

### Late-time activation

For each of `D`, `phi`, `psi`, and `W`, require a nonzero late-time eta=0.01 tangent norm on `z <= 2` and require that the late-time RMS exceeds the high-redshift RMS over `z >= 3` by at least a factor of 2 for the Weyl and matter channels. The individual-potential channels are diagnostic for this gate and must remain finite/nonzero at late time.

## Gates

### R4-G1 provenance and parent lock

Require:

- this pre-data commit and the R3 post-data commit are ancestors of HEAD;
- R3 classification is exactly `STABLE_AEST_GROWTH_WEYL_MEMORY_R3_SCALE_GENERALITY_CERTIFIED`;
- R2e classification is exactly `STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_ABSOLUTE_COMMON_MODE_CERTIFIED`;
- R1c remains `STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED`;
- stable host remains `FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED`.

### R4-G2 single-channel source topology

Require the stable physical source to contain exactly one physical `Bchi_aest *= pba->aest_eta` multiplication and exactly one `E_rhs_aest -= 0.5*Q_aest*Bchi_aest` closure, with stable `chi=Q*s` present and no diagnostic external-force hook in the science CLASS source.

### R4-G3 transfer basis and finite run validity

All 21 direct physical runs must be finite and provide `d_m`, `phi`, and `psi` on the requested transfer domain without extrapolation.

### R4-G4 individual finite-eta tangent consistency

Require at least 6/7 anchors to pass the strict consistency criterion and all seven to pass the loose criterion.

### R4-G5 single-amplitude metric/matter response

Require at least 6/7 anchors to pass the strict single-amplitude criterion and all seven to pass the loose criterion.

### R4-G6 slip invariance

Require at least 6/7 anchors to pass strict slip invariance and all seven to pass loose slip invariance.

### R4-G7 late-time activation

Require all seven anchors to pass the late-time matter/Weyl activation criterion and to have finite nonzero late-time individual-potential response.

## Classification priority

1. G1 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R4_INCOMPLETE`
2. G2 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R4_SOURCE_TOPOLOGY_FAIL`
3. G3 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R4_TRANSFER_BASIS_FAIL`
4. G4 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R4_TANGENT_FAIL`
5. G5 pass and G6 pass and G7 pass: `STABLE_AEST_GROWTH_WEYL_MEMORY_R4_SINGLE_AMPLITUDE_MODE_CERTIFIED`
6. G5 pass and G6 fail and G7 pass: `STABLE_AEST_GROWTH_WEYL_MEMORY_R4_COMMON_MODE_WITH_SLIP_RESPONSE`
7. otherwise: `STABLE_AEST_GROWTH_WEYL_MEMORY_R4_MECHANISM_UNRESOLVED`

## Interpretation lock

`SINGLE_AMPLITUDE_MODE_CERTIFIED` licenses the statement that, in the locked stable-AeST long-relaxation regime and tested scale/redshift domain, physical memory enters through one direct scalar-closure forcing channel and propagates predominantly as a common fractional amplitude modulation of total matter and both metric potentials. The metric-slip response is bounded by the preregistered one-percent criterion, explaining the previously certified common-mode Weyl/matter response as an amplitude mode rather than a positive growth-Weyl lag.

`COMMON_MODE_WITH_SLIP_RESPONSE` licenses only that total matter and Weyl remain common-mode while the two metric potentials do not share the same one-percent fractional response. In that case a cancellation inside `phi+psi` remains possible and the single-amplitude mechanism is not certified.

No R4 outcome licenses observational detection, permanent elasticity loss, exact equality of growth and Weyl response, or a general theorem outside the tested stable-AeST regime.