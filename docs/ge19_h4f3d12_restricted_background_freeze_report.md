# GE19 H4F3d12 — original homogeneous background identity and conditional F21 bound

**Status:** restricted GE06/GE07/Lambda continuum algebra PASS, independent actual D11 Fourier coefficient audit PASS; complete all-sector H4 Noether, actual F21, Z21 and lensing OPEN.

## Restricted continuum derivation (not a full AeST-memory-bath on-shell result)

Using the frozen original-action homogeneous GE06/GE07/Lambda partials previously verified in H4F3d11, and only the exact frozen Repair13 Friedmann, scalar-charge and dust-charge equations,

\[H^2=\frac{QK_Q-K}{3}+\frac{C}{a^3}+\rho_\Lambda,\quad (a^3K_Q)^{\prime}=0,\quad C^{\prime}=0,\quad\rho_\Lambda^{\prime}=0,\quad K^{\prime}=K_Q Q^{\prime},\]

where the prime denotes \(d/d\ln a\), it follows that \((H^2)^{\prime}=-QK_Q-3C/a^3\). The *restricted* original homogeneous action then gives

\[ E_{N00}=6a^3\left[H^2-\frac{QK_Q-K}{3}-\frac{C}{a^3}-\rho_\Lambda\right]=0,\]
\[ E_{L00}=2a^2\left[3H^2+(H^2)^{\prime}+K-3\rho_\Lambda\right]=0,\quad E_{R00}=2E_{L00}=0,\]
\[ E_{\phi00}=-2a^3 H(3K_Q+K_Q^{\prime})=0,\qquad E_{T00}=-6H C^{\prime}=0.\]

The remaining original homogeneous rows \(E_{b00},E_{u00},E_{\rho00}\) vanish by the action-source background restriction. **The original GE06 shift spatial momentum \(p_{b_\chi,00}=4a^3H\) remains nonzero**; only its derivative is zero for a spatially homogeneous background. Original GE07 uses the matter-action density \(\varrho_b=3C/a^3\), not the Friedmann density \(C/a^3\). These equalities are conditional on the exact restricted homogeneous equations. The original memory bath/background and full covariant Noether identity have not been certified.

**Exact symbolic tests:** 23 of 23 passed, including charge/Lambda/dust negative controls and a nonperiodic spatial-window counterexample. D12 derives from frozen source partials whose equality to the original GE06/GE07 action was proved in D11.

## Actual uploaded D11 grids: conditional bound, not an absolute physical Ward residual

For the unchanged original \(N_x=128\) spatial Fourier grid, \(k_\mathrm{fund}=0.0067332463908486599\) and the conservative full-band \(k_\mathrm{max}=64k_\mathrm{fund}=0.43092776901431423\). On the original spatially homogeneous background:

\[\left\|\sum_{i=1}^{8}E_{i00}\,\partial_\chi F_{i21}\right\|_2 \leq k_\mathrm{max}\!\left(\sum_i\|E_{i00}\|_{\infty,t}^{2}\right)^{1/2}\!\left(\sum_i\|F_{i21}\|_2^{2}\right)^{1/2}.\]

The numerical number below is **only the coefficient** multiplying the unknown eight-field \(F_{21}\) norm. It cannot establish actual Ward smallness without the original \(F_{21}\) field and a source-to-solution/error bound. The original \(m\leq40\) projection has a separately labeled coefficient but may NOT replace the full \(m\leq64\) parent.

| Original cohort | Scheme | Full m0..64 coefficient \(B\) | \(\|E_{L00}\|_\infty\), multiplies unknown \(\|L_{21}\|_2\) |
| --- | --- | ---: | ---: |
| C_min, Nt128 | FD4 | 6.857760551e-16 | 7.116932024e-16 |
| C_min, Nt128 | FD8 | 5.802329199e-18 | 3.332082031e-19 |
| C_star, Nt128 | FD4 | 6.858137595e-16 | 7.117323247e-16 |
| C_star, Nt128 | FD8 | 5.980377372e-18 | 2.618522947e-20 |
| C_max, Nt128 | FD4 | 6.857648852e-16 | 7.116816086e-16 |
| C_max, Nt128 | FD8 | 5.985559406e-18 | 2.597479472e-19 |
| C_min, Nt64 | FD4 | 1.121631127e-14 | 1.164020342e-14 |
| C_min, Nt64 | FD8 | 3.892074701e-19 | 1.126289122e-19 |
| C_star, Nt64 | FD4 | 1.121728440e-14 | 1.164121333e-14 |
| C_star, Nt64 | FD8 | 3.861387394e-19 | 1.006116323e-19 |
| C_max, Nt64 | FD4 | 1.121856244e-14 | 1.164253967e-14 |
| C_max, Nt64 | FD8 | 3.854205432e-19 | 9.760069484e-20 |

