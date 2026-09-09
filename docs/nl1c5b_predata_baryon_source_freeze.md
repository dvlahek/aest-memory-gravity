# NL1C5B predata — published quasistatic baryon-source freeze

Classification before implementation: **NL1C5B_PREDATA_BARYON_SOURCE_FREEZE**

This follow-up is created after `NL1C5_SCREENED_RECLOSURE_TRANSITION_REQUIRES_FULL_J` and before inspecting a fresh baryon-transfer extraction.

Historical classifications remain immutable. NL1C5 remains a fixed-total-matter diagnostic and is not retroactively reclassified.

## Reason for the follow-up

The published AeST static weak-field equations use the minimally coupled baryonic density `rho_b` as the source,

\[
\nabla^2\tilde\Phi+\mu^2\Phi
=\frac{4\pi G_N}{1+\beta_0}\rho_b,
\]

\[
\nabla^2\tilde\Phi
=\nabla\cdot[j(x)\nabla\chi],
\qquad
\Phi=\tilde\Phi+\chi.
\]

NL1C5 deliberately used the already retained total-matter state `d_m` and therefore cannot be promoted as the final physical quasistatic source convention.

The next full-J reclosure must use the native baryon transfer from the **same frozen CLASS AeST model**.

## Frozen extraction

Use the same pinned CLASS commit and unchanged AeST implementation as v0.77:

- CLASS `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- `KB=0.0665`;
- `Q0=1e-4 Mpc^-1`;
- `K2=9500`;
- `Z0=1e-17 Mpc^-1`;
- Exp background;
- `H0=67.3324639084866`;
- `omega_b=0.022377376877682164`;
- `omega_cdm=0.12006705327635288`;
- the same neutrino, primordial and recombination setup as v0.77;
- `k_per_decade_for_pk=80`, `k_per_decade_for_bao=560`, `P_k_max_h/Mpc=2`, `z_max_pk=5`;
- no memory forcing and no observational data.

Request the exact modes

\[
k_h=\{0.03,0.05,0.08,0.10,0.15,0.20\}\;h\,{\rm Mpc}^{-1}.
\]

Save the CLASS-native transfer blocks `d_b` and `d_m` on their common native `(k,z)` grid. If the pinned CLASS output exposes a massive-neutrino density transfer, save it as context only; it is not part of the primary published `rho_b` source freeze.

## Independent historical identity check

Download the retained v0.77 artifact

- run `34315590099`;
- artifact ID `10090367181`;
- SHA256 `24b97e5738eb07be4f12d433ff5f9fe22249e199e186d5617aca5dc81f748378`.

The newly extracted native `k`, `z`, and `d_m` arrays must reproduce the preserved v0.77 baseline before the new `d_b` block is accepted.

## Locked gates

- pinned CLASS commit is unchanged;
- native `d_b` key exists and all values are finite;
- native `d_m` key exists and all values are finite;
- fresh `k` grid versus v0.77 preserved grid relative mismatch `<=1e-12`;
- fresh `z` grid versus v0.77 preserved grid absolute mismatch `<=1e-12`;
- fresh `d_m` versus v0.77 preserved `d_m_base` global relative L2 `<=1e-10`;
- all six requested `k_h` values occur exactly to relative error `<=1e-12`;
- at least 8 native times lie in `0.2<=z<=1.5`;
- no finite physical eta and no observational data.

## Classification

All gates pass:

**NL1C5B_BARYON_SOURCE_FREEZE_PASS**

The fresh frozen baseline does not reproduce v0.77 or the required baryon source is unavailable/nonfinite:

**NL1C5B_BARYON_SOURCE_FREEZE_FAIL**

A PASS freezes `d_b(k,z)` as the primary matter source for the next full-J quasistatic AeST reclosure. It makes no memory-survival or nonlinear-growth claim by itself.
