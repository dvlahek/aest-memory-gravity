# GE19 / GravitationalElasticy — complete new-chat handoff (25 September 2026)

## Read this first

This is a self-contained continuation handoff for the project `dvlahek/aest-memory-gravity`, branch `physics-first-gravitational-elasticity`. The canonical detailed chronological log is [ge19_history.md](ge19_history.md). Verify live GitHub Actions status and the branch HEAD before changing code. The scientific theme is **gravitational elasticity with memory**: “gravitacija ima memoriju,” with a covariant NL0B Maxwell/viscoelastic memory realization in AeST. The immediate GE19 physics objective is a mathematically and numerically defensible corrected H4 mixed directional parent and ultimately a certified window-local particular `Z21`, before any lensing/observational claim.

**Strict current scientific status:** Corrected H3F `Z20` and H3G normalized-bath weighted `q20` are certified within their frozen low-mode window-local scope; actual H4F3b six-piece corrected H4 *source* is valid; H4F3d4 complete signed mixed Ward *formal* ledger is valid; H4F3d6 actual normalized-bath Ward *subset* is valid; H4F3d7 frozen R1 ODE–FD4 *compiler/manufactured* diagnostic has passed Actions. However, **the physical H4F3d7 decomposition has NOT been executed, full actual all-parent/operator H4 Ward Noether is NOT CERTIFIED, Z21 is NOT CERTIFIED, and lensing is BLOCKED**. Never call a manufactured/compiler PASS a physical/Noether science PASS.

## Exact latest Actions verified September 25, 2026

All most recent queried runs on the project branch finished `success`; the latest specific new result was [H4F3d7 compiler run 36148151670](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36148151670), job `108114383440`, marker `GE19_H4F3D7_R1_FD4_COMPILER_PASS_PHYSICAL_OPEN`, classification `GE19_H4F3D7_FROZEN_ODE_FD4_COMPILER_PASS_PHYSICAL_OPEN`. CI JSON 10,828 bytes SHA-256 `6a6fb22b1c25ee0ee66755eb8a82899b3cdf8292c1678e7f4c989922b94ed66d`, artifact ID `10869873062`. Independent prelock [36137851501](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36137851501) also passed. Immutable result: [ge19_h4f3d7_r1_fd4_compiler_valid_freeze.md](ge19_h4f3d7_r1_fd4_compiler_valid_freeze.md). Prereg `ge19/h4f3d7_predata_bath_fd4_vs_original_r1_interval_ode.json` blob `ccf3185b4f790d9d6068f80beb39a442b186158c`; code `ge19/h4f3d7_bath_fd4_vs_original_r1_interval_ode.py` blob `b598a5cc49b3d87827b4758c55d3ce7f3a1198a8`.

Other valid recent CI: H4F3d5 normalized Euler [36126850777](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36126850777); H4F3d6 actual bath *compiler* [36127944207](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36127944207); H4F3d6 local runner static [36128447037](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36128447037); H4F3d4 formal ledger [36106532215](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36106532215); H4F3d3 eta-regularized bath [36105927210](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36105927210); H4F3d2 dust/bath currents [36103744644](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36103744644); H4F3d1 canonical original operator [36102755011](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36102755011). These are separately scoped results, not full physical H4 Noether.

## Certified physical inputs — do not recompute casually or relabel

