# GE19 Repair30 reduced H2/Z11 reclosure — result freeze

## Status

First Repair30 execution that produced a valid science JSON:

`GE19_REPAIR30_REDUCED_H2_Z11_RECLOSURE_FAIL`.

This is frozen as the historical Repair30 science result under the original preregistered gates.

It is not rerun or relabelled.

The result also exposes strong evidence that at least two failed gates are dominated by certification/normalization pathologies, so the next step is a separately preregistered artifact-only diagnostic audit rather than an immediate H4/Z21 solve.

## Local output provenance

Science JSON:

- SHA-256:
  `de2d282eb0729b12f96e08be434b7bc0a320a606dd96d94057f1a2c94af22ce5`;
- bytes:
  `66490`.

Science NPZ:

- SHA-256:
  `02d7d9d52ca53f2495b84e5a339d396b3f63f9b03d05fd5416dcd4012c454429`;
- bytes:
  `1082384`.

FULL log:

- SHA-256:
  `de2d282eb0729b12f96e08be434b7bc0a320a606dd96d94057f1a2c94af22ce5`;
- bytes:
  `66490`.

Outer runner log:

- SHA-256:
  `d0d157fb7c9dba8cd95613540b3b11b1efa201409cb32cae3749b4decac61b3b`;
- bytes:
  `68084`.

The science JSON and FULL log are byte-identical.

Runner terminal route:

`GE19_REPAIR30_VALID_SCIENCE_FAIL_FREEZE_REQUIRED`.

## Passed controls

- parent hashes exact;
- GE05 normalized M1 symbolic identities exact;
- Repair27 B10 Nt128/Nt64 relative L2:
  `1.5452075499280114e-05`;
- linear-system relative L2:
  `4.4088853708561523e-16`;
- anisotropy backward error:
  `2.1064015525639715e-16`;
- initial dynamic boundary abs-or-rel:
  `1.7462031549538564e-21`;
- chi11 C-envelope relative L2:
  `2.4121909519463178e-04`;
- all outputs finite.

## Failed frozen gates

### Shift backward-error gate

Reported all-row maximum:

`0.9401687948604716`.

Frozen threshold:

`1e-6`.

However the worst reported mode has absolute shift residual only

`8.986480000960655e-23`

with a row scale of order

`1.9250641370845685e-21`.

This has the same qualitative signature as the previously frozen GE19 near-null shift-monitor pathology. Repair22 certification had already replaced an all-row interpretation by an active-row plus near-null absolute-residual treatment. Repair30 reused the raw all-row monitor.

Therefore this failed gate must not be interpreted as evidence of a large absolute equation violation without a dedicated near-null re-audit.

### Nt128/Nt64 state gate

Reported max per-field relative L2:

`0.96288293836063`.

The failure is entirely localized to the algebraic reduced dust-density coordinate `delta_varrho`.

For C_star the per-field controls are:

- N: `0.0018212508453560893`;
- S: `0.0016023936729083245`;
- u: `0.0003954887833823978`;
- varphi: `0.0005414034137820233`;
- T: `0.003267950727445378`;
- delta_varrho: `0.9549690055364972`.

The direct all-state global relative L2 reconstructed from the frozen NPZ is only

`0.0003954887835507251`

for C_star.

The dynamic-subset global relative L2 is

`0.0003954887833823978`.

Thus five of six reduced fields satisfy the 0.005 scale individually and the complete state is globally converged; the max-per-field gate is dominated by a near-zero algebraic dust-density coordinate.

The absolute Nt128/Nt64 delta_varrho L2 difference for C_star is

`5.93604241614674e-09`.

This requires a separately frozen normalization audit. Repair30 itself is not relabelled.

### Reduced chi11 versus Repair29B R2 parent

This is the remaining substantive mismatch.

Maximum C-envelope parent mismatch:

`0.4041196853909437`.

Per C:

- C_min:
  `0.4038626232978878`;
- C_star:
  `0.4039755940458639`;
- C_max:
  `0.4041196853909437`.

The mismatch is almost C-independent, while the C-envelope spread is only

`2.4121909519463178e-04`.

From the frozen NPZ, each of the six k modes has temporal-shape cosine approximately

`0.9990754`

against the Repair29B R2 parent.

A best complex rescaling of the reduced chi11 requires approximately

`1.67239`

and leaves a post-fit relative mismatch of approximately

`0.0430`.

The inherited a=0.4 chi11 boundary itself matches to machine precision.

This pattern is coherent and mode-independent, which points to a systematic reduced-H2 dictionary/source-normalization or closure mismatch rather than random Nt resolution noise. It is not yet sufficient to identify which dictionary factor is wrong.

## Scientific interpretation

Repair30 does not certify reduced Z11.

H4/Z21 remains blocked.

At the same time, the result does not support interpreting the raw 0.94 shift number or the 0.96 state number as physical instabilities:

- the main solve residual is at machine precision;
- B10 is Nt-converged;
- the dynamic reduced state is Nt-converged;
- the shift absolute residual is tiny;
- the large state metric is isolated to the near-zero algebraic dust-density coordinate;
- the chi11 mismatch is a coherent amplitude-level discrepancy.

Therefore the next licensed step is not a repeated Repair30 solve and not H4/Z21.

It is a separately preregistered artifact-only Repair31 audit of:

1. active versus near-null shift certification using the frozen Repair21/22 rule;
2. global/dynamic versus near-zero algebraic state normalization;
3. reduced/full chi11 modewise shape and amplitude;
4. exact GE05 raw-M1 to GE06 reduced-operator dictionary, including the relation to the frozen CLASS E-equation eta forcing.

## Canonical status

**Repair30 = historical science FAIL under its frozen gates. Reduced Z11 remains NOT CERTIFIED. H4/Z21 remains BLOCKED. Repair31 diagnostic audit is next.**
