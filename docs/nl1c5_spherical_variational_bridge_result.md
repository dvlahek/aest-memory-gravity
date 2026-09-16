# NL1C5 result — spherical variational bridge

Final classification: **NL1C5_SPHERICAL_VARIATIONAL_BRIDGE_PASS**

Predata commit: `7d6c43f62ef19487db7462f58d4c620859a8fc78`.

Implementation commit: `9f23f0d5bd86f70eab7221e604d8566aa322cb50`.

Official workflow/fix commit: `81e38a4a466220d97d7eba0acf79875da7e1d9c2`.

GitHub Actions run: `35087054333` — technical SUCCESS.

Artifact: `results_bundle_nl1c5_spherical_variational_bridge`, artifact ID `10441759239`, SHA256 `6831d0f81022a8c57d7f623fafc9ecfc1ef1f2cb94abd44cd84bed837cb290af`.

Scope: exact spherical variational reduction of the frozen NL0B memory sector plus the already frozen screened static AeST operator control. No spherical-collapse evolution, finite physical eta, halo statistic, lensing observable, likelihood or observational data were used.

## 1. Exact spherical memory reduction

For the frozen spherical coframe

\[
\theta^0=Ndt,\quad
\theta^1=L(dr+b\,dt),\quad
\theta^2=R d\theta,\quad
\theta^3=R\sin\theta\,d\varphi,
\]

with

\[
A=\cosh u\,e_0+\sinh u\,e_1,
\qquad
s=\sinh u\,e_0+\cosh u\,e_1,
\]

the frozen NL0B node action reduces exactly after angular integration to

\[
\widehat L_{j,1+1}
=\pi NLR^2\left[(Aq_j)^2-(\omega_jq_j-\sqrt{w_j}X)^2\right].
\]

The symbolic angular-reduction residual is exactly zero.

## 2. Frame and finite-reference source controls

The nonzero deterministic spherical test gives

\[
\max|A^2+1|=6.66\times10^{-16},
\]

\[
\max|s^2-1|=5.55\times10^{-16},
\]

\[
\max|A\cdot s|=8.33\times10^{-17}.
\]

Automatic/symbolic source blocks were checked against independent centered finite differences of the reduced action. The worst relative mismatch is

\[
\boxed{3.1562\times10^{-8}},
\]

well below the preregistered `1e-6` gate.

All finite-reference metric source blocks are nonzero on the deterministic test. Their L2 norms are approximately

- lapse: `16.0589`;
- shift: `4.6670`;
- radial scale: `7.3331`;
- areal radius: `14.8760`.

Thus the spherical reduction retains the direct finite-reference metric memory source identified in NL1C3/NL1C3A; it is not replaced by a phenomenological radial force.

## 3. FLRW recovery

Under

\[
N=1,\quad b=0,\quad L=a(t),\quad R=a(t)r,\quad u=0,
\]

the homogeneous memory action is exactly zero. The bath Euler equation reduces exactly to

\[
\ddot q_j+3H\dot q_j+\omega_j^2q_j
=\omega_j\sqrt{w_j}\,X,
\]

with zero symbolic residual. This reproduces the already certified NL1C3B/NL1C4 expanding-volume dynamics without inserting a friction coefficient by hand.

## 4. Regular center

For a regular odd radial flux

\[
F(r)=f_1r+f_3r^3,
\]

the spherical divergence is

\[
\frac1{r^2}\frac{d}{dr}(r^2F)=3f_1+5f_3r^2,
\]

with finite center limit `3 f1`. Therefore the action-derived radial structure admits the required regular-center parity and does not force a spurious `1/r` singular source.

## 5. Screened static spherical control

The frozen high-gradient AeST mass scale remains

\[
\mu=9.9129910089\times10^{-3}\;{\rm Mpc}^{-1}.
\]

For all co-primary `beta0={1,0.5,0.1}`, the spherical Helmholtz operator was checked using the regular `l=0` mode

\[
j_0(kr)=\frac{\sin kr}{kr},
\]

which satisfies

\[
\nabla_r^2j_0=-k^2j_0.
\]

The normalized operator residual is

\[
\boxed{2.15\times10^{-16}},
\]

well below the locked `1e-10` gate.

## 6. No phenomenological shortcut

The implementation contains no inserted `a_drag`, memory-drag, shell-force, MOND-force, extra-acceleration term, or direct reuse of the linear CLASS `E_rhs` closure as a nonlinear spherical force.

Every S1-S8 gate passes.

\[
\boxed{\mathrm{NL1C5\_SPHERICAL\_VARIATIONAL\_BRIDGE\_PASS}}
\]

## Consequence

The spherical memory sector is now reduced directly from the frozen covariant action and is compatible with both the previous FLRW expanding-memory bridge and the screened spherical/static AeST control.

This closes the objection that a later spherical calculation would need an ad-hoc memory drag law.

It does **not** yet provide self-gravitating spherical-collapse dynamics. The next task is **NL1C6 spherical self-gravity closure**: derive and evolve the Einstein/AeST spherical baseline together with the action-derived scalar, aether, bath and metric memory source blocks, first at eta=0 and only later at finite physical eta.
