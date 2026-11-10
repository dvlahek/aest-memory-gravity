# GE19 LW19 — exact temporal diffeomorphism of the *entire original reduced* GE06 + GE05 action

**10 November 2026.** Classification: **GE19_LW19_FULL_REDUCED_GE06_GE05_TEMPORAL_ACTION_COVARIANCE_PASS_CLASS_MAP_OPEN**.

## Scientific result

We no longer merely infer a time-Noether identity from the general field transformation, as in LW18. We **directly varied the complete original plane-symmetric, longitudinal analytic 1+1 GE06 Einstein+AeST plus positive normalized GE05 memory bath Lagrangian** under an arbitrary local time refoliation. It transforms exactly into spacetime boundary terms, including the nontrivial correction required because the original GE06 gravitational spatial curvature was **already integrated by parts**.

For the original coframe with lapse N, scale variables L,R, longitudinal shift b, aether rapidity u, scalar phi and auxiliary q,

\[
ds^2=-N^2dt^2+L^2(dx+b\,dt)^2+R^2(dy^2+dz^2),
\qquad \xi=f(t,x)\partial_t,
\]

the *frozen source code* defines

\[
k_L={L_t-bL_x-Lb_x\over NL},\quad
k_R={R_t-bR_x\over NR},
\]

\[
\mathcal L_{\rm GR}
=NLR^2(-4k_Lk_R-2k_R^2)
+{2NR_x^2\over L}+{4N_xRR_x\over L}.
\]

The combined scalar/aether/one-mode memory contribution is

\[
\mathcal L_{\rm other}=
NLR^2\left[
K_BE^2+2(2-K_B)EX-(2-K_B)X^2+2K(Q_{\rm inv})
+{\eta\over4}\{(Aq)^2-(\omega q-\sqrt w\,X)^2\}
\right].
\]

Here the original exact GE06/GE05 invariants are

\[
\sigma=(\phi_t-b\phi_x)/N,\quad
Q_{\rm inv}=\cosh u\,\sigma+\sinh u\,{\phi_x\over L},\quad
X=\sinh u\,\sigma+\cosh u\,{\phi_x\over L},
\]
\[
E=\cosh u\left[{u_t-bu_x\over N}+{N_x\over NL}\right]
+\sinh u\left[k_L+{u_x\over L}\right],\quad
Aq=\cosh u\,{q_t-bq_x\over N}+\sinh u\,{q_x\over L}.
\]

The **exact Lie variations** of the ADM fields are the already independently tested LW18 transformations. With the field and derivative-jet prolongations of these transformations, every Qinv, X, E, Aq has purely scalar transport \(\delta I=f I_t\); the volume NLR² has the correct weight-one density transport. Thus

\[
\boxed{\delta_f\mathcal L_{\rm other}=
\partial_t(f\mathcal L_{\rm other}).}
\]

For the **already-by-parts gravitational expression** a strict density equality would be **incorrect**. The exact extra expression is

\[
\delta_f\mathcal L_{\rm GR}
-\partial_t(f\mathcal L_{\rm GR})
=A f_x+Bf_{tx}+Cf_{xx}
\]

with

\[
B={4NRR_x\over L},\qquad
C=-{4NRR_t\over L},
\]

\[
A={4R\over L^2}
\left(LN_tR_x-LN_xR_t-L_tNR_x+L_xNR_t\right)
=\partial_tB+\partial_xC.
\]

Consequently,

\[
\boxed{
\delta_f\mathcal L_{\rm total}
=\partial_t\left(f\mathcal L_{\rm total}
+\frac{4NRR_x}{L}f_x\right)
-\partial_x\left(\frac{4NRR_t}{L}f_x\right).
}
\]

This identity holds **off shell** for arbitrary smooth reduced fields, arbitrary differentiable original analytic \(K(Q)\), any finite symbolic positive-bath eta mode and compactly supported f. There is **no numerical CLASS solution or cosmological parameter adjustment** in the proof.

Because the full **reduced original action** is invariant under compactly supported temporal reparametrization, its Euler derivatives obey the LW18 **reduced time-Noether differential operator**, now justified by directly varying the actual combined action. The geometric Noether operator itself remains the original LW18 result. For transparency, LW19 did **not** independently expand all seven complete Euler-source expressions and substitute them one by one into that differential operator. This is a legitimate direct action-level Noether proof for the **reduced** theory, not a full 3+1 CLASS action-to-fluid proof.