- H3F corrected complete-NL0C-Y scalar **and aether** source `Z20`: `GE19_H3F_CORRECTED_Y_H3_Z20_CERTIFIED`, original active shift Linf `8.067171756100188e-7` against UNCHANGED `1e-6`; matched Linf/L2 temporal orders `3.2357755676907107`/`3.1225511608309504` (both >=2.5); frozen Repair22 old-Y replay relative differences 0.0. JSON SHA `0616188d2bb7a6c09b2b56433a1f8a1860f360b2e54d2cb84e1ae214a407866b`; NPZ SHA `90840755fa9febb1d8cb84609d9e58f67dec2a0a01cd6bf8e47685b45caa4542`. Freeze [ge19_h3f_corrected_y_z20_valid_local_science_result_freeze.md](ge19_h3f_corrected_y_z20_valid_local_science_result_freeze.md).
- H3G corrected parent weighted normalized `q20`: `GE19_H3G_CORRECTED_Y_Q20_RECONSTRUCTION_PASS`; original Repair26 R1 full-history bath and unchanged GE05 normalized q20 equations. JSON SHA `9b93534e3ee90e1ce588bdbd3f271afd041f738b8dc6f62c4ec0d1413c27f2c4`; NPZ SHA `9e1bf36e1d81122225ff8c03f663501de7601a8fc9376fd86312e0ae1d809452` (3,550,825 bytes, independently uploaded and checked). New vs historical Repair27 q20 weighted relative L2 max approximately `3.285e-12`; historical q20 remains only comparator. Freezes [original H3G result](ge19_h3g_corrected_y_q20_valid_local_science_result_freeze.md) and [independent NPZ addendum](ge19_h3g_independent_uploaded_npz_audit_addendum.md).
- Exact certified historical Repair32B/32C `Z11` NPZ SHA `5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327`. User's scientific LOCAL environment had this binary and the actual H4F3b run verified its hash; it is **not automatically available in GitHub Actions checkout**. Never substitute manufactured `Z11` as physical.
- Original Repair13 background NPZ SHA `011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3`. Repair26 original R1 full-history trace `ge19_repair26_R1_full_history_trace.dat`, 26,643,162 bytes, SHA `608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8`.

## Actual H4 source, formal identity and material unresolved numerical issue

**Actual H4F3b on exact physical corrected parents:** classification `GE19_H4F3B_ACTUAL_CORRECTED_SIX_SOURCE_PASS_FULL_WARD_OPEN`. All 18 C/beta/Nt cohorts, source rows 8 x Nt x 41, all six signed families saved separately: `2Q_GE06_cross`, `2Q_GE07_cross`, `2Q_Lambda_cross`, `2DY2_action_complete_Y_u_and_phi`, `2M1_GE05_mapped`, `2M2_GE05_mapped`. Saved source minus exact sum of six pieces has maximum defect `0.0`. JSON SHA `1ec88fd3fd6b81bf30614b0cb78d722a02dd4f745e1f22cb9b8f956a44bac6c1`, NPZ SHA `787d5d177838b05078057aa932f379dd529449ce203f5664c36cf723acb0116b` (30,913,364 bytes, 146 finite fields). Actual source-only Ward max `3.610734858956584e-12` at Nt64 is **REPORT ONLY**, not a source-Ward-zero PASS gate. Freeze [actual six-source result](ge19_h4f3b_actual_corrected_six_source_valid_local_freeze.md).

**H4F3d4 complete FORMAL off-shell signed identity:** `GE19_H4F3D4_FULL_FORMAL_ETA_WARD_LEDGER_PASS_ACTUAL_GRID_OPEN`. It includes original independent canonical GE19 full L and shift rows, six physical-clock H4 source families, all nonbath parent Euler products, action boundaries and eta-regularized bath `+4 sum_j E_qj10,GE05 q_j10,x`. Signed split: `W_operator + W_six_source + W_all_parent = 0`. Formal algebra does NOT show actual-grid closure. Freeze [formal ledger](ge19_h4f3d4_complete_formal_eta_ward_valid_freeze.md). H4F3d1 operator `W_operator=-H FD4_x(E_b)-ik a E_L`, where `E_L=[Cmat[6]+2(Cmat[12]+Cmat[13])]w/3 - H FD4_x(Cmat[14]w)`. Keep FD4 derivative of COMPLETE Cmat times w product. GE05-to-GE06 raw source conversion factor 2 fixed.

