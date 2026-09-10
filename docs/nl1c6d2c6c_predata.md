# NL1C6D2C6C pre-data declaration — eta=0 retarded-memory tangent on all 27 nonlinear trajectories

## License and purpose

This stage is licensed only by the locked NL1C6D2C6B PASS on commit `3e1ec4a72be081318d06af174d3afcd855cbbc72`, Actions run `34447971316`, which reported exact 27/27 coverage and `NEXT_NONLINEAR_MEMORY_STEP_LICENSED=True`.

D2C6C is the mandatory eta=0 nonlinear-memory step before any finite physical eta or observational likelihood. It tests whether the already certified retarded Drude bath and first-order memory forcing can be propagated consistently on the D2C6B nonlinear scalar-current trajectories. It is a numerical/variational certification stage, not a detection or likelihood stage.

## Frozen physics and trajectory family

The corrected CLASS target remains v3.3.4 SHA `e85808324f51fc694d12e3ed7439552a3c3f9540`. The AeST background, `K_B=0.0665`, scalar-sector normalization, external linear metric/matter fields, D2C6B periodic box, six seeded modes/phases, redshift interval `z=6..0.2`, and nine frozen checkpoints are unchanged.

The 27 nonlinear members are exactly the D2C6B Cartesian family

- `sigma in {-1,0,+1}`,
- `kind in {simple, exponential, sharp}`,
- `beta0 in {1,0.5,0.1}`,
- `epsilon_mix=0.25`.

No member may be removed or selected after seeing a memory response.

The stable canonical base state remains

`y=(alpha, chi, P_chi, S_c)`, with `S_c=P_alpha+Q P_chi`,

and

`E=[invLap(-S_c/(2a))-(2-K_B) chi]/K_B`.

The historical D2C6A cancellation-form FAIL remains unchanged.

## Frozen eta=0 bath

Physical `eta` is exactly zero throughout this stage. The retarded bath is nevertheless evolved on the unperturbed base trajectory because its unscaled eta=0 response is the source of the variational tangent.

The bath is the previously validated positive compressed tau-H0=1 design from v0.19u/v0.19w:

- primary order: 39 positive nodes/weights,
- bath-order control: 47 positive nodes/weights,
- `tau H0 = 1`,
- regular primordial bath initial condition,
- no memory background correction,
- no direct linear Einstein stress.

For a scalar bath coordinate `z_j`, the equivalent real-space equation is

`z_j,tt + 3 H z_j,t + omega_j^2 z_j = omega_j^2 chi/a`,

with the eta=0 closure residual

`B_chi^(0) = chi - a sum_j w_j z_j`

(the stored positive weights sum to one). The stiff bath must be propagated with a stable analytic/frozen-background oscillator step or a numerically demonstrably equivalent scheme; explicit unstable stepping of the highest-frequency nodes is not allowed.

The bath at `z=6` is not reset to zero. Its state must contain the retarded prehistory accumulated from the regular early-time eta=0 solution. The first-order AeST tangent at `z=6` must likewise include its linear prehistory; a zero tangent imposed at `z=6` is outside this preregistration.

## Exact tangent equations in the stable canonical variables

Let

`v=(delta_alpha, delta_chi, delta_Pchi, delta_Sc)=d y/d eta |_(eta=0)`

and

`delta_E=[invLap(-delta_Sc/(2a))-(2-K_B) delta_chi]/K_B`.

Background quantities and the external CLASS metric/matter fields are held fixed at eta=0.

For the D2C6B nonlinear flux

`N[chi]=div[(1+j_eff(x,Z)) grad chi]`,

`x=ACC_CONV |grad chi|/a`, and

`j_eff=j(x;beta0,kind) [1 + sigma epsilon_mix x^2/(1+x^2) tanh(Z)^2]`,

the exact one-dimensional Frechet derivative used in D2C6C is

`delta_N = div[A_eff grad(delta_chi)]`,

`A_eff = 1 + j_eff + x d(j_eff)/dx`.

This form is regular at zero gradient and must use the analytic `j` derivative already present in the frozen D2C6B constitutive family.

