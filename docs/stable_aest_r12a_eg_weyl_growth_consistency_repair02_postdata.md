# Stable AeST R12a Repair02 — post-data freeze

Date: 2026-09-16
Branch: `fullj-evolving-weyl-bridge`

## Classification

`STABLE_AEST_R12A_INTERPOLATION_CONTROL_FAIL`

This is the first R12a execution that reached the transfer-level science gates. The earlier Repair01 failure was purely an extraction-interface failure.

Repair02 successfully replaced ambiguous multi-mode perturbation-history mapping with one requested k per CLASS compute and exactly one returned scalar history. The single-mode identity gate passed for all 21 cases x 6 frozen k modes, with zero background/Hconf inconsistency across the six per-case computes.

## Artifact hashes

- JSON SHA256: `8c7268c12afacf3faed98264d4154a613544f1d0529854773ef6b6563c8e22f2`
- NPZ SHA256: `ed89214a0e31813fc6dc592024dc928ae8af28298ff26640189ba4088a0bfd10`
- science log SHA256: `43d0e6bf3c66079d21a23914fb0f9776f03a94cfb781d2928ed2bea48f952a47`
- full runner SHA256: `06756defaf4ea87e3b65b8db467f304ed68035215faadb0fa453f268e7f009f6`
- environment SHA256: `9dae0a68c3d303877d1b57d64cd98156b59e5a146ca79ee9ac85f84e51b74a2d`

## Gate status

PASS:

- R12A-G1 provenance/source
- R12A-G2 mode/history coverage
- R12A-R02-G2 single-mode identity coverage
- R12A-G3 GR convention
- R12A-G4 eta-zero closure and tau invariance
- R12A-G7 differential decomposition
- R12A-G8 local eta=0.05 linearity

FAIL:

- R12A-G5 cubic/PCHIP interpolation control
- R12A-G6 epsilon consistency, because the PCHIP branch is not epsilon-stable

No science amplitude is certified because G5/G6 are frozen mandatory gates.

## Healthy controls

The pure-GR control passes in both time interpolators. Cubic gives E=`0.0041279289644169295`, C=`0.999999949873752`; PCHIP gives E=`0.004127806677289869`, C=`0.9999999498513135`. E_G stays positive over the frozen grid.

AeST eta=0 closes onto the GR reference at E about `2e-6` in both interpolation schemes, and tau variation at eta=0 is at most about `3e-7` pointwise in PCHIP and below `7e-10` in cubic.

The differential identity `T_EG = T_W - T_fdelta` passes at E of order `1e-8` to `4e-7` in both interpolation schemes. Therefore the E_G algebra and decomposition are not the source of the failure.

The primary cubic response is also epsilon-stable for every tau:

- tau10: E=`0.0006930132650444095`, C=`0.9999997765784681`
- tau5: E=`0.020105609893753335`, C=`0.999862814428487`
- tau2.5: E=`0.046465963942635774`, C=`0.9989969324825122`
- tau1.25: E=`0.02521189579205145`, C=`0.9997421825071439`

The direct eta=0.05 response is locally linear under the primary cubic operator for all tau.

## Failure localization

The failure is specific to constructing the extremely small eta derivative after separately interpolating the +eta and -eta perturbation histories in time.

At eps=0.025, cubic/PCHIP E_G tangent agreement is poor:

- tau10: E=`0.999343200404584`, C=`0.03750797228848129`; norms `3.3640e-7` vs `7.1291e-6`
- tau5: E=`1.014232729365706`, C=`-0.022774992272019214`; norms `3.2734e-7` vs `2.2108e-6`
- tau2.5: E=`0.9457255778215756`, C=`0.32551273081641124`; norms `3.2419e-7` vs `1.0572e-6`
- tau1.25: E=`0.3743007305229295`, C=`0.9276116099032202`; norms `3.1441e-7` vs `3.4785e-7`

PCHIP epsilon consistency also fails strongly, while cubic epsilon consistency passes. This pattern is consistent with time-interpolation error/noise dominating a derivative whose true response is extremely small. It does not support selecting cubic post-data and discarding the preregistered PCHIP control.

## Provisional scale only — not certified

The primary cubic fractional E_G tangent has L2 norm about `3.1e-7` to `3.4e-7` over the 36-point frozen k-z grid. Multiplying by the physical edge eta=0.05 gives an L2 fractional shift only about `1.6e-8` to `1.7e-8`.

Even the unstable PCHIP branch remains small in absolute scale: its largest tangent norm is about `7.13e-6`, corresponding to an eta=0.05 L2 shift about `3.56e-7`.

These values are diagnostic only. Repair02 has `science_evaluated=false`, `transfer_level_EG_response=false`, and no observational or parameter-bound claim is licensed.

## Repair direction

Do not relax G5/G6 and do not choose cubic as authoritative after seeing the result.

The next repair should remove time interpolation from the observable construction. Use CLASS transfer functions evaluated directly at the six frozen redshifts, in CLASS/Newtonian transfer convention, with the same frozen k, tau, eta, E_G definition, epsilon stencils, GR control, decomposition identity, and local-linearity gates. Any k interpolation needed on the dense transfer grid must itself have a preregistered independent operator control.

This Repair02 FAIL remains frozen and must not be reclassified after a later repair.