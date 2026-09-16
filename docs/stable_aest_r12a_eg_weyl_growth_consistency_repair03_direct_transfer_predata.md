# Stable AeST R12a Repair03 — exact-redshift CLASS transfer extraction (pre-data)

Date: 2026-09-16
Branch: `fullj-evolving-weyl-bridge`

## Trigger

R12a Repair02 reached the science gates and classified

`STABLE_AEST_R12A_INTERPOLATION_CONTROL_FAIL`.

The single-mode identity repair passed. GR convention, eta-zero closure/tau invariance, differential decomposition, and local eta=0.05 linearity passed. The remaining failure is localized to time interpolation of the extremely small eta response: cubic is epsilon-stable for every tau, while the independent PCHIP time interpolation produces unstable tangent directions and amplitudes.

Repair02 postdata freeze: `472ab501cfe564510b38e1c2831c4024ae012ecf`.

No G5/G6 threshold is relaxed and the Repair02 failure remains historical.

## Repair principle

Remove perturbation-history time interpolation from the observable construction entirely.

Use the frozen R8a2 patched CLASS build and CLASS-format transfer functions evaluated directly at each of the six frozen redshifts through the CLASS Python transfer interface. The direct transfer call must provide, at each requested redshift, a dense k grid together with the required Newtonian-gauge fields or accepted aliases:

- `phi`
- `psi`
- baryon density (`d_b` or `delta_b`)
- CDM density (`d_cdm` or `delta_cdm`)
- baryon velocity divergence (`t_b` or `theta_b`)
- CDM velocity divergence (`t_cdm` or `theta_cdm`)
- a reported k grid.

If the frozen local CLASS build does not expose this interface/fields, classify a technical direct-transfer-interface failure before evaluating the memory response. Do not fall back to perturbation-history time interpolation.

## Frozen science domain

Unchanged:

- `tau H0 = [10, 5, 2.5, 1.25]`
- `eta = [0, +0.025, -0.025, +0.05, -0.05]`
- primary epsilon `0.025`
- control epsilon `0.05`
- frozen k targets `[0.03, 0.05, 0.08, 0.10, 0.15, 0.20] h/Mpc`
- frozen redshifts `[0.29536404346937617, 0.5096288678782911, 0.7057956472488681, 0.9185851971138159, 1.3170658832980264, 1.4905017757527006]`
- no nonlinear corrections
- no smoothing, clipping, extrapolation, post-data k/z selection, fitted transfer template, or gate relaxation.

## Frozen physics

At every native transfer k and requested z:

`W = phi + psi`

`delta_cb = f_b d_b + f_c d_cdm`

`theta_cb = f_b t_b + f_c t_cdm`

`fdelta_cb = -theta_cb/Hconf(z)`

`E_G(k,z) = -k_phys^2 W / [3 H0^2 (1+z) fdelta_cb]`.

The same pure-GR sign/unit/normalization control is retained.

## Response-before-k-interpolation rule

The purpose of Repair03 is not to trade one interpolation artifact for another.

For each fixed `(tau,z)` require the native transfer k grids for `eta=0,+/-0.025,+/-0.05` to agree pointwise within relative tolerance `1e-10` on the common certified support. If they do not, fail the native-grid gate; do not silently remap individual eta cases first.

On the common native k grid, form the signed fractional responses before any target-k interpolation:

`T_X(eps) = [X(+eps)-X(-eps)] / [2 eps X(0)]`

for `X in {W, fdelta, E_G}` wherever the eta-zero denominator is finite and nonzero.

Also form the direct physical fractional shift

`D_EG_005 = E_G(eta=+0.05)/E_G(0) - 1`

on the same native grid.

Only these already-formed response arrays are interpolated to the six frozen target k values.

## Frozen k-interpolation operators

Primary: PCHIP in `ln k` of the signed/native response.

Independent control: linear interpolation in `ln k` of the same signed/native response.

No extrapolation. Every frozen target k must lie strictly inside the common native support.

For baseline GR/eta-zero controls, interpolate the baseline fields with the same two `ln k` operators.

## Gates

### R12A-R03-G1 — provenance/source

Require the complete original R12a / Repair01 / Repair02 lock chain, Repair02 postdata freeze `472ab501...`, authoritative R8a2/R10a/R11a parents, and the exact frozen R8a2 patched CLASS source topology.

### R12A-R03-G2 — direct-transfer interface and exact-redshift coverage

For the pure-GR control and all 20 AeST cases:

- direct CLASS transfer extraction succeeds at all six frozen redshifts;
- all required fields and k are present and finite;
- target redshifts are passed directly to the transfer interface; no time interpolation is called;
- each native k grid is strictly positive and increasing after deterministic finite-value cleaning;
- all frozen target k values are inside native support.

### R12A-R03-G3 — native k-grid eta closure

At each `(tau,z)`, native k grids for eta `0,+/-0.025,+/-0.05` must match pointwise at relative tolerance `1e-10`. Grid length must also match. This gate is evaluated before any response interpolation.

### R12A-R03-G4 — pure-GR convention

Retain the original R12a GR identity/sign/normalization criterion on the frozen 6x6 target grid under both k interpolation operators:

- `E <= 0.05`
- positive finite E_G.

### R12A-R03-G5 — eta-zero closure and tau invariance

Retain original R12a thresholds:

- AeST eta=0 vs pure GR: `E <= 0.02`, `C >= 0.999` under both k operators;
- eta-zero tau pointwise variation `<= 5e-6`.

### R12A-R03-G6 — k-interpolation response control

For every tau and epsilon, compare PCHIP-logk and linear-logk `T_EG` on the frozen 36-point target grid:

- `E <= 0.05`
- `C >= 0.995`
- both tangent norms `> 1e-12`.

### R12A-R03-G7 — epsilon consistency

For every tau and each k operator, compare `eps=0.025` with `eps=0.05`:

- `E <= 0.05`
- `C >= 0.995`
- both tangent norms `> 1e-12`.

### R12A-R03-G8 — differential decomposition

For primary epsilon and both k operators require

`T_EG = T_W - T_fdelta`

with

- `E <= 0.02`
- `C >= 0.999`.

### R12A-R03-G9 — local eta=0.05 linearity

For the primary PCHIP-logk operator compare direct `D_EG_005` with `0.05*T_EG(eps=0.025)`:

- `E <= 0.10`
- `C >= 0.99`.

### R12A-R03-G10 — tau coherence / reporting gate

After G1-G9 pass, report tau10-normalized tangent norms/cosines, maximum/RMS physical `eta=0.05` fractional shifts, the location of the maximum shift, and

`A_ratio = ||T_EG|| / max(||T_W||, ||T_fdelta||)`.

No amplitude threshold is a pass/fail criterion.

## Classification

If G1-G10 pass:

`STABLE_AEST_R12A_REPAIR03_DIRECT_TRANSFER_CERTIFIED`

Otherwise preserve the first failing classification. In particular, a direct-transfer-interface failure is technical, while a G6/G7 failure is a numerical response-robustness failure.

## Claim discipline

A PASS licenses only a transfer-level, linear-theory Weyl-to-growth consistency response on the frozen k-z grid. It does not license an observational E_G detection, galaxy-bias cancellation claim, nonlinear result, eta bound, tau bound, or survey likelihood inference.

Repair03 must not retroactively reclassify Repair02.