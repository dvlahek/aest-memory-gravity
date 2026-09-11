# ACT DR6 exploratory lensing R5 — linear baseline recertification

Date: 2026-09-11

Status: frozen after R4 returned INCOMPLETE and before any R5 target output.

## Historical status preserved

R4 remains

`ACT_DR6_LENSING_EXPLORATORY_R4_INCOMPLETE`.

Its failure occurred before any finite-positive-eta ACT point: the memory-disabled eta=0 reference produced non-finite CLASS lensing convergence power at every ACT-required physical multipole L=2..2999.

D2C6H remains a formal FAIL and `OBSERVATIONAL_CLAIM_LICENSED=False` remains frozen.

## Diagnosis motivating R5

Historical v0.62 CLASS-only diagnostics already isolated the same failure to the AeST nonlinear/Halofit lensing interface:

- AeST + Halofit: phi-phi non-finite at all 4499 tested multipoles;
- AeST linear: phi-phi finite at all 4499 tested multipoles;
- LCDM + Halofit: phi-phi finite at all 4499 tested multipoles;
- the AeST+Halofit z=0 P(k) output itself was finite in the interface audit.

Therefore R5 does **not** claim to repair Halofit. It removes the known unsupported/broken nonlinear mapping and asks only whether the current corrected AeST+memory CLASS build still has a finite linear lensing baseline.

No E-state rescaling, NDF15, tolerance, interpolation, memory, background, likelihood or cosmological parameter change is introduced.

## Single frozen technical change from R4

R4 explicitly forced

`non linear = halofit`.

R5 removes any `non linear` entry and uses CLASS linear lensing only.

Everything else in the baseline construction is inherited from R4.

## Frozen model

- upstream CLASS SHA: `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- current zero-safe finite-memory patch chain from `nl1c6d2c6c_r5/setup_zero_safe_class.sh`;
- fixed cosmology identical to R4/v063 START;
- `K_B=0.0665`;
- `tau H0=1`;
- memory order 39;
- `l_max_scalars=4000`;
- `output=tCl,pCl,lCl`;
- `lensing=yes`;
- **linear theory: no `non linear` entry**;
- precision file `v019p/pre/p3.pre`;
- CLASS executable + `_cl.dat` extraction;
- ACT support defined by `trim_lmax=2998`, requiring theory through L=2999.

R5 tests eta=0 only. It does not evaluate any eta>0 point and does not perform an ACT likelihood fit or scan.

## Frozen spectrum extraction

Use CLASS file column 5,

`D_L^{phi phi}=L(L+1) C_L^{phi phi}/(2 pi)`, 

and construct

`C_L^{kappa kappa} = (pi/2) L(L+1) D_L^{phi phi}`.

No non-finite value at L<=2999 may be masked, interpolated or replaced.

## R5 gates

R5 PASS requires all of:

1. memory disabled, eta=0 linear CLASS run returns successfully and `C_L^{kappa kappa}` is finite and nonzero for every physical multipole L=2..2999;
2. memory enabled, eta=0 linear CLASS run returns successfully and `C_L^{kappa kappa}` is finite and nonzero for every physical multipole L=2..2999;
3. relative L2 difference between the two spectra over L=2..2999 is <= `1e-8`;
4. provenance confirms the R4 executed head and this R5 preregistration are ancestors of the executed code.

No amplitude, sign, ACT chi2 or eta-response requirement is a gate.

## Non-gating diagnostics

Record min/max linear Ckk on ACT support and save both `_cl.dat` files in the result bundle.

A Halofit rerun is not required: the historical v0.62 evidence and R4 already establish the known nonlinear failure. R5 is deliberately minimal.

## Classification and license

PASS label:

`ACT_DR6_LENSING_EXPLORATORY_R5_LINEAR_BASELINE_PASS`

FAIL/INCOMPLETE label:

`ACT_DR6_LENSING_EXPLORATORY_R5_LINEAR_BASELINE_FAIL`

On PASS only:

`LINEAR_ACT_ETA_SCAN_LICENSED=True`.

Always:

`OBSERVATIONAL_CLAIM_LICENSED=False`.

A PASS licenses only a subsequent **exploratory linear-theory eta scan**. It does not license a physical ACT DR6 observational claim because the AeST-specific nonlinear lensing prescription remains unresolved.