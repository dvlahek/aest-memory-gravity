# GE19 — Exact X₂ equation and primordial boundary-data indicial screen

**22 November 2026. Physics-first analytic checkpoint; no CLASS, no DES, no parameter tuning.**

## 0. Verified researcher input

The researcher's original source-locked WSL [k² hierarchy report](../results/ge19_primordial_k2_XS_20261122_r1.json), SHA-256 \`0c12da2497911dfe0103534ed764ad5accfd017aa5b4501587b201b3145743e9\`, original Git blob \`e7236f671f9cdfe4dbe973e637aa0a4008a3d753\`, and original [runner log](../results/ge19_primordial_k2_XS_20261122_r1.log), SHA-256 \`591435a8320d53ec318ebb5519781806e72ab3f135997a1b89515d886b379791\`, Git blob \`c0659b30b81f52b0f062116d926dd9fb8ef9f946\`, were archived **byte-exactly**. **14/14 exact symbolic gates PASS, 4/4 source locks PASS, FULL_PHYSICS_GO false.** Repeated 17/17 source-lock JSON/log match the previous Git archive byte-for-byte.

The new [17-gate standalone SymPy source-locked derivation](../ge19/physics_gate/primordial_X2_second_order_radiation_asymptotic_20261122.py), commit \`6737660\`, was independently executed in local Python (**17/17 PASS**) and committed with an exact matching file SHA (\`ba121a146bbbc1a926275ee039c0db2650093faa\`). Researcher WSL source-lock run is pending.

**Scope:** rigorous algebra within the original *reduced* AeST+NL0B \`k²\` hierarchy, plus an explicitly labeled **reference** radiation-limit indicial model. It is **not** a proof of the actual full Einstein–AeST–NL0B primordial growing eigenvector.

## 1. Exact second-order equation for the actual reduced longitudinal X₂

Start with the previous two source-locked equations (cosmic proper time, \`C=2-K_B\`, \`c=c_a²\`):
\`\`\`math
\dot X_2=-\mathcal A X_2+\frac{S_2}{K_B}+f,\qquad
\dot S_2=(\mathcal A-H)S_2+Q(K_Q-2\mathcal A)X_2-\frac{\eta Q}{4}B_2,
\`\`\`
where \`\mathcal A=CQ/K_B\`, \`f=c\Delta_2\` and \`\dot Q=-3HcQ\`. Eliminate \`S_2=K_B(\dot X_2+\mathcal A X_2-f)\` **exactly**, including the derivative of time-dependent Q. The result is
\`\`\`math
\boxed{
\ddot X_2+H\dot X_2+
\left[\frac{Q(CQ-K_Q)}{K_B}+
\frac{CQH}{K_B}(1-3c)\right]X_2
=\dot{(c\Delta_2)}+
\left(H-\frac{CQ}{K_B}\right)c\Delta_2
-\frac{\eta Q}{4K_B}B_2.
}\tag{1}
\`\`\`
All coefficients and the **quarter** NL0B source come from the already source-locked reduced action. The independently checked half-source negative control produces a **nonzero** extra residual \`-eta Q B2/(4 K_B)\`; a half source does not solve (1). The bath term \`B_2=W_b QX_2-a\sum_j\omega_j\sqrt{w_j}q_{3j}\` must retain its full causal history and is not an externally arbitrary fit function.

Equation (1) isolates the **one** 2nd-order longitudinal physical-candidate operator to use in the future complete primordial Ward and Einstein analysis. Importantly it is not yet a closed cosmological eigenproblem, because \`\Delta_2\` remains dependent on the full AeST stress/metric/ordinary-species constraints and the auxiliary bath is dynamic.

## 2. Exact Exp background behavior in the extreme radiation limit

The original pinned Exp functions are
\`\`\`math
K_Q=4K_2Z_0 Z e^{Z²}=\frac{I_0}{a^3},\quad
Q=Q_0+Z_0Z,\quad
c=\frac{Z_0Z}{(Q_0+Z_0Z)(1+2Z²)}.
\`\`\`
Thus, with \`Z>0\` on the positive branch,
\`\`\`math
\boxed{Z²+\ln Z=\ln\!\left(\frac{I_0}{4K_2Z_0}\right)-3\ln a,}
\quad
\frac{dZ}{d\ln a}=-\frac{3Z}{1+2Z²},
\quad
\frac{dQ}{d\ln a}=-3cQ.\tag{2}
\`\`\`
Therefore, in the **strict mathematical** limit \`a->0\` at fixed positive original Exp parameters, \`Z~sqrt(3 ln(1/a))\`, and eventually \`Q~Z_0 sqrt(3 ln(1/a))\`. Also \`c~1/[6 ln(1/a)]\`. The limit is extremely remote for the physical frozen benchmark with \`Z0=1e-17\` and \`Q0=1e-4\`; over practically relevant early epochs Q can be extremely close to Q0. Nevertheless it is **incorrect** to identify a frozen-Q small-\`t\` expansion with the exact \`t->0\` Exp model without noting this logarithmic drift.

Given radiation domination \`a~A t^{1/2}\` (assuming AeST remains subdominant, as \`rho_A/rho_r\propto aQ->0\`), \`H~1/(2t)\` and \`QK_Q\sim t^{-3/2}\sqrt{\ln(1/t)}\`. The matter-like scalar potential in (1) is **more singular** than \`t^{-1}\` but **less singular** than the \`t^{-2}\` inertial derivative term. Formally, \`t H->1/2\` and \`t² V(t)->0\`, so the limiting homogeneous indicial polynomial is
\`\`\`math
\boxed{p(p-\tfrac12)=0.}\tag{3}
\`\`\`
The logarithmic Exp factors mean this is an **indicial screening**, *not* a completed Frobenius basis for the exact expanding background.

## 3. Reference constant-Q radiation model exhibits two different apparent branches

Only as a controlled **reference asymptotic**, freeze \`Q=\bar Q\`, put \`a=A\sqrt t\` and \`K_Q=I_0/(A³t^{3/2})\`. Neglect subdominant terms in the **homogeneous, bath-free and external-source-free** part of (1). Defining \`\Lambda=\bar Q I_0/(K_B A³)>0\`, the leading comparison ODE is
\`\`\`math
X_2''+\frac{1}{2t}X_2'-\Lambda t^{-3/2}X_2=0.\tag{4}
\`\`\`
Its two *formal* distinct leading behaviors are \`p=0\` and \`p=1/2\`. The next terms are
\`\`\`math
X_{2,(0)}(t)=1+2\Lambda\sqrt t\ln(t/t_*)+O(\sqrt t),\qquad
X_{2,(1/2)}(t)=\sqrt t+2\Lambda t+\cdots.\tag{5}
\`\`\`
The arbitrary fixed positive \`t_*\` keeps the logarithm dimensionless and only shifts the independent \`sqrt(t)\` component. Direct substitution cancels the leading unwanted \`t^{-3/2}\` (first branch) and \`t^{-1}\` (second branch) residuals. This is not an assertion that they solve all subleading terms or survive the complete Einstein/Ward selection.

Recover \`S_2=K_B(\dot X_2+\mathcal AX_2-f)\`. On the **reference** homogeneous branch with \`f=0\`:
\`\`\`math
S_{2,(0)}\sim K_B\Lambda t^{-1/2}\ln t,\qquad
S_{2,(1/2)}\sim \frac{K_B}{2\sqrt t}.\tag{6}
\`\`\`
The second branch has unbounded **un-normalized** stress coefficient \`S_2\` as \`t->0\`, but its *standalone gradient-density contribution* relative to the AeST dustlike background remains finite:
\`\`\`math
\frac{D_A^{\rm grad}}{\rho_A}
\sim-\frac{k²S_2}{a²QK_Q}
\longrightarrow -\frac{k² A K_B}{2\bar Q I_0}\quad\text{for reference }p=\tfrac12.\tag{7}
\`\`\`
For the constant branch, this gradient-only fraction instead contains a logarithm, \`[-k² S_2/(a²QK_Q)]/\ln t\to-k²/A²\`.

**Crucial decision:** **Do not discard all \`S_2\sim t^{-1/2}\` states by imposing boundedness of the raw field \`S_2\` alone.** Physical regularity must be assessed using the complete action density, entropy/adiabaticity, metric, aether multiplier equations, original temporal scalar current and Ward conditions, not one coordinate/amplitude of a partly reduced action. Eq. (7) demonstrates only a *necessary caution*, **not** that the \`p=1/2\` branch is a physically admissible primordial mode. Likewise a potentially logarithmic divergence of one stress component does not by itself prove the full \`p=0\` branch impossible before dictionary cancellations and mode mixing are assessed.

## 4. What this changes, and what is still missing

The earlier results established that a conditional analytic branch has \`X,S_A,B_{\rm delayed}=O(k²)\` and that a retarded NL0B bath retains temporal memory. The new proof reduces the remaining unknown scalar dynamics to one exact **second-order, action-normalized, history-forced equation** (1), with a controlled warning that standard pointwise field boundedness can reject plausible adiabatic/isocurvature candidates incorrectly.

The **next real physical acceptance test** is no longer another autonomous X/S algebra or an extra CLASS run. It is to insert the *actual original Exp* time-varying Q,K_Q,K_QQ and the full AeST stress dictionary into the **complete** Einstein+photon/baryon/neutrino+aether/multiplier and scalar Noether system, then find which of the two *candidate* early branches (if either) satisfies the jointly regular **adiabatic growing** condition and the genuinely transported retarded no-free-bath history. This could fix, suppress or rule out physical \`X_{2,i},S_{2,i}\`, and only then will a physical delayed Weyl response be justified.

**FULL_PHYSICS_GO = FALSE. DES_DETECTION = FALSE.** The earlier \`W1_delayed(z=.5)=-1.2006039315857457e-10\` remains a provisional historical CLASS tangent, not a prediction of this original-action mode.

## Reproducibility

[Single 17-identity proof code](../ge19/physics_gate/primordial_X2_second_order_radiation_asymptotic_20261122.py) completed locally without CLASS; source-locked WSL confirmation pending. Parent 14/14 k² report and earlier 17/17 X/S local Ward report were independently verified in researcher WSL and archived byte-exact.
