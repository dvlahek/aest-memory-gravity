# GE19 H4F2h — valid physical-clock and discrete source Ward bridge

## Classification and scope

`GE19_H4F2H_PHYSICAL_CLOCK_DISCRETE_SOURCE_WARD_BRIDGE_PASS`.

This is a valid **manufactured source-only derivative representation
audit**. It resolves the independent clock/scheme issue before any
source-plus-operator/parent Ward evaluation on physical GE19 arrays.

It does **not** establish full H4F2 all-sector Noether compatibility,
perform corrected-parent numerical sampling, integrate Z21, certify
the original active shift constraint or license lensing.

The previously valid H4F2g signed six-piece source assembler
remains immutable and valid within its original **source-only
synthetic** scope.

## Frozen provenance

- preregistration:
  `ge19/h4f2h_predata_physical_clock_discrete_ward_bridge.json`,
  blob `dc5b29219d25c89d18b1bc37a7ce116f3818e349`;
- standalone physically clocked source Ward implementation:
  `ge19/h4f2h_physical_time_source_ward_bridge.py`,
  blob `65ce1e68a2f77e063c4bb8848d770abb4baeeebf`;
- deterministic exact/negative-control selftest:
  `ge19/h4f2h_physical_time_source_ward_selftest.py`,
  blob `248dc1e815d345b56ff51d065327773518a9a0ae`;
- dedicated Actions workflow:
  `.github/workflows/ge19-h4f2h-physical-clock-ward.yml`,
  blob `593b5769e45be18e095e613a946b4516a5e9e809`;
- valid Actions run `36053845610`, job `107815811239`,
  conclusion `success`;
- terminal marker:
  `GE19_H4F2H_PHYSICAL_CLOCK_DISCRETE_SOURCE_WARD_PASS`;
- uploaded Actions artifact ID: `10831362813`;
- artifact name:
  `ge19_h4f2h_physical_clock_discrete_source_ward`;
- result JSON:
  `results/ge19_h4f2h_physical_time_source_ward.json`;
- result JSON SHA-256:
  `efb37f8dc66188183995ecd9909396cf58fee8ec8b819bb2a5301f4a1bca21f7`.

The CI asserted all frozen parent blob, exact symbolic
chain-rule, six manufactured `Nt={64,128}` and
`beta={1,0.5,0.1}` controls, wrong-clock negative
controls, source-family linearity, original source-support
and invalid-input rejection gates. Every assertion passed.

## Exact physical time/derivative issue

The frozen GE19 background grid is
`x=ln(a)`, not physical proper time `t`.
The background dictionary contains the physical
`H=(1/a) da/dt` in compatible units. Therefore

`partial_t S_b(x) = H(x) partial_x S_b(x)`.

The original Repair37 GE06/GE07/Lambda H4
source path uses `Dt=H[:,None]*FD8_x`;
the original Repair07/GE05 memory path uses
`Dt=H[:,None]*FD4_x`.
The two derivative representations are
not identically interchangeable at finite
time resolution.

H4F2g's original source-only helper evaluates
`np.gradient(S_b,time)` at second order.
Its synthetic source-summation test is
valid for the supplied coordinate `time`,
but passing the GE19 `bg["x"]` to that
routine without the physical `H` would
compute `partial_{ln a}`, not
`partial_t`, and also impose a new
second-order rather than frozen FD8/FD4
discretization. Its output must not be
relabeled as the physical H4 Ward remainder.

H4F2h provides a separately versioned
source-only interface for the physical
projection, in the unchanged original
GE19 eight-row and Fourier convention:

`D_S21=H(x) D_x S_b21+
  (a(x)/3) i k (S_iso21+2S_aniso21)`.

Each source family carries its explicitly
registered derivative scheme: FD8 for
GE06, GE07 and Lambda; FD4 for GE05
M1 and M2. The NL0C Y piece has zero
metric/shift/anisotropy rows and hence
exactly zero source-Ward projection;
its reported scheme cannot affect
the physical source-Ward scalar.

The bridge returns the sum of the
**separately differentiated** source
pieces. Applying a single FD8 matrix
to the sum of FD8 and FD4 source
families is retained only as a
diagnostic comparator, not silently
identified with the original mixed
numerical representation.

## What has NOT been tested

This CI used deterministic manufactured
smooth source arrays, **not** the
separately certified H3F Z20, H3G
q20, original H1 or Z11 arrays.
It did not recompute any actual
GE06/GE07/Lambda/M2 H4 source
from corrected parents; did not
evaluate the linear-operator Ward
expression or the signed dust/bath/
background/H1/Z11/Z20/q20 parent
Euler residuals; and did not test
the early-window hotspot or full
original active window.

The next **separately preregistered**
gate must bind exact physical parent
artifacts, use one common time
representation, reproduce all six
real action-derived sources and
evaluate source + independently
derived operator + parent Ward
residuals with a registered
FD8/FD4 compatibility treatment.
A full Noether PASS must not be
inferred from the algebraic
manufactured-clock PASS.

Historical Repair37 remains science
FAIL; Repair38–44 remain diagnostics.
Original active shift threshold
`1e-6` is unchanged.
**Z21 NOT CERTIFIED; lensing blocked.**
