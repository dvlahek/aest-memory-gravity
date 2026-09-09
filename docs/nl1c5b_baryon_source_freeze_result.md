# NL1C5B result — published quasistatic baryon-source freeze

Final preregistered classification:

**NL1C5B_BARYON_SOURCE_FREEZE_PASS**

Predata commit: `c947163457a7276dc6e02c15aadedaf5e95a0071`.

Implementation commit: `9375dae9ce558c31354e18512a2cc6b7455d19e0`.

Workflow commit: `a9ff040aee491e2399202c7d9e4ee517d98507de`.

GitHub Actions run: `34345121613` — technical SUCCESS.

Artifact: `results_bundle_nl1c5b_baryon_source_freeze`, ID `10101422385`, SHA256 `0ab60cbc32210ad3fb75c881f91a9db11148280e9223ea644680ed8cdfbaa590`.

The preserved v0.77 identity artifact was verified exactly before use: artifact ID `10090367181`, SHA256 `24b97e5738eb07be4f12d433ff5f9fe22249e199e186d5617aca5dc81f748378`.

No finite physical eta, memory forcing, observational data, or likelihood was used.

## Frozen CLASS identity

The run checked out official CLASS commit

`e85808324f51fc694d12e3ed7439552a3c3f9540`

and applied the same previously validated AeST patch stack used by v0.77. The fresh total-matter state reproduces the preserved v0.77 baseline exactly within the preregistered comparisons:

- fresh `k` grid versus v0.77: maximum relative mismatch `0.0`;
- fresh `z` grid versus v0.77: maximum absolute mismatch `0.0`;
- fresh `d_m` versus preserved `d_m_base`: global relative L2 `0.0`.

This closes the historical-identity control before accepting any new baryon transfer.

## Native baryon source

The patched CLASS transfer output exposes the native key `d_b`. All extracted baryon-transfer values are finite. Over the full frozen native grid,

- `n_k = 912`;
- `n_z = 24`;
- `8` native redshift times lie in `0.2 <= z <= 1.5`;
- `min |d_b| = 1.1992885288687465`;
- `max |d_b| = 1355776.4432419618`.

The massive-neutrino transfer `d_ncdm[0]` is retained as context only and is not part of the primary published `rho_b` source.

All six preregistered signal-band modes

`{0.03, 0.05, 0.08, 0.10, 0.15, 0.20} h/Mpc`

occur exactly on the fresh native grid, with maximum relative miss `0.0`.

## Locked gates

All preregistered gates pass:

- `d_b` exists and is finite;
- `d_m` exists and is finite;
- native `k` grid identity `<= 1e-12`;
- native `z` grid identity `<= 1e-12`;
- fresh `d_m` versus v0.77 relative L2 `<= 1e-10`;
- all requested signal-band modes match to relative error `<= 1e-12`;
- at least eight native times are present in the redshift window.

## Consequence

NL1C5B freezes `d_b(k,z)` on exactly the same native state and grid as the certified v0.77 baseline. This resolves the source-convention qualification identified after NL1C5: the next physical quasistatic AeST reclosure must use this baryonic state as `rho_b`, not the earlier total-matter diagnostic source.

NL1C5B makes no memory-survival or nonlinear-growth claim by itself. The next test is the preregistered full coupled `tildePhi`/`chi` quasistatic reclosure with the complete published `J(Y)` operator, across the frozen interpolation-function and `beta0` branches. Only after a self-consistent field branch is obtained should the eta=0 retarded memory source be evaluated on that reclosed state.
