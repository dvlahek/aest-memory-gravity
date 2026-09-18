# NL1C7B4 Repair11 — local result freeze

## Status

Frozen local WSL result for the preregistered Repair11 analytic/covariant E-sector momentum audit.

Terminal classification:

`NL1C7B4_REPAIR11_ESECTOR_ANALYTIC_COVARIANT_AUDIT_PASS`

with `SCIENCE_RC=0`.

This is a local WSL science result, not an official GitHub Actions run.

## Execution provenance

- execution HEAD: `b81c5e349b4074f730971211de4fa41b3807474d`;
- Repair11 preregistration commit: `02e1e7eaffd08aa289830810250057314594b9cf`;
- Repair11 implementation commit: `95ba6dd33105ff0b4cada77e0df44ed819edf4a0`;
- Repair11 implementation-lock commit: `1de607cfffef8c0862ddb14f6f296a584f9e92f1`;
- Repair11 local-runner commit: `907e273c60ed9acd29afe3f0ac611d74380d69a8`;
- Repair10 result-freeze commit: `de03f563ee3e8700b3159be5a46b73633c85db8d`;
- Repair10 JSON SHA-256: `f1fc1a86d2d488f5e88f0d32b0d3d1d5ce9dab22f52e51fa69801948aeb6de9d`;
- Repair08 NPZ SHA-256: `4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7`.

## Frozen local output hashes

- result JSON:
  - bytes: `39396`
  - SHA-256: `48c8caf0c5758b089318bcd18885c87725bc244ed5a47862ac841b37b834742d`
- evaluator log:
  - bytes: `39396`
  - SHA-256: `48c8caf0c5758b089318bcd18885c87725bc244ed5a47862ac841b37b834742d`
- local runner log:
  - bytes: `41410`
  - SHA-256: `70e91debdee3751bb28481932c2a7a5bcf01a460222dac38b80b3c8ccdb0e7ab`

## Gate result

All eight preregistered Repair11 gates pass:

- R11_G1 frozen provenance: PASS
- R11_G2 exact gauge shift identities: PASS
- R11_G3 first-order vanishing: PASS
- R11_G4 quadratic coefficients: PASS
- R11_G5 frozen implementation equivalence: PASS
- R11_G6 Repair10 hotspot reproduction: PASS
- R11_G7 quadratic amplitude scaling: PASS
- R11_G8 linear Fourier consistency and claim boundary: PASS

## Symbolic result

The frozen symbolic audit proves:

- `[epsilon^1] C_M^{E2}=0`;
- `[epsilon^1] C_M^{EX}=0`;
- `[epsilon^2] C_M^{E2}=2 K_B a^3 u_1 d_r(r^2 E_1)`;
- `[epsilon^2] C_M^{EX}=2 C a^3 u_1 d_r(r^2 X_1)`;

with

- `E_1=u_dot_1+H u_1`;
- `X_1=Q u_1+phi_{1,r}/a`.

All preregistered exact gauge identities pass.

Therefore the E2 and EX sectors carry no independent first-order radial-momentum source on the homogeneous B3 background.

## Frozen implementation equivalence

The independent closed-form E-sector momentum arrays agree with the frozen `build_nonK()` implementation on all six scale/grid pairs.

Largest observed normalized discrepancies:

- E2: `2.1127856072243302e-16`;
- EX: `2.1430993647304566e-14`;

both far below the locked `1e-10` limit.

## Repair10 hotspot reproduction

All 54 Repair10 hotspot records reproduce the stored E2 and EX signed contributions with zero reported absolute and relative error.

Representative scale-5, Nr=256 hotspot:

- `AeST_E2=-9.087177024783368e-13`;
- `AeST_EX=-9.232342448184978e-15`.

## Virtual amplitude-order audit

For diagnostic amplitudes

`lambda={1,1/2,1/4,1/8}`,

all E2 and EX momentum norms display quadratic scaling.

Across all six scale/grid pairs and both E-sector terms:

- minimum adjacent log2 slope: `1.999982824220407`;
- maximum adjacent log2 slope: `2.078878529682273`;
- locked interval: `[1.8,2.2]`.

As lambda decreases, the E2 slopes approach 2, and EX is essentially exactly quadratic throughout.

## Linear Fourier consistency

The frozen linear represented momentum source remains

`a[varrho_b theta_b + Q K_Q theta_A]`.

Because both E2 and EX first-order sources vanish exactly, their absence from this linear Fourier source is analytically consistent.

Thus Repair10 E2 dominance is not evidence for a missing linear E-sector source, a wrong E2 coefficient, or an E2 sign error.

## Interpretation boundary

Repair11 changes the interpretation of the Repair10 localization:

- the dominant E2 contribution is a genuine **quadratic-order residual** of the exact nonlinear constraint evaluated on a state constructed from first-order perturbations;
- E2/EX do not identify a linear interface mismatch;
- the frozen E-sector implementation matches the analytic variational result;
- the linear Fourier 0i bridge remains consistent.

However:

- B4 remains historically FAIL under its original exact nonlinear `1e-7` gate;
- Repair11 does not construct nonlinear constraint-corrected initial data;
- Repair11 does not establish nonlinear-evolution viability;
- Repair11 does not establish finite-eta viability;
- Repair11 does not establish an observational AeST detection.

## Licensed next step

The next legal diagnostic should audit the perturbative order of the **full signed raw Hamiltonian and momentum constraint numerators**, not only E2/EX.

Using the same frozen Repair08 state and the same homogeneous B3 background, virtual amplitudes may be introduced only diagnostically. The audit should determine if the total signed residuals have vanishing first-order coefficients and leading second-order scaling.

The historical B4 epsilon gate and classification remain unchanged.

If the full residual is verified to begin at second order, a later separately preregistered stage may distinguish:

1. certification of first-order constraint consistency of the linear growing-mode initial data; and
2. construction of genuinely nonlinear constraint-corrected initial data required for exact nonlinear B4 certification.

No historical B4 result may be relabeled.
