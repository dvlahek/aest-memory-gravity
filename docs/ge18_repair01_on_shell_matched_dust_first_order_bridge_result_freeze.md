# GE18 Repair01 on-shell matched-dust first-order bridge — result freeze

## Status

First locked GE18 Repair01 execution completed with terminal classification

`GE18_REPAIR01_ON_SHELL_MATCHED_DUST_FIRST_ORDER_BRIDGE_PASS`.

Historical GE18 remains

`GE18_ON_SHELL_MATCHED_DUST_FIRST_ORDER_BRIDGE_FAIL`.

## Local result provenance

Repository HEAD used by the locked Repair01 runner:

`13afb23c3da44c4f3b5cb61a3588ce622a751592`.

Uploaded local result files:

- JSON:
  - bytes `21121`;
  - SHA-256 `877cca7c2999316e9770b62ad6d34cdf717ee0a7744b449633d54cb951034261`;
- NPZ:
  - bytes `116913`;
  - SHA-256 `b6ccaf2257fbb09df701c43bc9a593a3f68238826277a510a0b3b531ea9fa6fe`;
- full log:
  - bytes `21121`;
  - SHA-256 `877cca7c2999316e9770b62ad6d34cdf717ee0a7744b449633d54cb951034261`;
- runner log:
  - bytes `23626`;
  - SHA-256 `5dd568e2a95c6217e33fe4cabe0b107bea9930242536f024770fff03213ec664`.

The JSON and full log are byte-identical because the diagnostic prints the JSON payload directly.

## Provenance result

All native provenance gates pass.

- parent GE15 classification is
  `GE15_CANCELLATION_FREE_S_STATE_PRECISION_CLOSURE_PASS`;
- R1 dense SHA equals the value frozen by GE15 exactly:
  `7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f`;
- dense accepted-step trace versus raw CLASS perturbations has
  abs-or-rel maximum `0.0`;
- requested-k relative-miss gate passes.

The historical mixed 64-node interpolation comparison remains visible as

`7.590304690330285e-8`

but is descriptive only, exactly as preregistered for Repair01.

## On-shell dust convergence

Primary/control DOP853 convergence:

- density global relative L2 maximum:
  `7.73203670933738e-9`;
- momentum global relative L2 maximum:
  `7.774364641179449e-9`.

Both remain below the frozen `1e-8` limits.

Initial absolute-density and absolute-momentum matches both pass the frozen
`1e-10` gates.

The exact dust-potential identity closes at

`max abs-or-rel(dot(T1),psi)=8.326672684688674e-17`

against the frozen `1e-9` limit.

All outputs are finite.

## Exact GE07 map certified

For each frozen dust background

`rho_d=C/a^3`

the certified map is

`varrho_bar=3 C/a^3`;

`delta varrho=3 rho_d delta_d`;

`T_1=a theta_d/k^2`;

`delta T_t=psi`;

`delta T_x=-a theta_d/k`

for the sine-phase spatial component.

No extra matter degree of freedom or coupling is introduced.

## Frozen matter backgrounds

CLASS-density normalizations:

- `C_min=2.566238549760586e-9`;
- `C_star=2.568543329983919e-9`;
- `C_max=2.5714842087496506e-9`.

## Descriptive model discrepancy versus full standard CLASS matter

No model-error acceptance gate is applied.

For the central `C_star` pressureless surrogate:

- density global relative L2:
  `1.3765302104657398e-3`;
- density pointwise relative maximum:
  `5.069139301271249e-3`;
- momentum global relative L2:
  `6.891936293682233e-3`;
- momentum pointwise relative maximum:
  `1.778016087606809e-2`.

These are reduced-model systematics, not numerical integration errors.

The GE17 background-normalization envelope produces much smaller shifts relative to the central dust solution:

- C_min density global L2:
  `4.3793528365838954e-5`;
- C_max density global L2:
  `5.58765717440552e-5`;
- C_min momentum global L2:
  `2.1965036600727895e-4`;
- C_max momentum global L2:
  `2.8020843420250804e-4`.

## Project boundary

The Repair01 result certifies

`on_shell_reduced_dust_Z10_certified=true`

and

`reduced_H3_Z20_input_bridge_ready=true`.

It does not declare effective dust exact.

It does not license or claim a full-species second-order CLASS solution.

Historical GE18 remains FAIL.

## Licensed continuation

A reduced-H3 Z20 computation is now licensed, provided that:

1. the first-order gravitational/AeST input is the frozen GE15 cancellation-free local jet;
2. the matter input is the frozen GE18 Repair01 on-shell pressureless bridge;
3. the central solve uses `C_star`;
4. the same H3 solve is repeated for `C_min` and `C_max`;
5. the spread is reported as the frozen background-normalization matter envelope;
6. the larger descriptive discrepancy between the reduced dust and full standard CLASS first-order state is carried explicitly as an external reduced-model systematic and is not hidden by the C envelope;
7. the result is called a **reduced-H3 Z20 solution**, not a full-species Z20 solution.

## Claim boundary

GE18 Repair01 closes the first-order reduced matter bridge needed by GE07/H3.

It does not itself solve Z20, introduce finite eta, or establish a nonlinear observable.
