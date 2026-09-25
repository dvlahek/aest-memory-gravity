# GE19 H4F3d7r1 — actual physical original R1 interval-ODE versus sampled FD4 bath diagnostic freeze

## Exact classification and claim boundary

**Frozen diagnostic classification: `GE19_H4F3D7R1_ACTUAL_PHYSICAL_DIAGNOSTIC_DECOMPOSITION_PASS_FULL_NOETHER_OPEN`.**

The original H4F3d7 physical Python report classifies its six cases
`GE19_H4F3D7_FD4_INTERVAL_ODE_DISCREPANCY_DECOMPOSED`.
The user-local versioned H4F3d7r1 runner ends with
`GE19_H4F3D7R1_PHYSICAL_DECOMPOSITION_PASS_FULL_NOETHER_OPEN`.
All six original physical `C x Nt` diagnostic cases have `pass=true`:
`C_min,C_star,C_max` at `Nt=128` and `Nt=64`.
Every case includes all original 2048 R1 frequency nodes, six
positive modes, both one-sided interval ODE traces and all
four preregistered phase bins.

This is an **actual physical original-R1 bath diagnostic PASS**:
the original R1 interval-ODE contribution and the
finite-difference approximation defect are quantitatively
separated on the unchanged frozen physical trajectories.
It is **not** a newly asserted bath-on-shell smallness PASS,
not full physical all-sector H4 Noether, not certified Z21,
and not licensed lensing. The original H4F3d6 near-unit sampled
bath Euler residual remains numerically present; its
derivative-discretization discrepancy is now localized.

## Physical artifact chain and exact hashes

Uploaded original user-local files were read directly and
compared with the actual versioned runner log.

| Physical output | SHA-256 | Bytes |
| --- | --- | ---: |
| `ge19_h4f3d7r1_physical_r1_fd4_vs_interval_ode.json` | `031229d570d29ae9c4ea0ab8e25222d94e9cda4520c991cd203e9d7b97e01dc9` | 35579 |
| `ge19_h4f3d7r1_physical_r1_fd4_vs_interval_ode.npz` | `4f011c96c2c11165df6332eafc459c5d2c5e7bc5164a436bde3d1563696f0e13` | 147857 |
| `ge19_h4f3d7r1_physical_r1_fd4_vs_interval_ode_FULL.log` | `031229d570d29ae9c4ea0ab8e25222d94e9cda4520c991cd203e9d7b97e01dc9` | 35579 |
| `ge19_H4F3D7R1_LOCAL_runner.log` | `39b1809b22c817ae25cb81ffaa7f52d7f2e2d537a86c90346515405a5d5b997f` | 4376 |

The FULL log is **byte-identical** to JSON. All JSON,
NPZ and FULL hashes/lengths printed by the original
local runner exactly match the uploaded file bytes.
The runner logged head
`e9987882493feee2461c43c969b4624cff3ba4eb`,
versioned runner blob
`6bdee189cf795a04e4d1b19822af6ed778b5af46`,
and all locked H4F3b/H4F3d6/R1 and parent preexecution
hash gates PASS. These original raw parent physical files
were checked by the *local runner*, not reuploaded here.

The original H4F3d7 code
`b598a5cc49b3d87827b4758c55d3ce7f3a1198a8`
and original H4F3d7 predata
`ccf3185b4f790d9d6068f80beb39a442b186158c`
remain immutable. The user ran separately versioned
single-expression finiteness-repaired module
`e4cb9d6638b427368647a29b86ccf5445b43d7a2`,
whose exact original-code diff passed static regression
[Actions 36153973088](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36153973088).
Original failed H4F3d7 FULL log was not overwritten.

The machine-readable independent archive audit manifest
`ge19/h4f3d7r1_actual_physical_discrepancy_independent_archive_audit.json`
is separately committed at blob
`b85b3bbd80603ed324a6cc54b0080489167fef31`.
Only a report/manifest is stored in Git: the uploaded
binary physical NPZ remains identified by the SHA-256 above
and is **not** claimed to be committed to GitHub.

## Six frozen physical cohorts

All listed norms are the original program's diagnostic
quantities, not newly fitted targets. The `relative`
column is the original report-only
`R_FD4_relative_original_natural_report_only`.