The homogeneous tangent is the exact linearization of the D2C6B stable-canonical RHS. The direct eta=0 memory source is frozen by the already certified CLASS variational identity

`dE'/deta|0 = -a Q B_chi^(0)/(2 K_B)`.

In stable canonical variables this is implemented as

`M = a^2 Lap(B_chi^(0))`,

with direct additions

`delta_Pchi' += M`,

`delta_Sc' += Q M`.

Differentiating the stable elliptic constraint must recover the CLASS forcing above. No additional memory term may be inserted into the background, metric stress, or elliptic definition of E.

## Prehistory and linear reference

The eta=0 retarded bath and tangent are initialized from the same corrected linear AeST history that supplies the D2C6B state at z=6. The implementation must retain the full retarded prehistory rather than restart the response at z=6.

A linear-control propagation from z=6 to z=0.2 must be compared with the already certified eta=0 variational CLASS tangent convention. The comparison uses `alpha`, `E`, and `chi` on the nine frozen checkpoints and is a numerical identity/regression test, not an observational fit.

## Frozen discretizations

For order 39:

- primary: `Nx=128`, tangent/base RK4 `Nstep=4096`,
- time control: `Nx=128`, `Nstep=8192`,
- spatial control: `Nx=256`, `Nstep=4096`.

The order-47 bath control uses the primary `Nx=128`, `Nstep=4096` trajectory discretization. Spectral resampling from 256 to 128 follows D2C6B. The base trajectory, bath and tangent must be evaluated consistently at RK4 stage times; bath substepping/analytic propagation may be used but its scheme is frozen before reading D2C6C results.

## Locked gates

D2C6C PASS requires all of the following.

**C1 — provenance and coverage.** Corrected CLASS provenance passes, the parent D2C6B result is the locked PASS above, and all 27 frozen members are present exactly once.

**C2 — algebraic/variational bridge.** The stable-canonical memory-source identity reconstructing `dE'/deta|0=-a Q B/(2 K_B)` has relative L2 error `<=1e-10`. A deterministic directional finite-difference audit of the nonlinear flux Jacobian `delta_N` has relative L2 error `<=1e-6` over the frozen constitutive family.

**C3 — linear eta=0 tangent regression.** For the shared linear control, relative L2 errors against the corrected CLASS eta=0 variational tangent over the nine checkpoints satisfy `alpha<=5e-3`, `E<=5e-3`, and `chi<=5e-3`.

**C4 — all-27 health.** Every primary base/tangent/bath trajectory is finite. The stable canonical tangent constraint residual is `<=1e-10`; the inherited base trajectory health condition `min(1+j_eff)>0` remains satisfied.

**C5 — bath-order convergence.** The maximum relative L2 difference between order-39 and order-47 tangent canonical checkpoint states `(delta_alpha,delta_chi,delta_Pchi,delta_Palpha)` over the 27 members is `<=1e-2`. Here `delta_Palpha=delta_Sc-Q delta_Pchi`. This inherits the 1% bath-order standard from the certified v0.19w forcing audit.

**C6 — time convergence.** The maximum relative L2 difference between the 4096-step and 8192-step order-39 tangent canonical checkpoint states over all 27 members is `<=2e-3`.

**C7 — spatial convergence.** After spectral resampling, the maximum relative L2 difference between Nx=128 and Nx=256 order-39 tangent canonical checkpoint states over all 27 members is `<=5e-3`.

**C8 — scope clean.** `eta=0` only; no finite physical eta, no likelihood, no parameter refit, no observational selection, no nonlinear matter evolution, and no post-data member removal or threshold change.

## Non-gating diagnostics

For each of the 27 members the implementation may report norms and signed projections of the eta=0 tangent in `alpha`, `E`, and `chi`, bath residual norms, and nonlinear-versus-linear tangent displacement. These quantities do not determine PASS/FAIL. In particular, no desired sign, monotonicity, ordering among `sigma/kind/beta0`, or minimum response amplitude is preregistered.

## Continuation rule

Only a D2C6C PASS licenses a separately preregistered finite-positive-eta nonlinear-memory test. A D2C6C FAIL remains historical. Technical implementation faults may be repaired only in a separately identified repair stage without changing the frozen physics or numerical thresholds above.
