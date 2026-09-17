# NL1C7B2 homogeneous-background reconciliation — implementation lock

Status: **LOCKED BEFORE OFFICIAL B2 EVALUATION**

Parent preregistration commit: `1478bc59b66adf5ab81b2d85fc025ea2b20a091c`.

## Frozen implementation

- implementation: `nl1c7b/homogeneous_background_reconciliation.py`
- implementation commit: `9e9cf2616d5b959cf98a4975555ab85a8ae95428`
- implementation blob: `526b60a64b42e3f98663a5367a3cf4c4bf2d4316`
- C7A trace-extension source blob: `21147e873e6cdee8b55260189eafb8c0e612f02b`
- AeST background source blob: `9a522a653a1855eda3cb67e856f9fc10a1e73d54`

The implementation is locked before inspecting the B2 closure result.

## Frozen retained inputs

Dense eta=0 trace:

- run `35149865129`
- head `4a275f4777a7e487004f4783bc2a929a93ac8188`
- artifact `10469031693`
- SHA256 `193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70`
- 128 exact k modes, 179 native accepted-source times.

Pressureless-matter closure:

- classification `NL1C7B1_PRESSURELESS_MATTER_VARIATIONAL_CLOSURE_PASS`
- result commit `a974473a3eeb32de01ac841afe1a52c3ded321e6`
- run `35185338047`
- head `6b555bc2ee3cba7c9e97706eb1a0949416e9932f`
- artifact `10481781728`
- SHA256 `645d29e4e8ac7cfa4fff9833a4ef500d34fc667373bfac3073883155fac519a7`.

## Frozen source-level energy convention

The frozen AeST background source defines

`rho8 = Q*KQ-K`

and stores the effective CLASS background density as

`rho_class = rho8/3`.

The output-only C7A trace reads `rhoA_trace` from that CLASS background slot. Therefore B2 uses the non-fitted, source-derived conversion

`rhoA_C6 = 3*rhoA_trace = Q*KQ-K`.

This factor is a unit/convention conversion fixed by the frozen source, not a fitted remainder or post-result normalization.

## No-result-change boundary

No CLASS rerun, parameter change, additional matter species, radiation source, neutrino source, cosmological term, fitted remainder, radial initial constraint, trajectory, finite eta, turnaround, or collapse calculation is permitted in B2.

Allowed final classifications remain exactly those in the preregistration:

- `NL1C7B2_HOMOGENEOUS_BACKGROUND_RECONCILIATION_PASS`
- `NL1C7B2_HOMOGENEOUS_BACKGROUND_RECONCILIATION_FAIL`
- `NL1C7B2_HOMOGENEOUS_BACKGROUND_SECTOR_INCOMPLETE`.
