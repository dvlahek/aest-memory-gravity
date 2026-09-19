# NL1C7B7 — reduced-radial shooting implementation lock

## Status

Implementation locked before the first NL1C7B7 execution.

Parent structural certification:

`NL1C7B6_SYMBOLIC_RADIAL_REDUCTION_PASS`.

Parent result-freeze commit:

`70c9fc2aa58b76bf3579260e54c6d85097769160`.

Parent result-freeze blob:

`2d2b64f15c581f750d7553af2bb101a54b8cf991`.

Parent result JSON SHA-256:

`ed1efdac5dee72d8c57cbda23d074213babd15fdf3bc7adc18e61789f862e635`.

## Preregistration

Final B7 preregistration commit:

`3d77dd915b1fe1f5b26d102e8c7d9f90ec508fca`.

Preregistration blob:

`f14c8bd97ebaf8817d0939b9ded54cd0c9e43166`.

## Final implementation

Implementation commit:

`edbda966c50bf1c2b5814f28ffd9db3a889cd474`.

Implementation file:

`nl1c7b/reduced_radial_initial_data_b7.py`.

Frozen implementation blob:

`adf268f4e49c1b8118d9bb40756269f959472b5a`.

## Frozen numerical construction

Exactly six cases:

- scales 5,10,20 h^-1 Mpc;
- Nr=256,512.

Only physical `L` and `R_t` change.

The exact B6 reduced H/M system is generated again from the frozen action source/flux dictionary.

No profile-wide nonlinear least-squares solve is used.

### Solved variables

`ell=log(L/a_i)`

and

`w=R_t/(a_i H_i R_s)`.

### Frozen-field representation

Every required frozen radial field is represented by the unique local degree-8 polynomial through the same nine-node stencil family used by the original B4 derivative matrix.

The implementation explicitly checks first-derivative reproduction against `b4.dmat` at all grid nodes.

Tolerance:

`1e-12` abs-or-rel.

### Regular-center launch

Primary:

`epsilon=1e-5 r_1`.

Control:

`epsilon=1e-4 r_1`.

For a trial `ell_0`:

`L_0=a_i exp(ell_0)`.

Launch:

`ell(epsilon)=ell_0`

and

`R_t(epsilon)=epsilon L_t(0)R_r(0)/L_0`.

No coefficient division occurs at `r=0`.

### Scalar shooting

Frozen bracket:

`ell_0 in [-0.5,0.5]`.

Only target:

`ell(r_max)=0`.

Thus

`L(r_max)=a_i`.

Root driver:

`scipy.optimize.brentq`.

Settings:

- xtol `1e-12`;
- rtol `1e-12`;
- maxiter `100`.

No bracket expansion or alternate root driver.

### Radial integrator

`scipy.integrate.solve_ivp`

with

`DOP853`.

Settings:

- rtol `1e-11`;
- atol `1e-13`;
- max_step equal to the frozen radial grid spacing.

No integrator or tolerance sweep.

## Frozen science gates

- center launch primary/control relative L2 in L <= `1e-6`;
- center launch primary/control relative L2 in R_t <= `1e-6`;
- predicted outer R_t relative background mismatch <= `1e-7`;
- exact-Q error <= `1e-12`;
- all non-`L,R_t` fields bitwise frozen;
- `max|log(L/L_parent)|<=0.5`;
- `max|(R_t-R_t,parent)/(a_i H_i R_s)|<=0.5`;
- unchanged original B4:
  - `max epsilon_H<=1e-7`;
  - `max epsilon_M<=1e-7`;
- two-grid correction ratio <= `2.0`.

Historical Repair18d1 `Y4/Qmean` functionals are descriptive only and are not imposed.

## Output rule

A state NPZ is written only for full

`NL1C7B7_REDUCED_RADIAL_INITIAL_DATA_CERTIFIED`.

Any non-PASS classification must leave the state NPZ absent.

## Frozen imported blobs

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
- Repair19:
  `2532094b518dfc2990fa0d77d8123d793b0107b3`;
- Repair19c:
  `f27ed8b39c1351e27d4f3b43b195ff4423e04c76`;
- Repair08:
  `94fb3f42a7c819b0525860f7344d5dbaff93da19`;
- C7A reconstruction:
  `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`.

## Terminal boundary

No B7a/B7b solver-parameter repair sequence is licensed after the first complete locked B7 run.

Only full B7 certification licenses eta=0 short-time evolution.