## Verified evidence

- Frozen original GE06 Lagrangian, Git blob: a7afe0035054a9dca55d74a6497c081422114b4c.
- Frozen original GE05 positive bath Lagrangian, Git blob: 40837d77f89028da30c28899e2d0530a4401844e.
- Original LW18 exact field transformations, source blob: 9a6b83d4188e5a4756c13ed8b946d2b0f49d8fce.
- Original researcher local LW18 14/14 output: results/ge19_lw18_reduced_time_diffeo_noether_20261110.json, SHA-256 **82ab6c7c9bb8efa676de8817cb0949ace86823dd92414709486020cfa0f9fc69**, previously archived byte-identical.
- LW19 predata formula freeze: ge19/lw19_reduced_full_action_temporal_invariance_predata_20261110.json, commit **8c4c4659c3100fbb054d6e955a6be9a26f4d7b93**, Git blob 397e276abaa597412bbbfe35faf9685107f8e403. The core algebra was inspected **before** this freeze; it is a reproducibility lock, not a blind prospective discovery.
- Reproducible source with hash and original source marker locks: ge19/lw19_reduced_full_action_temporal_invariance_20261110.py, commit **0bc0f1d1f9b2629d522b99fe32f033cee573caa7**. The historical 5/5 marker strings were checked against the matching original GitHub source files. This **canonical** runner has **not yet been executed in the researcher's WSL**.
- Actually executed independent private-container SymPy 1.14.0 prototype gave **16/16 exact PASS**, including all four invariant scalar transformation tests, correct density-weight test, complete matter action test, five exact GR anomaly coefficients, integrable GR boundary, whole action equality and negative controls: missing/opposite GR boundary and omitted aether rapidity boost. Archived as results/ge19_lw19_full_reduced_action_temporal_invariance_independent_20261110.json, commit **2ca2296e096839a7655d441fa076d2de284419a2**. This is the independent prototype replay, **not an assertion of canonical local WSL pass**. A synthetic negative-control wiring issue in exploratory Python was corrected before archiving the prototype; it did not alter the fixed physics theorem or model.

## Which remaining tests are now scientifically worth doing?

**We should stop repeating small-source Ward and high-precision numerical loops.** The exact reduced temporal covariance is now directly proven, but the observational model still needs:

1. **One physical action-to-CLASS bridge**, including full 3+1 scalar+aether+metric/multiplier first-order stress and the source-to-fluid Jacobian/constraints (the frozen reduced result alone is not sufficient to certify it).
2. **A full coupled smooth-branch observer**, including the other species. Compute a physically normalized \(G_{WE}\) and the matter–Weyl response to an **admissible** original positive-bath history pair. LW11/LW12 local forced-impulse Taylor jets are insufficient for an observed memory claim.
3. **A legitimate forward-modeling and sensitivity forecast**. Freeze cosmological parameters/priors, physical eta and survey windows *before* revealing observed residuals. An Asimov forecast can expose whether an existing DES Y3 redMaGiC galaxy/lensing window would discriminate a well-defined memory prediction from standard gravity and allowed alternatives.
4. **Only then the observed likelihood**; failure to detect is a valid constraint, not license to tune the physical model after inspecting the test residuals. A numerical tolerance refinement should follow forecast precision requirements, not an arbitrary decimal target.

Unchanged prior blockers: LW03 radial quadrature FAIL, LW05 full cosmic-shear line-of-sight support BLOCK, LW08 differential matter–Weyl source response UNRESOLVED and H4/Z21 uncertified. Full 3+1 CLASS action-equivalence, global retarded Green and observed sky signal still OPEN. No Nature-level detection is claimed.

### Local reproducibility, zero CLASS calls

Run in the existing WSL clone with original researcher LW18 file under results:

~~~bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate

python3 -u -m ge19.lw19_reduced_full_action_temporal_invariance_20261110 --self-test

python3 -u -m ge19.lw19_reduced_full_action_temporal_invariance_20261110 \
  --out results/ge19_lw19_reduced_full_action_temporal_invariance_20261110_r1.json
~~~

The program fails closed if source blobs or the original LW18 SHA differ and refuses to overwrite the output. It uses only SymPy and Git hash checks, **no CLASS numerics**.
