# GE19 Repair30 reduced H2/Z11 reclosure — implementation lock

## Scope

Repair30 solves only

`L_total Z11 = -M1[Z10,q10]`

on the same frozen reduced AeST+dust+Lambda operator/background used by the Repair22/Repair27 chain.

It does not solve H4/Z21 and does not introduce finite eta.

## Frozen files

Preregistration:

- file:
  `ge19/repair30_predata_reduced_h2_z11_reclosure.json`;
- blob:
  `264b52832e762dd2010df1eba83e5f2c1a4d8874`;
- commit:
  `5fd14e9dc46ced04a838d79cc3b47319c4e4f22f`.

Implementation:

- file:
  `ge19/repair30_reduced_h2_z11_reclosure.py`;
- blob:
  `2ce2bf7ccd5bf48504c619500d12d4eb03bfe259`;
- commit:
  `91e59269dbfd4476230cf8cc25c5579b44691b8d`.

Dedicated prelock:

- workflow:
  `.github/workflows/ge19-repair30-prelock-audit.yml`;
- blob:
  `3ad421859cb6745c0708fb247222b135381cf1db`;
- commit:
  `55e690ebe1414b0929eb75c72ea1b75b4ba9f4a3`;
- successful run:
  `35747790884`;
- job:
  `106813756378`.

Global static audits also passed for the preregistration and implementation commits.

## Frozen H2 parent chain

Repair13:

- JSON SHA-256:
  `ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7`;
- NPZ SHA-256:
  `011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3`.

Repair22:

- JSON SHA-256:
  `7d53b2458183c6b2cc326acdded70b2c3ce1fab959d8456e56d3b4f1f86ef374`;
- NPZ SHA-256:
  `3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16`.

Repair27:

- JSON/FULL SHA-256:
  `99a2183e7088c7492f624cae2d294612380714c1d81aa7ff49cc4fcd1c62c74b`;
- NPZ SHA-256:
  `2b1566d402e4c9e8daee8e5c7084b3da7735442b4fb604d51489b708662fd9c0`.

Repair29B:

- classification:
  `GE19_REPAIR29B_R2_PRIMARY_R3_CONTROL_FULL_STATE_ETA_TANGENT_PASS`;
- successful run:
  `35744723602`;
- certified representation:
  R2 primary complete eta tangent with targeted R3 numerical control.

R2 reference payload:

- frozen Repair28 NPZ SHA-256:
  `101c38d91344d12071ecb343c35769326f80975e013b7d159f573aae73879705`;
- bytes:
  `530980`.

GE15 cancellation-free dense trace:

- SHA-256:
  `7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f`.

## Frozen reduced dictionary

The Repair29B R2 tangent is mapped to the reduced variables as

- `N11 = psi_eta`;
- `S11 = -a phi_eta`;
- `u11 = -(k/a) alpha_eta` with the frozen sine parity;
- `varphi11 = Q a theta_dark_eta/k^2`;
- `T11 = a theta_dust_eta/k^2`;
- `delta_varrho11 = 3 rho_dust delta_dust_eta`.

The reduced dust tangent is evolved on each frozen C background and is initialized from the absolute full-standard-sector eta tangent at a=0.4.

## Frozen memory source

Define

`B10 = X10 - weighted_z10`

with

`X10 = Q u10 + i k varphi10/a`.

Repair27 supplies `weighted_z10`.

The normalized GE05 first-directional memory source reduces exactly to

- aether residual:
  `-Q a^3 B10/2`;
- scalar residual:
  `+a^2 partial_x(B10)/2`;
- direct metric M1:
  zero;
- dust M1:
  zero.

Therefore the H2 right-hand side is exactly

- aether:
  `+Q a^3 B10/2`;
- scalar:
  `-a^2 partial_x(B10)/2`.

The dedicated prelock re-derives and checks these identities symbolically.

## Frozen grids and gates

- primary: Nt128;
- control: Nt64;
- input Fourier modes: m={3,5,8,10,15,20};
- C envelope: C_min/C_star/C_max.

Frozen gates:

- B10 primary/control relative L2 <= `5e-3`;
- linear-system residual <= `1e-8`;
- shift backward error <= `1e-6`;
- anisotropy backward error <= `1e-6`;
- Nt128/Nt64 Z11 state relative L2 <= `5e-3`;
- inherited dynamic boundary mismatch <= `1e-8`;
- reduced chi11 versus Repair29B R2 parent relative L2 <= `5e-3`;
- reduced chi11 C-envelope relative L2 <= `5e-3`;
- all outputs finite.

No threshold may be changed after the first valid science result.

## Stop rule

The first Repair30 execution that emits a valid science JSON is frozen as PASS or FAIL.

- PASS licenses a separately preregistered H4/Z21 construction.
- FAIL keeps H4/Z21 blocked and must be localized without relaxing Repair30 gates.
- implementation/execution failures before a valid JSON may be repaired without changing the science contract.

Repair30 itself performs no H4/Z21 solve.
