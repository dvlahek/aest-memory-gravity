# NL1C3 predata — screened-resummed dynamical bridge

Classification before derivation: **NL1C3_PREDATA_SCREENED_RESUMMED_DYNAMICAL_BRIDGE**

This theory gate is created after `NL1C2_SCREENED_ASYMPTOTIC_RECLOSURE_PASS` and before any screened-resummed cosmological memory result.

No observational data or finite-eta outcome is used. Historical classifications remain immutable.

## 1. Scientific question

NL1C0 showed that the physical-amplitude late-time state has `x_rms ~ 1e7-1e8`. NL1C1 validated the full published interpolation family, and NL1C2 showed that all nine co-primary interpolation/beta0 branches have

\[
\mathcal J_{\mathcal Y}=1/\beta_0
\]

to part-per-million accuracy at the measured physical gradient amplitudes.

The next question is therefore not a deep-MOND weakly nonlinear expansion. It is:

> Can the time-dependent AeST scalar/aether system be consistently reclosed in the physical-amplitude screened branch, with the saturated Y-sector retained as an amplitude-resummed spatial stiffness, and can the frozen eta=0 memory direction then be defined around that reclosed state?

## 2. Frozen inputs

Retain exactly

- `K_B = 0.0665`;
- `K2 = 9500`;
- `Q0 = 1e-4 Mpc^-1`;
- the same Exp K(Q) cosmological branch and background as the closed linear chain;
- `beta0 in {1,0.5,0.1}` as co-primary;
- `mu^2 = 2 K2 Q0^2/(2-K_B)`;
- the NL0B local conservative memory completion and positive Drude spectrum;
- physical memory tangent at `eta=0` only for the first screened-resummed response calculation.

The Simple/Exponential/Sharp interpolation labels are retained as historical co-primary controls, but NL1C2 permits replacing their Y-sector coefficient by the common saturated limit `1/beta0` only within the certified high-gradient physical-amplitude regime.

No new screening coefficient is introduced.

## 3. Important distinction: this is an amplitude resummation

The homogeneous FLRW background still has `X_mu=0` and therefore the exact small-amplitude derivative of the published interpolation satisfies `J_Y(0)=0`.

NL1C3 must **not** rewrite the homogeneous background theory by setting `J_Y=1/beta0` at `X=0`.

Instead, the derivation must distinguish

1. the unchanged homogeneous FLRW background;
2. the finite physical-amplitude, band-limited inhomogeneous reference state established by NL1C0;
3. perturbations/tangents around that physical-amplitude screened reference.

Any derivation that simply inserts `1/beta0` into the original FLRW first-order equations without identifying this change of expansion point fails this gate.

## 4. Locked derivation checks

### D1. Saturated Y-sector tangent

Starting from the frozen covariant Y-sector action, show that around a reference configuration satisfying `sqrt(Y)/a0 >> 1`, the leading variation is

\[
\delta\left[\nabla_\mu(J_Y X^\mu)\right]
=
\frac1{\beta_0}\nabla_\mu\delta X^\mu
+O(10^{-6})
\]

through the NL1C2 certified amplitude range, with the interpolation-shape derivative terms bounded by the preserved NL1C2 stiffness result.

### D2. Background preservation

The FLRW background equations must remain exactly those of the frozen Exp AeST cosmology. The saturated coefficient is a property of the finite-amplitude reference state and must not generate a new homogeneous background source.

### D3. Static weak-field control

In the time-independent high-gradient limit, the reclosed equations must reduce to

\[
\nabla^2\Phi+(1+\beta_0)\mu^2\Phi=4\pi G_N\rho
\]

and

\[
\chi=\frac{\beta_0}{1+\beta_0}\Phi+\text{constant}
\]

up to the usual curl-free control assumptions.

### D4. Covariant source placement

The saturated Y-sector term must be placed in the scalar/aether equations by variation of the frozen covariant action. It may not be added directly to `delta_m`, a Poisson equation, or the CLASS matter transfer function by hand.

### D5. Noether/Bianchi consistency

The scalar, aether and metric equations must retain the diffeomorphism/Noether consistency relation around the finite-amplitude reference so the system is not over-constrained.

### D6. Memory tangent compatibility

With the saturated baseline held fixed, the NL0B auxiliary system must still define the eta=0 directional source

\[
\left.\partial_\eta E'\right|_0
=-\frac{aQ}{2K_B}B_{\chi,\rm raw}
\]

plus any additional eta-linear terms forced by variation of the covariant memory action around a nonzero finite-amplitude reference. These terms must be derived; they may not be omitted merely because direct linear Einstein stress vanished around FLRW.

This is a critical distinction from the original v0.77 tangent.

### D7. Deterministic numerical state

The resulting equations must be expressible as a deterministic initial-value/constraint system suitable for either

- a pseudo-spectral finite-amplitude evolution, or
- an equivalent screened-resummed mode system if the derivation proves exact mode locality in the saturated branch.

The derivation must state which option is justified. No GR/Poisson toy closure is allowed.

### D8. Pre-numerical validation plan

Before any memory-survival result is inspected, freeze tests for:

- recovery of the published static high-gradient Helmholtz limit;
- convergence to the frozen FLRW equations as the finite-amplitude reference is removed, noting the non-uniform `a0` limit;
- conservation/constraint residual;
- beta0 co-primary consistency;
- eta=0 memory-off baseline identity;
- numerical resolution convergence.

Quantitative tolerances for the actual implementation must be committed before running the screened-resummed memory response.

## 5. Classification

If D1-D8 are all closed without introducing a new physical function or outcome-dependent coefficient:

**NL1C3_SCREENED_RESUMMED_DYNAMICAL_BRIDGE_PASS**

If the frozen covariant theory contradicts the proposed reclosure:

**NL1C3_SCREENED_RESUMMED_DYNAMICAL_BRIDGE_FAIL**

If an additional theory choice or missing finite-amplitude field equation is unavoidable:

**NL1C3_SCREENED_RESUMMED_DYNAMICAL_BRIDGE_INCOMPLETE**

## 6. Interpretation rule

A PASS freezes the dynamical equations for the first physically amplitude-consistent eta=0 memory-survival calculation. It does not by itself establish delay, enhancement, saturation, nonlinear collapse, or observational agreement.

A FAIL/INCOMPLETE result is retained honestly and does not alter the certified v0.77/v0.78 linear-state tangent or NL1C0-NL1C2 results.
