# GE19 H4F3d10r1 — actual physical lossless Fourier nonbath known-boundary freeze

**Classification:** `GE19_H4F3D10R1_ACTUAL_ORIGINAL_PARENT_LOSSLESS_NONBATH_KNOWN_BOUNDARY_DIAGNOSTIC_PASS_FULL_NOETHER_OPEN`.

This is a confirmed **actual original-parent physical diagnostic PASS**
for the separately versioned H4F3d10r1 first-order eight-field
nonbath Euler and known signed lower-boundary calculation. It is
not a complete H4 Noether or covariant on-shell PASS.

## Actual uploaded execution: identity and immutable provenance

The user-local `ge19/run_local_h4f3d10r1_lossless_fourier_archive_repair.sh`
reported exact original source and original physical SHA checks PASS
and its final marker
`GE19_H4F3D10R1_LOSSLESS_ARCHIVE_KNOWN_NONBATH_DIAGNOSTIC_PASS_FULL_OPEN`.
All six original `C_min,C_star,C_max x Nt128,Nt64` cases report true.

Uploaded physical files independently compared against runner output:

| Artifact | SHA256 | Byte length |
| --- | --- | ---: |
| `ge19_h4f3d10r1_lossless_fourier_known_boundary.json` | `69eabf101a6ec1939b32323e25b207dc419fad57eb5b2cef0858874a50cfa1d2` | 157110 |
| `ge19_h4f3d10r1_lossless_fourier_known_boundary.npz` | `85c0fbd8b56037aae98615926b70bd60739a1af2fa1ff666ffc2e95485c2749b` | 35716618 |
| `ge19_h4f3d10r1_lossless_fourier_known_boundary_FULL.log` | `69eabf101a6ec1939b32323e25b207dc419fad57eb5b2cef0858874a50cfa1d2` | 157110 |
| `ge19_H4F3D10R1_LOCAL_runner.log` | `28af41e2d3f5aff7d4d5c504c1c23d9d1565e6ae83432e253bea8e37c88879d4` | 2358 |

FULL is byte-identical to JSON. All logged SHA and lengths match
the actual uploaded files. The raw original H3F/H3G/Repair13/
Repair32B+32C/Repair26 and original H4F3b/d6/d7r1 inputs were
SHA-verified by the **user-local runner**, not independently
re-integrated in this uploaded-artifact audit.

The original D10 failed JSON `df4240b40aa7f3b787e36dd0fd87212c6dcb746b35278f6cb36fc1083aa4ea21`
and original NPZ `1b9ff8e421f2b9241cd0ffbc65967ecc4f5efc8afc43d5747ae1216f5d944fab`
were separately checked from their original preserved uploaded bytes.
Their historical classification remains
`GE19_H4F3D10_ACTUAL_PARENT_INTERFACE_UNRESOLVED` and all
six original lossy archive PASS flags remain FALSE. No historical
gate was changed.

## Independent full original-grid NPZ checks

The new 35.7 MB compressed NPZ contains **1058 finite numeric arrays**:
the **same 530 original low-mode/clock arrays bitwise**, and **528**
additional high-band complex arrays `m41..64`. All 528 have
precisely `(128,24)` or `(64,24)` shapes and complete
original low-mode keys `m0..40` have `(Nt,41)`.
Original spectral products, all eight original fields and
both FD4/FD8 are present.

Original preregistered full-Nyquist archive inverse-FFT
tolerance remains `1e-12`. The largest original user-local
case report is only `2.8428133461119143e-16`.
No original source, 2048-node R1 bath, spectral positive mode,
FD4/FD8 operator, original shift, time convergence gate
or phase bin was modified.

Independently reconstructed all actual `Nx128` real fields
from `m0..64` for each of the **12** C/Nt/time-scheme cohorts:

- Recomputed all eight exact `2*(E_i10 F_i11,chi+E_i11 F_i10,chi)`
  contributions and full real `P_known`:
  maximum relative difference `4.163e-16` in 12 full sums
  and `4.565e-16` across 96 individual field terms.