**H4F3d6 actual physical bath Ward SUBSET:** `GE19_H4F3D6_ACTUAL_BATH_PARENT_WARD_SUBSET_PASS_FULL_OPEN`. JSON SHA `4607edde17c6820c85f32c0bbd774d5a58148eb01bfd0c81ce592e8c1b907791`; NPZ SHA `17b50c6ee584b2a8886f7114a90ea9396a127172dd9e02976b0e6275fe2fedc0` (1,315,867 bytes, 32 finite fields). All six subset and original hash/grid gates pass. But the actual normalized first-order GE05 bath Euler residual `R_z10=H FD4_x(a^3v10/tau)+a^3 omega^2(z10-X10)` has natural-scale relative L2 roughly `0.9985018--0.9993412`, **report-only**, with Nt128 absolute L2 roughly `9.27e-5--9.68e-5`. No bath on-shell smallness was proven; no full Ward claim. Freeze [actual bath subset](ge19_h4f3d6_valid_local_actual_bath_parent_ward_subset_freeze.md).

**H4F3d7 new compiler result:** frozen original Repair24 R1 interval ODE `dz/ds=v`, `dv/ds=-3h_mid v-r^2(z-X)`, `s=t/tau`, `h_mid=tau sqrt(H_i H_{i+1})`. Let `J=a^3v/tau` and `R_FD4=H FD4_x(J)+a^3 omega^2(z-X)`. For each original interval side at each sample, exact `R_ODE,side=3a^3(H-h_mid,side/tau)v/tau` and `D_FD4,side=H FD4_x(J)-J_t,side`; **`R_FD4=R_ODE,side+D_FD4,side`**. Retain BOTH interval sides at interior nodes, all 2048 nodes, modes 3/5/8/10/15/20, Nt128/Nt64, all C; preregistered phase bins <0.25, [0.25,0.5), [0.5,1), >=1; no exclusion, averaging, fitted clock or changed FD4. Manufacturer compiler PASS only; ACTUAL PHYSICAL d7 still open.

## Next work, in order (do not ask user to repeat known details)

1. **Execute PHYSICAL H4F3d7**, not `--manufactured`, on EXACT local H4F3b JSON/NPZ and H4F3d6 JSON/NPZ plus exact H3F/H3G/Repair32B Z11/Repair13/Repair26 R1 input hashes. The Python module already implements a physical CLI in `ge19/h4f3d7_bath_fd4_vs_original_r1_interval_ode.py` with `--results-dir --repair26-trace --source-json --source-npz --d6-json --d6-npz --json-out --npz-out`. There is **no frozen local d7 physical runner yet**. First create/prelock a separate safe local runner using absolute paths and **ISOLATED temporary CWD** with `PYTHONPATH` pointing to repo; importing frozen historic generators from repo CWD may write old result filenames. Preserve all old artifacts. If required physical arrays are available via authenticated GitHub artifact download, they may be transferred by exact bytes; otherwise use user's already successful local scientific environment. Report exact physical decomposition and original d6 FD4 Euler absolute-L2 reproduction <=1e-10, without inventing an on-shell gate. Freeze physical PASS/FAIL/implementation result separately.
2. In parallel independently derive/implement ALL remaining signed nonbath GE06/GE07/Lambda/Y, dust, metric/aether/scalar, homogeneous/H1/Z11/H3F/H3G Euler and action-boundary contributions on SAME actual physical H4F3b x grids. Use original H4F3d1 Cmat linear-operator FD4 full-product Ward and separately frozen H*FD8/H*FD4 source-family derivatives. The source-only Ward is NOT required to vanish.
3. Derive and preregister **full actual-grid H4F3d structural truncation/error budget from signed identity and FD4/FD8 accuracy BEFORE viewing its residual**, then execute one integrated original-cohort all-sector operator+source+all-parent+boundary Ward gate. Original registered early hotspot C_max/beta=1/m=8/Nt128/index=3 and complete active window must be retained; no posthoc masks, fitted source, time interpolation of one piece or relaxed threshold.
4. Only a separately valid full actual H4F3d STRUCTURAL PASS licenses separately preregistered corrected-parent H4/Z21 science run with unrelaxed active-shift <=1e-6 and matched temporal order >=2.5. Lensing and observations remain blocked until valid Z21 and observable-specific controls.

