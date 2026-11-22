# GE19 — DES Y3 first Asimov identifiability gate (no observed residuals)

**2026-11-22. Frozen, diagnostic-only observable-screen protocol.** No new CLASS, no DES fit, no optimisation over bins, no source physics adjusted to observed \`gamma_t\`. Accompanying executable: [des_y3_asimov_memory_amplitude_null_20261122.py](../ge19/observability/des_y3_asimov_memory_amplitude_null_20261122.py), latest initial commit \`73fdc88\`.

## Why this exact gate, not another claimed memory detection

The single historical patched-CLASS Weyl derivative gives **only one** \`(k,z)\` datum:
\`\`\`math
\frac{W_{1,\mathrm{delayed}}}{W_0}=-1.712922233834667\times10^{-9}\quad\text{per unit eta},
\`\`\`
at \`k=0.06732117 Mpc^-1,z=0.5\`. That number is *not* \`d gamma_t/d eta\`, does not define an angular DES shape, and is not action-normalized physical/primordial certified. Do **not** call it a survey memory prediction.

We already have a pinned older **non-best-fit, no-fit GR theory and full covariance reference**, \`obs06_fixed_gr_192.npz\` (SHA256 \`564542d47fa95d5b5fb3c5b0c8bb4eae1ecbc93f450bf993ea0bbb98310546e3\`), from a public CosmoSIS DES example on 192 selected real DES Y3 MagLim \`GAMMAT\` rows. The observational source was public \`2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits\`, verified original SHA256 \`83efa43f6609ff07248b9c4e411b9ab386ec569cba402364fb21edff456e8b76\`. This is **not** an official DES joint 3x2pt cosmology fit. The executable deliberately does not open observed data/value/residual arrays, even in its NPZ manifest: it reads only \`.npy\` headers for all keys and only materializes validated GR model, covariance, and tomographic indices by explicit allowed key names.

**Selection fixed before any new observed residuals**: MagLim foreground bin 4 × source bin 4 (target), and the same lens × source bin 3 (control). If the frozen 192-row asset lacks reliable \`(lens,source)\` mapping, the script must **fail closed**, not infer row ordering or invent angular cuts.

## The first exact Asimov discrimination result

Take \`mu\` the GR predicted \`gamma_t\` vector on the **same selected bins**, \`C\` their published full covariance and \`t=\partial gamma_t/\partial eta\`. For the **explicitly nonphysical comparator only**, force the historical one-point Weyl fraction into a uniform shape
\`\`\`math
t_{\mathrm{flat}}=\epsilon\,\mu,\qquad
\epsilon=-1.712922233834667\times10^{-9}.
\`\`\`
This is a *negative-control null hypothesis*, not the actual GE19 template. Let \`D\` contain one free amplitude column \`mu * 1_{source=3}\` and one \`mu * 1_{source=4}\`. The exact profiled information is
\`\`\`math
F_\perp=t^T\big[C^{-1}-C^{-1}D(D^TC^{-1}D)^+D^TC^{-1}\big]t .
\`\`\`
Since \`t_flat\in col(D)\`, **\`F_\perp=0\` algebraically for any positive definite covariance**. This is true whether or not a specific DES NPZ file is accessible. A robust Cholesky+SVD implementation in the executable checks this as an *amplitude-degeneracy negative control*, including a noncollinear synthetic positive control. Its output includes optional unprofiled diagnostics, but **the numerical roundoff-sized profiled F is NOT a detection or a DES physical forecast**.

The scientific result is limited but unambiguous: a **shape-independent fractional modification cannot be uniquely attributed to memory**, because it is absorbed into ordinary amplitude nuisance parameters. Consequently a nontrivial, calibrated delayed-only *angular/source/redshift-shape* derivative \`t_phys\` is necessary.

## What may legitimately happen in the first WSL run

- If pinned OBS06 \`.npz\` with covariance, GR theory and 1-based \`(lens,source)\` metadata is found and matches its SHA, the 40-ish selected rows (counts set by the actual frozen angular cuts) are whitened against the published covariance. Report \`GE19_DES_Y3_FROZEN_GR_COVARIANCE_PROXY_AMPLITUDE_DEGENERACY_PASS_ONLY\`.
- If the NPZ or reliable selection labels are missing, report \`GE19_ASIMOV_ASSET_BLOCKED_...\`, preserving a **header-only manifest** of available keys. The failure is missing asset metadata, NOT evidence for zero or nonzero physical memory.
- If a matching physically action-certified \`d gamma_t/d eta\` is absent (current state), **NO** numerical \`sigma_eta\`, \`Delta chi²\` or observed detection can be claimed. Do not replace with the historical single-point W1.
- At no stage inspect observed \`VALUE\` rows, fit cosmological/nuisance parameters, select the most promising residual, or claim to reproduce the official DES joint likelihood.


## WSL researcher execution 2026-11-22 — asset lookup erratum, corrected

The researcher executed the first canonical run and uploaded an original JSON/log which were archived **byte-for-byte** in [r1 JSON](../results/ge19_des_y3_asimov_20261122_r1.json) (Git blob \`9ae1f9a1492f8d451816743eb1acf1621d4a0c5f\`, SHA-256 \`8a2fd8b078622cdd9c76948a3640ee6958ed66ae1e04cdb49f6c4816e29bb52c\`) and [r1 log](../results/ge19_des_y3_asimov_20261122_r1.log) (Git blob \`73d4239a73009b288ee025d0ed59fb10fdd57561\`, SHA-256 \`96f0607c4b86293cb0b08c526a87670e4a83cc5d930f5bd1a95c0d2f64177d54\`).

\`GE19_ASIMOV_PROJECTION_SELFTEST_PASS 3\` passed, followed by \`GE19_ASIMOV_ASSET_BLOCKED_REFERENCE_MISSING\`; therefore **no real DES covariance submatrix, GR rows or survey Fisher information was loaded**. This is **not a null observational result** and no memory \`sigma_eta\` is available.

A pre-existing researcher [OBS06R2 WSL log](https://chatgpt.com) documents the actual original file path and checksum:
\`\`\`text
/home/dino/aest-memory-gravity/results/obs06_des_y3_gr/obs06_fixed_des_example_gr_192.npz
SHA256 564542d47fa95d5b5fb3c5b0c8bb4eae1ecbc93f450bf993ea0bbb98310546e3
\`\`\`
The first GE19 Asimov script mistakenly looked only for \`obs06_fixed_gr_192.npz\`, **not the original longer filename**. In commit \`153469fb\`, the unchanged mathematical diagnostic now searches *both* filename aliases within the known project trees and accepts only the exact pinned hash. A direct explicit \`--reference-npz results/obs06_des_y3_gr/obs06_fixed_des_example_gr_192.npz\` argument remains the strongest reproducibility route. If source files have been moved/removed since OBS06R2, existence must be rechecked; original log provenance is not proof the bytes still exist now.

The rerun should use output suffix \`r2\` to avoid overwriting the original r1 asset-blocked evidence. If the original OBS06 NPZ lacks individually certified \`GR\`, \`cov\` or reliable 1-based lens/source mappings, the script will return \`GE19_ASIMOV_ASSET_BLOCKED_...\` with a header-only NPZ manifest rather than manufacture an index. **No manual mapping is authorized based solely on presumed ordering or observed data.**

## What is required for the next *physical* Asimov go/no-go

Generate **one** original quarter-normalized, finite-k growing-state- and retarded-history-certified delayed *galaxy-Weyl cross-spectrum* across the actual survey \`k,z,ell\` support. Project it through pinned lens/source n(z), calibrated \`gamma_t\` angular windows and scale cuts and verify numerical errors below the resulting template norm. Construct the full nuisance/instantaneous-rival columns \`D_phys\` with physically stated priors; calculate profiled \`F_\perp\). Only then, if sufficiently distinguishable, unblind the existing public \`gamma_t\` data for an actual test. The current strict classification is **PHYSICAL_ASIMOV_BLOCKED_MISSING_DELAYED_GAMMAT_TANGENT; DES_DETECTION=FALSE**.

A small \`W_1/W_0\` at a single \`k,z\` does NOT establish an upper bound on the survey projection. The flat-comparator degeneracy does NOT exclude shape-dependent physical memory; it prevents a spurious optimistic detection announcement.
