# NL1C7B5 Repair01 — regular-center source-limit implementation lock

## Status

Locked after Repair01 implementation and before the first Repair01 execution.

Parent B5 result remains frozen as

`NL1C7B5_CONSERVATIVE_INITIAL_DATA_IMPLEMENTATION_FAIL`

at result-freeze commit

`0c7c6fcc736c2f218b5704d2c6676a20c7944861`.

Parent result JSON SHA-256:

`6f59e45621d4895ee8fbb4ce125943fcd2939a534a7266fbebae4759190f79bc`.

## Frozen B5 preregistration and lock

Original B5 preregistration commit:

`13a1e33cc170688441fe979a277c3826952de5e0`.

Original B5 preregistration blob:

`f03e657c5f3ec3eebd4cffef65083dc789182103`.

Original B5 implementation lock commit:

`b0c03b610522be1c6b676eaa06c836e5e4c9f9a0`.

Original B5 implementation-lock blob:

`75eb60344353929941886e270a453ce047c173bc`.

All original B5 science gates, solver settings, quadrature rules and claim boundaries remain inherited unchanged.

## Repair01 preregistration

Repair01 preregistration commit:

`33a89e4fce0701bf69923e0cfe60ca5aa4751ab4`.

Repair01 preregistration file:

`docs/nl1c7b5_repair01_predata_regular_center_source_limit.md`.

Repair01 preregistration blob:

`4645bb34bad3fb01b6bd4ba0f72da067e38943b9`.

## Final Repair01 implementation

Initial center-limit implementation commit:

`4c2a727de0049d63f6d1337d324d92091873ea49`.

Final provenance-complete implementation commit:

`d88513127f694a7c1334f8ba6d7d8b3189680074`.

Frozen implementation file:

`nl1c7b/conservative_integral_initial_data_b5.py`.

Frozen implementation blob:

`3427a5e356230020a9418b320fbdecd2ec9fee1f`.

## Exact Repair01 code change

Relative to the original frozen B5 constructor, Repair01 changes only the following scientific-evaluation behavior:

1. after assembling the total local Hamiltonian source array, set
   `S_H[0]=0`;
2. after assembling the total local momentum source array, set
   `S_M[0]=0`;
3. evaluate the conservative residual at `z=0` before invoking the nonlinear driver;
4. abort as implementation failure if that initial residual is nonfinite;
5. record the finite initial-residual flag and Repair01 provenance.

No noncenter source or flux value is changed.

No quadrature weight is changed.

No solver setting is changed.

No Jacobian setting is changed.

No science threshold is changed.

## Analytic basis

The raw lambdified source expressions contain removable spherical-coordinate `0/0` forms at `R=0`.

For the frozen regular center,

- `R(0)=0`;
- `R_t(0)=0`;
- `L_r(0)=0`;
- radial fluxes vanish;
- all regular scalar quantities remain finite.

The total local source limits are therefore

`S_H(0)=0`

and

`S_M(0)=0`.

The repair replaces undefined floating-point evaluation of these removable center forms with their analytic regular limits.

It introduces no fitted center value and no numerical extrapolation.

## Frozen construction and certification

Still exactly inherited from B5:

- eta=0;
- Simple, beta=1;
- scales 5,10,20 h^-1 Mpc;
- Nr=256,512;
- lambda=1 only;
- physical variables only `(L,R_t)`;
- `Y4=0,Qmean=0`;
- degree-8 nine-node conservative cell quadrature;
- parent-fixed normalization;
- `3-point, abs_step=3e-6`;
- half-band 16;
- one TRF solve from `z=0`;
- `ftol=xtol=gtol=1e-12`;
- `max_nfev=200`;
- `x_scale='jac'`;
- no restart, continuation, multistart or fallback;
- safety bounds `|y_L|,|q_Rt|<=0.5`;
- exact-Q and gauge tolerances `1e-12`;
- final science gate remains the unchanged original differential B4
  `max epsilon_H,max epsilon_M <=1e-7`;
- historical two-grid correction ratio `<=2`;
- state NPZ only on full science PASS.

## Allowed interpretation

The first B5 implementation-fail result remains frozen and may not be relabelled.

Repair01 may produce any of the already frozen B5 terminal science classifications after the implementation issue is removed.

No second center-representation repair and no B5 solver-parameter tuning sequence is licensed after the first Repair01 execution.
