# NL1B2 predata — directional second-order eta-tangent closure

Classification before derivation: **NL1B2_PREDATA_DIRECTIONAL_SECOND_ORDER_ETA_TANGENT**

This is a theory-only preregistration created after the historical NL1B gate was classified `NL1B_SECOND_ORDER_DYNAMICAL_CLOSURE_INCOMPLETE` and before any directional weakly nonlinear memory result.

Historical results remain immutable. NL1B remains INCOMPLETE; v0.77, v0.78, NL0B, NL0C and NL1A remain PASS; all earlier FAIL classifications remain FAIL.

## 1. Scientific target

The first strong nonlinear quantity will be the **eta derivative at eta=0 of the second-order scalar response**, not a finite-eta nonlinear simulation.

This choice is fixed before the outcome because:

1. the linear eta=0 memory tangent is already numerically certified by v0.77;
2. it avoids introducing or selecting a finite physical eta before the weakly nonlinear response is controlled;
3. it is sufficient to answer whether the certified linear memory direction propagates into the first nonlinear AeST response;
4. the frozen `Y^(3/2)` sector is naturally directional rather than globally bilinear at the FLRW zero-gradient state.

No observational data, likelihood, finite physical eta, interpolation-function choice, or outcome-dependent beta0 selection is allowed.

## 2. Frozen exact theory

Use exactly the theory frozen by NL0B/NL0C:

\[
S=S_{AeST}+S_{mem},
\]

with

\[
\mathcal F(\mathcal Y,\mathcal Q)
=-2\mathcal K(\mathcal Q)+(2-K_B)\mathcal J(\mathcal Y),
\]

\[
\mathcal J(\mathcal Y)=
\frac{2}{3(1+\beta_0)a_0}\mathcal Y^{3/2}+O(\mathcal Y^2),
\]

\[
\beta_0\in\{1,0.5,0.1\},
\qquad a_0=1.2\times10^{-10}\,{\rm m\,s^{-2}},
\]

and the NL0B local conservative positive Drude memory action. The frozen cosmological parameters, Exp `K(Q)` branch, `K_B=0.0665`, `tau H0=10`, background calibration and Drude spectrum are unchanged.

The numerical tangent amplifier `lambda` is not a physical parameter and is absent from the theory definition.

## 3. Directional hierarchy

Let `Z` denote the complete scalar-projected field state required by the exact equations: metric scalar variables, AeST scalar/aether variables, minimally coupled matter variables, and the normalized memory auxiliaries after `U_j=sqrt(eta) q_j`.

Expand simultaneously in perturbation amplitude `epsilon` and physical memory coupling `eta` around the same FLRW background:

\[
Z(\epsilon,\eta)=\bar Z
+\epsilon Z_{10}
+\eta\epsilon Z_{11}
+\frac{\epsilon^2}{2}Z_{20}
+\frac{\eta\epsilon^2}{2}Z_{21}
+O(\epsilon^3,\eta^2).
\]

Interpretation:

- `Z10`: baseline first-order AeST perturbation;
- `Z11 = partial_eta Z^(1)|_0`: certified linear memory tangent;
- `Z20`: baseline directional second-order response;
- `Z21 = partial_eta Z^(2)|_0`: target first weakly nonlinear memory tangent.

No finite eta is needed in NL1B2/NL1C.

## 4. Exact operator split

Write the exact memory-off Euler-Lagrange residual as

\[
\mathscr E_0[Z]=\mathscr E_{an}[Z]+\mathscr E_Y[Z],
\]

where `E_an` contains all terms analytic around FLRW (Einstein, vector/aether, Q-sector, constraints and minimally coupled matter), while `E_Y` is the NL0C nonanalytic small-gradient Y-sector.

Define

\[
L\equiv D\mathscr E_{an}[\bar Z],
\]

\[
Q(V,W)\equiv D^2\mathscr E_{an}[\bar Z](V,W).
\]

The directional Y source is

\[
Y_2[V]\equiv
\lim_{s\downarrow0}s^{-2}\mathscr E_Y[\bar Z+sV].
\]

The coefficient of physical eta in the normalized NL0B equations is denoted

\[
\mathscr M[Z,q],
\]

and its first and second perturbative directional coefficients around FLRW are `M1` and `M2`. They are defined by functional differentiation of the frozen NL0B action, not by a nonlinear Fourier `k chi` rule.

