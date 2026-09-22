# GE19 Repair29B targeted R3 full-state eta-tangent precision closure — implementation lock

## Scope

Repair29B is a separately preregistered numerical precision follow-up to frozen Repair28 and artifact-only Repair29A.

It was preregistered and implemented before the Repair29A localization result was known.

It cannot choose target lambda values manually. The only permitted target set is the deterministic set emitted by the frozen Repair29A selector.

Repair29B does not relabel Repair28.

## Frozen files

Preregistration:

- file:
  `ge19/repair29b_predata_r3_full_state_tangent_precision_closure.json`;
- blob:
  `22e38e3462288ae3e9eacc6ddc0c703ad4081b57`;
- commit:
  `a25b82be6785612ff62401a93f771085342cecad`.

R3 precision file:

- file:
  `ge19/pre/R3_repair29b.pre`;
- blob:
  `5b6f992e426124f40eea14ee0f4730d111ce9ee7`;
- commit:
  `9b621e807bcdf763ffc24b3cad3301ee3edba090`.

Implementation:

- file:
  `ge19/repair29b_r3_full_state_tangent_precision_closure.py`;
- blob:
  `ac0085148ad3032758c36b9593461285a9fdc152`;
- commit:
  `a1874cfdca60751319b1160003757a899de34db7`.

Dedicated prelock workflow:

- file:
  `.github/workflows/ge19-repair29b-prelock-audit.yml`;
- blob:
  `606998b4e178fc5d3efdb3cd829b1f9997652394`;
- commit:
  `a618f5d7775bd38208d2c7feab04d683225d8b78`;
- successful run:
  `35741531144`;
- job:
  `106792246438`.

Global static audits also passed for the Repair29B preregistration, R3 precision file and implementation commits.

## Frozen R3 refinement

R1:

- `tol_perturbations_integration = 2.5e-8`;
- `perturbations_sampling_stepsize = 0.00125`.

R2:

- `1.25e-8`;
- `0.000625`.

R3:

- `6.25e-9`;
- `0.0003125`.

R3 is therefore the exact next factor-two refinement of both frozen controls.

## Frozen selector

Repair29B must read the successful Repair29A result and recompute the target set from:

1. the R1 global-worst field/lambda pair;
2. the R2 global-worst field/lambda pair;
3. every R1 field/lambda pair whose Repair28 even residual exceeded `5e-3`.

The recomputed target-lambda set must exactly equal the set stored by Repair29A.

No result-informed manual additions or removals are allowed.

## Frozen normalization

For each R3 target field/lambda pair,

[
R_{even}^{R3}
=
\frac{\|x_+^{R3}+x_-^{R3}-2x_0^{R3}\|_2}
{2|\lambda|\,\|\bar x_{,\eta}^{R2}\|_2}.
]

The denominator is the already frozen Repair28/Repair29A R2 consensus tangent.

No R3 consensus is fitted.

R3 tangent precision is compared against the already frozen R2 same-lambda tangent.

## Frozen gates

- forcing 1024/2048 relative L2 <= `1e-2`;
- forcing cosine >= `0.9999`;
- requested-k mismatch <= `1e-12`;
- background-grid mismatch <= `1e-12`;
- R3 vs R2 same-lambda tangent relative L2 <= `5e-3`;
- every tracked R3 even residual <= historical Repair28 limit `5e-3`;
- every tracked R3 even residual <= its corresponding R2 value;
- all outputs finite.

## PASS meaning

A PASS may certify:

`R2 primary complete eta-tangent representation with targeted R3 numerical control`.

It may then license a separately preregistered reduced H2/Z11 reclosure.

It does not:

- relabel Repair28;
- solve reduced Z11;
- solve H4/Z21;
- introduce finite eta;
- make observational claims.