## Operating rules

Use Croatian for conversational work and the user's problem-first academic style (simple, precise, avoid inflated claims). New code/prereg/result documents should be versioned, action-locked and preserved in GitHub; do not edit historical Repair07/22/27/32/37--44 or relabel their outcomes. Read/check exact GitHub files, source blobs and CI logs; `success` is not automatically a physical science PASS—inspect marker, classification and claim boundary. Use local CPU for hash-locked actual physical binary runs only when necessary. No background promises. Update `docs/ge19_history.md` after confirmed results, freezing artifacts and code hashes. Do not proceed to new Z21 until full actual H4 Noether passes.

## Post-handoff actual D10 archive outcome and versioned D10r1 (2026-09-25)

Original physical H4F3d7r1 diagnostic was independently hash-audited
PASS as an FD4-versus-original interval-ODE **decomposition only**.
H4F3d10 restricted eight-field actual H1/Z11 nonbath Euler
and signed known L/b boundary were subsequently run on all six
original C/Nt cohorts. Original H4F3d10 original-parent/code locks
PASS, all 530 original NPZ arrays finite, but its archived
`m0..40` inverse-FFT check on unprojected near-zero
Euler rows fails in every case (max relative 0.395–0.472):
original classification **UNRESOLVED**; do not relabel.
Independent low-mode known parent/boundary/ward internal
identities close around `1e-16`. The unsaved high
`m41..64` band of near-zero `E_rho10/E_T11` accounts
for the archive projection mismatch. Original D10 JSON
SHA256 `df4240b40aa7f3b787e36dd0fd87212c6dcb746b35278f6cb36fc1083aa4ea21`,
NPZ `1b9ff8e421f2b9241cd0ffbc65967ecc4f5efc8afc43d5747ae1216f5d944fab`.
Manifest `ge19/h4f3d10_original_physical_archive_projection_failure_independent_audit.json`.

New preregistered H4F3d10r1 **implementation-only**
lossless Fourier archive retains original low
`m0..40` arrays BITWISE and explicitly saves
all `m41..64` positive bins; full-Nyquist inverse
reconstruction retains the original `1e-12`
archive-only threshold. Dedicated CI
[36169632733](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36169632733)
is STATIC PASS; actual local r1 physical run is OPEN.
New runner:
`bash ge19/run_local_h4f3d10r1_lossless_fourier_archive_repair.sh`.
Details, exact blobs, SHA evidence and stop conditions:
`docs/ge19_h4f3d10_original_physical_archive_failure_and_r1_static_freeze.md`
(blob `154ef2d35c5556c1b9e4d00935d27ac0b7a649a2`).
Do not interpret small known boundary or nonzero
`W_known` as full H4 Noether.
Unknown `E_i00*F_i21,chi`, original
`L21*E_L00-b21*E_b00`, complete H4 Ward
and a valid physical FD4/FD8 error bound remain
unresolved. No certified Z21 or lensing.


## Actual H4F3d10r1 lossless nonbath diagnostic PASS (2026-09-25)

