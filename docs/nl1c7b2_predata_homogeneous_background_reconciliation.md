# NL1C7B2 predata — homogeneous-background reconciliation

Status: **PRE-RESULT / FROZEN BEFORE TRACE INSPECTION**

Classification before evaluation:

`NL1C7B2_PREDATA_HOMOGENEOUS_BACKGROUND_RECONCILIATION`

## Purpose

NL1C7B1 has certified the missing pressureless-matter variational backreaction sector. Before any radial initial-constraint or time-evolution calculation, NL1C7B2 tests if the homogeneous eta=0 spherical action containing the frozen AeST scalar sector plus the newly certified baryonic pressureless dust reproduces the same homogeneous background used to generate the certified NL1C7A initial state at `a_i=0.02`.

No additional background density, radiation source, neutrino source, cosmological term, fit parameter, or post-result normalization may be introduced in this checkpoint.

## Frozen provenance

### NL1C7A dense eta=0 trace

- dense trace run: `35149865129`
- head: `4a275f4777a7e487004f4783bc2a929a93ac8188`
- artifact: `10469031693`
- artifact SHA256: `193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70`
- exact k coverage: 128/128
- accepted native times: 179
- interpolation used in trace generation: false

The final C7A evaluator result remains

`NL1C7A_REPAIR01_DENSE_TIME_SPHERICAL_BRIDGE_CERTIFIED`

from run `35183893359`, artifact `10481526695`.

### NL1C7B1 pressureless-matter closure

- classification: `NL1C7B1_PRESSURELESS_MATTER_VARIATIONAL_CLOSURE_PASS`
- result commit: `a974473a3eeb32de01ac841afe1a52c3ded321e6`
- official run: `35185338047`
- head: `6b555bc2ee3cba7c9e97706eb1a0949416e9932f`
- artifact: `10481781728`
- artifact SHA256: `645d29e4e8ac7cfa4fff9833a4ef500d34fc667373bfac3073883155fac519a7`

### Frozen cosmological parameters

Use the same values already frozen by the C7A trace generator:

- `H0 = 67.3324639084866 km s^-1 Mpc^-1`
- `omega_b = 0.022377376877682164`
- `omega_cdm = 0.12006705327635288`
- `N_ur = 2.046`
- `N_ncdm = 1`
- `m_ncdm = 0.06 eV`
- `a_i = 0.02`
- AeST Exp branch, `KB=0.0665`, `Q0=1e-4`, `K2=9500`, `Z0=1e-17`
- `eta=0`.

`omega_cdm` must not be inserted as an ordinary pressureless-dust source in the spherical action. In the frozen AeST cosmological implementation the scalar-dark sector is represented by the AeST background quantities traced as `Q`, `rhoA`, `KQ`, and `KQQ`. This checkpoint tests that frozen representation; it does not reinterpret `omega_cdm` after the result.

## Frozen homogeneous identity

In the flat homogeneous specialization

`N=N(t), b=0, L=a(t), R=a(t) r, u=0, X=0, E=0`, 

with eta=0 and comoving baryonic dust, the lapse variation of the C6 field action plus the B1 dust action must reduce exactly to

\[
3H^2 = \rho_A + \varrho_b,
\]

where

\[
\rho_A = QK_Q-K(Q),
\qquad
\varrho_b = 8\pi G\rho_b.
\]

The baryon contribution is not fitted. With `h=H0/100`, `Omega_b=omega_b/h^2`, and `c=299792.458 km/s`, use

\[
H_{0,\rm geo}=H_0/c,
\qquad
\varrho_b(a)=3H_{0,\rm geo}^2\,\Omega_b\,a^{-3}.
\]

Equivalently,

\[
\varrho_b(a)=3(100/c)^2\,\omega_b\,a^{-3}.
\]

## Interpolation rule

Evaluate `H_Mpc_inv`, `Q`, `rhoA`, and `KQ` at `a_i=0.02` from the retained dense native trace using the already certified C7A primary rule: PCHIP in `ln a` separately at every exact native k mode.

As controls:

1. background quantities must agree across all 128 k modes to relative spread `<=1e-10` after interpolation;
2. replacing PCHIP by linear interpolation in `ln a` must change the normalized closure residual by `<=2e-2`, the same frozen interpolation-control scale already used by C7A.

No nearest-neighbour substitution is allowed.

## Locked gates

### B2-G1 — provenance

The C7A dense-trace artifact/digest and B1 result/run/artifact must match exactly.

### B2-G2 — exact homogeneous lapse identity

A symbolic reduction of the frozen C6 homogeneous action plus the B1 dust action must give exactly

`3 H^2 - rhoA - varrho_b = 0`

with `rhoA = Q K_Q - K`.

### B2-G3 — trace scalar-energy consistency

Using the frozen Exp branch,

\[
K(Q)=2K_2Z_0^2\left(e^{Z^2}-1\right),\qquad
K_Q=4K_2Z_0 Z e^{Z^2},\qquad
Z=(Q-Q_0)/Z_0,
\]

the traced `rhoA` must agree with `Q*KQ-K(Q)` at `a_i` to normalized relative error `<=1e-8`.

If the trace uses a documented equivalent background-energy convention, the implementation must identify it from the frozen source before classifying this gate. No post-result rescaling is allowed.

### B2-G4 — baryon normalization

The baryon source must be exactly the frozen `omega_b` contribution

`varrho_b(a_i)=3*(100/c)^2*omega_b*a_i^-3`

in Mpc^-2. No `omega_cdm`, radiation, neutrino, or fitted remainder may be folded into this term.

### B2-G5 — homogeneous Hamiltonian closure

Define

\[
\epsilon_H=
\frac{|3H^2-\rho_A-\varrho_b|}{\max(3H^2,10^{-300})}.
\]

PASS requires

`epsilon_H <= 1e-7`,

the same scale as the frozen NL1C7 initial-constraint gate.

### B2-G6 — k-independence and interpolation control

The 128 exact-k reconstructions must satisfy the k-spread and PCHIP-vs-linear controls above.

### B2-G7 — missing-sector diagnostic without repair

If B2-G2 through B2-G4 are internally consistent but B2-G5 fails, report the signed remainder

\[
\rho_{\rm rem}=3H^2-\rho_A-\varrho_b
\]

and its fraction of `3H^2`.

The implementation may compare the magnitude and scaling of this remainder against standard background species already explicitly present in the frozen CLASS parameterization, but this is diagnostic only. It must not add the remainder to the spherical equations in this checkpoint.

## Classification

All B2-G1 through B2-G6 pass:

`NL1C7B2_HOMOGENEOUS_BACKGROUND_RECONCILIATION_PASS`

The action/trace definition of the already frozen AeST scalar energy is inconsistent with the exact homogeneous reduction:

`NL1C7B2_HOMOGENEOUS_BACKGROUND_RECONCILIATION_FAIL`

The exact dust/AeST identities are consistent, but the full frozen CLASS background contains a non-negligible additional standard background sector not represented by the present spherical action, so B2-G5 fails:

`NL1C7B2_HOMOGENEOUS_BACKGROUND_SECTOR_INCOMPLETE`

An `INCOMPLETE` result forbids radial initial-constraint or trajectory execution until the missing background stress-energy sector is explicitly preregistered and closed. It does not permit changing `a_i` after the result.

## Claim boundary

No radial initial constraint, time step, turnaround, collapse, finite eta, or observable is evaluated in NL1C7B2.