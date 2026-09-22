# GE19 Repair30 Repair02 — shape repair implementation lock

## Status

Repair02 records the second implementation-only repair before any valid
Repair30 science JSON exists.

The Repair30 preregistered science contract is unchanged.

## Frozen failure parent

Failure freeze:

- file:
  `docs/ge19_repair30_repair01_execution_implementation_fail02_freeze.md`;
- blob:
  `31e6febbb9684cdfd4a1a9433127611753e73102`;
- commit:
  `9cbd12a85d82831f88f73860157d7aa4ecba6587`.

The failure was a shape/broadcasting bug only.

## Repair02 implementation

Code:

- file:
  `ge19/repair30_reduced_h2_z11_reclosure.py`;
- blob:
  `e32631bceb4ceb11037eef70b8a47b5f7622faff`;
- final Repair02 code commit:
  `fc1f12f68df99e0e5cd7bc2e76090bf36a84e2f5`.

Repair02 removes only the erroneous singleton axes in the standard-sector
tangent subtraction and adds explicit shape guards.

The frozen identities are still

`delta_rho_std_11 = total_delta_rho_eta - rho_dark*delta_dark_eta`

and

`momentum_std_11 = total_rho_plus_p_theta_eta - (rho_dark+p_dark)*theta_dark_eta`.

No physics/source/boundary/gate change is present.

## Dedicated Repair02 prelock

Workflow:

`.github/workflows/ge19-repair30-repair02-prelock-audit.yml`.

Blob:

`6593ac916076a8a1d05a7cb4c087bcb18d8fb806`.

Workflow commit:

`a61287a0fe451c550239f1a1456d0b6e029dd4ea`.

Run:

`35750958907`.

Job:

`106824641242`.

Conclusion:

`success`.

The prelock additionally downloaded the frozen lean Repair29B/R2 reference
and verified real data shapes:

- `ln_a: (128,)`;
- `k_Mpc: (6,)`;
- R2 delta_dark tangent: `(6,128)`;
- R2 theta_dark tangent: `(6,128)`;
- R2 total_delta_rho tangent: `(6,128)`;
- R2 total_rho_plus_p_theta tangent: `(6,128)`;
- R2 phi/psi/alpha tangent arrays: `(6,128)`;
- R2 chi11: `(6,128)`.

## Unchanged science contract

Still frozen:

- `L_total Z11=-M1[Z10,q10]`;
- `B10=X10-weighted_z10`;
- Repair22/Repair27 parents;
- Repair29B-certified R2 reference;
- Nt128/Nt64 precision pair;
- C envelope;
- all Repair30 thresholds;
- no finite eta;
- no H4/Z21 execution.

## Science status

No valid Repair30 science JSON has yet been produced.

Therefore the next runner invocation remains the first valid Repair30 science
attempt under the original preregistered contract.
