# GE19 — retarded NL0B bath: exact source convolution, positive oscillator energy, and the amplification decision

**12 November 2026. Physics-first closeout of two canonical original WSL results.**  
**Status:** `GE19_FIRST_MEMORY_SOURCE_WSL_PASS / BATH_PASSIVE_AS_FORCED_OSCILLATOR / FULL_COUPLED_GAIN_UNBOUNDED_BY_EXISTING_EVIDENCE / PHYSICS_GO_BLOCK`.

This note is **not** a new CLASS run, DES fit, multi-eta scan, or new validation of the full Einstein–AeST+NL0B system. It analyzes what can be concluded from the archived source-locked local tests **and** the original per-mode positive quadratic bath action in an expanding FLRW background.

## 1. Canonical reproducibility now confirmed on researcher WSL

The actual four uploaded WSL files have been archived **byte-for-byte** in the original `physics-first-gravitational-elasticity` branch. Git blob IDs checked after archive:

| Original WSL file | SHA-256 of uploaded bytes | Git blob | Result |
|---|---|---|---|
| [First source JSON](../results/ge19_first_retarded_memory_onset_20261111_wsl.json) | `eb94017e24e4037dacd5670860ef79b2604d3c09574f2d4cf790f88629b37849` | `22a502a964e52850f95cae67435894b376531167` | 14/14 exact, 4/4 source locks |
| [First source log](../results/ge19_first_retarded_memory_onset_20261111_wsl.log) | `a8751805a5569f788b19ae3e72c82eff9ee5c797ad36cfd88566aece14de30da` | `92e8f6ce20c023e533640776b0a709b0cc858562` | Reporter says full physics GO false |
| [Radiation source JSON](../results/ge19_radiation_neutrino_delta_source_20261111_wsl.json) | `6daab23c840d4a5c9531d762e4ab43ea0588afa11dbbbbdfbc80279f261fc188` | `17211e344c8eacdd1ae3d3d8bd99ecc0e21cf294` | 9/9 exact, 3/3 source locks |
| [Radiation source log](../results/ge19_radiation_neutrino_delta_source_20261111_wsl.log) | `40f57c84ad7c4e931934e09ea55d7247e94b0fb21d43e8222c648bb82f4a96fa` | `842314147f933bd720a0f72e25863767f4186326` | Reporter says full physics GO false |

The WSL results and prior standalone JSON reports match on **all fields other than provenance** (`source_locks_executed` and `source_blobs`); expected differences because only WSL reverified the original source tree. An older duplicate [baryon-Weyl JSON](../results/ge19_existing_baryon_weyl_20261111.json) and log are byte-identical reuploads of existing archived evidence; **not new observational information**.

## 2. Exact independent energy argument for the frozen bath — no new numerical integrator

For each positive-weight mode (\(\omega_j>0,w_j\ge0\)) in the source-selected quadratic longitudinal NL0B action at \(\eta>0\),
\[
\ddot q_j+3H\dot q_j+\omega_j^2q_j
=F_j(t),\qquad
F_j(t)=\omega_j\sqrt{w_j}\frac{k\chi(t)}{a(t)}.
\tag{1}
\]
The original \(\eta\)-dependent coupling to the aether uses
\[
B_\chi(t)=\sum_j\left[w_j\chi(t)-\frac{a(t)\omega_j\sqrt{w_j}}{k}q_j(t)\right].
\tag{2}
\]

For a chosen no-free-bath-mode state \(q_j(t_i)=\dot q_j(t_i)=0\), let \(G_{R,j}(t,s)\) be the retarded Green function of \(D_j=\partial_t^2+3H\partial_t+\omega_j^2\) normalized to a unit jump in \(\partial_tG\) across \(t=s\). Then
\[
q_j(t)=\omega_j\sqrt{w_j}k
\int_{t_i}^t G_{R,j}(t,s)\frac{\chi(s)}{a(s)}ds
\]
and hence the **exact causal memory functional** is
\[
\boxed{
B_\chi(t)=W_b\,\chi(t)
-a(t)\sum_j w_j\omega_j^2
\int_{t_i}^t G_{R,j}(t,s)\frac{\chi(s)}{a(s)}ds,
\qquad W_b=\sum_j w_j.
}\tag{3}
\]
This is a **retarded response**, not a new free parameter, and the kernel \(G_R\) is *not* claimed pointwise nonnegative (oscillatory solutions can change sign).

