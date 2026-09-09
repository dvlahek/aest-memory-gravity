# NL1C0 result — linear-state gradient-regime validity audit

Final classification: **NL1C0_LINEAR_STATE_HIGH_GRADIENT_REGIME**

Predata commit: `51843cd4352fe64eed89248dd850d085d701f822`.

Implementation commit: `b3b258512bbb6fba5939bdb882d08033b70483d8`.

Workflow commit: `80cc43add26e1420a884d52d847f592c52592486`.

GitHub Actions run: `34324584204` — technical SUCCESS.

Artifact: `results_bundle_nl1c0_linear_gradient_regime_audit`, artifact ID `10093307179`, SHA256 `71b2ae820c81851765218fe275f7e34472b0f5af3f6b3aeebfd45c331f78fe8d`.

Scope: theory/amplitude-validity audit only. No observational data, no likelihood, no finite physical memory coupling, and no nonlinear evolution were used.

The audit was explicitly result-informed by the large `chi` values already visible in the historical v0.77 accepted-source traces. The regime thresholds and physical-gradient formula were frozen before the NL1C0 result.

## Primary observable

For the certified linear scalar transfer state, the aether-orthogonal spatial gradient is

\[
X_{\hat i}^{(1)}=a^{-1}\partial_i\chi.
\]

CLASS scalar perturbations are transfer functions normalized to primordial curvature `R=1`, so the band-limited stochastic physical-gradient RMS is

\[
\langle |\nabla_{\rm phys}\chi|^2\rangle
=\int d\ln k\,\left(\frac{k}{a}\right)^2
\mathcal P_{\mathcal R}(k)|T_\chi(k,z)|^2.
\]

The dimensionless AeST gradient-regime variable is

\[
x_{\rm rms}(z)
=\frac{c^2}{a_0}
\sqrt{\langle |\nabla_{\rm phys}\chi|^2\rangle}.
\]

The primary integral used the exact frozen six-mode band

\[
0.03\le k\le0.20\ h\,{\rm Mpc}^{-1}
\]

with a trapezoidal rule in `ln k`, the frozen primordial spectrum, and only common accepted CLASS source times in

\[
0.2\le z\le1.5.
\]

No off-native time interpolation was used.

## Numerical controls

Every preregistered numerical gate passed:

- requested-mode relative k miss: `0.0`;
- common native-time mismatch: `0.0`;
- common native times in the redshift window: `8`;
- all `chi`, `Q`, `a`, and `z` values finite;
- primordial powers finite and positive;
- logarithmic trapezoid-width sum exactly equals `ln(0.20/0.03)` to reported precision.

Thus the classification is not caused by a failed numerical control.

## Result

Across all eight common native times,

\[
\boxed{x_{\rm rms}\gg 1}.
\]

Specifically,

\[
\min x_{\rm rms}=1.0911\times10^7,
\]

\[
\operatorname{median}x_{\rm rms}=4.3274\times10^7,
\]

\[
\max x_{\rm rms}=9.4551\times10^7.
\]

Counts in the preregistered safety bands were

- `x_rms <= 0.1`: `0/8`;
- `0.1 < x_rms < 10`: `0/8`;
- `x_rms >= 10`: `8/8`.

Therefore

\[
\boxed{\text{NL1C0\_LINEAR\_STATE\_HIGH\_GRADIENT\_REGIME}}.
\]

The dominant contribution to the RMS over the tested band is extremely stable with time: approximately 48.2% comes from `k=0.15 h/Mpc`, about 20.5% from `k=0.20`, about 17.0% from `k=0.10`, and about 13.8% from `k=0.08`. The `0.03` mode is negligible and `0.05` contributes about 0.55%.

## Physical meaning

This is a decisive amplitude-validity result.

The NL0C expansion

\[
\mathcal J(\mathcal Y)
\simeq \frac{2}{3(1+\beta_0)a_0}\mathcal Y^{3/2}
\]

is the correct **directional small-amplitude** expansion around the zero-gradient FLRW state. NL1A correctly validated its numerical operator. Neither result is invalidated.

However, the actual frozen linear cosmological transfer state multiplied by the observed-order primordial curvature amplitude is not remotely in the small-gradient regime on the tested late-time band. It lies many orders of magnitude beyond

\[
\sqrt{\mathcal Y}/a_0\sim1.
\]

Therefore the deep-MOND `Y^(3/2)` operator must **not** be promoted to a physical-amplitude nonlinear prediction for this state.

The published AeST large-gradient limit instead requires

\[
\mathcal J(\mathcal Y)\rightarrow\frac{1}{\beta_0}\mathcal Y,
\qquad
\mathcal J_{\mathcal Y}\rightarrow\frac{1}{\beta_0}.
\]

Thus the physical-amplitude state is in the screened/high-gradient branch of the Y-sector rather than the deep-MOND branch.

## Consequence for the interpretation of the certified linear signal

The v0.77/v0.78 statement remains unchanged: the eta=0 memory tangent is a legitimate, numerically certified response of the **linearized frozen AeST system**.

NL1C0 adds a separate physical caveat: at the actual primordial amplitude, the same linearized state is not amplitude-consistent with neglecting the full nonlinear Y-sector. The perturbative small-gradient expansion is therefore non-uniform in the tiny acceleration scale `a0` for this frozen model.

Accordingly, the project must no longer interpret the linear CLASS trajectory as a controlled approximation to the full physical-amplitude late-time AeST solution until the full `J(Y)` branch is included self-consistently.

This is not evidence that the memory signal disappears. It means the strong-path question has sharpened to:

> does the certified memory direction survive after the AeST Y-sector is restored in its correct high-gradient/full-interpolation regime?

## Required continuation

Per the preregistered NL1C0 rule, the next step is to freeze the full published interpolation family before physical-amplitude nonlinear evolution. The Simple, Exponential and Sharp `j(x)=dJ/dY` forms must be treated as co-primary functions, together with all three already frozen `beta0={1,0.5,0.1}` values. No interpolation function or beta0 value may be selected after seeing the nonlinear outcome.

Historical classifications remain unchanged, including `NL1B_SECOND_ORDER_DYNAMICAL_CLOSURE_INCOMPLETE` and `NL1B2_DIRECTIONAL_SECOND_ORDER_ETA_TANGENT_PASS`.
