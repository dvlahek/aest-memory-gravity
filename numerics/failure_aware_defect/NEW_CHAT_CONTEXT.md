# New chat handoff — Failure-Aware Numerical Certification

We are starting a separate numerical-methods project extracted from the AeST Memory Gravity work. Keep it separate from the physics-certification thread.

## Repository

Repository: `dvlahek/aest-memory-gravity`

Branch:

`numerics/failure-aware-defect-certification`

Frozen science base commit:

`6282ed54e35d4db6b58fcd13d1c7403419f8afb7`

Main directory:

`numerics/failure_aware_defect/`

The branch is intentionally based on the frozen physics commit, but this new project may evolve independently. Do not merge exploratory numerics changes into `physics-first-gravitational-elasticity` without a separate science review.

## Research question

Can numerical certification for stiff continuum-memory systems detect when a formally valid high-order truncation bound has become non-informative, then switch to a lower-order direct-defect or regularized representation that preserves the actual numerical accuracy?

The key distinction is:

- solver failure,
- physical/model failure,
- discretization failure,
- certificate-width or proof-width failure.

The last category is the central target.

## Starting observation

In the AeST memory case, a conventional FD8 Taylor certificate requires a ninth derivative bound. Absolute UV majorization produces values of order `1e28` to `1e39` even when the finite production trajectory remains regular.

This led to the alternative target

`E_h(f) = D_h[f] - f'`

which should be enclosed directly from source values at the stencil nodes plus an exact or separately certified first derivative at the target node.

This changes the required regularity dramatically:

- old parent derivative order: up to 10,
- new parent derivative order: up to 2,
- old bath derivative order: up to 10,
- new bath derivative order: up to 1.

This derivative-order collapse is one of the strongest candidate contributions.

## Existing files

`README.md`
- project framing, novelty target and benchmark plan.

`toy_stiff_continuum_fd8.py`
- self-contained synthetic continuum example.
- demonstrates that a conventional FD8 ninth-derivative certificate can become much wider than the actual defect as stiffness increases.
- use this as the first reproducible methods benchmark.

`aest_regularized_uv_case_study.py`
- isolated AeST case-study diagnostic.
- uses existing frozen parent files from the main repository.
- writes only to `results/failure_aware_defect/`.
- does not certify the continuum tail or the full gravity problem.

`results_seed.json`
- frozen numerical evidence from the B1C -> R1A -> B2A/B2B -> B2C2A path.

## Key numerical evidence

### Naive high-jet route

Approximate representative values:

- weighted bath order 9: `3.125e34`
- weighted bath order 10: `1.303e39`

Interpretation: formal absolute high-derivative certificate is too wide to be useful.

### Signed finite-production route

- signed weighted order 9: about `1.897e28`
- compact core order 9: about `88`
- essentially the entire high-order value is carried by the UV sector.

Interpretation: the problem is not merely loss of cancellation among quadrature nodes. The stiff representation itself produces enormous high derivatives.

### Direct-defect reformulation

The dependency contract reduces the new required regularity to parent order 2 and bath order 1.

### Regularized UV variables

Use

`u = z - X`

and

`q = (v - X_s) / r^2`.

Observed finite frozen UV slopes:

- `p ~ r^-1.986`
- `q ~ r^-1.952`
- `u_s = v-X_s ~ r^0.048`

The finite-quadrature absolute UV proxy for the target `B10_x` contribution is about `6.05e-8`.

Important limitation: the global fitted slope of `sqrt(Eq)` is not sufficient for a uniform continuum proof. At the extreme last UV nodes the term `r|u|` begins to grow. Do not claim a uniform `Eq` theorem from B2C2A.

## Candidate paper

Working title:

**When High-Order Error Bounds Fail: Direct Defect Certification for Stiff Continuum-Memory Models**

Alternative:

**Failure-Aware Numerical Certification for Stiff Memory Models: Choosing Between High-Derivative and Direct-Defect Bounds**

Potential venues depend on theoretical strength:

- empirical/methodological workflow: Operations Research Forum is plausible,
- theorem + rigorous parameter-uniform bounds: Numerical Algorithms / Applied Numerical Mathematics / Journal of Scientific Computing become stronger targets.

Do not oversell novelty. There is existing literature on defect-based a-posteriori estimation and validated numerics. The novelty must be demonstrated around failure-aware route selection, representation-induced certificate blow-up, direct stencil-defect enclosure under continuum stiffness, and the derivative-order collapse.

## Next tasks in this numerics project

1. Run and freeze the self-contained toy benchmark over a broader stiffness/grid sweep.
2. Add a second non-gravity Maxwell/viscoelastic memory benchmark.
3. Define quantitative metrics:
   - actual defect,
   - Taylor certificate width,
   - direct-defect certificate width,
   - certificate-width / actual-error ratio,
   - runtime,
   - stiffness parameter.
4. Determine a rigorous direct-defect theorem under explicit source-value and first-derivative enclosures.
5. Investigate a principled route-selection criterion that detects proof-width failure without using the unknown actual error.
6. Use AeST only as the hard case study after the generic method is established.

## Style and scientific boundary

Problem-first and limitation-driven. Avoid claiming that a failed certificate means the physical model or numerical trajectory failed. Keep finite diagnostics separate from rigorous continuum certificates. Do not tune thresholds using observations. Do not use the gravity science gate as a methods-paper performance target.

## Suggested first prompt in the new chat

> We are starting the numerical-methods project on branch `numerics/failure-aware-defect-certification` in `dvlahek/aest-memory-gravity`. Read `numerics/failure_aware_defect/NEW_CHAT_CONTEXT.md`, `README.md`, `results_seed.json`, and the two Python scripts. Treat the AeST material only as a case study. First audit the novelty against current validated-numerics / defect-estimation literature, then design the generic benchmark and theorem path without changing the frozen gravity science branch.
