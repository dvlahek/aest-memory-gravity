# ACT DR6 exploratory scan R3 — nonfinite low-ell diagnostic/repair

Date: 2026-09-11

The R2 local execution again ended as `ACT_DR6_LENSING_EXPLORATORY_SCAN_INCOMPLETE`, now after CLASS accepted the input and computed the first memory-off eta=0 reference, but before any ACT likelihood point was evaluated. The immediate error was `nonfinite CLASS lensing-potential spectrum`.

Because the first spectrum evaluated by the frozen scan is `compute_clpp(False,0)`, this failure occurs already in the memory-disabled AeST reference and therefore cannot by itself be attributed to finite positive memory coupling.

## Frozen R3 rule

Preserve unchanged:

- official ACT DR6 likelihood package/version/data/variant;
- `act_baseline`, `lens_only=True`, `like_corrections=False`;
- all cosmological and AeST parameters;
- eta grid `{0,1/256,1/128,1/64,1/32,1/16,1/8}`;
- `modes=s`, `output=tCl,lCl`, `lensing=yes`, `l_max_scalars=4000`;
- removal of `z_max_pk` and `P_k_max_h/Mpc` from R2;
- halofit exploratory setting;
- eta-zero memory-on/off regression gate `1e-8` on `2<=L<=2999`;
- ACT likelihood and interpretation scope.

R3 changes only the handling of nonfinite entries returned by CLASS `raw_cl()['pp']`:

1. Report every nonfinite multipole index for each CLASS call.
2. If and only if all nonfinite entries are confined to `L=0` and/or `L=1`, replace those entries by zero before conversion to `C_L^{kappa kappa}`. These multipoles are outside both the eta-zero regression domain and the ACT baseline lensing range.
3. If any nonfinite entry occurs at `L>=2`, terminate as `INCOMPLETE` and print the offending indices. No masking, interpolation or likelihood evaluation is allowed in that case.

This is a technical low-ell sanitization rule, not a theory change. The historical R2 `INCOMPLETE` result remains unchanged.