Now define the **nonnegative oscillator energy**
\[
\mathcal E_j(t)=\tfrac12(\dot q_j^2+\omega_j^2 q_j^2).
\]
On an expanding background \(H(t)\ge0\), multiplication of (1) by \(\dot q_j\) gives **exactly**
\[
\boxed{
\dot{\mathcal E}_j
=-3H\dot q_j^{\,2}+F_j\dot q_j.
}\tag{4}
\]
For \(r_j=\sqrt{2\mathcal E_j}\), \(r'_j\le |F_j|\) in the a.e./regularized sense, implying from the selected zero initial data
\[
|\omega_j q_j(t)|\le r_j(t)
\le\omega_j\sqrt{w_j}|k|
\int_{t_i}^{t}\frac{|\chi(s)|}{a(s)}ds.
\]
Therefore the original bath force satisfies the following finite-interval **rigorous amplitude bound**:
\[
\boxed{
|B_\chi(t)|\le
W_b|\chi(t)|
+a(t)\sum_j w_j\omega_j
\int_{t_i}^t\frac{|\chi(s)|}{a(s)}ds.
}\tag{5}
\]

**What it proves:** a damped positive auxiliary bath cannot create a nonzero \(q_j\) from exactly zero initial data in the absence of forcing \(\chi\), nor can it supply unbounded autonomous energy growth when \(H\ge0\) and \(F=0\). Its amplitude at a fixed finite interval is bounded by the **actual supplied scalar driving history**. This is a transparent analytic passivity statement and gives the finite causal kernel needed for any future physical source-to-Weyl transfer.

**What it does NOT prove:** a sign-definite \(B_\chi\), stability of the complete coupled Einstein+aether+fluid+bath model, time-uniform bounds, no resonance, or suppression of a Weyl observable. The bath exchanges energy with the aether/metric system, and those other sectors can support additional modes, cancellations or instabilities. Eq. (5) is an **input–response** bound, not a full coupled stability certificate.

## 3. Bridge to the 23 newly WSL-verified identities

The combined original reduced action/CLASS mapping gives, for \(R_A=\rho_A+p_A\), \(C=2-K_B\) and \(\Delta_A=\delta_A/(1+w_A)+3\mathcal H\theta_A/k^2\),
\[
\dot\chi=Q E_A+Q c_a^2\left[
\Delta_A-\frac{3H}{Q}\chi+
\frac{k^2}{3a^2R_A}(K_B E_A+C\chi)\right].
\tag{6}
\]
The source-normalized aether equation in the **separate** quarter candidate is
\[
K_B(\dot E_A+HE_A)
=K_Q\chi-C[\dot\chi-QE_A+(H+Q)\chi]
-\frac{\eta Q}{4}B_\chi.
\tag{7}
\]

At fixed initial time with \(\chi=E=q=\dot q=0\), (6) and (7) show
\[
\dot\chi_i=Q_i c_{a,i}^2\Delta_{A,i},\qquad
\dot E_i=-\frac{C}{K_B}Q_i c_{a,i}^2\Delta_{A,i},\qquad
B_{\chi,i}=0.
\tag{8}
\]
The first \(\eta\)-dependent term in \(E_A\) is quadratic in the *local* \(\Delta\tau=\tau-\tau_i\), as independently confirmed by the archived WSL exact-source JSON. At leading radiation order, the second WSL source derivation gives
\[
\Delta_A=-\frac{15+4R_\nu}{40}\Psi_0(k\tau)^2
+O((k\tau)^4,\rho_A/\rho_r,c_a^2),
\tag{9}
\]
where the meaning of the omitted terms follows the frozen source's asymptotic truncation.

Equations (3)–(9) show the **mechanism of suppression**: with the chosen zero-free-bath mode, the *direct input* to the coupled scalar/aether/bath subsystem is \(c_a^2\Delta_A\); in the frozen Exp benchmark \(c_a^2\) is \(O(10^{-14})\) at early times, and \(\Delta_A\) starts at \(O((k\tau)^2)\). For a prescribed bounded \(\Delta_A\) and a bounded finite-time fundamental matrix of the coupled linear subsystem, the physical response must inherit a bound proportional to that small forcing times the operator gain.

However **the required full Einstein–AeST–NL0B operator gain has not been computed or bounded**, and the matter \(\Delta_A\) itself evolves with the metric. The finite-time energy argument proves **no autonomous growth of the isolated bath**; it does not rule out amplification via coupled aether/Einstein modes. Therefore no quantitative bound on \(\Delta W(k,z)\) or any DES shear significance is presently supported.

The earlier fixed-\(\eta\) CLASS output difference \(O(10^{-6})\) in a *max-baseline-normalized native transfer* cannot be directly compared to the dimensionful \(c_a^2\) coefficient or used to infer a physical gain factor: different state normalizations, integrated history, and unquantified solver errors intervene.

## 4. One physics decision: where to spend effort next

1. **Established**: reduced quarter-source compatibility with the frozen action; selected no-free-bath branch; leading radiation adiabatic mode; \(O((k\tau)^2)\) first comoving source; first retarded \(\eta\) Taylor contribution; source-locked WSL exact verification; isolated bath passivity and exact causal convolution.
2. **Unresolved**: bounded gain and stability of the **joint** Einstein–AeST–NL0B initial-value operator, including the physical metric constraints and real transfer/survey observable. A local oscillator energy estimate alone cannot certify the full system.
3. **Decisive next work**: one targeted analytic stability / fundamental-solution assessment of the **frozen quarter-source full coupled linear operator** using the existing action and all-species metric source conventions. The aim is to determine whether the \(c_a^2\Delta_A\) drive can be amplified by a genuine coupled mode. Do not solve a new free parameter fitting problem or tune memory to DES data; do not run broad parameter sweeps.
4. **Status**: `PHYSICS_BLOCK`, `OBSERVATION_NOT_FOUND`. No new CLASS run was done in this analysis.

Original sources: [first source script](../ge19/physics_gate/first_retarded_memory_onset_20261111.py), [radiation source script](../ge19/physics_gate/radiation_neutrino_delta_source_20261111.py), [joint action/CLASS source map](ge19_20261111_joint_action_to_CLASS_scalar_source_matrix.md), [leading-mode physical background](ge19_20261111_exp_superhorizon_joint_growing_mode_and_real_IC_bound.md), [P0 tracking issue](https://github.com/dvlahek/aest-memory-gravity/issues/2).
