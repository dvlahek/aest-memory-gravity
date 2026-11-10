# GE19 LW18 — reduced time-diffeomorphism Noether identity and linear memory-source cancellation

**2026-11-10. Classification:** GE19_LW18_REDUCED_TIME_DIFFEO_NOETHER_KINEMATICS_AND_BATH_LINEAR_IDENTITY_PASS_CLASS_ACTION_MAP_OPEN.

**Proven scope.** This phase derives the temporal refoliation transformation of the frozen original GE06 plane-symmetric 1+1 ADM metric and unit aether, the corresponding **off-shell Noether differential operator**, and an exact first-order GE05 positive-bath scalar/rapidity source cancellation. The independently run SymPy 1.14.0 tests pass **14/14**. This is not a full independent substitution of every original GE06+GE05 Euler derivative into the operator, and does not establish the complete 3+1 AeST+NL0B-to-CLASS stress dictionary, constrained full Weyl Green function, or an astronomical detection.

**LW17 status clarified:** researcher ran corrected LW17 in WSL and reports 11/11 symbolic gates, SOURCE_CHECKS=True, JSON_VALID=True, classification GE19_LW17_REDUCED_COMBINED_AEST_MEMORY_SCALAR_CURRENT_EXACT_PASS_FULL_CLASS_ACTION_MAP_OPEN. This supersedes the first known WSL failure from a corrected SymPy derivative-substitution bug. The researcher has not uploaded the actual valid LW17 _r1.json bytes, so there is **no byte-exact GitHub archive of that original WSL artifact** in this turn.

Source provenance: original GE06 analytic action source Git blob a7afe0035054a9dca55d74a6497c081422114b4c, original GE05 positive memory action source blob 40837d77f89028da30c28899e2d0530a4401844e, and corrected LW17 source blob df5acc2c97076736ccdd7755691cacdaaada0e22. LW18 predata ge19/lw18_reduced_time_diffeo_noether_predata_20261110.json, commit 5b9c29c806aaddabe4af63caed0a1888e2365a54, blob c87e52553aacfa0eb2ece6cd9a6e4571c86bdad4. Canonical Git-locked script ge19/lw18_reduced_time_diffeo_noether_20261110.py, commit bfaa8f5e927ae2a6e72fd19d6ec56dc711de9bbf, is **not** yet executed on researcher WSL. Independently computed evidence is results/ge19_lw18_reduced_time_noether_independent_symbolic_20261110.json, commit c3b6e69b3840ba86c034184ef27e4235b591ee94, 14/14 PASS. The analytic formulas were explored before predata: no blind preregistration claim.

## 1. Exact temporal Lie transformation in the original reduced ADM coframe

Frozen original GE06/GE05 metric and unit timelike aether:
\[
ds^2=-N^2dt^2+L^2(dx+b\,dt)^2+R^2(dy^2+dz^2),
\]
\[
A^t=\cosh u/N,\qquad
A^x=-b\cosh u/N+\sinh u/L.
\]

For a compactly supported arbitrary time refoliation vector field \(\xi=f(t,x)\partial_t\) and active convention \(\delta=+\mathcal L_\xi\), exact direct metric/aether Lie calculations give
\[
\boxed{\begin{aligned}
\delta N&=fN_t+Nf_t-Nb f_x,\\
\delta L&=fL_t+Lb f_x,\quad
\delta R=fR_t,\\
\delta b&=fb_t+b f_t-(N^2/L^2+b^2)f_x,\\
\delta u&=fu_t-\frac NL f_x,\\
\delta\phi&=f\phi_t,\qquad \delta q=fq_t.
\end{aligned}}
\]

Crucially the rapidity u is **not** a spacetime scalar under a change of time foliation; its \(-(N/L)f_x\) compensation is compulsory. The independent tests confirm metric \(tt,tx,xx,yy\), aether vector \(t,x\) components, and
\[
\boxed{\delta(NLR^2)=\partial_t(fNLR^2).}
\]
The deliberately wrong choice \(\delta u=fu_t\) fails the Lie test.

## 2. Exact reduced time-Noether differential operator

Let \(E_z=\delta S/\delta z\) be the Euler derivatives of the full **reduced** action for \(z=(N,L,R,b,u,\phi,q)\). Define
\[
\mathscr A=N E_N+b E_b,\qquad
\mathscr B=-Nb E_N+Lb E_L-(N^2/L^2+b^2)E_b-(N/L)E_u.
\]

The Lie transformations give, algebraically and exactly,
\[
\sum_z E_z\delta z
=f\mathscr I+\partial_t(f\mathscr A)+\partial_x(f\mathscr B),
\]
with
\[
\boxed{\begin{aligned}
\mathscr I={}&N_tE_N+L_tE_L+R_tE_R+b_tE_b+
u_tE_u+\phi_tE_\phi+q_tE_q\\
&-\partial_t(N E_N+b E_b)\\
&-\partial_x[-Nb E_N+Lb E_L-(N^2/L^2+b^2)E_b-(N/L)E_u].
\end{aligned}}
\]

For the original diffeomorphism-invariant reduced action, \(\mathscr I=0\) **off shell** follows by Noether's second theorem when f has compact support. The SymPy test confirms the full integration-by-parts identity for completely arbitrary symbolic Euler functions. GE06 gravitational boundary-by-parts terms do not change the bulk Euler identity.

