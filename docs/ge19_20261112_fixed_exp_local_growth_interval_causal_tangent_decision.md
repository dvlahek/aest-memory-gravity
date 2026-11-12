# GE19 — fixed Exp local-growth interval, not yet a physical Weyl-gain result

**12 November 2026. Physics-first.**
**Verdict: frozen reduced local-root sufficient condition PASS on 1e-8 <= a <= 0.7; full time-dependent Einstein–AeST–NL0B gain and DES remain BLOCK.**

No CLASS execution, DES fit, eta scan, source retuning or observation was performed. This is one analytic bound on the already WSL-verified (17/17) local *frozen-coefficient* scalar+aether+positive bath eigencondition. It is not yet the full Einstein-constrained all-species mode.

## Fixed action and conditional frozen root

The 17/17 result states that for Q>0, H>0, K_B>0, positive bath weights and frequencies, a **positive real root** of the isolated frozen longitudinal system exists if
\[
K_Q>C(H+Q-3Hc_a^2)+3K_BH^2c_a^2/Q,\qquad C=2-K_B.
\tag{1}
\]

The unchanged Exp benchmark uses K_B=0.1, Q_0=1e-4, Z_0=1e-17, K_2=9500, omega_cdm=0.1201075 and H_0=67.32117 km/s/Mpc. Its original analytic background is
\[
Q=Q_0+Z_0Z,\quad
K=2K_2Z_0^2(e^{Z^2}-1),\quad
K_Q=4K_2Z_0Ze^{Z^2}=I_0/a^3,\quad
c_a^2=\frac{Z_0Z}{Q(1+2Z^2)}.
\]
Original-density calibration at a=1 gives
\[
I_0=0.000400912849822208377,\quad Z(1)=4.392819968216,\quad Z(10^{-8})=8.595790151089.
\]

## Rigorous sufficient **whole-interval** certificate

Assume spatially flat FLRW with nonnegative background components whose equations of state remain -1 <= w_i <= 1/3. This includes ordinary radiation, baryons, nonrelativistic massive neutrinos, the fixed dustlike AeST background, and a nonnegative cosmological constant. The standard total Friedmann and continuity equations imply
\[
0<H(a)\le H_0/a^2\quad (0<a\le 1).
\]
The monotone Exp background for 1e-8 <= a <= 0.7 obeys the conservative bounds
\[
Q_0\le Q<Q_{\max}=Q_0+10^{-16},\qquad
0<c_a^2<c^2_{\max}=1.2\times 10^{-14}.
\]
Dropping the *negative* term -3CH c_a^2 in (1) gives a conservative sufficient condition. Multiply it by a^4 and define
\[
\boxed{f(a)=I_0a-CH_0a^2-CQ_{\max}a^4-
3K_BH_0^2c^2_{\max}/Q_0>0.}
\]
Because f''(a)=-2CH_0-12CQ_max a^2<0, f is concave and lies **above the chord between endpoints**. The independently high-precision evaluated margins are
\[
f(10^{-8})=4.009126640188956924\times10^{-12}>0,\qquad
f(0.7)=2.595533164771302608\times10^{-5}>0.
\]

**Hence the reduced frozen positive-real-root criterion is guaranteed for every 1e-8 <= a <= 0.7 under the stated background assumptions.** This is not just a handful of numerical snapshots, and it is not a physical full-cosmology instability theorem.

Using the conservatively enlarged H=H_0/a^2, the ratio K_Q to the *enlarged* threshold gives a lower bound on the ratio with actual H(a):

| a | K_Q / threshold at H_0/a^2 |
|---|---:|
| 1e-8 | 4,373,338.0 |
| 1e-4 | 9,396.48 |
| 0.001 | 939.65 |
| 0.01 | 93.9607 |
| 0.1 | 9.35483 |
| 0.3 | 3.01147 |
| 0.5 | 1.69104 |
| 0.7 | 1.10191 |

At the already frozen z=0.5 native CLASS transfer epoch, a=2/3, this conservative ratio is about 1.17660. At k=0.1 h/Mpc within the previously fixed k-window, the projected-operator coupling g=c_a^2 k^2/(a^2 K_Q) is ~8.13e-14 Mpc^-1, g/Q~8.13e-10. This does **not** determine the amplitude of the metric eigenvector or a true Weyl derivative.

## Physics interpretation and stop rule

- **Proved:** the pre-existing *reduced frozen* positive real-root criterion is actually satisfied across a broad interval by the original fixed Exp benchmark; the tiny initial drive c_a^2~1e-14 cannot **by itself** rule out a potential later gain channel.
- **Not proved:** whether the full photon–baryon–neutrino + Einstein-constrained time-dependent system retains and **excites** that root from primordial adiabatic / no-free-bath IC, or how much Weyl response results.
- **Already known:** the source-locked 21/21 Einstein stress projection gives R_A Delta_A+sum_s R_s Delta_s=-2k^2 Phi/(3a^2), so the artificial frozen external Delta_A=0 root is not automatically a physical mode.
- **Actual relevant observable bridge:** the reduced quarter-model derivative is
\[
\left.\partial_\eta W(t,k)\right|_0=
-\int_{t_i}^t ds\,L_W(t)U_0(t,s)e_E
\frac{Q(s)}{4K_B}B_{\chi,0}(s,k).
\]
The complete **time-dependent U_0(t,s)** and error control have not been computed. The old tiny jagged finite-eta CLASS array differences are **not** a measured value of this derivative or a DES detection.

## Provenance and one possible short WSL confirmation

- [Fixed-model source-locked high-precision certificate](../ge19/physics_gate/exp_local_growth_interval_certificate_20261112.py). Its mathematical inequality and fixed-parameter evaluations were independently reproduced in a standalone local analysis, **not yet source-locked on researcher WSL**.
- [21/21 researcher source-locked constraint equations](../results/ge19_constraint_projected_joint_operator_20261112_wsl.json).
- [17/17 researcher source-locked frozen bath dispersion](../results/ge19_coupled_frozen_gain_20261112_wsl.json).
- [Causal eta-to-Weyl tangent derivation](ge19_20261112_causal_eta_to_weyl_tangent_and_strict_dust_null.md).

To reproduce **only** the mathematical interval certificate (no CLASS), use:

    cd ~/aest-memory-gravity
    git pull --ff-only
    source .venv/bin/activate
    set -o pipefail
    python3 -u ge19/physics_gate/exp_local_growth_interval_certificate_20261112.py --out results/ge19_exp_local_growth_interval_20261112_wsl.json 2>&1 | tee results/ge19_exp_local_growth_interval_20261112_wsl.log
    echo "EXIT=$?"

Expect the exact source-lock PASS 3, interval-certificate PASS, and FULL_PHYSICS_GO False labels.

**Next justified computation if pursuing detectability:** one fixed initial-state, full-constraint-compatible **tangent or adjoint E-source-to-Weyl evolution**, with independent convergence verification. No additional broad eta amplitude scans or DES likelihood before genuine physical action/source certification.
