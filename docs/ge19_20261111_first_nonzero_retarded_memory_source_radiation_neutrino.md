# GE19 — first nonzero *retarded* gravitational-memory source from an adiabatic radiation universe

**11 November 2026. One physics-first result, no new CLASS run or DES fit.**  
**Scientific classification:** `REDUCED_LOCAL_MEMORY_ONSET_EXACT / RADIATION_NEUTRINO_DELTA_A_X2_EXACT / GLOBAL_PHYSICS_GO_BLOCK`.

**What was actually completed:** The action/CLASS scalar dictionary has been reduced to an exact closed forced two-field subsystem for \(\chi,E_A\), coupled to the original NL0B oscillators and a physical AeST comoving density. A separately solved radiation+free-streaming-neutrino Einstein–Boltzmann expansion supplies the *first nonzero* \((k\tau)^2\) coefficient of that density, in the dustlike AeST/test-matter limit. Two original source-bound scripts were symbolically tested **standalone** (14/14 and 9/9); the original researcher WSL source-lock execution is **still unperformed**. The exact tested script bytes and JSON outputs are now archived on GitHub. No full finite-k/finite-time solution, \(\eta\)-response transfer, DES statistic or observational detection has been computed.

## 1. Exact reduced nonlinear-in-time, linear-in-perturbations source identity

Start with the **original** AeST background and CLASS-form perturbation equations already derived independently and WSL source-locked in the older 15/15 matrix:
\[
c_a^2=\frac{K_Q}{QK_{QQ}},\quad
\dot Q=-3Hc_a^2Q,\quad
\rho_A+p_A=R_A,\quad C=2-K_B,
\]
\[
\chi=Q\left(\frac{a\theta_A}{k^2}+\alpha_A\right),\qquad
\dot\alpha_A=E_A-\Psi,
\]
\[
\theta_A'=(3c_a^2-1)\mathcal H\theta_A+
k^2\!\left[\frac{\Pi_A}{1+w_A}+\Psi\right],\qquad
\frac{\Pi_A}{1+w_A}=c_a^2\left[
\frac{\delta_A}{1+w_A}+\frac{k^2(K_BE_A+C\chi)}{3a^2R_A}\right].
\]
Primes mean conformal time and dots mean proper time.

Define an **AeST enthalpy-normalized comoving density** from its *own* actual effective stress:
\[
\boxed{\Delta_A\equiv\frac{\delta_A}{1+w_A}
+\frac{3\mathcal H}{k^2}\theta_A .}\tag{1}
\]
**Do not confuse this with CLASS's pressureless-only default `d_m` transfer.** This expression is gauge invariant at linear order for a separately conserved effective AeST fluid using the same gauge/velocity conventions.

Direct differentiation gives the exact identity in the fixed **reduced action/CLASS state dictionary**:
\[
\boxed{\dot\chi=QE_A+
Qc_a^2\left[\Delta_A-\frac{3H}{Q}\chi+
\frac{k^2(K_BE_A+C\chi)}{3a^2R_A}\right].}\tag{2}
\]
The original aether action with arbitrary source coefficient \(\gamma\) yields
\[
\boxed{K_B(\dot E_A+HE_A)=K_Q\chi-
C\left[\dot\chi-QE_A+(H+Q)\chi\right]
-\eta\gamma QB_\chi,}\tag{3}
\]
\[
B_\chi=\sum_j\left[w_j\chi-\frac{a\omega_j\sqrt{w_j}}{k}q_j\right],\quad
q'_j=p_j,\quad
p'_j=-2\mathcal H p_j-a^2\omega_j^2q_j+
ak\omega_j\sqrt{w_j}\,\chi.\tag{4}
\]
The **fixed reduced original action** selects \(\gamma=1/4\) under its LW33 scalar Euler/density dictionary assumptions. The historical frozen CLASS source is \(\gamma=1/2\), and is not silently modified.

