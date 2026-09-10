# C3 direct bath bridge R1 — finite-domain technical repair pre-data declaration

## Historical status

The first direct bath-bridge audit on commit `a6e9af831193db92f393bb93ff7161f8728a4999`, workflow run `34481903014`, is an immutable technical `C3_BATH_BRIDGE_INCOMPLETE`. CLASS and the 39-state instrumentation built successfully, but the audit stopped before the first `BATH_POINT` comparison with `ValueError: y must contain only finite values.`

The failure occurs because the dense CLASS perturbation history begins earlier than the independent offline background interpolator used by D2C6C. Evaluating `data["bg"]["Q"](a)` outside its retained domain returns non-finite values, which then enter the PCHIP source construction.

No physical or numerical bath comparison was produced by the incomplete run.

## Frozen repair

R1 changes only the diagnostic-domain selection in `nl1c6d2c6c_bathaudit/direct_bath_bridge_audit.py`.

For each of the same six frozen modes, after sorting and uniquing the dense CLASS history, the audit will evaluate the offline background `Q(a)` on the CLASS scale-factor samples and retain the earliest contiguous usable history for which all quantities needed by the comparison are finite:

- tau and scale factor a;
- CLASS alpha and theta;
- CLASS eta0 tangent-force output;
- all 39 CLASS q_j states;
- all 39 CLASS p_j states;
- offline-background Q(a);
- the derived chi and chi/a source.

The audit will report both the raw earliest CLASS tau and the retained common-domain start tau. The retained start must still precede the z=6 checkpoint and contain at least 100 samples. No extrapolation of Q, chi, q_j, p_j, or the source is permitted.

The offline bath is initialized from the transformed CLASS q_j,p_j states at that retained common-domain start exactly as preregistered previously. From that identical state onward, the existing D2C6C `bath_advance` routine and the same main-step scale are used.

## Frozen equations and gates

R1 does not change:

- CLASS SHA or any physical AeST/memory patch;
- physical eta=0;
- tau H0=1;
- bath order 39;
- six k modes or nine redshift checkpoints;
- mapping `z_j = omega_j q_j / (k sqrt(w_j))` and the corresponding derivative mapping;
- D2C6C `bath_advance` equations;
- source construction after the finite common-domain start;
- thresholds `Z_STATE_REL <= 5e-3`, `ZP_STATE_REL <= 5e-3`, `B_REL <= 5e-3`, and `CHI_REL <= 1e-8`;
- classification logic;
- `FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False` for this diagnostic regardless of outcome.

A failure to find a valid common finite interval before z=6 remains `C3_BATH_BRIDGE_INCOMPLETE`. A technically complete comparison keeps the previously frozen `C3_BATH_BRIDGE_PASS` versus `C3_BATH_BRIDGE_MISMATCH_IDENTIFIED` logic.
