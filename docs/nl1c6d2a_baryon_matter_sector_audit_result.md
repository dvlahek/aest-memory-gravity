# NL1C6D2A result — baryon matter-sector audit

Status: **LOCKED RESULT**.

Classification:

```text
NL1C6D2A_BARYON_MATTER_SECTOR_AUDIT_PASS
```

This result follows the preregistered D2A matter-sector audit and does not alter any historical R3 or D1 classification.

## Frozen identities

Repository branch:

```text
v053-model-freeze-planck
```

Result-producing head:

```text
4b27318b3587fa8182de98d6d50b165c44e7790a
```

Audit code SHA-256:

```text
c2b20da51bfb6390e78dc878e46cd811433ba345c0419d8e435ecab307b0670e
```

Frozen CLASS commit:

```text
e85808324f51fc694d12e3ed7439552a3c3f9540
```

Frozen NL1C5B input artifact SHA-256:

```text
0ab60cbc32210ad3fb75c881f91a9db11148280e9223ea644680ed8cdfbaa590
```

## Results

The fresh density block is exactly identical to the frozen NL1C5B source on the native grid:

```text
k-grid relative mismatch = 0
z-grid absolute mismatch = 0
fresh d_b vs frozen relative L2 = 0
fresh d_m vs frozen relative L2 = 0
t_b finite = true
```

The Newtonian-gauge baryon continuity equation

```text
delta_b' + theta_b - 3 phi' = 0
```

was tested on dense CLASS histories for all six frozen low-k modes. The maximum normalized L2 residual was

```text
2.247707644786448e-06
```

against the preregistered gate

```text
2e-3.
```

The independent dense-history/native-grid interpolation closure gave

```text
max d_b relative L2 = 2.1416094427359878e-07
max t_b relative L2 = 5.446349587568204e-07
```

against the frozen gate

```text
2e-4.
```

All D2A gates passed.

## Preserved matter state

The resulting matter artifact contains on the same native grid

```text
k_native_h
z_native
d_b
t_b
d_m
phi
psi
```

with 912 native k values and 24 native times. The six primary modes `{0.03,0.05,0.08,0.10,0.15,0.20} h/Mpc` are exact native modes.

## Interpretation

This PASS establishes that the frozen baryon-density source used by NL1C5B/R3 has a finite same-model baryon velocity-divergence history and that the pair satisfies the Newtonian-gauge CLASS continuity equation within the preregistered tolerance.

It does **not** establish nonlinear full-J AeST evolution, physical branch selection, finite eta, or a causal-memory result.

In particular, D1A validated a one-dimensional longitudinal weak-field gravitational reduction about the Minkowski/static weak-field setting. D2A supplies a cosmological FLRW matter history. A further action-derived FLRW source/gravity coupling audit is therefore required before a time-dependent cosmological nonlinear branch-selection run. Hubble/friction terms or a time-dependent `P_alpha` source may not be inserted by hand.
