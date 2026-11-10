# GE19 LW26 — spatial Noether identity and direct linear metric source of the memory bath

**Date:** 2026-11-10. **Physics decision:** the original GE06+GE05 *reduced* plane-symmetric analytic action is spatial-diffeomorphism covariant; the positive NL0B bath has zero **direct first-order metric Euler source** about relaxed FLRW. The LW25 conditional factor-two action/CLASS eta-source mismatch is NOT resolved. Do not certify the original physical matter–Weyl derivative or fit DES lensing data.

## 1. Researcher's LW25 original result — frozen and archived

The uploaded WSL log and JSON were read directly, all 15 recorded symbolic checks were true, and all six original source hashes agreed. The original hashes are:
- \`results/ge19_lw25_r1.log\`: SHA-256 \`00b23af78cb100d4b43b5f4f1b1516e823d0b7adab0d5ae299b66a87f6966978\`; Git blob \`afa800adf877b67d0ec8f2ef054cfc37523b8c7e\`.
- \`results/ge19_lw25_aether_shift_class_source_consistency_20261110_r1.json\`: SHA-256 \`ce02df636fac121d54fd0115a1ed1401725e5cff660ecd83e295494a86ac213f\`; Git blob \`6e2f7f5326c0e54f5177603aaa9bd04660e980d3\`.

Both GitHub files have been fetched and verified to have **exactly the uploaded Git blob digests**. The repeated LW24 JSON and log SHA-256 match the already archived originals, so no duplicate was archived. Actual LW25 classification remains \`GE19_LW25_REDUCED_AETHER_CLASS_ETA_SOURCE_FACTOR_TWO_CONDITIONAL_REVIEW_REQUIRED\`. It is not a whole-theory failure.

## 2. New exact spatial-diffeomorphism Ward identity of original reduced action

For the frozen coframe
\[
ds^2=-N^2dt^2+L^2(dx+b\,dt)^2+R^2(dy^2+dz^2),
\]
take an arbitrary smooth compactly supported spatial generator \(\xi=g(t,x)\partial_x\), active convention \(\delta=\mathcal L_\xi\). The exact transformations are
\[
\begin{aligned}
\delta N&=gN_x,&\delta L&=gL_x+Lg_x,&\delta R&=gR_x,\\
\delta b&=gb_x+g_t-bg_x,&\delta u&=gu_x,&
\delta\phi&=g\phi_x,&\delta q&=gq_x.
\end{aligned}
\]
Unlike the temporal refoliation boost in LW18, the aether rapidity is an ordinary scalar under a pure spatial coordinate relabeling that preserves the time slices.

Direct prolongation of all first jets shows \(Q_{\rm inv},X,E,Aq,k_L,k_R,\sigma\) transform as exact spatial scalars. The volume \(NLR^2\), original reduced GR density, AeST analytic density, and GE05 bath density each satisfy
\[
\delta\mathcal L=\partial_x(g\mathcal L).
\]
All seven invariants, four density-weight tests passed exact algebraic independent SymPy checks.

Let \(E_z=\delta S/\delta z\) for the full **reduced** Euler equations. Integration by parts of \(\sum_zE_z\delta z\) gives the **off-shell** spatial Noether identity
\[
\boxed{\begin{aligned}
\mathscr I_x={}&N_xE_N+L_xE_L+R_xE_R+b_xE_b+
 u_xE_u+\phi_xE_\phi+q_xE_q\\
&-\partial_x(LE_L-bE_b)-\partial_tE_b=0.
\end{aligned}}
\]
The integration-by-parts operator was independently verified for seven entirely arbitrary symbolic Euler functions. Negative controls dropping the necessary \(g_t\) shift term, reversing the \(bg_x\) term, or dropping the \(Lg_x\) term fail.

## 3. Exact zero direct bath metric Euler source at linear order

In the original reduced NL0B action
\[
\mathcal L_{\rm bath}=\frac{\eta NLR^2}{4}
\left[(Aq)^2-(\omega q-\sqrt w X)^2\right],
\]
the relaxed FLRW background has \(Aq_0=X_0=q_0=u_0=0\). Exact differentiation and first-order expansion show all *direct* bath Euler metric pieces vanish:
\[
(E_N^{\rm bath})_1=(E_L^{\rm bath})_1=
(E_R^{\rm bath})_1=(E_b^{\rm bath})_1=0,
\]
and the first-jet metric conjugates to \(N_x,L_t,L_x,R_t,R_x,b_x\) also vanish, in the original **coframe field basis** (10/10 exact gates). This result is consistent with original GE05's source-level metric M1 zero. It does **not** say the Weyl potential has zero response: the bath modifies scalar/aether Euler sources, causing *indirect* changes in the metric through constraints.

**Important boundary:** zero direct first-order bath metric source and a spatial Ward identity do **not alone** prove the original effective-fluid CLASS \(\theta_A'\) equation is unchanged for nonzero eta. A time-dependent field redefinition, a constraint-eliminated source or a scalar/aether-momentum Euler combination may induce a correction while preserving covariance. That full map has not yet been derived.

## 4. Implications for LW25 factor-two physics gate

LW25 already identified, **under the unchanged CLASS velocity and original \(\chi\) dictionary**, the reduced action \(-\eta QB_\chi/4\) versus the original patched CLASS E-row \(-\eta QB_\chi/2\). The extra bath direct linear metric stress cannot by itself supply the missing term in the reduced coframe because it is identically zero. However this does not exclude a term from the full constrained scalar/aether redefinition.

Do not patch the 1/2 to 1/4 merely to force algebraic agreement. Do not add an ad hoc correction to \(\theta_A'\). Preserve the old LW01–LW08 numerical results as **formal implemented response** and the genuine LW22 DES Y3 source-geometry PASS as distinct; physical eta normalization and observational discrimination remain OPEN.

## 5. Reproducibility

- Predata \`ge19/lw26_reduced_spatial_noether_bath_metric_source_predata_20261110.json\`, committed before canonical runner, commit \`b51af13dcde5a859e204c5e9008fcf3008e2a654\`, blob \`82c503068e2d8bf5c9c60badd62e491ed6c2714d\`. Preliminary algebra was inspected before this freeze; do not claim blind preregistration.
- Canonical \`ge19/lw26_reduced_spatial_noether_bath_metric_source_20261110.py\`, commit \`b77ab221165eb2bb31b5d4f8cbc3e3953f5e2cc7\`. Its parent lock requires the *actual user WSL LW25 JSON* and the five source blobs.
- Independently checked 25 exact SymPy statements in two simple analysis probes (7 reduced scalar invariants, 4 density covariance, 10 metric-source zeros, 1 offshell Noether operator, 3 deliberate negative controls). This is **not** a claim the new canonical WSL runner has been executed. Its expected output is \`GE19_LW26_SPATIAL_NOETHER_SELFTEST_PASS 25\`.

No parameter sweeps, CLASS computations, observed DES residual inspection, or likelihoods were performed.

**Next physical task after local replay:** derive the joint scalar/aether/shift Euler state-to-effective-fluid velocity change of variables, including the eta-dependent piece, and independently test whether it accounts for the LW25 difference. Preserve an unresolved factor-two status if it does not.

The full 3+1 nonanalytic Y, H4 Z21, full physical \(\partial_\eta P_{\delta W}\), DES angular \(\gamma_t\), galaxy-bias/IA nuisance marginalization, and detection remain uncertified.