The user-local physically executed, preregistered H4F3d10r1
lossless archive corrected only the original D10's lossy
Fourier output. All six original C/Nt cohorts and original
dual FD4/FD8 report-only nonbath first-order
GE06/GE07/Lambda Euler and signed known L/b lower boundary
passed original archive-only lossless full-Nyquist gate
(max `2.8428133461119143e-16`, original threshold `1e-12`).
Uploaded JSON SHA256
`69eabf101a6ec1939b32323e25b207dc419fad57eb5b2cef0858874a50cfa1d2`,
NPZ SHA256
`85c0fbd8b56037aae98615926b70bd60739a1af2fa1ff666ffc2e95485c2749b`;
FULL log byte-identical to JSON and runner hashes match.
Original failed D10 NPZ SHA
`1b9ff8e421f2b9241cd0ffbc65967ecc4f5efc8afc43d5747ae1216f5d944fab`
was independently rechecked: **all 530 original arrays
bitwise-identical** in r1, alongside 528 extra finite
`m41..64` high-band arrays. Independently
reconstructed all 12 actual C/Nt/scheme full-real
eight-field parent sums (max relative `4.163e-16`),
signed known boundaries (`3.769e-16`), and
`W_known=P_known-partial_chi(B_known)` (exact at
saved full-real reconstruction). Machine manifest
`ge19/h4f3d10r1_actual_physical_lossless_archive_independent_audit.json`
blob `2921f79dbb0ce99200418bfba924b699ff8cd67f`.
Detailed frozen science-boundary record
`docs/ge19_h4f3d10r1_actual_physical_lossless_known_boundary_freeze.md`,
blob `e9329cd24631241d0ef9610d104336cf4f6590b9`.

**Scientific boundary:** an actual *known first-order
nonbath* diagnostic PASS, NOT full H4 Noether,
not certified source/bath/action background
on-shell, not a solved Z21 or licensed lensing.
Original D10 six FAILs and Repair37 SCIENCE_FAIL
immutable. Unknown background
`sum_i E_i00 F_i21,chi` and
`L21 E_L00 - b21 E_b00` must be evaluated from
the original action and certified F21 rather than
asserted zero. Original H4F3d7r1 physical
FD4/interval ODE decomposition remains diagnostic.
Next: preregister and evaluate actual background
Euler E00, then the missing original mixed H4
boundary and all-sector integrated Ward with
a valid original-grid error budget, before Z21.


## D11 action-bound actual-background E00: static PASS, physical run OPEN (2026-09-25)

H4F3d10r1 actual original-parent signed known
first-order nonbath Euler and lower boundary are
independently audited PASS as a DIAGNOSTIC only.
Original D10 archive FAIL remains unchanged.
Machine manifest
`ge19/h4f3d10r1_actual_physical_lossless_archive_independent_audit.json`
(blob `2921f79dbb0ce99200418bfba924b699ff8cd67f`);
original physical JSON/NPZ SHA256
`69eabf101a6ec1939b32323e25b207dc419fad57eb5b2cef0858874a50cfa1d2`
and `85c0fbd8b56037aae98615926b70bd60739a1af2fa1ff666ffc2e95485c2749b`.

New D11 exact frozen original-action background
E00 all-eight field compiler and physical driver
are committed and static PASS:
[original action source CI 36189149840](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36189149840),
[driver CI 36189465789](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36189465789).
Symbolically source-bound all original 15 GE06
and 7 GE07 FLRW local partials at stable
`pt=Q0+Z0*Z_action`; exact original Lambda
action, GE07 dust and NL0C/Y homogeneous
zero-gradient included. Original FD4 and FD8
background Euler evaluated separately only in
a future user-local PHYSICAL run, with every
E_i00 nonzero residual retained report-only.
Prereg blob
`deb4b35e6a147b48fe93d6c99d798572650000ac`;
source `1f085efec4ea64b42822ddeaac566f532d9dccf1`;
physical driver `b162fad1db2a855917b5f8e29fce10c67d30737f`;
local runner `8c4f34ad79b347b3810093a1bba0b4129468f7fc`.
Detailed static freeze:
`docs/ge19_h4f3d11_source_bound_actual_background_e00_static_freeze.md`
(blob `bf178afbaa6886202b857503d8cc6e1a39b80290`).