## 5. Locked hierarchy to derive

The gate must establish the scalar-projected equations

### H1. Baseline first order

\[
L Z_{10}=0.
\]

### H2. Linear eta tangent

\[
L Z_{11}=-M_1[Z_{10},q_{10}],
\]

with scalar reduction exactly equal to the preserved v0.77 forcing system.

### H3. Baseline directional second order

\[
L Z_{20}=-Q(Z_{10},Z_{10})-2Y_2[Z_{10}].
\]

### H4. Directional second-order eta tangent

\[
L Z_{21}=
-2Q(Z_{10},Z_{11})
-2DY_2[Z_{10};Z_{11}]
-M_1[Z_{20},q_{20}]
-M_2[Z_{10},q_{10};Z_{10},q_{10}],
\]

where the exact sign convention follows from putting all Euler-Lagrange residuals on the left-hand side. If the explicit derivation requires a notational regrouping, it must be algebraically identical to this functional expansion; no term may be omitted because it is inconvenient.

## 6. Locked Y-sector tangent identity

For

\[
\mathbf g=\nabla_{phys}\chi_{10},
\qquad
\mathbf h=\nabla_{phys}\chi_{11},
\]

and

\[
F(\mathbf g)=|\mathbf g|\mathbf g,
\]

the directional derivative must be

\[
DF_{\mathbf g}[\mathbf h]
=|\mathbf g|\mathbf h
+\frac{\mathbf g\cdot\mathbf h}{|\mathbf g|}\mathbf g
\quad (|\mathbf g|>0),
\]

with the continuous directional derivative set to zero at `|g|=0`.

Therefore

\[
DY_2[\chi_{10};\chi_{11}]
=\frac{2(2-K_B)}{(1+\beta_0)a_0}
\nabla_{phys}\cdot
\left[
|\mathbf g|\mathbf h+
\frac{\mathbf g\cdot\mathbf h}{|\mathbf g|}\mathbf g
\right].
\]

This is a primary identity and must be checked numerically against centered finite differences of the already validated NL1A operator before any physical source map is interpreted.

## 7. Scalar projection and generated vector/tensor modes

Scalar-scalar products generate second-order vector and tensor modes, but on an FLRW background the linearized SVT operator is block diagonal. Therefore generated `O(epsilon^2)` vector/tensor fields do not feed back into the scalar equations until higher order. NL1B2 freezes the **scalar projection of the exact second-order hierarchy** as the target for the first nonlinear memory response.

This does not claim that vector/tensor second-order observables vanish.

## 8. Constraint consistency

Because `L`, `Q`, `Y2`, `M1` and `M2` are obtained by differentiating one diffeomorphism-invariant frozen action, the exact Noether identity is differentiated in the same hierarchy. The scalar constraint equations are therefore propagated by the same order-by-order identity provided the complete projected source at each order is retained.

A later implementation must verify the chosen independent constraint residual rather than assume it numerically.

## 9. No new physics freedom

NL1B2 introduces no new physical coefficient or function. All source operators are derivatives of the already frozen action. The three beta0 values remain co-primary and enter only through the common `1/(1+beta0)` factor in the leading Y-sector.

## 10. Implementation requirements before NL1C interpretation

A numerical NL1C source/evolution implementation must, before looking at the physical sign:

1. reproduce the NL1A operator tests;
2. verify `DY2` by finite difference for deterministic 1D and 3D fields;
3. reproduce the v0.77 first-order eta tangent when nonlinear terms are disabled;
4. use the same native-state/interpolation lessons from v0.78;
5. report a scalar constraint residual;
6. use fixed grids/resolution gates preregistered before the physical nonlinear source/evolution result.

## 11. Classification

If H1-H4, the Y tangent identity, scalar projection, Noether inheritance and no-new-freedom statement are all established:

**NL1B2_DIRECTIONAL_SECOND_ORDER_ETA_TANGENT_PASS**

If the functional expansion contradicts the frozen action:

**NL1B2_DIRECTIONAL_SECOND_ORDER_ETA_TANGENT_FAIL**

If a new coefficient/function is required:

**NL1B2_DIRECTIONAL_SECOND_ORDER_ETA_TANGENT_INCOMPLETE**

A PASS does not retroactively turn historical NL1B into PASS. It freezes a narrower, outcome-independent eta=0 directional route to the first controlled weakly nonlinear memory result.
