# GE19 — causal eta-to-Weyl response from the constraint-projected system; strict-dust null theorem

**12 November 2026. Physics-first continuation.**  
**Status:** `CAUSAL_LINEAR_ETA_TANGENT_IDENTITY_DERIVED / STRICT_DUST_NO_FREE_BATH_MEMORY_NULL / FULL_PHYSICAL_GAIN_AND_DES_BLOCK`.

This note makes the next theoretical connection **without another CLASS parameter sweep**. It is an exact variation-of-constants identity **for the frozen reduced linear CLASS/action dictionary with the quarter aether source**, conditional on the already documented operator, conservation, initial-state, and stress assumptions. It does not derive an unrestricted covariant Einstein–AeST–NL0B physical observable. No DES fit, physical signal-to-noise, finite-\(\eta\) convergence or production acceptance is claimed.

## 1. Starting point — source-locked joint stress/metric equations

Original researcher WSL results have now verified the [constraint-projected all-species source algebra](ge19_20261112_joint_all_species_constraint_projected_operator_decision.md) **21/21 PASS with 5/5 original source locks**, preserved as [JSON](../results/ge19_constraint_projected_joint_operator_20261112_wsl.json), Git blob `1cf3a81c61f252f96a2a1a45740bbd668af1b869`, and [log](../results/ge19_constraint_projected_joint_operator_20261112_wsl.log), blob `b8561488ee1524c45485faed3cc10fc0d9203931`.

Let \(X_\eta(t,k)\) be the perturbation state assembled from \(\Phi,\varphi,\chi,E_A\), the independently conserved or collision-coupled standard species' perturbations, plus the *normalized* finite positive NL0B oscillator coordinates \(q_j,\dot q_j\) (and the necessary photon/neutrino multipoles). The algebraically constrained Einstein lapse/momentum/shear relations determine \(\Psi,D_A\) from that state. Let the independent standard species source \(\Omega_s=\sum_s[D_s+3aHT_s/k^2]\) evolve according to the actual *summed* standard stress equations.

The original action-normalized **separate quarter candidate** inserts the bath parameter \(\eta\) directly only in the E equation:
\[
\dot E_A =\bigl[\dot E_A\bigr]_{\eta=0}
-\frac{\eta Q}{4K_B}B_\chi,\qquad
B_\chi=\sum_j\left(w_j\chi-\frac{a\omega_j\sqrt{w_j}}kq_j\right),
\tag{1}
\]
while each normalized oscillator obeys
\[
\ddot q_j+3H\dot q_j+\omega_j^2q_j=
\omega_j\sqrt{w_j}\,\frac{k\chi}{a}.
\tag{2}
\]
For the **fixed and relaxed zero-bath FLRW background** the memory has no direct first-order metric stress, and \(Q,H,K_B\), frequency nodes and weights are held fixed while differentiating with respect to \(\eta\). At \(\eta=0\), the normalized \(q_j\) still have the *chosen continuous retarded solution* from (2), although their original action loses a kinetic prefactor in the strict limit. This is an explicit limiting prescription, not uniqueness of all \(\eta=0\) auxiliary states.

On a fixed finite interval \([t_i,t_f]\), if the same initial cosmological state and the same **no-free-bath** \(q_j(t_i)=\dot q_j(t_i)=0\) are chosen for all \(\eta\), and the constrained linear IVP is well posed, write
\[
\dot X_\eta=(\mathsf A_0(t,k)+\eta\mathsf V(t,k))X_\eta,
\quad X_\eta(t_i)=X_i
\]
for the finite-dimensional actual linearized candidate system (with any finite Boltzmann hierarchy truncation held fixed). The only explicit \(\mathsf V X\) term is the E-row \(-Q B_\chi/(4K_B)\). For \(\eta=0\), define \(\mathsf U_0(t,s)\) as the fundamental matrix of \(\mathsf A_0\).

## 2. Exact first variation — no cancellation of two almost equal CLASS runs

Define the derivative at zero source strength:
\[
X_1=\left.\frac{\partial X_\eta}{\partial\eta}\right|_{\eta=0},
\qquad X_1(t_i)=0.
\]
Differentiating the full *fixed candidate* linear IVP with respect to \(\eta\) gives
\[
\boxed{
\dot X_1=\mathsf A_0 X_1
-\mathbf e_E\frac{Q(t)}{4K_B}\,B_{\chi,0}(t,k),
\qquad
X_1(t)=-
\int_{t_i}^t ds\,
\mathsf U_0(t,s)\mathbf e_E\,
\frac{Q(s)}{4K_B}\,B_{\chi,0}(s,k).
}\tag{3}
\]
Here \(B_{\chi,0}\) is evaluated from the **baseline \(\eta=0\) scalar trajectory** and its *separately retarded* normalized bath coordinates, with no fitting of free initial q/p modes.

