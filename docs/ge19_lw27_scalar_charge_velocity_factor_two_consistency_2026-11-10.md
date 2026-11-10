# GE19 LW27 — scalar charge closes the conditional aether/CLASS factor-two test

**Date:** 2026-11-10. **Scientific classification:** \`REDUCED_SCALAR_CHARGE_FACTOR_TWO_COMPATIBILITY_REVIEW_FULL_3PLUS1_OPEN\`. This is an exact linearized **reduced analytic GE06+GE05** consistency test; it is **not** a complete 3+1 action-to-CLASS proof, a rewritten physical theory, or a DES memory observation. The problem was diagnosed from exploratory analysis before the LW27 predata freeze; no blind-preregistration claim.

## Original WSL LW26 evidence, verified and archived

User-supplied \`results/ge19_lw26_r1.log\` SHA-256 \`f6db7f2910fa1e240c9c671b96be7f2c090e2743c1a3f99ac377c8d49311123b\`, 356 bytes; original Git blob \`5a343c108f30b56df6d495b79497a037fd690f3b\`.
Original \`results/ge19_lw26_reduced_spatial_noether_bath_metric_source_20261110_r1.json\` SHA-256 \`dd11a35d4124091a277e835e7edfa541691a31b63c0436dbc89ac85fd9f146fc\`, 2,727 bytes; original Git blob \`b6c695f0f39f894c55db0a8458c5b05bcd2d1053\`. **Both GitHub archive blobs were independently fetched and matched original blobs byte-exactly**. LW26 WSL 25/25 PASS, five original source locks PASS. Its scalar-aether/CLASS normalization remains unresolved, not relabeled.

Resubmitted LW25 log and JSON were SHA-identical to earlier archived LW25, so no duplicate archives were created.

## 1. The missing exact constraint: theta evolution is a kinematic identity under the locked dictionary

From the LW24 action-derived reduced stress and original CLASS background,
\[
\rho_A=(QK_Q-K)/3,\quad p_A=K/3,\quad
c_a^2=K_Q/(QK_{QQ}),\quad \dot Q=-3Hc_a^2Q.
\]
The original LW24 linear pressure is \(\delta p_A=K_Q\delta Q/3\), where
\(\delta Q=\dot\varphi-Q\Psi\). Hence
\[
\frac{\Pi_A}{1+w_A}=\frac{\delta p_A}{\rho_A+p_A}=\frac{\delta Q}{Q}.
\]

If the frozen scalar/CLASS phase-velocity dictionary \(\varphi=Qa\theta_A/k^2\) is imposed, then differentiating it (with the fixed Newtonian gauge metric convention) gives **identically**
\[
\boxed{\dot\theta_A=(3c_a^2-1)H\theta_A
+\frac{k^2}{a}\left(\frac{\Pi_A}{1+w_A}+\Psi\right).}
\]
This is exactly the original v019 CLASS \(\theta_A'\) equation divided by \(a\). Crucially, there is **no independent explicit bath eta term** unless the fundamental phase/velocity dictionary or the reduced pressure identification is changed. This is a **conditional identity**, not a proof that the full 3+1 physical velocity dictionary must take that form.

The same dictionary and \(\chi=\varphi+Q\alpha\), \(\dot\alpha=E_A-\Psi\) imply
\[
\boxed{\dot\chi=Q\left[E_A+\frac{\Pi_A}{1+w_A}-3c_a^2H\alpha\right].}
\]
The formal LW25 compensation \(\Delta\dot\chi=\eta Q B_\chi/[4(2-K_B)]\) therefore cannot be independently inserted while retaining all original definitions and the phase-velocity identity. It requires a genuinely new **action-derived** \(\eta\)-dependent field redefinition or modified equation.

## 2. Reduced scalar-charge continuity selects the aether coefficient

The exact original reduced GE06+GE05 scalar current from LW17 is, at first perturbative order,
\[
\delta J_\phi^t=2a^3K_{QQ}\delta Q-6a^3K_Q\Phi,
\]
\[
\delta J_\phi^x=ik a
\left[2C(E_A-\chi)+2K_Q\alpha-\frac{\eta B_\chi}{2}\right],
\quad C=2-K_B.
\]
The linear action-derived density from LW24 is
\[
\delta\rho_A=\frac{1}{3}\left[QK_{QQ}\delta Q
-\frac{k^2}{a^2}(K_BE_A+C\chi)\right].
\]
Eliminate \(\delta Q\) in the temporal current:
\[
\boxed{
\delta J_\phi^t=\frac{2a^3}{Q}
\left[3\delta\rho_A+\frac{k^2}{a^2}(K_BE_A+C\chi)\right]
-6a^3K_Q\Phi.
}
\]

The *original action scalar Euler* \(-\partial_t J_\phi^t-ikJ_\phi^x=0\), after differentiating at **fixed perturbation state and metric** with respect to the physical action parameter \(\eta\), yields the necessary **explicit source** relation
\[
\boxed{
\frac{6a^3}{Q}\,\partial_\eta\dot{\delta\rho}_A
+\frac{2ak^2}{Q}
\left(K_B\partial_\eta\dot E_A+C\partial_\eta\dot\chi\right)
+\frac{ak^2 B_\chi}{2}=0.}
\tag{S}
\]
These \(\partial_\eta\) symbols denote *explicit partial derivatives of the right-hand-side ODE at fixed state*, **not** total response along a solution, which would include state variations.

With the fixed phase-velocity dictionary, \(\partial_\eta\dot\chi=0\). The reduced aether Euler from LW25 requires
\[
\partial_\eta\dot E_A\big|_{\rm action}
=-\frac{Q B_\chi}{4K_B}.
\]
Putting this in (S) gives exactly \(\boxed{\partial_\eta\dot{\delta\rho}_A=0}\), i.e. no additional explicit bath source in the density evolution. **The two original action sources cancel: the scalar flux source is not optional.**

However, the original v019j CLASS memory E-row is
\[
\partial_\eta\dot E_A\big|_{\rm patch}
=-\frac{Q B_\chi}{2K_B}.
\]
With the *unchanged* theta/chi dictionary, equation (S) then requires
\[
\boxed{
\partial_\eta\dot{\delta\rho}_A\big|_{\rm required}
=\frac{Qk^2 B_\chi}{12a^2}.
}
\]
Yet the original v019/v019j patch has **no explicit eta-dependent term in its \(\delta_A'\) or \(\theta_A'\) rows**: it injects the bath only into the E-row while evolving the auxiliary coordinates. This establishes a stronger **conditional source-compatibility mismatch** in the reduced scalar+aether+effective-fluid model: the patched E coefficient and the unchanged fluid equations cannot all satisfy original reduced scalar charge for nonzero \(QB_\chi\) under the same fixed dictionary.

The formal LW25 compensator \(\partial_\eta\dot\chi=Q B_\chi/(4C)\) would restore equation (S) even with the patched E coefficient, but is **not** a licensed physics fix: it breaks the exact phase-velocity identity unless an independently action-derived eta-dependent definition is supplied.

## 3. Scientific interpretation

The obstruction is more specific than a numerical factor mismatch: **the frozen original memory patch injects an E-row source without demonstrating compatibility of the complete scalar continuity source, density and velocity phase map at first order in eta.** The reduction identifies a minimal conservation/normalization gate. It does not determine whether the *full covariant AeST theory* demands a corrected E source, extra effective-fluid sources, a different phase/velocity map, or an additional constraint combination.

Do **not** edit the frozen original patch coefficients or add a theta/density compensator ad hoc. Any proposed corrected implementation must first be derived from the full action and independently checked against *both* the aether Euler and scalar charge equations, as well as Einstein constraints and original CLASS gauge. It should be treated as a **new model version** with its own frozen predictions, not a silent alteration of LW01–LW08 results.

**Observable status:** LW22 original DES lensing geometry remains PASS; LW23 original offline source factor matches the *implemented* E coefficient (a source-level identity, not full action equivalence); LW24 reduced density/pressure PASS; LW25 factor 2 REVIEW; LW26 spatial Noether PASS. A fully physical \(\partial_\eta P_{\delta W}\), actual DES \(\gamma_t\) forward, nuisance-marginal signal and memory detection remain **UNAVAILABLE/UNCERTIFIED**.

## 4. Reproducibility and one bounded run

Frozen data:
\`ge19/lw27_scalar_charge_velocity_source_closure_predata_20261110.json\`,
commit \`373e9f41b2264d53f8713b5daa4564245bef64ed\`, Git blob \`8de2caa72db8d17b44e3554d1bee58b031207f72\`.

Canonical source-locked script:
\`ge19/lw27_scalar_charge_velocity_source_closure_20261110.py\`.
The initial commit \`ab1c3d406b7f1f8364ebb19427d31f2f2472798a\` contained a false **self-test sign check and inert placeholder**, corrected in commit \`dd7b03ed16fbb63818d8d536e7b734a9b5da1e95\`. The actual physical equations and frozen predata were not changed. The 18 final exact algebraic checks were independently replayed with SymPy and all passed in the analysis container; required strings in eight original GitHub source files and their blobs also matched. The fixed canonical script has **not** been run in researcher's WSL. Do not misstate independent mathematical checks as original WSL results.

Run once, no CLASS/observational data:
~~~bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
set +e
set -o pipefail
python3 -u -m ge19.lw27_scalar_charge_velocity_source_closure_20261110 --self-test
python3 -u -m ge19.lw27_scalar_charge_velocity_source_closure_20261110 \
  --out results/ge19_lw27_scalar_charge_velocity_source_closure_20261110_r1.json \
  2>&1 | tee results/ge19_lw27_r1.log
echo "EXIT=$?"
~~~

The expected output is \`GE19_LW27_SCALAR_CHARGE_SELFTEST_PASS 18\`, \`GE19_LW27_SOURCE_LOCKS_PASS 8\`, classification \`GE19_LW27_REDUCED_SCALAR_CHARGE_FACTOR_TWO_COMPATIBILITY_REVIEW_FULL_3PLUS1_OPEN\`. On a provenance failure, preserve the failure and investigate the source, rather than changing the physics or the gate.

**Next only meaningful physics milestone:** write a single **full action-derived, gauge-consistent** scalar–aether–Einstein effective-fluid change of variables (including all eta source rows and unit-aether constraints) and decide whether the original v019j implementation is physically admissible. Until then, no more broad CLASS sweeps and no claimed observation.