**Full-period spatial zero mode:** for a truly periodic spatial cell and homogeneous \(E_{i00}(t)\), the *unweighted* spatial integral of \(E_{i00}(t)\,\partial_\chi F_{i21}(t,\chi)\) vanishes exactly at each time. This identity does not hold pointwise, on arbitrary spatial subwindows, with nonhomogeneous spatial weights, or at nonzero Fourier modes. It does not complete the full action boundary or bath-inclusive Ward audit.

For the original action lower boundary \(B_\mathrm{background}=L_{21}E_{L00}-b_{21}E_{b00}\), a separate conditional bound retains \(\|E_{L00}\|_{\infty}\,\|L_{21}\|_2+\|E_{b00}\|_{\infty}\,\|b_{21}\|_2\). Neither unknown field is set to zero; the original full spatial derivative of this boundary has a further factor \(k_\mathrm{max}\).

## Audit and limitations

- Original D11 JSON SHA256 `d62436b12bb5e5d9b7cbf1ea24abd0e6c06ac3ff1bfd43a41556aef284e3d3df`, NPZ SHA256 `7679dc6765b87c0b1294b3915d0d1305e4fa59ac86a18d75621d5bf85c616229`. All six original C/Nt backgrounds, 12 FD4/FD8 rows, 578 finite parent arrays, exact original D10r1 hashes and original diagnostic claim boundaries were checked.
- Max restricted analytic \(\|E_{L00}\|_2\) from original floating Repair13 grids is `4.110387e-22`; max finite-arithmetic reassembly difference against saved original FD temporal defect is `3.643976e-22`. These are *rounding diagnostic* quantities, not new science tolerances.
- D12 r0 failed only an **implementation-level** comparison because it divided a rounding difference by an almost-zero cancellation residual. The preserved D12r1 code uses the original action-component natural L2 scale with the same implementation comparator 1e-12; no source, physical output, parent threshold or acceptance criterion was changed.
- Independently retested all 12 eight-field Fourier derivative inequalities on synthetic inputs, exact symbolic controls, deterministic output SHA, no-overwrite behavior and tampered-parent SHA rejection. Synthetic inputs are not actual F21.
- No original GE05 bath background Euler, no full all-sector H4 Ward, no original physical F21/L21/b21, no certified Z21 or lensing. Original Repair37 SCIENCE_FAIL remains immutable.

## Files and provenance

- Original predata `ge19_h4f3d12_predata_restricted_background_and_f21_bound.json` SHA256 `d704bd35c71f80133c7e5b3bb7b71423366f4a692be48fb5797526c2f31db183`.
- Reproducible corrected analysis script `ge19_h4f3d12r1_restricted_background_and_conditional_f21_bound.py` SHA256 `cc637acbe41941247bdf0382dfd1d517790795ba5e7c1562482e0ac0ca757017`.
- Actual original-D11-derived machine report `ge19_h4f3d12_actual_d11_conditional_f21_bound.json` SHA256 `5d94ac19e3176e8e6d2948260b957718eba9620ea9fced2981fe2e6df2c5837e`.
- Freeze manifest `ge19_h4f3d12_freeze_manifest.json` SHA256 `e4a6030f85d1bfbe22c095c82ee572497de1c602e37d57c516373cf59be0bfea`.
- The connected GitHub write action did not accept the new D12 commit. These generated artifacts are local and downloadable; do not assume they were pushed to `dvlahek/aest-memory-gravity`. Last verified branch HEAD before D12: `3c44790d0e360e25b9a6504bf5779bf4f2101edc`.

## Reproduce from the unchanged actual D11 files

```bash
python ge19_h4f3d12r1_restricted_background_and_conditional_f21_bound.py \
  --predata ge19_h4f3d12_predata_restricted_background_and_f21_bound.json \
  --d11-json ge19_h4f3d11_actual_original_action_background_e00.json \
  --d11-npz ge19_h4f3d11_actual_original_action_background_e00.npz \
  --json-out ge19_h4f3d12_actual_d11_conditional_f21_bound.json
```
