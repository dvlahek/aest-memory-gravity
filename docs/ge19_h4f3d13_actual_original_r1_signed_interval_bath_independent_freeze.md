# GE19 H4F3d13 — actual original R1 signed interval bath: independent physical archive freeze

**Original local result:** `GE19_H4F3D13_ACTUAL_ORIGINAL_R1_SIGNED_INTERVAL_BATH_PARENT_DIAGNOSTIC_PASS_ONSHELL_OPEN`.

**Independent post-run result:** `GE19_H4F3D13_ACTUAL_ORIGINAL_R1_SIGNED_INTERVAL_BATH_PARENT_INDEPENDENT_ARCHIVE_AUDIT_PASS_ONSHELL_OPEN`.

Original Repair26 R1 bath dynamics, original GE05 action and six Fourier modes `[3,5,8,10,15,20]` remain unchanged. The completed **diagnostic** evaluates both original one-sided interval ODE bath Euler terms, their **signed** `+4 E_q10 partial_chi q10` Fourier convolution and the original sampled FD4 bath contribution and its derivative defect, with original `Nq=2048` and an independent `Nq=1024` control for all original `C_min,C_star,C_max` and `Nt=128,64`. The bath is NOT certified on-shell.

## Original uploaded physical bytes

| Actual user-local artifact | SHA-256 | Bytes |
| --- | --- | ---: |
| `ge19_h4f3d13_actual_original_r1_signed_interval_bath_parent.json` | `2b4dfbd30ec6466292e0dcf62eeed8b723555d1890a127a5e0a6ff761d2ebe76` | 38083 |
| `ge19_h4f3d13_actual_original_r1_signed_interval_bath_parent.npz` | `1608fe98dd924b2b235ecf0f8fce768f2f3a2fa4a2854de04a56fe622ad3df89` | 28446953 |
| `ge19_h4f3d13_actual_original_r1_signed_interval_bath_parent_FULL.log` | `2b4dfbd30ec6466292e0dcf62eeed8b723555d1890a127a5e0a6ff761d2ebe76` | 38083 |
| `ge19_H4F3D13_LOCAL_runner.log` | `3326712c9a1b42593c457ccdd94191f4a976a7a42dfd3f439a18405e7b5cf76e` | 2401 |

The actual JSON and FULL log are byte-identical. Independently computed original upload hashes/sizes agree with every original runner line; original runner source and physical-input hash gates PASS. The historical raw Repair26 R1 accepted-step trace, H3F/H3G/Z11/Repair13 and original six-piece source remain protected by their original local runner SHA checks; the historical raw trace was not repropagated independently in this audit.

The actual NPZ contains **134 finite distinct numeric arrays**, with both original x clocks and twelve `C/Nt/Nq` cohort archives. Its signed output is the original **`m=0..40`** convolution for the six frozen positive-frequency modes and their negative-frequency conjugates, not an independently full-Nyquist `m=0..64` bath Euler archive. Do not transplant the earlier D10r1 known nonbath full-Nyquist certification onto D13's bath archive.

## Independent original-parent and algebraic verification

For each of twelve cohorts and both one-sided interval endpoints, the originally stored complex convolution satisfies

```text
W_FD4(endpoint, m) =
  W_interval_ODE(side, m) + W_sampled_FD4_derivative_defect(side, m)
```

with **maximum relative discrepancy `4.778325451736743e-16`**, independently recomputed from actual uploaded complex arrays. All archived arrays are finite. Original signed FD4 `m0` maximum absolute coefficient across the cohorts is `3.2202e-24`, a tiny floating residual, not an asserted exact bitwise zero.

Unlike a report-only JSON identity, the original previously uploaded and SHA-verified D7r1 physical NPZ was loaded independently: **all 24 original `R_ODE` and `FD4_defect` mode-time L2 arrays are bitwise identical** to the actual D13 Nq2048 corresponding arrays, **all six clock arrays match** and **all six original phase-bin node-interval count arrays are exactly reproduced** by direct counting of D13's archived Nq2048 phase. Thus D13 did not alter earlier original R1 dynamics or original D7r1 phase bins. Original D7r1 NPZ SHA256: `4f011c96c2c11165df6332eafc459c5d2c5e7bc5164a436bde3d1563696f0e13`.

