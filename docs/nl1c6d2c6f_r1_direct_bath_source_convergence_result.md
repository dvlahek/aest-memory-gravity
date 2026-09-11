# D2C6F-R1 result — direct-bath gravitational-source convergence

Date: 2026-09-11

Parent D2C6F classification remains historically unchanged:

`NL1C6D2C6F_FINITE_ETA_DIRECT_GRAVITATIONAL_SOURCE_FAIL`

D2C6F-R1 final classification:

`NL1C6D2C6F_R1_DIRECT_BATH_SOURCE_CONVERGENCE_PASS`

The local R1 run evaluated the preregistered six members at `eta=0.125` with the independent direct tan-Gauss-Legendre Drude sequence `N_bath={128,256,512}`. All direct trajectories were finite and healthy, retained the scalar-current constraint and positive `1+j_eff`, and satisfied the completed-square energy identity.

The primary preregistered convergence results were:

- worst direct `256 -> 512` gravitational-source relative L2: `2.07e-7`;
- worst direct `256 -> 512` retained-state/E relative L2: `1.52e-9`;
- frozen source and state/E gate: `1e-2`.

Thus the direct quadrature is converged by roughly five to seven orders of magnitude below the frozen gates on the previously unresolved source sectors. The original compressed `39 -> 47` failure is therefore retained as a compressed-bath limitation for quadratic direct metric-stress observables, not reclassified as a physical instability.

The run explicitly returned:

`SELF_CONSISTENT_WEAKFIELD_FEEDBACK_STEP_LICENSED=True`

The license is restricted to a separately preregistered weak-field feedback stage using direct `N=256` as primary and direct `N=512` as bath-order control. It does not license arbitrary-amplitude nonlinear GR/AeST evolution or observational inference.
