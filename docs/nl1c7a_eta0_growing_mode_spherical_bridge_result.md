# NL1C7A result — eta=0 growing-mode spherical bridge

Status: **RESULT / FROZEN**

Final classification:

`NL1C7A_REPAIR01_DENSE_TIME_SPHERICAL_BRIDGE_CERTIFIED`

## Scope

This result certifies the eta=0 linear growing-mode to spherical-initial-state bridge used by NL1C7. It does not certify nonlinear spherical evolution, finite physical memory coupling, turnaround, collapse, splashback, lensing, or an observational signal.

## Parent nonlinear closure

NL1C6 spherical self-gravity closure:

- classification: `NL1C6_SPHERICAL_SELF_GRAVITY_CLOSURE_PASS`
- official G11 run: `35089436959`
- head: `0f868057e788423b588cda5bc654287c784ebee7`
- artifact: `10442933686`
- SHA256: `12b83f6f67f473937514005f6a87764646407e3b2141b4451d47bd92b62c6ddc`

## Historical initial-data result

The first NL1C7 initial-data closure audit correctly terminated before evolution as

`NL1C7_INITIAL_DATA_CLOSURE_INCOMPLETE`.

The reason was structural: the frozen matter overdensity and growing-mode matter velocity did not uniquely determine all scalar/aether/metric initial functions after the two retained lapse/shift constraints. No arbitrary `u=0`, `delta phi=0`, shell force, drag, pressure floor, viscosity, or other physical prescription was introduced.

NL1C7A was opened specifically to obtain the missing initial functions from the frozen eta=0 cosmological growing mode.

## A2–A5 chain

A2 certified the exact gauge/variable bridge into the proper-time, zero-shift spherical gauge, including the initial-slice metric dictionary, aether transform, and the exact identities

`X_C6 = chi_,r / a`

and

`E_C6 = E_A,r / a`.

A4 native trace coverage was certified on run `35104087182`, artifact `10450205501`, SHA256 `9b1a4f998af55ce594cbdd6db78b9b99944cd25a3f690c68bab49ffef290ffc6`. All 128 preregistered k modes were present exactly, with no interpolation or nearest-neighbour substitution.

A5 denominator audit was certified on run `35105898962`. The global minimum transfer-function denominator ratio was

`min |T_delta_b| / max |T_delta_b| = 1.6495563290682825e-3`,

well above the frozen rejection floor `1e-12`.

## Historical A6 fail

The first sparse-native-time A6–A10 evaluation is retained as a real historical numerical fail:

- classification: `NL1C7A_TIME_INTERPOLATION_CONTROL_FAIL`
- run: `35106735707`
- head: `8b02243fc0b1ea58f00466868d58170c73dbc4e4`
- artifact: `10450343358`
- SHA256: `99b795389566a21b0438977af55bae21f92b428d52ad50ba2c9855bafda28fb5`
- freeze commit: `ccf2ac18dd3187f67bafcba4eeeb2b1c0dc524ae`

The sparse trace had 46 native accepted source times. The preregistered PCHIP-vs-linear time-interpolation control failed only for aether rapidity `u`, at approximately 3.63%, above the frozen 2% limit. The limit and interpolation methods were not changed.

## Repair01 boundary

Repair01 changed only the CLASS accepted source-function sampling density:

- historical default `perturbations_sampling_stepsize = 0.1`
- Repair01 `perturbations_sampling_stepsize = 0.025`
- perturbation integration step-size override: false
- integration tolerance override: false
- physics/evolution equations changed: false
- k grid changed: false
- A6 threshold changed: false
- interpolation methods changed: false

The dense native trace was generated on run `35149865129`, head `4a275f4777a7e487004f4783bc2a929a93ac8188`, artifact `10469031693`, SHA256 `193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70`.

It contained 179 native accepted source times instead of 46, all 128/128 preregistered k modes exactly, and 9 native times below plus 16 above `a_i=0.02` in the frozen local window.

A metadata-only evaluator compatibility repair was then applied to the retained dense artifact. It added only the legacy `repair05.interpolation_used=false` alias expected by the frozen A5 wrapper; it did not modify the trace, physics, or science gates.

## Official final certification

Official final evaluator run:

- run: `35183893359`
- head: `e650fcb2344813cc0e3c91a2f0ae99b9c7bf43ac`
- conclusion: `success`
- artifact: `10481526695`
- artifact SHA256: `c2ede2e602e35bbd52afdc0a5eee22cb1bf5c6efc2e1063bf8f2b91a0554fb6c`

Final science classification:

`NL1C7A_REPAIR01_DENSE_TIME_SPHERICAL_BRIDGE_CERTIFIED`

All retained gates passed.

### A6 — time interpolation

PASS. Frozen limit: `2e-2`.

Maximum active relative difference:

`2.656978791225352e-3`

or approximately `0.266%`.

For the previously failing aether rapidity `u`:

- `R_sigma = 5 h^-1 Mpc`: `2.6564571436855696e-3`
- `R_sigma = 10 h^-1 Mpc`: `2.656978791225352e-3`
- `R_sigma = 20 h^-1 Mpc`: `2.6562040104148757e-3`

For `udot`, the maximum is approximately `1.2895e-3`.

### A7 — k interpolation

PASS. Maximum active relative difference:

`1.6264270315725152e-3`

below the frozen `2e-2` limit.

### A8 — target-profile reconstruction

PASS. Maximum error or primary/control mismatch:

`6.299255876414729e-7`

below the frozen `1e-4` limit.

### A9 — bridge identities

PASS. Maximum bridge relative error:

`1.7958746026710248e-7`

below the frozen `1e-6` limit. The E-identity residual is at approximately machine precision.

### A10 — no free-mode injection

PASS. The frozen scale ladder is retained, no profile clipping call is used, no independent free-mode assignments are introduced, and the state is normalized by the single frozen baryon target.

## Certified output

The final artifact contains the primary eta=0 spherical initial-state arrays for the three frozen scales

`R_sigma = {5, 10, 20} h^-1 Mpc`,

with `a_i = 0.02`, 256 radial points, the frozen 128-mode k grid, and the reconstructed metric, scalar, aether, matter-density and matter-velocity initial data required by NL1C7.

The evaluator explicitly reports

- `unique_eta0_initial_data_certified = true`
- `primary_state_npz_written = true`.

## Claim boundary

This PASS closes the initial-data bridge that blocked NL1C7. It licenses the preregistered eta=0 spherical evolution test using the certified initial-state artifact. It does not itself establish nonlinear memory enhancement or any physical observable.