# v0.19n — strict structural-null extra-state control

v0.19p established that the persistent Exp–CDM residual is not ordinary CLASS precision error: the primary TT/EE/TE difference stayed at `6.855294693e-4` from the standard run through the strictest tested perturbation tolerance, while the CDM and Exp self-convergence changes were zero at written-output precision.

v0.19n tests the remaining software explanation directly.

The official CLASS tree is first patched with the validated v0.19 bridge, but the physical AeST switch remains **off**. A second test-only patch adds the flag

```text
aest_null_states = yes
```

which allocates the same two extra scalar state slots used by the eta=0 AeST bridge,

```text
alpha_aest
E_aest
```

while keeping all physics exactly CDM:

- standard CDM background;
- standard CDM density and velocity equations;
- no AeST pressure or stress-energy contribution;
- `alpha_aest = E_aest = 0` initially;
- `alpha_aest' = E_aest' = 0` identically.

Thus the only intended change is the ODE-vector dimension and the presence of two frozen zero components.

The campaign runs both the standard precision (`p0`) and the strict v0.19p precision (`p3`). It compares CMB spectra, matter power, background, and thermodynamics numerically.

Interpretation:

- if null-extra-states and CDM are identical, ODE dimension/adaptive error normalization cannot explain the v0.19 Exp–CDM residual;
- if a residual appears and changes with precision, the extra-state solver structure is implicated;
- memory remains strictly OFF in every run.

A PASS here still does **not** make the regular `chi_i=0, E_i=0` AeST proxy the exact radiation-era adiabatic initial condition. It only isolates the origin of the numerical residual more sharply.