| C | Nt | Sampled FD4 L2 | FD4 relative (report-only) | R1 interval ODE left L2 | R1 interval ODE right L2 | Sampled derivative defect left L2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| C_min | 128 | 9.532128838e-5 | 0.998501801 | 2.243717902e-11 | 2.205252688e-11 | 9.532127484e-5 |
| C_star | 128 | 9.684778205e-5 | 0.998639636 | 2.241378491e-11 | 2.201680192e-11 | 9.684776850e-5 |
| C_max | 128 | 9.269917660e-5 | 0.998585464 | 2.242389484e-11 | 2.203665927e-11 | 9.269916165e-5 |
| C_min | 64 | 6.724022398e-5 | 0.998999059 | 3.207639590e-11 | 3.096433024e-11 | 6.724014217e-5 |
| C_star | 64 | 6.627074249e-5 | 0.999341193 | 3.212391747e-11 | 3.099945867e-11 | 6.627065479e-5 |
| C_max | 64 | 6.584600693e-5 | 0.998872137 | 3.221939211e-11 | 3.108027719e-11 | 6.584591321e-5 |

The maximal registered normalized algebraic identity
discrepancy in any of the six cases is
`2.289808148773898e-16`; frozen original tolerances
are unchanged. Original R1 weighted `z10` reproduction
and H4F3d6 sampled bath Euler absolute-norm reproduction
are both exactly zero in all six saved reports.

On `Nt=128`, the original `phi>=1` bin contains
2527 of 260096 **node-interval pairs** in each C cohort.
It contains between `0.9999999999996148` and
`0.9999999999996467` of the **squared L2 norm of the
left sampled derivative defect**. On `Nt=64`, the same
original bin contains 1789 of 129024 node-interval pairs
and between `0.9999999999993796` and
`0.999999999999405` of the squared left defect norm.
This describes *which original, unremoved, high-phase
nodes dominate the sampled FD4 discrepancy*. It does not
omit those nodes or replace the original physical bath
operator by a different high-frequency solver.

## Independent uploaded JSON/NPZ/runner integrity audit

From the uploaded files, a separate reader verified:

1. Exactly six unique original `(C,Nt)` cases, every
   original JSON diagnostic gate true, all reported
   frozen parent/code locks true, and 2048 nodes and
   six positive modes in every case.
2. Exactly 44 expected NPZ arrays, all numeric and finite,
   exact key set, proper `6xNt` sampled-FD4 and
   `6x(Nt-1)` one-sided/defect array shapes, phase
   count shapes, and matching strictly increasing
   shared `x` grids.
3. All five independently recomputed NPZ mode-time
   L2 norms per case agree with their JSON absolute
   L2 summaries at relative tolerance `1e-12`
   (cross-check tolerance for archive comparison only,
   **not a new physical certification threshold**).
4. Every original four-bin count sums exactly to
   `2048*(Nt-1)`, and the squared per-bin original
   interval-ODE and sampled-defect norms recombine
   to both original global one-sided norms.
5. Every uploaded SHA and length equals the user-local
   runner log, the FULL log equals JSON byte-for-byte,
   and the exact locked original-code/parent-input
   preflight and explicit final PASS marker are present.

The uploaded D7r1 NPZ stores aggregated mode-time
norms and phase-bin counts, **not** the original
`2048x6xNt` complex physical trajectories.
The raw H3F, H3G, Z11, H4F3b/H4F3d6 and R1 source
binary files were not part of these four uploads.
The independent archive audit therefore validates
the saved original physical diagnostic and its recorded
local provenance but does **not** claim an independent
rerun of the original ODE from raw parent trajectories
in this environment.

## Physical interpretation and next gate

The high sampled FD4 Euler residual of roughly
`0.9985–0.9993` relative to its original natural
scale is real *as an FD4 diagnostic*. The unchanged
original R1 interval-ODE side residuals are only about
`2.2e-11` on the primary grid and `3.1e-11`
on the time control. The FD4-versus-original-ODE
identity closes at numerical precision, and the
sampled derivative defect almost entirely explains
the FD4 norm in the original `phi>=1` cohort.
Thus the near-unit sampled Euler value cannot be
promoted to a demonstrated **original-ODE bath
on-shell violation**. Conversely, small original
interval-side diagnostics alone cannot certify
the full covariant bath-action on-shell identity
or integrated all-sector H4 Ward.

Next: retain frozen original physical sources,
construct/evaluate **actual nonbath H4 parent Euler
and boundary residuals**, building on the restricted
independent symbolic H4F3d8 compiler PASS; then
check the *complete* integrated H4 Noether identity
with original bath/interface and operator contributions.
Use H4F3d9's already frozen exact FD4/FD8 structural
constants only with independently valid **actual**
high-derivative envelopes and floating arithmetic
bounds; the current conditional coefficients are
not a physical error budget. Do not use any
observation for theory tuning.

No changes to original phase bins, 2048 R1 nodes,
FD4/FD8 operators, action/source/clock, original
shift `1e-6`, matched temporal order `>=2.5`,
or old Repair37 SCIENCE_FAIL. No new bath on-shell
smallness gate or source-only Ward-zero shortcut.

**Full actual H4 Noether NOT CERTIFIED.
Window-local particular reduced Z21 NOT CERTIFIED.
Lensing BLOCKED.**
