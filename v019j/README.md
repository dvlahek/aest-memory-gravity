# v0.19j — first finite-eta cosmological memory gate

v0.19i closed the leading radiation-era adiabatic initial-condition gate in a CDM-controlled start-time window. v0.19j is the first CLASS campaign with `eta > 0`.

The intended implementation uses the positive finite Drude bath already validated in v0.17. For each positive node `r_j,w_j`, define `omega_j=r_j/tau` and normalized bath variables `u_j` through `y_j=sqrt(eta w_j) u_j`. In cosmic time,

```text
u_j¨ + 3 H u_j˙ + omega_j^2 u_j = omega_j (k/a) chi
```

and

```text
B_chi = eta sum_j w_j [ chi - (a omega_j/k) u_j ].
```

The AeST closure receives `-(Q/2) B_chi`. The leading adiabatic mode has `chi_i=0`, so the regular bath initial condition is `u_j=u_j'=0`.

Memory remains excluded from the background and from an independent first-order Einstein stress source, consistently with the zero-bath FLRW background derivation.

Before the patch is committed, the applied v0.19i CLASS source is inspected to anchor the memory states and conformal-time normalization exactly.
