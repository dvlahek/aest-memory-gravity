# NL1C7B2 Repair01 implementation lock

Pre-result implementation lock for stable Exp background-energy evaluation.

- Repair01 prereg commit: `0b509efb43f5d8d681d3e906b4b96b144e5ded77`
- Repair01 implementation commit: `4c6378b73c7668190474c5f5ff880ebf1a0d6975`
- Repair01 implementation blob: `ac41fbe5688f299f8bd5290c9748092697dc2643`
- original B2 evaluator blob remains: `526b60a64b42e3f98663a5367a3cf4c4bf2d4316`
- historical B2 result-freeze commit: `22923058c883dd36c6b507fa7079efba5000b4e0`
- historical run: `35190742632`
- historical artifact: `10483358073`
- historical artifact SHA256: `aa017449e0d4bc2afa4906925c4c53151c4c1eae1571916851aeacf87ef16281`

Only the primary numerical route used to recover Exp `Z` for B2-G3 is changed: `KQ -> Z` now follows the frozen CLASS source algorithm. Original thresholds, interpolation rules, Hamiltonian closure test, baryon normalization and claim boundary are unchanged.