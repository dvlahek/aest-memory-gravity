# GE19 — quantitative DES Y3 shape threshold and exact regular retarded-bath observable kernel

**Date:** 2026-11-22. **Decision:** the first **real-covariance** DES Y3 MagLim4 × Source4/Source3 Asimov control is closed and scientifically informative. No observed residuals, no physical Weyl prediction, no DES detection. This note provides (i) a numerical **noise-normalized target** derived only from the published covariance and a previously saved unfitted GR template and (ii) an exact transformation of the original NL0B bath that eliminates the explicit \`1/k\` from the causal source, simplifying a future full physical transfer calculation without changing its physics.

## 1. Actual DES covariance provides an absolute numerical shape target

Source: archived researcher WSL [DES Y3 Asimov r3 JSON](../results/ge19_des_y3_asimov_20261122_r3.json) and [runner log](../results/ge19_des_y3_asimov_20261122_r3.log), original byte-exact Git blobs \`b937b93d760b84055b5a65ee411e52627bff3045\` and \`d43519641391d53d431bc6ccad3827df12f9b71a\`. Frozen OBS06 original reference NPZ SHA-256 \`564542d47fa95d5b5fb3c5b0c8bb4eae1ecbc93f450bf993ea0bbb98310546e3\`; it contains the **published full covariance** and **unfitted fixed-example GR** \`gamma_t\`, not the official DES cosmological best-fit. Selected MagLim lens bin 4 × source bin 4 (13 rows) plus same lens × source bin 3 (13 rows); C is the original 26×26 principal covariance submatrix. Original r3 calculation did not materialize the observed \`gamma_t\` or signed residual arrays.

The intentionally nonphysical r3 control set \`t_flat=epsilon*mu_GR\`, where the numerically inherited one-point historical Weyl ratio was \`epsilon=-1.712922233834667e-9\` per eta, and computed \`F_raw=2.7245822792610327e-15\` from the actual reference C. **Because epsilon cancels in the following inversion, its lack of physical validity does not contaminate the norm of the frozen GR template**:

\`\`\`math
\boxed{
N_{\rm GR}:=\|\mu_{\rm GR}\|_{C^{-1}}
=\frac{\sqrt{F_{\rm raw}}}{|\epsilon|}
=30.47279690877705 .
}\tag{1}
\`\`\`

For an arbitrary **future physically certified** predicted change \`\Delta\mu_{\rm mem}\`, let \`L L^T=C\`, \`v=L^{-1}\Delta\mu_{\rm mem}\` and \`A=L^{-1}D\`, with \`D\` the nuisance template columns. The unregularized orthogonal projection onto the nuisance span is \`\Pi_A=A(A^TA)^+A^T\` (SVD in implementation), and define the noise-weighted *residual shape fraction*

\`\`\`math
\boxed{
r_\perp(\eta)=
\frac{\|(I-\Pi_A)L^{-1}\Delta\mu_{\rm mem}(\eta)\|_2}
{\|L^{-1}\mu_{\rm GR}\|_2}.
}\tag{2}
\`\`\`

The expected fixed-Gaussian-covariance, fixed-template Asimov test distance is \`\sqrt{\Delta\chi^2_{\rm Asimov}}=N_{\rm GR}r_\perp\`. Thus within **this same 26-point data vector and only the two freely profiled source-amplitude nuisances** the quantitative required normalized residual is:

| Asimov \`sqrt(Delta chi²)\` | Required \`r_perp\` |
|---|---:|
| 1 | \`0.03281615412571371\` = **3.2816%** |
| 3 | \`0.09844846237714114\` = **9.8448%** |
| 5 | \`0.16408077062856857\` = **16.4081%** |

These are **not** per-angular-bin percent shear changes, are **not** a confidence-calibrated discovery p-value, and are **not** a physical \`eta\` upper bound. The result is an exact algebraic normalization benchmark for that frozen C and GR model: a physical memory template would have to leave this much of its **noise-weighted orthogonal shape** to reach the stated *nominal* Asimov distance in this restricted comparison. A full physically constrained nuisance model, realistic alternative cosmologies, priors, numerical errors and nonlinear scale cuts generally reduce information; additional probes, lens bins or priors could improve it. In particular, this is not a universal lower bound for the entire DES Y3 data set.

The flat-control \`t_flat\` is exactly in \`col(D)\`, hence its \`r_perp=0\` independent of the artificial epsilon, in agreement with r3's \`F_profiled=3.748285e-46\` **roundoff**. Never substitute \`epsilon\` as the whole DES physical response, and never infer that actual memory is below the threshold from a single \`k,z\` Weyl value.

## 2. Eliminate the apparent singular \`1/k\` in the original retarded source **exactly**

From the frozen original reduced quadratic NL0B action and its Euler equations, for each active oscillator \`w_j>0,omega_j>0\` and comoving Fourier \`k>0\` in cosmic proper time \`t\`:

\`\`\`math
\ddot q_j+3H\dot q_j+\omega_j^2q_j
=\omega_j\sqrt{w_j}\frac{k\chi}{a},
\quad
B_\chi=W_b\chi-\frac{a}{k}\sum_j\omega_j\sqrt{w_j}q_j,
\quad W_b=\sum_j w_j.
\`\`\`

Define the **regular, directly source-normalized causal bath coordinate**
\`\`\`math
\boxed{r_j:=\frac{a\,\omega_j\sqrt{w_j}}{k}\,q_j .}\tag{3}
\`\`\`
A direct differentiation, using \`H=dot a/a\` with no frozen-coefficient approximation, gives

\`\`\`math
\boxed{
\ddot r_j+H\dot r_j+
\bigl(\omega_j^2-2H^2-\dot H\bigr)r_j
=\omega_j^2 w_j\chi,
\qquad
B_\chi=W_b\chi-\sum_j r_j.
}\tag{4}
\`\`\`

**Exact identity, not a new model.** The \`1/k\` and rescaling-dependent factors disappear from the memory forcing; the bath is a causal time-history filter of the gauge-invariant relative strain \`chi\`. This does **not** make the full observable independent of k: \`chi(k,t)\` and its matter–Weyl propagation, source/observer projection, primordial initial-state selection and any complete physical stress can depend on k. For a conditional analytic branch \`chi=O(k²)\`, the r_j and B_chi are also \`O(k²)\`, consistent with the source-locked k² hierarchy. There is no fake extra \`1/k\` enhancement or loss of two k powers.

One useful original-equation simplification occurs **exactly for a radiation-dominated power-law FLRW reference** \`a(t)=A t^(1/2)\`:

\`\`\`math
H=\frac{1}{2t},\quad \dot H=-\frac{1}{2t²}
\quad\Longrightarrow\quad
\boxed{\ddot r_j+\frac{1}{2t}\dot r_j+\omega_j^2r_j
=\omega_j^2w_j\chi.}\tag{5}
\`\`\`
The geometric shift \`-2H²-dot H\` cancels identically. The **true** Exp early background, with time-dependent AeST and radiation feedback, is not *exactly* this pure radiation power law; Eq. (4) remains the exact appropriate operator.

For a static Minkowski reference \`a=1,H=0\` and a retarded steady harmonic input \`chi(t)=chi_omega e^{-i Omega t}\` (with the standard retarded pole prescription), the causal bath susceptibility is

\`\`\`math
\boxed{
\frac{B_\chi(\Omega)}{\chi(\Omega)}
=-\Omega² \sum_j \frac{w_j}{\omega_j²-(\Omega+i0)^2}.
}\tag{6}
\`\`\`
The relaxed zero-frequency response is exactly zero; at low frequencies away from the oscillator poles \`B_chi\approx(\sum_j w_j/\omega_j²)\ddot\chi\`. This illustrates a **time-frequency filter rather than uniform rescaling**. It does **not** assert finite-bath damping or guarantee an observable k/ell-dependent signal. Initial-time transients can persist, and the true cosmological expanding background requires Eq. (4) and correct retarded data from the physical past.

I independently verified Eq. (4) symbolically: substitution \`q_j=(k/(a omega_j sqrt(w_j))) r_j\` into the original q equation leaves **identically zero residual**, with arbitrary differentiable a(t). This is not a canonical full covariant/Einstein equivalence or a newly discovered physical mode.

## 3. What is the single remaining actual detector-facing calculation?

The restricted original action establishes a genuine history-sensitive response **at the level of the internal AeST strain and auxiliary source**. It does not supply the complete physical transfer. The required quantity is not \`W1_delayed(k0,z0)\`; it is a signed, uncertainty-controlled **matter–Weyl cross-power derivative** across the actual lens-window support:

\`\`\`math
\left.\frac{\partial P_{\delta W}(k,z)}{\partial\eta}\right|_{0^+,\rm delayed}
=P_{\mathcal R}(k)
\bigl[T_{\delta,1}^{\rm delayed}(k,z) T_{W,0}(k,z)
+T_{\delta,0}(k,z)T_{W,1}^{\rm delayed}(k,z)\bigr]
\`\`\`

for a common real primordial seed, with any necessary complex conjugation for general transfer conventions. It must arise from a **full constraint-preserving action-consistent** Einstein–AeST–NL0B + photon/baryon/neutrino solution with physically selected finite-k adiabatic initial state and retarded bath. The old historical CLASS \`gamma=1/2\` source is **not** the original \`gamma=1/4\` model. Retarded/instant comparator and any initial-state \`eta\` tangent must be identified without assuming the arbitrary finite checkpoint q/p reset. The observable is then a real, signed \`d gamma_t/d eta\` after the calibrated DES source/lens kernels, angular windows and nuisance/instant-only rivals, and is inserted into Eq. (2).

**Decision:** the validated **observer infrastructure** and quantitative noise-weighted target now exist. The physical \`T_{\delta,1},T_{W,1}\` do not. Stop testing manufactured flat responses; next physics work should assemble the *actual* action/constraint-correct transfer and evaluate \`r_\perp\` once, not invent numerical signals. No DES residuals unblinded, no detection, no physical sensitivity bound from the 1-point historical W1.

**Current status: DES_OBSERVER_COVARIANCE_GO / ABSOLUTE_SHAPE_NORM_TARGET_ESTABLISHED / REDUCED_BATH_REGULAR_CAUSAL_OPERATOR_ESTABLISHED / PHYSICAL_TRANSFER_BLOCKED / FULL_PHYSICS_GO=FALSE / DES_DETECTION=FALSE.**
