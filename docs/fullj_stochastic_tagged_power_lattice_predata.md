# Pre-data declaration: stochastic tagged power-lattice adequacy

## Purpose

The locked full response-kernel POC established that the broadband tagged tangent response is diagonal to extremely high precision in the tested regime. Therefore the repeated late-time K0->K1 and K1->K2 radial failures are not hidden off-diagonal mode-coupling effects. The remaining problem is radial sampling of a sharply structured scalar diagonal response.

For lensing and Weyl-power construction the relevant object is not the sign of the scalar transfer itself but its power response. This milestone therefore tests the bounded radial adequacy of

`P_tag(k,z) = < |T_tag(k,z|G)|^2 >_G`

directly, without requiring the signed transfer to satisfy a smoothness gate across its zero crossings.

This is a pre-data declaration. Thresholds, grids, adaptive-selection rules and scope are fixed before any new missing-lattice or half-lattice result is inspected.

## Required locked ancestry

- evolving R2 bridge PASS: `1f42f88e9724c58d2d242a65ca7266a207e4a0f8`
- Gaussian 1D stochastic ensemble PASS: `05e38b273f91eb04b7b4c8753731017d0ed839c1`
- 3D saturated closure PASS: `f6eb7099cffc9ae6f4fe11ddef1794f0e6dd6e4f`
- tagged-mode POC PASS: `aff670fa8551163f5cde2b5146e0e5840d53b424`
- K1 radial FAIL: `2531a10772f97958ab221bd1f39ceffc23e964a5`
- K2 radial FAIL: `a293ff5d02824ba170fcf46251df1e480682386c`
- response-kernel POC PASS result: `2a5f884a50b7b30b90ddff01721914626dbde20f`
- history through kernel POC: `6eea250e82c2ed2b161a776594948062a6d77743`

Historical FAIL classifications remain FAIL and are not reinterpreted.

## Frozen physics and stochastic setup

- reference nonlinear member: `sigma=0`, `kind=simple`, `beta0=1`
- Gaussian coefficient seed: `20260912`
- frozen coefficient SHA256: `9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200`
- primary backgrounds: `B4={0,1,2,3}`
- half-lattice validation backgrounds: `B2={0,1}`
- symmetric tag amplitude: `epsilon=0.05`
- redshifts: `z={6,5,4,3,2,1.5,1,0.5,0.2}`
- time integration: `NSTEP=4096`
- canonical trajectory remains the locked one-way R2 construction; no nonlinear reconstructed-metric feedback is introduced.

The B2 half-lattice control is allowed because the preceding K1, K2 and full-kernel campaigns already established B2->B4 convergence many orders of magnitude below the radial power thresholds. The half-lattice comparison itself is B2-to-B2, so no sample-count mismatch enters its direct interpolation test.

## Stage A: complete the exact 0.005 lattice

Primary radial lattice:

`K_full = {0.030,0.035,...,0.200} h Mpc^-1`

with uniform spacing

`Delta k/h = 0.005 Mpc^-1`.

There are 35 nodes. The 21 locked K2 nodes are reused unchanged. Only the 14 missing nodes are newly integrated:

`H_full={0.060,0.075,0.105,0.115,0.120,0.130,0.140,0.145,0.155,0.165,0.170,0.180,0.190,0.195}`.

Common Stage-A geometry:

- `kF/h=0.005 Mpc^-1`
- `NX=256`
- `box=2*pi/(kF*h)`

New Stage-A cost: `14 nodes x 4 backgrounds x 2 signs = 112` R2 integrations.

For each node/background, recover the symmetric scalar tagged response and its direct power `|T|^2`. Merge new nodes with the immutable locked K2 response to form a complete B4 and B2 power lattice.

## Stage B: preregistered adaptive half-lattice validation

Half-lattice geometry:

- `kF/h=0.0025 Mpc^-1`
- `NX=512`
- box doubled relative to Stage A
- the physical real-space grid spacing is therefore preserved.

Candidate half-lattice nodes are the 34 midpoints between adjacent Stage-A nodes:

`k_half/h = 0.0325,0.0375,...,0.1975 Mpc^-1`.

No half-lattice science result may be inspected before the selection rule below is applied.

### Frozen adaptive selection rule

Using only the completed Stage-A B2 mean power lattice, compute for each interior full-lattice node and for `z={1.0,0.5,0.2}` the normalized discrete curvature

