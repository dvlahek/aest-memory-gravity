# GE19 — Joint photon–baryon–neutrino–AeST-like leading seed and rigorous frozen Exp dust bounds

**2026-11-21. Physics-first decision with no new CLASS runs.** This note proves (i) a coupled, tight-coupled-baryon extension of the radiation-era Einstein seed to first order in the *total* matter/radiation ratio, and (ii) strict analytical upper bounds on pressure and adiabatic sound speed of the exact pinned AeST Exp background. The algebra was independently checked with 27 exact SymPy residuals in an isolated local prototype. Source-locked researcher WSL confirmation of [the executable](../ge19/physics_gate/physical_baryon_Exp_leading_seed_20261121.py) remains pending.

**Classification:** \`LEADING_EINSTEIN_BOLTZMANN_BARYON_SEED_CONSISTENT_AND_FROZEN_EXP_EOS_UNIFORMLY_DUSTLIKE / ORIGINAL_FULL_FINITE_K_ACTION_WARD_PRIMORDIAL_MODE_OPEN / DES_NOT_DETECTED\`.

## 1. The full leading tight-coupled background has *two* independent small matter fractions

Use conformal time \`tau\`, \`k tau <<1\`, photons + tightly coupled baryons, relativistic collisionless neutrinos, and a separately conserved **pressureless AeST-like** effective species. Let \`R_nu=rho_nu/rho_r\` be a constant radiation fraction. Set
\`\`\`math
y_A=\rho_A/\rho_r,\quad y_b=\rho_b/\rho_r,\quad y_m=y_A+y_b\ll1,\quad \mathcal H=\frac{1+y_m/4}{\tau}+O(y_m^2),
\`\`\`
\`\`\`math
a^2\rho_r=\tau^{-2}(1-y_m/2)+O(y_m^2),\quad
a^2\rho_A=y_A/\tau^2+O(y_m^2),\quad
a^2\rho_b=y_b/\tau^2+O(y_m^2).
\`\`\`
The normalization absorbs the constant \`8 pi G/3\`. To this order \`y_A'=y_A/tau,\ y_b'=y_b/tau\`. The expanding background satisfies both the Friedmann and Raychaudhuri equations to O(y_A,y_b).

Write \`P=Psi0\`, \`Phi0=(1+2 R_nu/5)P\`, \`Phi=Phi0+Phi_1 y_m\`, \`Psi=P+Psi_1 y_m\`. Leading density and velocity laws are
\`\`\`math
\delta_\gamma=\delta_\nu=-2P+4\Phi_1 y_m,\quad
\delta_b=\delta_A=-\tfrac32P+3\Phi_1 y_m,
\`\`\`
\`\`\`math
\theta_{\gamma b}=\theta_\nu=k^2\tau\left[\tfrac12P+\tfrac12(\Phi_1+\Psi_1)y_m\right],
\quad
\theta_A=k^2\tau\left[\tfrac12P+\tfrac13(\Psi_1-\tfrac18P)y_m\right],
\`\`\`
\`\`\`math
\sigma_\nu=k^2\tau^2\left[\tfrac{P}{15}+
\tfrac{2(\Phi_1+\Psi_1)}{45}y_m\right].
\`\`\`
\`theta_b=theta_gamma\` is the *tight-coupling baryon* velocity, not the unforced CDM Euler velocity at O(y_b). For \`R_b=3 rho_b/(4 rho_gamma)=3y_b/[4(1-R_nu)]\`, its joint Euler equation is
\`\`\`math
\theta_{\gamma b}'+\frac{\mathcal H R_b}{1+R_b}\theta_{\gamma b}
=k^2\left(\frac{\delta_\gamma}{4(1+R_b)}+\Psi\right)+O(\mathrm{photon\ shear}).
\`\`\`
A non-obvious but exact first-order identity is
\`\`\`math
-\mathcal H R_b\,\theta_{\gamma b}
-\frac{k^2R_b}{4}\delta_\gamma
= -R_b k^2(P/2)+R_b k^2(P/2)+O(y_m^2,k^4\tau^2)
=0+O(y_m^2,k^4\tau^2).
\`\`\`
Thus baryon inertia *does not create a new independent* leading O(y_b) velocity coefficient: it cancels against pressure dilution. Neutrino shear is kept nonzero throughout; the photon shear is suppressed by tight coupling.

## 2. Exact universal leading gravitational backreaction

The joint Einstein Hamiltonian, momentum, traceless shear and spatial trace, together with the photon–baryon and neutrino Euler, continuity and quadrupole rows, uniquely yield
\`\`\`math
\boxed{\Phi_1=-\frac{15+16R_\nu}{16(15+2R_\nu)}P,\qquad
\Psi_1=\frac{40R_\nu-15}{16(15+2R_\nu)}P.}
\`\`\`
**Crucially the same coefficients multiply \`y_A\` and \`y_b\`.** They are not separately adjustable in a regular adiabatic leading mode. At \`R_nu=0\`, both metric potentials are \`P(1-y_m/16)\`; for general \`R_nu\`, the nonzero neutrino slip is retained. The result extends our successful 16-gate radiation+Aest-like model to include the leading baryon contribution in the *same* coupled Einstein–Boltzmann seed.

**Scope:** this is a controlled \`O(y_A,y_b)\` and leading \`k\tau\` result with a pressureless AeST-like sector and **massless relativistic neutrinos**. It is not the full finite-k physical Einstein–AeST–NL0B growing mode. Baryon-photon recombination and higher multipoles, massive-neutrino transitions, the AeST scalar/aether longitudinal state, and the retarded bath have **not** been solved here.

## 3. Rigorous, all-Z positive-branch bound for the pinned Exp benchmark

The original [CLASS Exp background](../v019/patch/source/aest_memory.c) and immutable [input](../v019/ini/aest_exp.ini) set \`Q0=1e-4\`, \`Z0=1e-17\`, \`K2=9500\` and \`K_B=0.1\`, with the positive \`K_Q=I0/a^3>0\` branch \`Z>0\`:
\`\`\`math
Q=Q_0+Z_0Z,\quad
K=2K_2 Z_0^2(e^{Z^2}-1),\quad
K_Q=4K_2Z_0Z e^{Z^2},\quad
K_{QQ}=4K_2e^{Z^2}(1+2Z^2).
\`\`\`
The exact equation of state and adiabatic sound speed are
\`\`\`math
w_A=\frac{K}{QK_Q-K}
=\frac{Z_0(1-e^{-Z^2})}{2Q_0Z+Z_0[2Z^2-1+e^{-Z^2}]},
\quad
c_a^2=\frac{K_Q}{QK_{QQ}}=
\frac{Z_0 Z}{(Q_0+Z_0Z)(1+2Z^2)}.
\`\`\`
Since \`0<1-e^{-Z^2}<min(Z^2,1)\` for \`Z>0\`, the denominator of w is larger than \`2Q0 Z\` and \`(1-e^{-Z²})/Z<min(Z,1/Z)<=1\`. Therefore **uniformly in Z, without choosing any epoch or numerical background trajectory**,
\`\`\`math
\boxed{0<w_A<\frac{Z_0}{2Q_0}=5\times10^{-14}.}
\`\`\`
Also \`Z/(1+2Z^2)<=1/(2 sqrt 2)\`, so
\`\`\`math
\boxed{0<c_a^2\leq\frac{Z_0}{2\sqrt2\,Q_0}
=3.5355339059\times10^{-14}.}
\`\`\`
The identity \`dw_A/d ln a=-3(1+w_A)(c_a²-w_A)\` is verified from the original Exp functions and \`K_Q\propto a^{-3}\`; it uses no constant-c approximation.

For \`a_f>=a_i>0\`,
\`\`\`math
0\leq\ln\frac{(\rho_A a^3)(a_i)}{(\rho_A a^3)(a_f)}
=3\int_{a_i}^{a_f} w_A(a)\,d\ln a
<3(5\times10^{-14})\ln(a_f/a_i).
\`\`\`
For the previously archived historic first recorded \`a_i=2.251984948309577e-6\` and \`a_f=1\`, the right-hand side is \`1.951e-12\`; the exact Exp background is hence uniformly near the dust density scaling **in the particular fixed benchmark**.

The inherited dust IC relative entropy from the earlier independently verified CLASS initial-condition audit is
\`\`\`math
S_{A\gamma}=\frac{3w_A}{4(1+w_A)}(4\mathcal H\alpha-d_\gamma^S).
\`\`\`
Thus its **coefficient**, not the absolute entire perturbation transfer, satisfies
\`\`\`math
\boxed{|S_{A\gamma}|<3.75\times10^{-14}\,
|4\mathcal H\alpha-d_\gamma^S|.}
\`\`\`
This resolves the **background size** of the pressureful-dust initialization mismatch that was previously recorded as conditional. It does **not** prove this small initial entropy cannot be dynamically amplified; nor does a bound on w,c bound \`c_a² k² S_A/(a²R_A)\` when state components or denominators behave nontrivially. The exact original-action finite-k seed remains needed.

## 4. Scientific decision

The leading photon–baryon–neutrino–AeST-like Einstein model is algebraically consistent at O(y_m); the pinned Exp background is rigorously extremely dustlike. Therefore **do not spend another campaign trying to resolve a w_A background correction already uniformly bounded below 5e-14**. In the wider theory, however, w/c are not necessarily this small and the proof is benchmark-specific.

The remaining research bottleneck is **not** the photon–baryon O(y_m) backreaction or scalar background pressure but the **full action-normalized, finite-k primordial scalar/aether state and Noether/Ward propagation**. The minimal necessary next physics problem is to select X(t_i)=chi_i/Q_i and E_A(t_i) under the real original scalar/aether plus Einstein constraints, with photon/neutrino shear and no independent free bath mode, then transport the bath with original \`-\eta Q B_\chi/(4K_B)\` force. The historical \`W1_delayed=-1.2006039315857457e-10\` at one k/z remains a conditional CLASS diagnostic, not certified physical memory or an observation.

**FULL_PHYSICS_GO = FALSE. DES_DETECTION = FALSE.**

## Reproducibility

[Single source-locked 27-gate symbolic derivation](../ge19/physics_gate/physical_baryon_Exp_leading_seed_20261121.py). No expensive numerical pipeline. No cosmological evidence is tuned or reprocessed.