Because original linear NL0B has no direct metric shear/stress on its relaxed FLRW background, the Weyl transfer \(W=(\Phi+\Psi)/2\) is a linear functional \(\mathsf L_W(t,k)X\) of the shared perturbation state with no extra explicit \(\eta\) derivative. With the original Newtonian Einstein shear sum,
\[
W(t,k)=\Phi(t,k)-\frac{9a^2}{4k^2}S_\sigma(t,k).
\]
Thus the reduced candidate's **exact linear-response bridge** is
\[
\boxed{
\left.\frac{\partial W(t,k)}{\partial\eta}\right|_0
=-\int_{t_i}^{t} ds\,
\mathsf L_W(t,k)\,\mathsf U_0(t,s)\mathbf e_E\,
\frac{Q(s)}{4K_B}\,B_{\chi,0}(s,k).
}\tag{4}
\]
The metric/hierarchy factor inside this integral is the *entire coupled, constraint-compatible response*, not the isolated \(2\times2\) frozen scalar+aether eigenvalue. For \(t\ge s\), \(\mathsf L_W(t)\mathsf U_0(t,s)\mathbf e_E\) is the actual Weyl readout of an E-source impulse **in the chosen truncated/normalized reduced model**. Positivity of \(\mathsf U_0\) or a nonzero sign for the integral is **not** assumed.

The baseline bath force itself has the exact causal representation
\[
\boxed{
B_{\chi,0}(s,k)
=W_b\chi_0(s,k)
-a(s)\sum_jw_j\omega_j^2
\int_{t_i}^{s}du\,G_{R,j}(s,u)\frac{\chi_0(u,k)}{a(u)},
\quad W_b=\sum_jw_j.
}\tag{5}
\]
Equations (4) and (5) are the precise two-stage Volterra/Green chain **baseline scalar \(\chi_0\) → positive retarded bath → E-source → entire Einstein+species evolution → Weyl**, without subtraction of two nearly equal finite-\(\eta\) numerical runs.

## 3. Strict-dust / no-free-mode **null theorem**, even with arbitrary standard matter forcing

The constraint-projected original AeST scalar equation already source-locked by researcher 21/21 is
\[
\dot\chi=QE_A-3Hc_a^2\chi+
g(K_BE_A+C\chi-2\Phi)-\frac{3c_a^2}{K_Q}\Omega_s,
\qquad
g=\frac{c_a^2k^2}{a^2K_Q}.
\tag{6}
\]
For **strict** \(c_a^2=0\) holding the other finite background quantities fixed so \(g=0\), and original scalar/aether initial states \(\chi(t_i)=E_A(t_i)=0\), this becomes \(\dot\chi=QE_A\). The quarter/zero-memory E equation at \(\chi=E_A=B_\chi=0\) gives \(\dot E_A=0\). Each normalized oscillator with zero \(q_j,\dot q_j\) stays zero because its forcing is proportional to \(\chi\). By uniqueness of the reduced IVP:
\[
\boxed{
c_a^2\equiv0,\quad
(\chi,E_A,q_j,\dot q_j)_{t_i}=0
\ \Longrightarrow\
\chi=E_A=q_j=\dot q_j=B_\chi=0
\ \Longrightarrow\
\partial_\eta W\big|_0=0.
}\tag{7}
\]
This statement holds for any permitted \(\Omega_s(t)\) and \(\Phi(t)\) **inside the specified reduced constrained equations**, because their coupling to the \(\chi,E_A\) subsystem enters with \(c_a^2\). It does *not* claim the original full covariant theory has exactly zero matter-memory response in every nonlinear mode, and does not imply that small but finite \(c_a^2\) has a proportionally small final Weyl signal without a finite operator gain bound.

At the actual fixed Exp \(c_a^2\sim10^{-14}\), the initially vanishing scalar/aether modes receive a force
\[
\boxed{
\dot\chi_i=
-\frac{c_{a,i}^2}{K_{Q,i}}
\left(\frac{2k^2}{a_i^2}\Phi_i+3\Omega_{s,i}\right)
=Q_i c_{a,i}^2\Delta_{A,i}.
}\tag{8}
\]
The equality on the right uses *the Einstein constraint*, not an arbitrary external density drive. If the complete time-dependent \(\mathsf U_0\) has a finite controllable gain, the response will inherit small \(c_a^2\); if there is an allowed amplified mode or stiff ill-conditioning, that gain must be established **independently**, without interpreting the earlier \(10^{-6}\) jagged CLASS subtraction as a detection.

## 4. What an actually decisive numerical check would look like later

**Not run now.** Fix the original-action quarter-source, the primordial adiabatic/no-free-bath initial state, all original Boltzmann species and one already predetermined \(k,z\) window. Compute the *single* \(\eta=0\) baseline with normalized auxiliary q chosen by its retarded Green solution, then integrate **the one linear tangent equation (3)** or an adjoint source–Weyl Green function with an independent step/precision convergence check. Do **not** estimate the tangent from unqualified \(\eta=0.01\) historical-minus-quarter finite differences or from a native \(d_mW\) transfer product.

Only after this **time-dependent physical tangent and its error are controlled** can the model produce \(P_{gW}\) with a physically defined galaxy tracer/bias, line-of-sight projection and nuisance covariance. The available prior CLASS outputs do **not** contain the necessary full \(\chi_0\), retarded auxiliary history and \(\mathsf U_0\) information to evaluate (4) just from one native \(d_b,W\) table.

## 5. Decision

The first-order *causal source-to-Weyl functional* is now mathematically explicit for the reduced, constraint-projected candidate, and the strict-dust/no-free-mode memory-null limit is proved from that system. Both facts substantially narrow the remaining uncertainty.

**Still BLOCK:** full independent unrestricted action-to-CLASS equivalence, physical primordial mode selection, time-dependent full hierarchy Green gain, numerical conditioning/convergence, galaxy–Weyl survey transfer and observed DES significance. No observed memory detection is claimed. **No additional unconstrained numerical or symbolic micro-campaign is justified.**