`C_j(z)=|P_{j+1}-2 P_j+P_{j-1}| / max(P_{j-1},P_j,P_{j+1},1e-14*Pmax(z))`.

Assign to each adjacent interval the maximum curvature of its endpoint nodes and take the maximum across the three late redshifts. Boundary intervals use the nearest available interior-node curvature.

Select exactly 16 half-lattice intervals as follows:

1. include six fixed domain-coverage controls with midpoints nearest `{0.0325,0.0625,0.0925,0.1225,0.1625,0.1975}`;
2. add intervals in descending curvature score until 16 unique intervals are selected;
3. ties are broken by increasing midpoint k.

This selection algorithm is frozen before Stage-A results and is not manually modified after seeing the selected intervals.

Each selected half-lattice node is run for `B2={0,1}` and both signs. Stage-B cost: `16 x 2 x 2 = 64` R2 integrations at NX=512.

## Interpolant under test

The observable-facing object is power. For each redshift and each B2 background-mean lattice, construct a nonnegative PCHIP interpolant of direct power versus `ln k` from the complete Stage-A `Delta k/h=0.005` lattice. No interpolation of signed transfer is used for the primary gate.

Evaluate that power interpolant at the 16 directly computed half-lattice nodes and compare with their direct B2 mean tagged power.

Signed/complex transfer midpoint errors are stored only as descriptive diagnostics and cannot fail this milestone.

## Frozen gates

### PL-G1 provenance and frozen identity

All required ancestry locks, coefficient hash, grids, backgrounds, epsilon, NSTEP and selection algorithm must match this declaration exactly.

### PL-G2 Stage-A solver/constraint health

All 112 new Stage-A integrations finite. Across all new Stage-A runs:

- canonical residual `<=1e-10`
- Hamiltonian, momentum and shear metric constraints each `<=1e-8`.

### PL-G3 Stage-A broadband saturated closure

Across all 112 new Stage-A runs and all redshifts:

`epsilon_sat <= 2e-2`.

### PL-G4 complete-lattice algebra/background sanity

- all 35-node responses and powers finite
- direct power nonnegative
- `|T|^2 = Re(T)^2+Im(T)^2` relative residual `<=1e-12`
- on the 14 new nodes, B2->B4 response global relative L2 `<=1e-2`, per-node max `<=3e-2`
- on the 14 new nodes, B2->B4 power global relative L2 `<=2e-2`, per-node max `<=5e-2`.

### PL-G5 Stage-B solver/constraint and saturation health

All 64 selected half-lattice integrations finite with the same canonical/metric thresholds as PL-G2 and `epsilon_sat<=2e-2`.

### PL-G6 power half-lattice interpolation accuracy

Across the 16 direct half-lattice controls, separately at each redshift:

`E_P(z)=||P_interp-P_direct||_2 / max(||P_interp||_2,||P_direct||_2)`.

Require:

- `max_z E_P(z) <= 5e-2`
- `median_z E_P(z) <= 2.5e-2`.

Also define

`E_peak(z)=max_i |P_interp_i-P_direct_i| / max_i P_direct_i`

and require

- `max_z E_peak(z) <= 1e-1`.

Interpolated power must remain finite and nonnegative at every selected midpoint.

### PL-G7 no unresolved selected-interval power spike

For every selected half-lattice midpoint and redshift, direct midpoint power must satisfy

`P_mid <= 2 * max(P_left,P_right) + 1e-14*Pmax(z)`.

This veto is applied to power, not signed transfer.

## Classification

PASS only if PL-G1 through PL-G7 all pass:

`FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_PASS`.

Otherwise:

`FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_FAIL`.

Use `INCOMPLETE` only for missing provenance/runtime/input artifacts that prevent the frozen diagnostic from being executed.

## Scope of a PASS

A PASS licenses only:

- `STOCHASTIC_TAGGED_FULL_005_LATTICE_TESTED=True`
- `STOCHASTIC_TAGGED_BOUNDED_POWER_INTERPOLANT_TESTED=True`

It does **not** by itself license a 3D cosmological Weyl power spectrum. Keep false:

- `THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`.

If PASS, the next milestone is the 3D/isotropic stochastic power lift using the already locked 3D geometry and saturated-closure results. If FAIL, do not loosen thresholds; use the directly identified half-lattice failures to determine if a finer bounded radial power lattice is required.
