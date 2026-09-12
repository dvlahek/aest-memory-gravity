# Dense radial Weyl extension — loader-only repair

## Trigger

The first execution of the preregistered dense-radial milestone aborted before any dense R2 trajectory was integrated. The frozen grids were printed correctly (`K0=6`, `K1=11`, `K2=21`), then the inherited D2C6 input loader raised

`InputIncomplete: expected 6 dense scalar histories, got 21`.

This is a technical input-cardinality guard inherited from the original six-mode D2C6 campaign. It is incompatible with the preregistered dense test, whose purpose explicitly requires 21 CLASS output wave numbers.

## Scope of repair

The repair is runtime-local to the dense-radial executable. It generalizes only the inherited check

`len(histories) == 6`

to

`len(histories) == len(K_MPC)`.

No D2C6 source file is edited. No equations, theory member, corrected-CLASS provenance, redshifts, radial nodes, RK4 settings, embedding mode, amplitudes, phases, interpolation method, tolerances, gates, or classification rules are changed.

The existing NumPy denominator source-load repair remains unchanged.

## Result status

The aborted execution produced no dense-node physics result and evaluated no preregistered dense-radial gate. Therefore it is classified as a pre-evaluation implementation abort, not as a physical or numerical FAIL of the dense-radial milestone.
