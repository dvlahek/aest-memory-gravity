# NL1C7B8 — zero-parameter regular-center IVP implementation lock

## Status

Implementation locked before the first NL1C7B8 execution.

B8 is a new regular-center representation. It is not a B7 bracket repair.

## Parent results

B6 structural certification:

`NL1C7B6_SYMBOLIC_RADIAL_REDUCTION_PASS`.

B6 result-freeze commit:

`70c9fc2aa58b76bf3579260e54c6d85097769160`.

B6 result-freeze blob:

`2d2b64f15c581f750d7553af2bb101a54b8cf991`.

B7 construction result:

`NL1C7B7_REDUCED_RADIAL_CONSTRUCTION_FAIL`.

B7 result-freeze commit:

`6bd01d8e4c825fe4f150a851c4dc402644b664cc`.

B7 result-freeze blob:

`ab9c2de0d97f39e98b97fa4ca205a95d8d15b8a3`.

B7 result JSON SHA-256:

`449201305c535e24e592296f5e2a53e7fc0866b5cae2970a147c2bcebe12bfc6`.

## Preregistration

B8 preregistration commit:

`6f0bda207d8f38e3f24b747564196a42750aa668`.

Preregistration file:

`docs/nl1c7b8_predata_regular_center_ivp_initial_data.md`.

Frozen preregistration blob:

`9eb6db56a241f45a00bec59148ef45a649cc2c02`.

## Final implementation

Initial implementation commit:

`439323450b7ad6bd095c2c1dbb1691e4d0e34098`.

Final center-audit-complete implementation commit:

`68b0ee45ed27e6db571571cf3998c24c8f8ab814`.

Implementation file:

`nl1c7b/regular_center_ivp_initial_data_b8.py`.

Frozen implementation blob:

`9e629cdc49b9fe1defc9b5308cb72c7613890cbf`.

The only post-initial-implementation change replaces descriptive non-GR center-order assertions by SymPy machine checks.

No physical equation, threshold or numerical setting changed.

## Exact center representation

B8 fixes the regular center algebraically.

Hamiltonian center identity:

`H(0)=2L_0-2R_r(0)^2/L_0`.

Positive regular solution:

`L(0)=R_r(0)`.

Momentum center data:

`R_t(0)=0`

and

`R_{t,r}(0)=L_t(0)R_r(0)/L(0)=L_t(0)`.

There is no shooting parameter.

## Frozen numerical method

Use the exact B6/B7 reduced first-order RHS.

Reuse the frozen B7 local degree-8 / nine-node representation of all parent fields.

Primary launch:

`epsilon=1e-5 r_1`.

Control launch:

`epsilon=1e-4 r_1`.

For each launch:

`ell_0=log[R_r(0)/a_i]`;

`ell(epsilon)=ell_0`;

`R_t(epsilon)=epsilon L_t(0)`.

Integrator:

`scipy.integrate.solve_ivp`, method `DOP853`.

Settings:

- rtol `1e-11`;
- atol `1e-13`;
- max_step equal to the frozen radial grid spacing.

No root finder, no bracket, no shooting, no boundary fit.

## Frozen outer predictions

Both are predictions.

Require primary-state:

`abs[L(r_max)-a_i]/a_i <=1e-7`.

Require:

`abs[R_t(r_max)-a_i H_i r_max]/abs[a_i H_i r_max] <=1e-7`.

No constant shift or outer correction is allowed.

## Frozen science gates

- parent/provenance exact;
- local polynomial derivative reproduction <= `1e-12` abs-or-rel;
- exact B6/B7 RHS identities PASS;
- center symbolic identities and non-GR order checks PASS;
- all six primary/control IVPs complete;
- primary/control relative L2 in L <= `1e-6`;
- primary/control relative L2 in R_t <= `1e-6`;
- outer L relative mismatch <= `1e-7`;
- outer R_t relative mismatch <= `1e-7`;
- exact-Q error <= `1e-12`;
- non-`L,R_t` fields bitwise frozen;
- all-node L/R_t correction safety <= `0.5`;
- unchanged original B4:
  - `max epsilon_H<=1e-7`;
  - `max epsilon_M<=1e-7`;
- two-grid correction ratio <= `2.0`.

## Output rule

State NPZ only on full

`NL1C7B8_REGULAR_CENTER_INITIAL_DATA_CERTIFIED`.

Any non-PASS leaves NPZ absent.

## Frozen imported blobs

- B7 implementation:
  `adf268f4e49c1b8118d9bb40756269f959472b5a`;
- base B4:
  `8559120dc273be3174eca130ca313ed6ff5acb25`;
- Repair01:
  `253a0ae2a19a597f06358704ea276c9005973af3`;
- Repair09:
  `0cd67cecfbd590cb8819ad37314dc5b49047bc93`;
- Repair16:
  `fbd7d24f748fc398638d4eea4b7707801161e52a`;
- Repair18a:
  `767199e8ab620f5d6dabd50d0efde9828f22048b`;
- Repair08:
  `94fb3f42a7c819b0525860f7344d5dbaff93da19`;
- C7A reconstruction:
  `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`.

## Terminal boundary

No B8a/B8b parameter-tuning sequence is licensed after the first complete locked B8 execution.

Only full B8 certification licenses eta=0 short-time evolution.
