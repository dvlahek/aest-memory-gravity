# GE19 H4F3d9 — original FD4/FD8 exact stencil constants; physical error budget OPEN

## Frozen result

**Classification:** `GE19_H4F3D9_EXACT_FD4_FD8_STENCIL_CONSTANTS_PASS_PHYSICAL_BUDGET_OPEN`.

The restricted AST-only compiler independently extracted every exact
original FD4 five-point and FD8 nine-point finite-difference row
directly from their pinned historical production-source files. For
each edge and interior row it proved the complete rational monomial
moment identities through degree 4 or 8 and calculated exact rational
conditional Taylor-error constants. Neither the production FD4/FD8
implementation nor any source/parent/threshold was modified.

This establishes only the *stencil* component of an independently
preregistered full-H4 numerical error protocol. It does NOT certify
physical C5/C9 regularity, actual high-derivative envelopes,
piecewise-R1 interval derivatives, Y zero-gradient smoothness,
roundoff propagation, a full physical FD4/FD8 tolerance, all-parent
H4 Noether, Z21 or lensing.

## Immutable provenance and CI

- Original preregistration `ge19/h4f3d9_predata_original_fd4_fd8_structural_error_budget.json`,
  blob `98e6fd8835fdbe3bd169d062431eefe80a3e9232`, unchanged.
- Versioned, single-SHA provenance amendment
  `ge19/h4f3d9_predata_amendment01_correct_d7_git_blob.json`,
  blob `34cea0c62ef2dc962bc43ef93b2fbbd70b9c2180`.
  The original prereg accidentally copied only the H4F3d7 source
  SHA incorrectly. No scientific equation, tolerance or cohort
  was amended. All other eight source pins were independently
  compared to the actual Git blobs and were exact.
- Original frozen physical H4F3d7 code blob:
  `b598a5cc49b3d87827b4758c55d3ce7f3a1198a8`
  (the only correction in the versioned provenance amendment).
- Final AST-only independent compiler
  `ge19/h4f3d9_exact_original_fd4_fd8_stencil_budget_compiler.py`,
  blob `03864a08110e341038056dd4cefd5842d4a5eb1e`.
- Dedicated CI `.github/workflows/ge19-h4f3d9-original-fd4-fd8-stencil-budget.yml`,
  blob `d708be67bf9a6bc139c83951160cc36939c4f9a2`.
- Compiler/workflow atomic SHA-amendment lock commit
  `6e7d25680ce672a37a4b8f20b62a1de99a7aa84f`.
- [GitHub Actions run 36152551838](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36152551838):
  job `108129154468`, **success**, terminal marker
  `GE19_H4F3D9_ORIGINAL_STENCIL_CONSTANTS_PASS_PHYSICAL_BUDGET_OPEN`.
- Successful 16,783-byte JSON artifact
  `results/ge19_h4f3d9_exact_fd4_fd8_stencil_budget_compiler.json`,
  SHA-256
  `27ba90ea35b074f6036aff7a41fbc4e27c4a2ead2291daf806f8bdc2e3d40461`.
  GitHub artifact ID `10871484108`.

The earlier initial CI run
[36152370247](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36152370247)
**failed safely** on the incorrect preregistered H4F3d7 blob,
BEFORE running a stencil derivation. It is an implementation/
provenance STOP, not a physical diagnostic; it has not been
reclassified. The original preregistration remains available,
with a separate explicit single-pin amendment and exact pin
for the amendment itself.

## Source-bound exact algebra and scientific boundary

For each original row `i`, write the fixed rational
dimensionless weights `c_ij=h D_ij` and the integer offsets
`s_j=j-i`. The compiler independently verifies in rational
arithmetic

`sum_j c_ij s_j^k = 1` for `k=1`, and
`sum_j c_ij s_j^k = 0` for all other `0<=k<=p`,
with `p=4` or `p=8`.

For each original endpoint or interior row, the registered
conditional remainder factor is the exact rational number

`K_(p,i)=[sum_j abs(c_ij) abs(s_j)^(p+1)]/(p+1)!`.

ONLY for a function `f` with independently proved bounded
`(p+1)`th derivative on its WHOLE stencil interval does this
give

`abs(D_p f_i - f'_i) <= h^p K_(p,i) M_(p+1,i)`,

where `M_(p+1,i)=sup_stencil abs(f^(p+1))`.
The outer one-sided rows have their own exact `K_(p,i)`;
the central coefficient cannot be substituted at the edges.
The original FD4 matrix has five distinct row types, FD8 nine.

The original canonical operator differentiates its entire
`Cmat*w` product by FD4. The six actual source families
retain their separately frozen FD8 (GE06/GE07/Lambda/Y)
or FD4 (GE05 M1/M2) physical-clock schemes. The
signed Euler-parent/action-boundary numerical errors
require a separate action-derived termwise propagation
bound, not a synthetic source-only Ward zero gate.

The exact full-H4 error-budget *formula/procedure* is now
preregistered in H4F3d9 predata. Its independent physical
`M5/M9` derivative envelopes, original stepwise R1
differentiability, Y zero-set lower-regularity alternative
and operation-level roundoff proof are **not yet
available or numerically certified**. The actual full-H4
numeric structural tolerance remains UNDEFINED until
those requirements are frozen before any integrated
physical residual calculation. The near-unit H4F3d6 bath
Euler residual and any nonzero H4F3d7 interval-ODE
residual are not permitted as an a posteriori error floor.

## Next gate

1. Execute the already static-PASS locked physical
   H4F3d7 local runner ONLY on the original certified
   user-local source/parent/R1 bytes. Freeze both
   original one-sided interval results, all nodes and bins.
2. Derive/evaluate missing GE06/Y, GE07/Lambda and
   all signed background/H1/Z11/H3F/H3G Euler
   and lower-boundary terms on the same original
   actual H4F3b grids.
3. Independently certify and freeze the physical
   derivative/regularity and floating-point bounds,
   then define the full structural error budget
   without observing or fitting the full Ward defect.
4. ONLY THEN attempt the integrated original
   canonical `W_operator+W_six_source+W_all_parent`
   all-cohort physical H4 test.

**No full actual H4 Noether PASS. No Z21 certification.
No lensing. Repair37 SCIENCE_FAIL unchanged.
Original active shift <=1e-6 and time order >=2.5 unchanged.**
