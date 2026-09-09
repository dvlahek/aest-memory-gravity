# Nonlinear program after linear-chain closure

The linear numerical chain is closed by the preserved v0.77 and v0.78 PASS results. This document defines the stronger next path without re-opening CLASS interpolation debugging.

## Scientific target

Test whether the certified linear retarded-memory response in the native matter state changes the approach to and evolution of nonlinear structure formation.

The central question is:

`certified linear memory tangent -> nonlinear mode coupling / collapse / saturation ?`

The project must distinguish three levels of claim:

1. **Certified linear precursor** — already established.
2. **Controlled weakly nonlinear consequence** — next target.
3. **Full nonlinear AeST+memory structure formation** — later target requiring the nonlinear modified-gravity field system or a justified numerical realization.

## Phase NL0 — equation audit before simulation

Before any nonlinear numerical claim, derive or source the nonlinear equations actually implied by the AeST model and the retarded-memory extension.

Required output:

- identify the nonlinear matter continuity and Euler equations;
- identify the nonlinear AeST gravitational-field closure entering the force law;
- identify how the memory kernel enters beyond first order;
- separate standard fluid convective vertices from genuinely modified-gravity nonlinear vertices;
- state which terms are exact consequences of the theory and which, if any, are controlled approximations.

No numerical result from a phenomenological or standard-GR nonlinear closure may be labelled "nonlinear AeST+memory" unless this audit justifies that identification.

## Phase NL1 — controlled weakly nonlinear bridge

If the equation audit permits it, construct the minimal second-order / mode-coupling system around the certified linear state.

Primary objects should be the second-order kernels or their equivalent time-domain response, schematically

`delta^(2)(k) = int F2(k1,k2) delta^(1)(k1) delta^(1)(k2)`.

The first scientific question is whether the eta=0 memory tangent changes:

- the amplitude of the second-order density correction;
- the mode-coupling kernel shape;
- the position/time of the order-unity threshold;
- the sign of the previously observed delay/advance tendency.

The linear `d_m` state and its certified tangent are inputs/controls, not quantities to be re-fitted.

## Phase NL2 — collapse/onset test

Use a nonlinear observable that remains well-conditioned near transfer-function zeros. Preferred candidates are broadband variance, smoothed density amplitude, spherical-collapse variables if derivable consistently, or a mode-coupled variance measure.

A preregistered comparison should ask whether positive physical memory coupling shifts a nonlinear threshold toward larger or smaller physical scale / later or earlier time.

Do not use local `d ln P / d eta` near power minima as the primary nonlinear diagnostic.

## Phase NL3 — full nonlinear realization

If NL1/NL2 show a robust effect, implement or interface a full nonlinear solver appropriate to the derived AeST+memory equations. Possible realizations may include a modified particle-mesh/N-body code or a field-plus-matter solver, but the implementation choice must follow the equation audit rather than precede it.

Primary final targets:

- nonlinear matter power spectrum;
- halo/collapse statistics if the theory supports them;
- redshift evolution of the memory effect;
- comparison with the certified linear precursor.

## Observations come after nonlinear theory control

Only after the nonlinear prediction is under control should the project return to observational likelihoods. The natural observables are scale-dependent late-time structure probes rather than a single compressed `sigma8` number.

Candidate classes include full-shape clustering, RSD, weak lensing and related cross-correlations, with the exact choice made only after the nonlinear signal shape is known.

## Integrity constraints

- v0.77 and v0.78 remain preserved PASS results.
- Earlier FAIL classifications remain unchanged.
- No post-result retuning of frozen historical tests.
- New nonlinear tests must be separately preregistered.
- Approximate nonlinear closures must be labelled as approximations and cannot be promoted to full AeST nonlinear dynamics without derivation.
