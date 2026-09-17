# NL1C7B2 homogeneous-background reconciliation — historical result freeze

Final historical classification:

`NL1C7B2_HOMOGENEOUS_BACKGROUND_RECONCILIATION_FAIL`

Official provenance:

- run `35190742632`
- head `c13207ef37540e7c01171c4d638b4058ad1fadd3`
- artifact `10483358073`
- artifact SHA256 `aa017449e0d4bc2afa4906925c4c53151c4c1eae1571916851aeacf87ef16281`.

Gate outcome:

- B2-G1 provenance: PASS
- B2-G2 exact homogeneous lapse identity: PASS
- B2-G3 trace scalar-energy consistency: FAIL
- B2-G4 baryon normalization: PASS
- B2-G5 homogeneous Hamiltonian closure: FAIL
- B2-G6 k-independence/interpolation control: PASS.

The historical B2 result is immutable. No radial initial constraint, nonlinear evolution, finite eta, turnaround or collapse calculation was executed.

## Numerical findings

At `a_i=0.02`, using the preregistered PCHIP evaluation:

- `3 H^2 = 0.006048691658420088 Mpc^-2`
- `3*rhoA_trace = 0.0050097116488726345 Mpc^-2`
- `varrho_b = 0.000933682111398225 Mpc^-2`
- signed unassigned remainder `= 0.00010529789814922824 Mpc^-2`
- remainder fraction of `3H^2 = 0.01740837590930068`
- PCHIP-vs-linear normalized residual change `= 0.00021072388418288956`
- all four traced background quantities have zero measured k-spread across the 128 exact modes.

The direct G3 reconstruction from printed `Q` gave a relative mismatch `0.0010201652130933522`; the analogous reconstructed `KQ` mismatch was `0.001020165213093598`.

## Post-result technical diagnosis, not reclassification

The frozen source shows that the Exp background does not recover its internal `Z` by subtracting `Q-Q0`. It evolves `KQ=I0/a^3`, solves the monotone relation

`KQ/(4*K2*Z0) = Z*exp(Z^2)`

for `Z`, and then evaluates `Q`, `K`, `KQ`, `KQQ`. The printed double `Q=Q0+Z0*Z` combines a `1e-4` leading value with an approximately `5.5e-17` offset; reversing that addition by `(Q-Q0)/Z0` is cancellation-limited in double precision at roughly the observed `1e-3` level.

Using the frozen source's own stable `KQ -> Z` inversion on the retained B2 values gives

- `Z = 5.549669381009492`
- `Q*KQ-K = 0.005009711648872634 Mpc^-2`
- `3*rhoA_trace = 0.0050097116488726345 Mpc^-2`,

which agree at machine precision. This diagnostic does not alter the historical FAIL. A separate preregistered repair is required before using this stable representation in G3.