**Claim boundary:** this derives the required **structural temporal Noether operator**; the exact *full* original GE06+GE05 lapse, shift, metric, aether, scalar and bath Euler source expressions have **not all been computed and substituted** here as an independent source-code Ward check. That is the next missing verification.

On a relaxed FLRW solution \(N=1,L=R=a,b=u=q=0,\phi_t=Q\), assuming all background Euler equations hold, the linear operator reduces to
\[
\boxed{
-\partial_t E_N^{(1)}
+\dot a[E_L^{(1)}+E_R^{(1)}]
+Q E_\phi^{(1)}
+\partial_x[a^{-2}E_b^{(1)}+a^{-1}E_u^{(1)}]=0.
}
\]
The transverse \(E_R\) coefficient is \(\dot a\), not a separate arbitrary factor of two: \(E_R\) is already the derivative with respect to the transverse scale field R.

## 3. The actual quadratic bath **source** satisfies the time Ward

For the original normalized positive one-mode bath around relaxed FLRW,
\[
\mathcal L_{\rm bath}^{(2)}
=\frac{\eta a^3}{4}\left[
(\dot q_1)^2-(\omega q_1-\sqrt w X_1)^2
\right],\quad
X_1=Q u_1+a^{-1}\partial_x\varphi_1,
\]
and
\[
B_{X,1}=wX_1-\omega\sqrt w\,q_1.
\]

Direct action variation gives
\[
J_{\phi,\rm bath}^{x,(1)}
=\frac{\partial\mathcal L_{\rm bath}^{(2)}}{\partial(\partial_x\varphi_1)}
=-\frac{\eta a^2}{2}B_{X,1},
\qquad
E_{u,\rm bath}^{(1)}
=\frac{\partial\mathcal L_{\rm bath}^{(2)}}{\partial u_1}
=-\frac{\eta a^3Q}{2}B_{X,1}.
\]
Thus \(E_{\phi,\rm bath}^{(1)}=-\partial_xJ_{\phi,\rm bath}^{x,(1)}
=\partial_x(\eta a^2 B_{X,1}/2)\), consistent with LW17.

For Fourier convention \(\partial_x\mapsto ik\), \(B_{X,1}=(ik/a)B_{\chi,\rm raw}\),
\[
E_{\phi,\rm bath}^{(1)}
=-\frac{\eta a k^2}{2}B_{\chi,\rm raw},\qquad
E_{u,\rm bath}^{(1)}
=-i\frac{\eta a^2kQ}{2}B_{\chi,\rm raw}.
\]
As the relaxed quadratic bath has no *direct* first-order metric source (old original NL0B Identity 6, not independently recalculated here), the bath contribution to the reduced **linear time-Noether identity** is precisely
\[
\boxed{
Q E_{\phi,\rm bath}^{(1)}
+\frac1a\partial_x E_{u,\rm bath}^{(1)}=0.
}
\]
The two terms cancel exactly:
\[
-\eta a k^2 Q B_{\chi,\rm raw}/2
+\eta a k^2 Q B_{\chi,\rm raw}/2=0.
\]
Independent exact action differentiation verifies the aether rapidity source and scalar spatial current, and its negative control removing the scalar Euler partner does **not** cancel.

This is stronger than inserting \(J_D=J_T=0\) into conservation-form fluid equations (LW15): it checks the **physical bath scalar and aether Euler sources and the actual foliation-induced rapidity term**. It is still a **restricted first-order bath source check**, not full action-derived physical \(J_D,J_T\) certification.

## 4. What next, and what cannot be claimed

**LW18 completed:** all 14/14 exact geometric, integration-by-parts, quadratic-action and negative-control checks; no numerical tuning or CLASS runs. The time-Noether operator of the **reduced** action is explicit; positive bath sources satisfy its first-order Ward component.

**OPEN:** full source-by-source Euler substitution of entire GE06+GE05 action into this Noether identity; full 3+1 nonanalytic Y, aether normalization and auxiliary multipliers; independent complete action-to-CLASS density/momentum dictionary and physical total \(J_D,J_T\); photons/baryons/neutrinos full \(A_{\rm eff}\), globally retarded \(G_{WE}\), physically admissible two-history Weyl difference, finite physical eta and DES/ACT lensing data fit. LW03 radial FAIL, LW05 full cosmic-shear LOS BLOCK, LW08 differential source UNRESOLVED and H4/Z21 uncertified remain unchanged.

**One next physical gate:** independently build the actual full **reduced** GE06+GE05 Euler rows (including GR lapse/shift, metric and aether) and test their contraction against the derived off-shell \(\mathscr I\), with the bath auxiliary equation and exact source normalizations. Only then try mapping the properly constrained reduced metric/energy source to original CLASS variables. Do **not** launch further CLASS resolution sweeps or claim observational memory.

## Optional lightweight local WSL selftest, no CLASS

Run a single original-source-locked symbolic check if needed:
~~~bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
python3 -u -m ge19.lw18_reduced_time_diffeo_noether_20261110 --self-test
python3 -u -m ge19.lw18_reduced_time_diffeo_noether_20261110
~~~

The original valid LW17 _r1.json is **not** required by this script because its bytes have not yet been received. WSL run of canonical LW18 source has not been performed here; independently executed algebra and archive evidence already exist.
