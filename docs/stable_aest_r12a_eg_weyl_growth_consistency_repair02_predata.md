# Stable AeST R12a Repair02 — single-mode perturbation-history identity (pre-data)

Date: 2026-09-16
Branch: `fullj-evolving-weyl-bridge`

## Trigger

The first R12a Repair01 execution passed all lock/source/import checks and entered the science driver, but every attempted CLASS worker failed before any case artifact was written because this patched CLASS build does not include a reported k field inside the dictionaries returned by `Class.get_perturbations()`.

The repeated exception was:

`RuntimeError: history has no recognized k key`

The available histories do contain the required physical fields (`phi`, `psi`, `delta_b`, `theta_b`, `delta_cdm`, `theta_cdm`) and the time coordinates, but not `k (...)` metadata.

Therefore the original multi-mode mapping rule cannot be evaluated as preregistered. This is an extraction-interface failure, not a GR-control failure and not an AeST science result. No `E_G`, tangent, physical shift, or G3--G8 science quantity was licensed by the failed run.

## Frozen parents

Keep unchanged:

- original R12a preregistration: `bb69d8ac1d83228ba879316c61141823c3e5c665`;
- original R12a implementation: `1af8327e73fbe1f70d1a8c8d14564b80c4bfacc1`;
- R12a Repair01 provenance correction preregistration: `1ca886585e03dc11db0a3e109884a869eb8468b9`;
- R12a Repair01 implementation: `05d638089fcea26cb7a70e06273fbc282b794af7`;
- R12a Repair01 runner: `29b4f737c61a47cf79251ff5f1a27ce1f9bd6f47`;
- authoritative R11a Repair02 postdata: `84c4ba550ce3b262c78c69054056ab2778014677`.

All original R12a physical definitions, grids, stencils, and G3--G8 thresholds remain frozen.

## Repair principle

Do not infer mode identity from list position and do not patch the science source to invent missing metadata.

Instead, request exactly one frozen k mode in each CLASS compute:

`k = [0.03, 0.05, 0.08, 0.10, 0.15, 0.20] h/Mpc`.

For each single-mode compute:

1. `k_output_values` contains exactly one requested physical mode;
2. `Class.get_perturbations()` must return exactly one scalar history;
3. that unique history is assigned to the uniquely requested input k by construction;
4. all required fields must exist and be finite;
5. the history must cover all six frozen redshifts without extrapolation.

This replaces only the impossible reported-k metadata check in R12A-G2. It does not change the physical k grid or select modes after inspecting the response.

## Case construction

For every original R12a case (one pure-GR case plus four tau values times five eta values), run the six frozen k modes separately and combine the resulting six uniquely identified histories into the exact case schema expected by the frozen R12a science engine.

Require background consistency across the six independent single-k computes within each case:

- `h`, `H0`, `Omega_b`, `Omega_cdm`, `Omega_nu`, `Omega_m`, `f_b`, and `f_c` must agree to relative tolerance `1e-12` (absolute fallback `1e-14`);
- all six computes must return one and only one scalar history.

Use the same exact R8a2 patched CLASS build and the same `AEST_R7A_EPOCH_MODE=full` source topology.

## Frozen science domain

Unchanged from R12a:

- `tau H0 = [10, 5, 2.5, 1.25]`;
- `eta = [0, +0.025, -0.025, +0.05, -0.05]`;
- primary epsilon `0.025`;
- control epsilon `0.05`;
- the six frozen DESI/R9b2k effective redshifts;
- the same six frozen k modes;
- cubic spline in scale factor as primary time interpolation;
- PCHIP in scale factor as the independent interpolation control;
- no smoothing, clipping, extrapolation, fitted transfer template, or post-data k/z selection.

## Frozen physics

Unchanged:

`W = phi + psi`

`delta_cb = f_b delta_b + f_c delta_cdm`

`theta_cb = f_b theta_b + f_c theta_cdm`

`fdelta_cb = -theta_cb/Hconf`

`E_G(k,z) = -k_phys^2 W / [3 H0^2 (1+z) fdelta_cb]`.

The pure-GR sign/unit/normalization control and all response identities remain exactly as preregistered.

## Gates

### R12A-R02-G1 — provenance/source

Require all original parent hashes/classifications, the authoritative R11a Repair02 lock, the Repair01 lock chain, and the exact R8a2 patched source topology.

### R12A-R02-G2 — single-mode identity and coverage

For all 21 cases and all six frozen k modes:

- exactly one k is requested per CLASS compute;
- exactly one scalar history is returned;
- all required physical fields are present and finite;
- all six frozen redshifts are covered without extrapolation;
- per-case backgrounds agree across the six computes at the frozen tolerance.

No list-position mapping of a multi-mode history list is permitted.

### R12A-R02-G3 through G8

Use the original frozen R12A-G3 through R12A-G8 definitions and thresholds without modification:

- G3 pure-GR convention control;
- G4 eta-zero closure and tau invariance;
- G5 cubic/PCHIP interpolation control;
- G6 epsilon consistency;
- G7 differential decomposition `T_EG = T_W - T_fdelta`;
- G8 local eta=0.05 linearity.

No threshold is relaxed.

## Classification

If the single-mode identity/coverage gate and all original G3--G8 science gates pass, classify:

`STABLE_AEST_R12A_REPAIR02_SINGLE_MODE_IDENTITY_CERTIFIED`

Otherwise preserve the failing gate and do not report physical amplitudes as certified.

## Claim discipline

A PASS licenses only the same transfer-level linear-theory `E_G` / Weyl-to-growth response intended by the original R12a preregistration. It remains non-observational and does not license a detection, eta/tau bound, galaxy-bias cancellation claim, nonlinear result, or survey likelihood claim.