**NEXT physical action:**
`cd ~/aest-memory-gravity && git checkout physics-first-gravitational-elasticity && git pull --ff-only && source .venv/bin/activate`;
`bash ge19/run_local_h4f3d11_actual_original_action_background_e00.sh 2>&1 | tee results/ge19_H4F3D11_LOCAL_runner.log`
(with `set -o pipefail`).
Collect four distinct new D11
JSON/NPZ/FULL/LOCAL outputs for byte and physical
audit before any E00 on-shell conclusion.
Background `E00*F21` and `L21*EL00-b21*Eb00`
remain EXPLICITLY UNRESOLVED, not silently
zeroed. No actual complete H4 Noether,
no Z21 or lensing, no physics tuning to observations.


## H4F3d11 actual original background E00: independent audit PASS, original full H4 OPEN (2026-09-26)

The user uploaded FOUR actual original-local D11 artifacts.
Actual D11 classification:
`GE19_H4F3D11_ACTUAL_BACKGROUND_E00_ARRAYS_DIAGNOSTIC_PASS_ONSHELL_OPEN`.
JSON SHA256 `d62436b12bb5e5d9b7cbf1ea24abd0e6c06ac3ff1bfd43a41556aef284e3d3df`,
49826 bytes. NPZ SHA256
`7679dc6765b87c0b1294b3915d0d1305e4fa59ac86a18d75621d5bf85c616229`,
358182 bytes. FULL log byte-identical to JSON;
runner SHA `5d8f7f5cc306cce969ad498aa86db0737246e5055415c3d372ece6bd109537e9`,
2167 bytes; all runner SHA/length checks independently match.
Original H3F/H3G/Repair13/Z11/Repair26 physical parent locks
verified by local runner. Original passed D10r1 SHA
also verified on local physical run; original D10
archive FAIL and Repair37 SCIENCE_FAIL immutable.

Independent NPZ audit: 578 finite arrays, six
original C/Nt cases, all eight E00 fields,
original FD4 and FD8 separately. Every one
of 96 saved E00 fields is exactly recomposed
from signed archived local action components;
all 48 original pLt,pRt,phi_t,T_t time derivative
components independently recomputed exactly
from original FD4/FD8 coefficients.
Original GE07 varrho_b=3*C/a^3 versus Repair13
rho_dust_action=C/a^3: preserve factor three.
Independent source partial matches frozen original
GE06 GE07 action to max `3.7032e-15` relative.

Frozen exact original nonbath homogeneous charge
and Friedmann identities on actual grid give
conditional continuum `E_L00=E_R00=0`.
The analytic original-grid E_L after replacing
FD derivative by exact derivative has maximum
L2 `4.961e-22` across six backgrounds;
original discrete vs exact Euler difference
matches original temporal derivative defect
to `6.484e-23` L2. At C_star/Nt128
FD4 E_L L2 `1.5441856e-15` but
FD8 E_L L2 `5.80716e-20`.
GE06 scalar charge about `0.0004007778406741802`
is constant to `1.0842e-19` span, Lambda exactly
constant in all actual archived backgrounds.
Do NOT infer all-sector original covariant E00
on-shell, or delete numerical E00*F21 because
original actual F21 is unknown and lacks a
certified error bound.

Machine audit
`ge19/h4f3d11_actual_original_background_e00_independent_archive_audit.json`
(blob `c3f238c2914ff18e43030ec31a3debb0edab81f1`).
Detailed science freeze
`docs/ge19_h4f3d11_actual_original_background_e00_independent_freeze.md`
(blob `5d38c45430bf0207d5e0b383f9c3f6be6d7e7613`).

NEXT: preregister an independent symbolic exact
original nonbath homogeneous on-shell
identity with original conserved charges, then
an actual source- and F21-bound numerical
E00*F21 defect test and missing original
`L21*E_L00-b21*E_b00` boundary before full
original bath-inclusive integrated H4 Noether.
NO Z21 certification or lensing yet.
