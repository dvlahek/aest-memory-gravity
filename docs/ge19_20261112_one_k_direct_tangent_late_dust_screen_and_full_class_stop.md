# GE19 — first directly integrated time-dependent eta-to-Weyl tangent, in a deliberately RESTRICTED late-time model

**12 November 2026 | no CLASS run, no DES data, no parameter or eta scan.**

**Classification:** `LATE_TIME_CONSTRAINTED_DUST_PROXY_DIRECT_TANGENT_CONVERGED / NOT_FULL_CLASS / NOT_PRIMORDIAL_MEMORY_GAIN / P0_PHYSICS_BLOCK`.

**What has ACTUALLY changed:** Unlike the previous frozen-coefficient positive-root calculations and symbolic Green-function identities, a time-dependent perturbation initial-value system was numerically integrated once at the **fixed** Exp parameters and **fixed** \(k=0.1\,h/{\rm Mpc}\), together with the exact **first derivative** of its Weyl response with respect to \(\eta\) at zero. The historical and action-quarter \(\eta=0.01\) CLASS transfers were **not** subtracted. A second ODE integrator independently reproduced the result, and an **independently propagated AeST fluid density** confirmed Hamiltonian constraint consistency.

**What this is NOT:** This is **not** a result for the full original Einstein–AeST–NL0B + CLASS photon–baryon–massive-neutrino hierarchy. The program intentionally omits radiation and substitutes pressureless dust for standard late-time species, treats the 0.06 eV massive-neutrino energy density as dust, omits shear, and **restarts all free/forced memory bath states at \(z=19\)** instead of propagating their primordial retarded history. These distinctions are substantive physical limitations, not implementation details. The numerical value must **not** be interpreted as a full cosmological memory sensitivity limit or compared directly with old jagged finite-\(\eta\) CLASS transfer differences.

## 1. Reproducible one-shot initial-value experiment

The [exact executable code](../ge19/physics_gate/late_dust_tangent_reproducer_20261112.py) and [verbatim local result](../results/ge19_late_dust_tangent_screen_20261112_standalone.json) were executed in an isolated Python analysis environment and then archived in GitHub with independently fetched, byte-matching Git blobs:
- Code SHA-256 `cc0b8c629773caf0dfe6f4a73c2a5a30bbd786b651ea56142d0d1a5d941b5cba`, Git blob `58acff8465d4f27af7d29b139ca94c17f4c106b3`.
- JSON SHA-256 `c2418c12564b9213696c1c252f07ac461f00414775c533dd50207d48a0c094df`, Git blob `177610f1f61c777813e6d1024393547dc952a7d2`.

The JSON explicitly records `source_locks_executed=false`: the offline numeric run used a byte-identical code copy and independently referenced original GitHub source, but the **new source-lock code has NOT yet been executed on the researcher's original WSL checkout**. Reproducibility requires that WSL source-lock check; a PASS there confirms the *restricted* model only, not full CLASS.

Fixed input:
- Original Exp action: \(Q_0=10^{-4}\), \(Z_0=10^{-17}\), \(K_2=9500\), \(I_0=0.000400912849822208377004114\), \(K_B=0.1\).
- Original NL0B `aest_memory_order=16` uses **15 active positive nodes**, exact source weights and frequencies, \(\omega_j=r_j H_0/\tau_{H0}\) with \(\tau_{H0}=1\), and source-normalized **quarter** coefficient \(-\eta Q B_\chi/(4K_B)\).
- One fixed \(k=0.1\,h/{\rm Mpc}\), \(h=0.6732117\), from \(a_i=0.05\), \(z_i=19\), to \(a_f=2/3\), \(z_f=0.5\).
- For an unambiguously linear density seed, \(\Phi_i=-10^{-7}\), and set \(\dot\Phi_i=0\); use Einstein momentum/Hamiltonian conditions to determine \(\theta_{\rm dust}\) and \(\delta_{\rm dust}\), enforcing \(\delta_A/(1+w_A)=\delta_{\rm dust}\) at \(a_i\). The seed \(\dot\Phi_i=0\) is a **matter-growth proxy**, **not** a derived primordial adiabatic growing eigenvector.
- \(\chi_i=E_i=q_{j,i}=\dot q_{j,i}=0\) at this **late-time starting epoch**, and all tangent states initially zero. A physical primordial history generally produces nonzero bath memory by \(a=0.05\); this model discards it deliberately.

We construct self-consistent flat **AeST + standard dust proxy + cosmological constant** background
\[
H(a)^2=\rho_A(a)+\rho_{{\rm std,dust}}(a)+\rho_\Lambda,
\quad \rho_A=\frac{QK_Q-K}{3},\qquad
\rho_{{\rm std,dust}}=
\frac{\omega_b+(0.06/93.14)}{2997.92458^2 a^3},
\]
with \(\rho_\Lambda\) calibrated to original \(H_0\). This is not the actual full CLASS background with relativistic neutrinos, photons and recombination.

At \(\eta=0\), the full internal **reduced** state \((\Phi,\delta_s,\theta_s,\varphi,\chi,E_A,\{q_j,p_j\}_{15})\) is evolved in \(\ln a\) with the exact source-normalized original action density/velocity and Einstein momentum dictionary (see the already WSL-confirmed [21/21 source](../results/ge19_constraint_projected_joint_operator_20261112_wsl.json)). Simultaneously the exact tangent \((\Phi_1,\delta_{s,1},\theta_{s,1},\varphi_1,\chi_1,E_{A,1})=\partial_\eta(\ldots)|_0\) obeys the same linear operator with the unique direct source \(-QB_{\chi,0}/(4K_B)\) in its \(E_A\) equation. The normalized baseline q/p states are retarded forced states **even though** they do not backreact at \(\eta=0\); this is the explicitly chosen continuous \(\eta\to0^+\) prescription.

