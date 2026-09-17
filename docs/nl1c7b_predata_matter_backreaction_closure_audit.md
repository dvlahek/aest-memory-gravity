# NL1C7B predata — pressureless-matter backreaction closure audit

Status: **PRE-RESULT / FROZEN BEFORE AUDIT EXECUTION**

Classification before audit:

`NL1C7B_PREDATA_MATTER_BACKREACTION_CLOSURE_AUDIT`

## Motivation and boundary

NL1C7A has certified unique eta=0 growing-mode spherical initial data. Before any nonlinear spherical trajectory is evolved, NL1C7B must establish that the frozen NL1C6 spherical equations contain the gravitational backreaction of the pressureless matter whose overdensity and radial velocity are supplied by NL1C7A.

The purpose of this checkpoint is only to audit the already frozen NL1C6 implementation. It must not add a matter action, stress-energy source, force law, pressure floor, viscosity, shell prescription, gauge driver, finite eta, or any collapse observable.

Historical NL1C6 and NL1C7A classifications remain immutable. If this audit identifies a missing matter-backreaction component, the result is `INCOMPLETE` for the requested NL1C7 self-gravitating evolution, not a retroactive rewrite of historical artifacts.

## Frozen provenance

Parent NL1C7A result:

- result commit: `4090367131f0a4fac22cf13571f157cab0a284dc`
- classification: `NL1C7A_REPAIR01_DENSE_TIME_SPHERICAL_BRIDGE_CERTIFIED`
- official evaluator run: `35183893359`
- head: `e650fcb2344813cc0e3c91a2f0ae99b9c7bf43ac`
- artifact: `10481526695`
- artifact SHA256: `c2ede2e602e35bbd52afdc0a5eee22cb1bf5c6efc2e1063bf8f2b91a0554fb6c`

Frozen NL1C6 implementation under audit:

- `nl1c6/spherical_self_gravity_g1_g10.py`
- blob: `e3eeb820fa1826fb7ac29f3fce2fe0bdde8d564f`
- `nl1c6/g11_solver_readiness.py`
- blob: `970ccb164f8ab7d3de6681ff4af940b1638d1686`
- C6 result classification: `NL1C6_SPHERICAL_SELF_GRAVITY_CLOSURE_PASS`
- C6 G1-G10 run: `35088549978`
- C6 G11 run: `35089436959`

## Frozen specification under audit

The NL1C6 preregistration requires pressureless minimally coupled matter and a closed spherical component system for `(g_ab,R; u,phi,q_j; T_m^{mu nu})` directly from the frozen action. It also requires independent variations with respect to `N,b,L,R,u,phi`, with lapse and shift retained as constraints. Matter conservation/geodesic equations alone are not sufficient to establish gravitational backreaction.

## Audit questions

The audit must answer mechanically, from the frozen source only:

1. Does the action expression used for the NL1C6 variational audit contain a pressureless-matter degree of freedom, matter density/current, or an equivalent matter action contribution?
2. Do the generated `N`, `b`, `L`, or `R` Euler-Lagrange/source blocks depend on matter variables or a stress-energy contribution?
3. Are matter continuity/geodesic equations present only as a separate conservation control?
4. Is the C6 matter gate set independently of an action-derived matter source?
5. Would evolving the existing field equations with an NL1C7A overdensity therefore evolve test matter on the field-sector geometry instead of a self-gravitating overdensity?

No semantic judgement may be substituted for source inspection. The audit implementation must parse the frozen Python source and report the exact relevant assignments/symbol dependencies.

## Locked gates

### B0-G1 — provenance

The parent NL1C7A result commit and the two NL1C6 source blobs must match exactly.

### B0-G2 — variational-action matter inclusion

PASS only if the action expression used to generate the NL1C6 variational source blocks contains an explicit pressureless-matter contribution or an equivalent matter variable/current whose metric variation can generate `T_m^{mu nu}`.

A standalone textual matter-conservation dictionary does not satisfy this gate.

### B0-G3 — gravitational source dependence

PASS only if at least the lapse/Hamiltonian and metric/radial variational blocks generated from that action depend on matter variables or an action-derived matter stress-energy source.

### B0-G4 — conservation/backreaction consistency

PASS only if the same matter sector that supplies the stress-energy backreaction also supplies, or is demonstrably consistent with, the pressureless continuity/geodesic equations used by C6.

### B0-G5 — no hidden phenomenological closure

The audit must confirm that no shell force, GR/Poisson replacement force, drag, pressure floor, artificial viscosity, or finite-eta term is being used to compensate for missing matter backreaction.

## Classification

If B0-G1 through B0-G5 all pass:

`NL1C7B_MATTER_BACKREACTION_CLOSURE_AUDIT_PASS`

This licenses construction of the eta=0 nonlinear method-of-lines evolution from the already frozen equations.

If the source is internally inconsistent with an explicit frozen matter action/stress-energy implementation:

`NL1C7B_MATTER_BACKREACTION_CLOSURE_FAIL`

If the pressureless matter dynamics are specified through conservation/geodesic equations but their stress-energy backreaction is absent from the variational field equations, or if completing it requires adding a matter action/physical field representation not present in the frozen implementation:

`NL1C7B_MATTER_BACKREACTION_CLOSURE_INCOMPLETE`

The `INCOMPLETE` classification requires a separate preregistered pressureless-matter variational closure before any self-gravitating collapse/turnaround result may be produced.

## Claim boundary

This audit does not test a trajectory. It does not alter NL1C6 or NL1C7A. It only determines if the frozen equations already licensed by those checkpoints are sufficient for the self-gravitating eta=0 initial-value problem required by NL1C7.