Equations (2)–(4) isolate one necessary physical driving field \(\Delta_A\). They do **not** by themselves determine it, because the complete species+metric evolution is coupled.

**Strict dust invariant subspace:** for \(c_a^2=0\) and initial \(\chi=E_A=q_j=p_j=0\), the identical zero scalar-memory trajectory remains a solution for any external gravitational \(\Delta_A\). This is an invariant sector of the **reduced linear scalar system**, not a general theorem that the full covariant AeST+NL0B model has no memory.

## 2. Exact local *first nonzero* retarded onset (no large-time expansion assumed)

At a finite starting time \(\tau_i>0\) select the **no-free-bath-mode** initial state \(\chi_i=E_{A,i}=q_{j,i}=p_{j,i}=0\) and hold the same cosmological initial data across both source normalizations. From (2)–(3),
\[
\boxed{
\dot\chi_i=Q_i c_{a,i}^2\Delta_{A,i},\qquad
\dot E_{A,i}=-\frac{(2-K_B)Q_i c_{a,i}^2}{K_B}\Delta_{A,i}.
}\tag{5}
\]
The first conformal derivative of the full force and leading induced auxiliary mode are
\[
\boxed{
B'_{\chi,i} = a_iQ_ic_{a,i}^2\Delta_{A,i}\sum_jw_j,\qquad
q_j(\tau_i+h)=\frac{a_i^2k\omega_j\sqrt{w_j}Q_ic_{a,i}^2\Delta_{A,i}}6 h^3+O(h^4).
}\tag{6}
\]
The direct \(\eta\)-dependent \(E_A'\) forcing vanishes at \(\tau_i\), but has a nonzero first derivative. In the **separate quarter candidate**, with \(h=\tau-\tau_i\),
\[
\boxed{
E_{\eta}-E_{\eta=0}=
-\frac{\eta\,a_i^2Q_i^2c_{a,i}^2\Delta_{A,i}}{8K_B}
\left(\sum_jw_j\right)h^2+O(h^3),
}\tag{7}
\]
at the same initial state and fixed background. The **half-minus-quarter difference** has the same first \(h^2\) coefficient, because \(\gamma_{\rm half}-\gamma_{\rm quarter}=1/4\). These are Taylor coefficients of **one local solution**; neither the full later-time propagation nor a gauge-invariant observed signal is inferred. At \(h\) comparable to any bath period, Hubble time or stiff aether scale, the expansion is **not** valid and cannot be used as a transfer prediction.

## 3. Full radiation+neutrino \(\mathcal O((k\tau)^2)\) drive coefficient, neglecting matter backreaction

Now determine the previously unspecified \(\Delta_{A,i}\) to first nonzero superhorizon order, in a **controlled additional approximation**: \(x=k\tau\ll1\), flat radiation domination with \(\mathcal H=1/\tau\), a tightly coupled photon fluid, free-streaming neutrino fraction \(R_\nu\), zero baryon/AeST contribution to the *leading* radiation Einstein potentials, and treat AeST as a conserved **test dustlike component** to \(O(c_a^0)\) when computing its \(\Delta_A\). The memory-force formula retains the explicit small \(c_a^2\).

Set
\[
\Phi=\Phi_0+\Phi_2x^2+O(x^4),\quad
\Psi=\Psi_0+\Psi_2x^2+O(x^4),\quad
\Phi_0=(1+2R_\nu/5)\Psi_0.
\]
For radiation, the leading photon/neutrino densities are \(-2\Psi_0\), their velocities are \(k[\Psi_0x/2+O(x^3)]\), neutrino shear is \(\sigma_\nu=\Psi_0x^2/15+\sigma_{\nu4}x^4\), and its octupole begins at \(F_{\nu3}=2\Psi_0x^3/105\).

Substituting into *six* independent nontrivial equations (photon Euler, neutrino Euler, neutrino quadrupole, Einstein momentum, shear and Hamiltonian) gives the unique coefficients
\[
\boxed{
\frac{\Phi_2}{\Psi_0}=
-\frac{56R_\nu^2+580R_\nu+525}{630(2R_\nu+25)},\quad
\frac{\Psi_2}{\Psi_0}=
\frac{56R_\nu^2+10R_\nu-525}{630(2R_\nu+25)}.}\tag{8}
\]
For a pressureless test AeST component, its Euler/continuity equations imply
\[
\delta_A=-\frac32\Psi_0+
\left(3\Phi_2-\frac14\Psi_0\right)x^2+O(x^4),\quad
\frac{\theta_A}{k}=\frac12\Psi_0x+\frac14\Psi_2x^3+O(x^5).
\]
Therefore the *first nonzero* enthalpy-comoving density remarkably simplifies to
\[
\boxed{
\Delta_A=-\frac{15+4R_\nu}{40}\Psi_0(k\tau)^2
+O((k\tau)^4,\rho_{\rm matter}/\rho_{\rm rad},c_a^2).}\tag{9}
\]
With \(R_\nu=0\), coefficient is \(-3/8\); with \(R_\nu=1\), \(-19/40\). Thus at the initially unexcited bath one obtains
\[
\boxed{\dot\chi_i=
-\frac{15+4R_\nu}{40}\,Q_ic_{a,i}^2\Psi_0(k\tau_i)^2+
\text{higher-order terms}.}\tag{10}
\]
**Scope condition:** this is a **double asymptotic expansion** around radiation domination and the frozen Exp pressureless effective-fluid limit. It does **not** solve the \(\mathcal O(\rho_A/\rho_r)\) backreaction, the full next-order time evolution of \(\chi,E_A\) or the projected Weyl spectrum. The coefficient is sign-relative to \(\Psi_0\), not a predicted sign of an angular lensing correlation.

The frozen Exp benchmark has \(c_a^2\sim10^{-14}\) at early times. This suppresses the **local initial source** but provides no uniform later-time amplitude bound: the aether equations also involve \(K_Q\), \(H\), retarded oscillators and evolving matter/radiation fractions. A separate stability/Green-response estimate is required before claiming memory is physically undetectable (or detectable).

## 4. Reproducibility, source identity, stop decision

- [First-source exact reduced operator and retarded Taylor gate](../ge19/physics_gate/first_retarded_memory_onset_20261111.py): 14/14 symbolic PASS, **byte-identical** standalone tested code (Git blob `9c41778234a734643d2527ff539d5fdb255bd66a`).
- [Frozen standalone 14/14 JSON](../results/ge19_first_retarded_memory_onset_20261111_standalone.json), exact tested Git blob `49022a1c2fbfdeef6a653e428e415936bb3666b4`.
- [Radiation + neutrino next-order solver](../ge19/physics_gate/radiation_neutrino_delta_source_20261111.py): nine symbolic summary gates, including exact residual zero of the six solved coupled equations; byte-identical tested Git blob `19e9efd5713dc8df3057c4b33f8c4a2921a96687`.
- [Frozen standalone radiation JSON](../results/ge19_radiation_neutrino_delta_source_20261111_standalone.json), exact tested Git blob `4dbae3bd47656c21a87d1b0d380a0f8d9dae469e`.

Each standalone JSON truthfully has `source_locks_executed=false`: the analysis was executed on an isolated copy. The original source and its Git blobs were independently inspected in the repository; **the WSL source-locked reproductions remain pending**. None of these gates claims full physical equivalence.

**Next action, one bounded physical decision rather than another LW sweep:** evaluate whether the exact *coupled* retarded \(\chi,E_A,q_j,p_j\) response can amplify this source given frozen \(K_Q/H\), \(\omega_j\), and the adiabatic initial data, while retaining Einstein Hamiltonian/momentum constraints. A positive physical response must then pass a single numerical-error qualification before any DES forecast. If such amplification is absent, record an early-memory suppression/null prediction instead of trying to tune \(\eta\) or other parameters from survey residuals. **Production PHYSICS_GO and DES detection remain BLOCK.**
