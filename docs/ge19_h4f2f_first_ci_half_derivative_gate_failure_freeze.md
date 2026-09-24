# GE19 H4F2f — first CI half-derivative gate implementation failure (immutable)

## Exact frozen first outcome

Run `36030973726`, job `107739337676`,
workflow `.github/workflows/ge19-h4f2f-ge06-ward-shift.yml`,
conclusion `failure`, implementation blob
`851edb2c393c531732c97b8dcaa24c36bc63882d`,
predata blob `551294c5763b086919c9f27076a922c29ca953e5`.

Failed-run artifact `10822295746` contains the original
4187-byte JSON and identical FULL log, both SHA-256
`42feee656d907b281a49bb43be40311520760d2b00d6d3de57391675e0c735e2`.
The raw result classification is
`GE19_H4F2F_GE06_ACTION_SHIFT_SOURCE_SUBSET_FAIL`.

All exact frozen blob checks, actual frozen action bindings,
all 10 coframe/jet Ward and density gates, both GE06
mixed direct-vs-polarization and reverse-direction
checks, and both deterministic GE06 `f_c2`
numerical checks passed. In particular, all
sampled numeric outputs were finite and
the b_f and b_x relative errors were 0.0
and `1.6592729300491167e-16`.

The only false gates, for both `b_f` and `b_x`,
were named
`original_minus_two_source_equals_negative_physical_mixed`.

## Precisely localized factor-two mistake in the audit

The test defined

`physical_mixed = (1/2) sum_d (partial_d c2) eta_d`,

and independently verified

`physical_mixed = Q_bilinear = [c2(d+eta)-c2(d-eta)]/4`.

But the **full** physical mixed derivative is

`d_eta [c2(d+eta e)]|eta=0
 = sum_d (partial_d c2) e_d
 = 2 Q_bilinear`.

The unchanged frozen GE19 source is
`S_GE06 = -2 Q_bilinear`,
therefore `S_GE06 = -d_eta c2`.
The failed audit incorrectly required
`-2 Q_bilinear = -physical_mixed`,
which is off by a factor of two **inside the test
definition**, not in the frozen action or source.

The narrow prospective repair changes ONLY
the failed audit equality to

`-2 Q_bilinear = -2 physical_mixed`,

and renames its gate so the half/full convention
is explicit. Preregistration, frozen source,
mixed generator, inherited signs, original
`1e-6` H4 shift target and all parent files
remain unchanged.

This first result is an **audit implementation
failure**, not evidence of an action inconsistency
or an H4/Z21 science failure. It is not relabelled
by any later valid run.

No corrected H3F/H3G common-grid source
evaluation or H4/Z21 state solve was performed.
Full six-piece Noether remains open;
Z21 NOT CERTIFIED and lensing blocked.