On the same physical time nodes, the relative original `Nq=2048` versus `Nq=1024` differences in **signed interval ODE W** are at most `7.3175e-8` on the left and `7.6608e-8` on the right (report-only). This convergence controls interval quadrature at frozen phase and time resolution; it does **not** establish a weighted phase/time/bath on-shell truncation error.

## Physical interpretation: signed cancellation and phase-tail caveat

At `C_star,Nt128,Nq2048`, the original left interval signed W has L2 `1.4132200209806873e-12`, its sampled FD4 derivative-defect signed W has L2 `1.3664519122854888e-12`, but the final original sampled FD4 signed W is `4.8422385381524534e-14`. On the right the corresponding norms are `1.3358149081747353e-12`, `1.3794385628153709e-12` and `4.511961673510633e-14`. Thus an apparent small **sampled FD4** result is produced by cancellation of two substantially larger, oppositely phased terms. The original left interval and defect complex-array cosine is about `-0.999959` (right about `-0.999964`). These are report-only physics diagnostics, not a tuned new smallness gate.

Across all original cohorts, the ratio of a one-sided signed interval-W norm to the corresponding sampled FD4-W norm ranges from `14.3802` to `29.6093`; the sum of separate interval and derivative-defect norms can be **60.1854** times the final FD4 norm. Crucially, actual original sampled FD4 signed W changes by up to **`0.0135477` relative** (about 1.35%) from Nq2048 to Nq1024, despite the interval signed W changing by less than `7.7e-8` relative. This reflects amplification in a near-cancelling total and prevents treating the small quadrature difference of one component as an absolute error bar for the cancelled total.

The original archived one-sided phase is `r_j Delta(ln a)/(tau sqrt(H_i H_{i+1}))`. In the primary `C_star,Nt128,Nq2048` cohort, **about `0.5433%` of node-interval pairs have phase greater than `pi`**, with a maximum of about `961.03`. In the control `Nt64,Nq2048` cohort the maximum is about `1933.48`. These are unweighted counts; they do not prove those high-phase nodes dominate or negligibly contribute to the **signed, source-weighted** bath parent. A separate source-weighted tail and interval approximation/error budget is required.

The one-sided interval formula uses the frozen R1 accepted-step geometric mean `h_mid=sqrt(H_i H_{i+1})`, hence its residual is proportional to `H_endpoint-h_mid` with original R1 state and drive. It must not be equated to a source-independent proof of the *continuous-time* bath EOM or treated as an original on-shell bound without controlling phase, time approximation and quadrature together.

## Source-first continuation

Freeze this exact physical diagnostic in machine manifest
`ge19/h4f3d13_actual_original_r1_signed_interval_bath_independent_archive_audit.json`
(Git blob `886ac54bd7ad6f802895145fd7776f2ebd6c64d1`).
The original actual D13 source, runner, JSON/NPZ output and historical original FAIL files remain immutable.

**Recommended next stage D14:** preregister an original R1 **source-weighted high-phase-tail and interval-time approximation error budget**, retaining both signed original `Nq=2048/1024` full complex mode-time W arrays, and independently control cancellation-sensitive FD4 totals instead of using a relative interval-only Nq difference as a bath-on-shell criterion. The original GE05 full action boundary and the unknown `E_i00 partial_chi F_i21`, `L21 E_L00-b21 E_b00` and `a E_L21` pieces must remain explicit. Only after original source-bound all-sector Ward consistency and the active-window error budget can a window-local particular `Z21` be certified; lensing comes after it and cannot be used to tune the theory.

**Current scientific gates:** original D13 signed interval bath parent diagnostic PASS; original GE05 bath first-order on-shell OPEN, all-sector H4 Noether OPEN, `Z21_certified=false`, `lensing_licensed=false`; original Repair37 SCIENCE_FAIL and original D10 archived FAIL unchanged.
