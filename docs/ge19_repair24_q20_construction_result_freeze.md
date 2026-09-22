# GE19 Repair24 q20 construction result freeze

## Status

Frozen first valid post-implementation Repair24 science execution.

Final classification:

`GE19_REPAIR24_Q20_CONSTRUCTION_FAIL`.

This is a **science FAIL**, not an implementation failure.

Repair22 remains Z20 certified.

Repair23 remains q20 normalization/equation bridge PASS.

Repair24 does **not** certify q20 and does not license H4/Z21.

## Frozen local artifacts

Outer local runner:

- bytes: `7832`;
- SHA-256:
  `cb1e79438f6aac558c428e600fe6f476b099f1afc44ad4929019d8dac28d156b`.

Science JSON:

- bytes: `7496`;
- SHA-256:
  `71f463524b47f72d2c5082667fe99141d2286ebc2938c4eed6b89a1583339f2a`.

Inner FULL log:

- bytes: `7496`;
- SHA-256:
  `71f463524b47f72d2c5082667fe99141d2286ebc2938c4eed6b89a1583339f2a`.

Science NPZ:

- bytes: `3551600`;
- SHA-256:
  `6591adf8659cb96eda55eae32613424c0464cd42a9d20e0872371fb9254814f4`.

The JSON and FULL log are byte-identical because the science script prints the JSON payload directly.

## Frozen provenance

The run reproduces the frozen parent hashes exactly:

- Repair22 JSON:
  `7d53b2458183c6b2cc326acdded70b2c3ce1fab959d8456e56d3b4f1f86ef374`;
- Repair22 NPZ:
  `3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16`;
- Repair13 JSON:
  `ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7`;
- Repair13 NPZ:
  `011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3`;
- v0.77 artifact run:
  `34315590099`;
- v0.77 artifact ID:
  `10090367181`;
- frozen artifact digest:
  `sha256:24b97e5738eb07be4f12d433ff5f9fe22249e199e186d5617aca5dc81f748378`.

The runner passed:

- Repair24 lock audit;
- frozen GE19 input audit;
- frozen v0.77 artifact audit.

The q20 science construction itself then executed to completion.

## Background and boundary provenance

Repair24 Nt64 backgrounds reproduce the frozen Repair13 Nt64 primary arrays exactly:

- C_min: `0.0`;
- C_star: `0.0`;
- C_max: `0.0`.

Repair24 Nt128 backgrounds are rebuilt deterministically with the frozen Repair13 `reduced_background` function on the target grid, as preregistered after the pre-science implementation repair.

The exact frozen v0.77 bracket is reproduced:

- `a_lo=0.3799548579266745`;
- `a_hi=0.41924557250685585`;
- partial-step fraction in ln(a):
  `0.5224573485469814`;
- target a mismatch:
  `0.0`;
- k relative mismatch:
  `0.0`;
- common-time mismatch:
  `0.0`.

Therefore the FAIL is not caused by moving the GE19 initial surface.

## q20 numerical controls

Every convergence/control gate except the initial first-order drive bridge passes.

### Normalized source and interval propagation

- normalized c2 sqrt(w) cancellation:
  PASS;
- vectorized interval propagator self-test:
  `0.0`.

### Spatial source convergence

Nx256 versus Nx512 low-mode G2 relative L2:

`2.2947298319652412e-15`.

Frozen threshold:

`1e-10`.

PASS.

### Drude quadrature convergence

Nq1024 versus Nq2048 weighted-z20 relative L2:

`8.251855068695476e-05`.

Frozen threshold:

`1e-2`.

PASS.

### Time convergence

Nt64 versus Nt128 weighted-z20 relative L2:

`3.245459862000118e-05`.

Frozen threshold:

`5e-3`.

PASS.

First-order weighted-z10 Nt64 versus Nt128 relative L2:

`0.003453755379112942`.

Frozen threshold:

`5e-3`.

PASS.

### Finiteness and completeness

- all weighted q20 outputs finite: PASS;
- all C,beta,m cases complete: PASS.

## Sole failed gate

The only failed frozen gate is

`H1_X10_initial_match_abs_or_rel_le_1e10`.

Measured maximum:

`0.9999999471925649`.

Frozen threshold:

`1e-10`.

Therefore the current v0.77 -> GE19 first-order bath-boundary dictionary is not certified.

This gate is upstream of q20 certification because z10 at the GE19 initial surface supplies the first-order bath state entering the second-directional G2 source.

## Constructed-but-not-certified q20 telemetry

The numerical q20 construction itself is stable and finite.

Representative primary weighted-z20 L2 norms are approximately

`1.582e7`

across the C envelope.

Representative linear second-order drives:

- X20 L2 approximately `1.130e9`;
- B20_linear L2 approximately `1.114e9`.

Weighted G2 L2 is approximately

`0.0324--0.03525`.

Beta0 dependence is negligible at the displayed precision, consistent with the certified memory-off Z20 baseline.

These values are descriptive only because the first-order bath boundary bridge failed.

## Scientific interpretation

Repair24 localizes the remaining q20 blocker to the **initial first-order bath-drive bridge**, not to:

- the normalized second-directional bath equation;
- the GE05 G2 source generator;
- spatial reconstruction;
- Drude quadrature;
- time integration;
- Repair22 Z20;
- finiteness/completeness.

The frozen v0.77 trace stores the CLASS eta=0 AeST source

`chi_aest = Q_aest (theta_potential_aest + alpha_aest)`

and NL1C4 drives the bath with

`chi/a`.

The certified GE15/GE19 first-order state instead reconstructs the same physical drive through the local-jet variables and the on-shell reduced state.

Repair24 shows that the currently assumed direct normalization of those two representations at a=0.4 is wrong or incomplete.

No post-result rescaling is licensed.

## Next licensed diagnostic

A separately preregistered Repair25 may audit the first-order boundary dictionary only.

It should compare on the exact same a=0.4 surface:

1. frozen v0.77 transported `chi/a`;
2. frozen GE15 certified
   `chi=Q(a theta/k^2+alpha)`;
3. Repair22 on-shell
   `X10 = Q_action u10 + partial_x(varphi10)/a`.

Required diagnostics should include:

- per-mode complex/raw ratios;
- GE15 vs Repair22 closure;
- v0.77 vs GE15 closure;
- Q background ratios;
- best-fit global and per-mode multiplicative normalization residuals;
- shape closure on the full overlapping 0.4<=a<=0.8333... window if the two traces are both available;
- explicit tests of any candidate unit/normalization factors before one is adopted.

No q20 rerun, threshold relaxation or H4/Z21 solve is licensed until this boundary bridge is resolved and frozen.

## Stop rule

- q20 not certified;
- `q20_constructed=false` in the frozen science classification;
- `q20_certified_projection=false`;
- `Z21_licensed_after_freeze=false`.

Repair22 Z20 certification remains unchanged.
