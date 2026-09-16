# Stable AeST R12a — transfer-level E_G / Weyl-to-growth consistency (pre-data)

Date: 2026-09-16
Branch: `fullj-evolving-weyl-bridge`

## Purpose

R9b2k/Repair02 established a certified compressed DESI ShapeFit physical null. R10a established a certified live ACT DR6 lensing physical null. R11a Repair02 established a certified linear-theory pairwise-velocity response, but the physical eta=0.05 shift is only about 0.11 m/s.

R12a therefore asks a different question:

**Can the ratio between the Weyl field seen by light and the growth/velocity field seen by matter amplify the AeST-memory signature even when each absolute channel is small?**

R12a is a theory-only transfer-level test. It is not an observational E_G likelihood and does not use galaxy bias, lensing data, kSZ data, or an observational covariance.

## Frozen parents

- R8a2 live tau-generality postdata: `590dbc69e2823f583b157af2297e357991103c47`
- R10a ACT live-Weyl postdata: `b7da648f1810ea0c047b6e511e3f87211e830329`
- R11a Repair02 certified postdata: `d9e2e0e6da65126a81d02f32e65f83410bc8cc7c`
- R8a2 JSON SHA256: `2d6289c2fbd37bebcb904dade89f64c15a009e5c7454754b39d4dcc72924ca66`
- R8a2 NPZ SHA256: `c81b2093a88719423e87ff5c180d790a56da6f396c0070858624879c90f26ee1`

R12a uses the same patched stable AeST CLASS source topology as R8a2. No historical result is reclassified.

## Frozen physical domain

Use:

- `tau H0 = [10, 5, 2.5, 1.25]`;
- eta stencil `eta = 0, +/-0.025, +/-0.05`;
- primary epsilon `0.025`;
- control epsilon `0.05`;
- the six frozen DESI/R9b2k effective redshifts
  - 0.29536404346937617
  - 0.5096288678782911
  - 0.7057956472488681
  - 0.9185851971138159
  - 1.3170658832980264
  - 1.4905017757527006;
- audited transfer modes `k = [0.03, 0.05, 0.08, 0.10, 0.15, 0.20] h/Mpc`.

The k grid is fixed before the run and is not selected after inspecting the response.

## CLASS extraction

Use the stable R8a2 AeST source with `AEST_R7A_EPOCH_MODE=full` and output `mTk,vTk`, with lensing C_ell disabled. Request the six frozen k modes through `k_output_values` and obtain dense scalar perturbation histories through `Class.get_perturbations()`.

For each returned mode, identify k from the reported history k value rather than list position. Require one unique returned history for every requested k.

Extract the Newtonian-gauge fields already used/audited in the project:

- `phi`, `psi`;
- baryon density/velocity divergence `delta_b`, `theta_b`;
- CDM density/velocity divergence `delta_cdm`, `theta_cdm`.

Evaluate histories at the six frozen redshifts using scale factor `a=1/(1+z)`.

Primary time interpolation: cubic spline in `a`.

Independent control: PCHIP in `a`.

No smoothing, clipping, extrapolation, fitted transfer template, or post-data k/z selection is allowed.

## cb matter and Weyl definitions

Use background density weights

`f_b = Omega_b/(Omega_b+Omega_cdm)`

`f_c = Omega_cdm/(Omega_b+Omega_cdm)`

and define

`delta_cb = f_b delta_b + f_c delta_cdm`

`theta_cb = f_b theta_b + f_c theta_cdm`.

With conformal Hubble rate `Hconf = H(z)/(1+z)`, define

`fdelta_cb = -theta_cb/Hconf`.

Define the Weyl transfer

`W = phi + psi`.

The sign convention is fixed before the run as

`E_G(k,z) = - k_phys^2 W / [3 H0^2 (1+z) fdelta_cb]`,

where `k_phys = k_h * h` in 1/Mpc and CLASS `H0` is in 1/Mpc.

The leading minus sign is the Newtonian-gauge Fourier-space sign convention that makes the GR control positive for growing overdensities. It is not chosen after inspecting R12a.

## Pure-GR convention control

Run one source-matched control with `aest_enabled=no`, `aest_memory_enabled=no` and the same k/z extraction.

For the GR control require:

1. all `E_G` values finite and positive;
2. all `fdelta_cb` values finite and nonzero;
3. the convention identity `E_G ~ Omega_m0/f_cb` to agree within a conservative 5% vector relative error, where `f_cb=fdelta_cb/delta_cb` and `Omega_m0` is read from CLASS.

This gate validates sign, units, velocity convention, and transfer normalization. It is not a science comparison to data.

## Response definitions

For each tau and interpolation operator define the central fractional tangent

`T_EG = [E_G(+eps)-E_G(-eps)]/[2 eps E_G(0)]`.

Also define component tangents

`T_W = [W(+eps)-W(-eps)]/[2 eps W(0)]`

and

`T_fdelta = [fdelta(+eps)-fdelta(-eps)]/[2 eps fdelta(0)]`.

Because k, H0 and z are fixed, the differential identity is

`T_EG = T_W - T_fdelta`

up to finite-difference truncation. R12a audits this identity explicitly.

The direct physical shift is

`Delta_EG/E_G = [E_G(eta=0.05)-E_G(0)]/E_G(0)`.

No amplitude threshold is a pass/fail gate.

## Frozen gates

### R12A-G1 — provenance and source topology

Require all parent locks/hashes, the certified R8a2 and R11a Repair02 classifications, and the stable R8a2 source-topology audit to pass.

### R12A-G2 — mode/history coverage

For every run and every requested mode:

- exactly one reported k matches each frozen requested k within `5e-12 h/Mpc`;
- all required fields exist and are finite;
- dense histories cover all six frozen redshifts without extrapolation.

### R12A-G3 — GR convention control

Require the pure-GR control described above, including `E <= 0.05` relative to `Omega_m0/f_cb`.

### R12A-G4 — eta-zero closure and tau invariance

At eta=0:

- AeST `E_G` must agree with the pure-GR control with vector relative error `E <= 0.02` and cosine `C >= 0.999` for both interpolation operators;
- eta-zero AeST `E_G` must be tau invariant with maximum pointwise relative difference `<= 5e-6`.

### R12A-G5 — interpolation control

For every tau and both epsilon values, cubic-spline and PCHIP `T_EG` must satisfy

- `E <= 0.05`;
- `C >= 0.995`;
- both tangent norms > `1e-12`.

### R12A-G6 — epsilon consistency

For every tau and both interpolation operators, epsilon=0.025 versus epsilon=0.05 `T_EG` must satisfy

- `E <= 0.05`;
- `C >= 0.995`;
- both tangent norms > `1e-12`.

### R12A-G7 — differential decomposition identity

For every tau and both interpolation operators, compare the primary `T_EG(eps=0.025)` with `T_W-T_fdelta` at the same epsilon. Require

- `E <= 0.02`;
- `C >= 0.999`.

### R12A-G8 — local eta=0.05 linearity

For every tau, compare the direct cubic-spline eta=0.05 fractional shift with `0.05*T_EG(eps=0.025)`. Require

- `E <= 0.10`;
- `C >= 0.99`.

## Reported science quantities after PASS

For each tau report:

- min/max baseline `E_G`;
- max and RMS `|T_EG|`;
- max and RMS physical eta=0.05 fractional shift;
- `(k,z)` location of the largest physical shift;
- norms of `T_W`, `T_fdelta`, and `T_EG`;
- amplification/cancellation diagnostic
  `A_ratio = ||T_EG|| / max(||T_W||, ||T_fdelta||)`;
- tau tangent cosine and norm ratio relative to tau10.

The purpose of `A_ratio` is descriptive. It is not a pass/fail criterion.

## Allowed classification

PASS:

`STABLE_AEST_R12A_EG_WEYL_GROWTH_CONSISTENCY_CERTIFIED`

Otherwise use a gate-specific FAIL classification.

## Claim discipline

A PASS licenses only a numerically controlled transfer-level linear-theory `E_G` / Weyl-to-cb-growth response over the frozen k/z/tau/eta domain.

It does not license:

- an observational E_G measurement or detection;
- galaxy-bias cancellation in a real survey;
- a DESI/ACT cross-correlation constraint;
- eta or tau bounds;
- nonlinear or halo-scale claims;
- a full modified-gravity cosmological fit.

If R12a shows a materially larger physical fractional response than the already certified absolute lensing and pairwise-velocity channels, the next step is an observational CMB-lensing x galaxy / E_G-style projection. If it remains microscopic, the linear-cosmology route should be deprioritized in favor of nonlinear halo/cluster/void tests.