- Recomputed original signed
  `B_known=2L10 E_L11+2L11 E_L10-2b10 E_b11-2b11 E_b10`:
  maximum full-real relative difference `3.769e-16`.
- Full saved `W_known=P_known-partial_chi(B_known)`
  recomposed with **zero** difference across 12 cases.
  Maximum independent reconstituted 36 original
  `P_known,B_known,W_known` L2 norm discrepancy:
  `2.062e-16` relative.
- All 192 separately reported `E10/E11` field norms
  agree with independent full-real reconstruction to
  `3.004e-16` relative.
- All original low-band Fourier parent-sum, signed
  Ward and spectral chi report-only identity
  discrepancies are at most `2.6490057104221805e-16`.

The extra high-band values are *not* interpreted as
physical excitation in near-zero Euler fields:
the old lossy projection could omit 44.4% of a field
whose original absolute L2 is only `9.09e-21`.
The bitwise test is of original versus new saved
low-mode *arrays*. The original unarchived, pre-FFT
real arrays are available only in the user-local
actual run, which compared them against the complete
lossless r1 inverse transform; the four uploaded
outputs do not constitute a second independent
physical H3F/H3G/Z11 propagation.

## Actual known nonbath first-order physical quantities

| Original cohort | FD4 P_known real L2 | FD8 P_known real L2 | FD4 B_known real L2 |
| --- | ---: | ---: | ---: |
| C_min, Nt128 | 2.860137994e-6 | 2.860137543e-6 | 7.780332052e-29 |
| C_star, Nt128 | 2.859204475e-6 | 2.859204023e-6 | 7.778362623e-29 |
| C_max, Nt128 | 2.858013984e-6 | 2.858013532e-6 | 7.775847724e-29 |
| C_min, Nt64 | 2.054125327e-6 | 2.054119100e-6 | 4.629233869e-28 |
| C_star, Nt64 | 2.053453506e-6 | 2.053447282e-6 | 4.628068079e-28 |
| C_max, Nt64 | 2.052596752e-6 | 2.052590532e-6 | 4.626581116e-28 |

For the primary `C_star,FD4` original full-real arrays,
the `u` parent contribution L2 is about
`2.858772e-6` of `2.859204475e-6` total.
The `phi` parent contribution is `7.441612e-10`.
These report-only norms identify which computed
original nonbath first-order channel contributes.
They do **not** imply the complete H4 Ward vanishes.
The known lower boundary is `~7.78e-29`, but
the genuine background/Z21-dependent original
action-boundary piece has not been evaluated.

The original same-grid FD4/FD8 `W_known`
full-real relative differences are
`~3.22e-7` on Nt128 and `~6.32e-6` on Nt64.
These are report-only and **not** an independently
certified actual FD4/FD8 full-H4 derivative error
budget or matched-order gate.

## Exact stop: no premature Z21 or lensing

Not yet computed or ruled out:

```text
P_background = sum_i E_i00 * F_i21,chi
B_background = L21 * E_L00 - b21 * E_b00
```

The current actual known-source calculation is
`P_known-partial_chi(B_known)` only.
The complete original integrated H4 Noether
still requires actual original on-shell/interface
bath and boundary contributions, source/operator,
GE06/GE07/Lambda/Y sectors and a valid **actual**
high-derivative error bound before a full-action
test. H4F3d7r1 is a diagnostic FD4/interval-ODE
decomposition, not full bath-on-shell certification.
Original Repair37 SCIENCE_FAIL remains immutable.

**Full all-sector physical H4 Noether NOT CERTIFIED;
window-local particular reduced Z21 NOT CERTIFIED;
lensing and observation tuning BLOCKED.**

Machine-readable independent artifact audit:
`ge19/h4f3d10r1_actual_physical_lossless_archive_independent_audit.json`,
Git blob `2921f79dbb0ce99200418bfba924b699ff8cd67f`.
Actual user-local NPZ is identified by the immutable
SHA above, **not** claimed committed to GitHub.
