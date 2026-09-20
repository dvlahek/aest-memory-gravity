# GE08 Repair01 source-derivative semantics — result freeze

## Status

Frozen first locked Repair01 execution.

Terminal classification:

`GE08_REPAIR01_FULL_FIRST_ORDER_STATE_BRIDGE_PASS_MATTER_INCOMPLETE`.

Historical parent classification remains unchanged:

`GE08_FULL_FIRST_ORDER_STATE_BRIDGE_FAIL`.

GitHub Actions run:

`35492326169`.

Execution HEAD:

`21d80b554735bf31f3ad6d705b412c7e5a692e10`.

Artifact:

- ID: `10598944561`;
- name: `results_bundle_ge08_repair01_source_derivative_semantics`;
- ZIP SHA-256:
  `d237aaf4b8f7314992de8dc1a0b432b4fb81eb80fe08352ac3f9d95cfc54982d`.

## Frozen output hashes

Result JSON:

- bytes: `3471`;
- SHA-256:
  `92d185b93688287d0aee5d23f0074cfe7ec1408296830e09fc3d02c88cdf2891`.

Result log:

- bytes: `3471`;
- SHA-256:
  `92d185b93688287d0aee5d23f0074cfe7ec1408296830e09fc3d02c88cdf2891`.

Result NPZ:

- bytes: `13230`;
- SHA-256:
  `807833b6692f91f10d4716be1f59baee8f7376d1569fbabec9d76d3e35bbe8fd`.

Legacy chi trace:

- bytes: `350249`;
- SHA-256:
  `aed5ed209239f35adaaa35be7114df7dbd440f01f830b26cddc33d8b34aefcbf`.

Full-state trace:

- bytes: `1611070`;
- SHA-256:
  `3ee90a0cf6a281214b35f0eafe30efdd99bb540b80793eccf3dfa7c76f41c01a`.

Diagnostic trace-patch report:

- bytes: `489`;
- SHA-256:
  `b61f1f2747b44f577cf1bf54b58033d036211a409877344cd0ec4af378a8c7fa`.

Repair01 preregistration:

- bytes: `4013`;
- SHA-256:
  `af417e0d094d6409c2b1f94e3819741e9d70ee18c7704abef468b73c371ebffd`.

Repair01 implementation lock:

- bytes: `2351`;
- SHA-256:
  `c3a8844a36617e7245f6a18f968de058905977a76ddd72cdabab353afbb54913`.

## Bridge result

The repaired first-order state bridge passes every frozen bridge gate.

Exact/machine-level controls:

- legacy/full source-grid mismatch: `0`;
- reconstructed chi versus historical trace: `0`;
- traced native delta_m versus CLASS source: `0`;
- requested-k miss: `0`;
- native-tau mismatch: `0`;
- trace rows: `2904` in both streams;
- selected rows: `48`;
- distinct native times in `0.2<=z<=1.5`: `8`;
- all traced values finite.

The repaired derivative-semantics gates all pass:

- CLASS phi physical RHS identity present: true;
- AeST alpha physical RHS identity present: true;
- NDF15 interpolated derivative path present: true;
- NDF15 passes `ypinterp` to the source callback: true.

The historical callback-`dy` mismatches remain recorded only as descriptive diagnostics:

- alpha callback dy mismatch:
  `2.2022065445364682e-4`;
- phi callback dy mismatch:
  `1.18987731579593e-8`.

They are not physical-RHS failures.

## Exact matter-completeness result

The exact single-pressureless-fluid readiness condition fails.

After subtracting the frozen AeST effective-dark scalar stress:

- `||delta p_std||/||delta rho_std|| =
  4.0296809261404915e-7`;
- `||shear_std||/||delta rho_std|| =
  5.717716788656946e-10`;
- standard density versus baryon-only relative L2 =
  `1.3238516018121685e-3`.

The frozen exact limit remains `1e-12`.

Therefore:

`full_CLASS_pressureless_basic_state_ready = false`.

No tolerance was relaxed.

## Project consequence

The **basic eta=0 first-order gravitational/AeST state dictionary is now certified** on the frozen late-time CLASS reference.

However:

- the full standard-matter sector is not exactly one pressureless fluid;
- the complete GE06 local first-order jet has not yet been certified;
- a `Z20` solve remains unlicensed.

## Next licensed work

Two separate gaps remain and must not be conflated.

### 1. Complete GE06 local first-order jet

Construct and independently certify the complete local directional data required by GE06:

`(N,L,R,b,u,phi; Lt,Lx,Rt,Rx,bx,ut,ux,pt,px,Nx)`.

No new physical parameter is allowed.

### 2. Standard-matter closure

The exact full-CLASS matter sector must either:

- receive additional explicit source blocks; or
- be replaced by a separately preregistered controlled late-time effective-dust approximation with an independently frozen truncation-error gate.

Repair01 itself licenses neither choice.

## Claim boundary

This result does not solve `Z20` or `Z21`, does not introduce finite eta and does not make nonlinear-collapse, halo, lensing or observational claims.