A separate AeST density perturbation \(D_A\) and its tangent are **independently integrated through fluid continuity**, *not* reconstructed from Einstein Hamiltonian on every step. This permits the terminal Hamiltonian residual to test real propagation rather than a tautological substitution.

## 2. Actual fixed-model numerical result

At the only predeclared endpoint \(a_f=2/3\), in this restricted **no-shear** system \(W=\Phi\):

\[
\boxed{
W_0=-9.090234447697688\times10^{-8},\quad
\left.\partial_\eta W\right|_0
=-1.7703855116681344\times10^{-27},\quad
\frac{\left.\partial_\eta W\right|_0}{W_0}
=1.947568593367276\times10^{-20}.
}\tag{R}
\]

This relative *tangent* is per unit \(\eta\), not a finite-\(\eta\) difference and not observational SNR. It describes only memory newly generated after the artificial \(z=19\) reset.

Three **fixed-parameter, differing integration-accuracy choices**:

| Solver | Integrator accuracy | Direct \((\partial_\eta W)/W_0\) |
|---|---|---:|
| DOP853 | rtol \(3\times10^{-8}\), \(\Delta\ln a\le0.04\) | \(1.9475685933670253\times10^{-20}\) |
| DOP853 | rtol \(3\times10^{-10}\), \(\Delta\ln a\le0.01\) | \(1.947568593367276\times10^{-20}\) |
| **Radau (independent implicit algorithm)** | rtol \(5\times10^{-9}\), \(\Delta\ln a\le0.04\) | \(1.9475685933696202\times10^{-20}\) |

The ratio's relative difference is \(1.29\times10^{-13}\) across the two DOP853 tolerances and \(1.20\times10^{-12}\) against the independent Radau method. These differences are evidence of **numerical reproducibility of the selected reduced IVP**, *not* total physical error or primordial initial-condition uncertainty.

The independently evolved AeST density gives a normalized terminal Hamiltonian residual \(\lesssim1.1\times10^{-15}\) for the baseline and its tangent in these runs. Exact original standard full-species CLASS constraint propagation is **not** implied by this single background/proxy result.

## 3. Physical interpretation: why this result can coexist with a frozen positive root

The source-locked 17/17 theorem established a **local** positive eigenvalue condition for the externally prescribed-\(\Delta_A\), frozen-coefficient scalar+aether+positive-bath subsystem; the fixed Exp interval certificate later verified its threshold across \(10^{-8}\le a\le0.7\). None of this proves that an allowed **adiabatic, finite-time, constraint-projected perturbation** excites that root with appreciable projection into Weyl.

In this late-time dust proxy, *two* structurally small conversions are present under bounded finite-time gain and the chosen zero-modes-at-\(a_i\) prescription:
1. Standard-matter and metric forcing enters the \(\chi,E_A\) system initially through \(c_a^2\).
2. At \(\eta=0\), variation of \(E_A\) arises only from the retarded baseline \(B_{\chi,0}\). For this dust/no-shear constrained system, the \(E_A,\chi\) tangent reaches \(\Phi,\delta_s,\theta_s,\varphi\) through an additional coupling \(g=c_a^2 k^2/(a^2K_Q)\).

Thus the *formal weak-coupling* Weyl tangent has a **double suppression** by \(c_a^2\), potentially modified by large/evolving operator gains. The numerically tiny (R) is consistent with that causal chain; it does **not** establish that the true primordial GE19 bath, neutrino multipoles, photon source and CLASS approximation-switch system have the same response. In particular the **artificial late-time reset removes the entire earlier memory history**, the very physical effect under investigation. The experiment therefore cannot prove non-detectability or invalidate the original observational program.

The old \(z=0.5,\eta=0.01\) historical-half-vs-quarter CLASS native \(\Delta W\sim10^{-7}\)-baseline-normalized diagnostic belongs to a substantially different system with unquantified numerical error. Neither the magnitude nor disagreement between it and (R) is a valid estimate of true memory observability.

## 4. What is actually required for the next full physical response

**Stop launching further late-time proxy initial conditions.** We now have a verified tangent-integration *method*, independent Einstein stress constraint check, real bath source, and absolute solver control. The next justified implementation step is to incorporate this tangent into **the pinned full CLASS perturbations solver** (original `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`, original AeST v019/v019j and isolated quarter-candidate C source), with:
- all actual photons, baryons, UR and ncdm Boltzmann variables (and collision terms) in **both** baseline and tangent states;
- the same adaptive approximation switches, correct linear map for state-vector rebuilds and original primordial adiabatic/no-free-bath initial condition evolution from the true early universe;
- no free-eta tuning: the \(E_A\) tangent equation receives only \(-aQB_{\chi,0}/(4K_B)\) in conformal time; the normalized q/p \(\eta\to0^+\) continuation is frozen;
- one predeclared k from the earlier window, one redshift \(z=0.5\), and an independently controlled source-sampling/integration error, with original all-species physical action/CLASS acceptance still required before an observational claim.

The original CLASS's `perturbations_derivs`, `perturbations_vector_init`, `perturbations_einstein` and approximation transitions must all be handled; it is **not** enough to reconstruct a derivative from original one-redshift `mTk` tables. This part has **not yet been coded or run** and remains P0.

**Verdict:** `TIME_DEPENDENT_REDUCED_DIRECT_ETA_TANGENT_CONVERGED / ORIGINAL_FULL_CLASS_AND_DES_BLOCK`. No detection claim and no implied forecast at \(\eta=0.01\).
