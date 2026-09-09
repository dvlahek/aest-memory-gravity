# NL1C6R predata — full-J solver globalization repair

Classification before implementation: **NL1C6R_PREDATA_SOLVER_GLOBALIZATION_REPAIR**

This repair gate is frozen after the immutable `NL1C6_FULL_J_BARYONIC_RECLOSURE_FAIL` result and before inspecting any repaired full-J solution.

NL1C6 failed uniformly at Newton iteration zero on the first `lambda=1/64` source-continuation step, while its independent high-gradient regression passed at `1.57e-14`. NL1C6R therefore changes **only the numerical globalization path**. The physical equations, source, interpolation branches, resolutions, residual gates, and branch-consistency logic remain unchanged.

## 1. Immutable physical problem

Use exactly the NL1C6 published quasistatic system

\[
\Phi=\tilde\Phi+\chi,
\]

\[
\nabla_{\rm phys}^2\tilde\Phi+\mu^2\Phi
=\frac{S_b}{1+\beta_0},
\]

\[
\nabla_{\rm phys}^2\tilde\Phi
=\nabla_{\rm phys}\cdot[j(x)\nabla_{\rm phys}\chi],
\qquad
x=\frac{c^2|\nabla_{\rm phys}\chi|}{a_0}.
\]

The source remains the NL1C5B baryonic artifact only:

- artifact ID `10101422385`;
- SHA256 `0ab60cbc32210ad3fb75c881f91a9db11148280e9223ea644680ed8cdfbaa590`;
- native `d_b`;
- `omega_b = 0.022377376877682164`.

All other constants, six k modes, phases, primordial normalization, periodic box, zero-mode convention, and physical-coordinate scaling are exactly those preregistered in NL1C6.

No observational data, likelihood, finite eta, or memory source is introduced.

## 2. Immutable co-primary theory branches

Retain all nine combinations:

- `Simple`, `Exponential`, `Sharp`;
- `beta0 = {1.0, 0.5, 0.1}`.

No outcome-dependent branch selection is allowed.

## 3. Diagnosis being repaired

At `chi=0`, the full interpolation satisfies `j(0)=0`, so the first derivative of the nonlinear Y-sector operator vanishes and the local Newton linearization is mass dominated. NL1C6 used the first source amplitude `lambda=1/64` and backtracking only down to `alpha=1/128`. For all nine branches the GMRES linear solve converged, but no tested finite Newton step reduced the nonlinear residual.

This is a globalization failure, not a sign/factor failure: the constant-`j=1/beta0` high-gradient regression in the same implementation passed for all beta0 values and all eight evaluation snapshots with maximum error `1.5679255329173794e-14`.

## 4. Frozen repair

The final physical equation at `lambda=1` is unchanged.

Replace only the failed source/globalization schedule by:

### R1. Fine zero-source continuation

At the first native slice of each branch, start again from the exactly homogeneous field and solve the source-scaled equation on the deterministic sequence

\[
\lambda=2^{-24},2^{-23},\ldots,2^{-1},1.
\]

Every accepted solution initializes the next factor-of-two step. No adaptive insertion or deletion of continuation points is permitted.

### R2. Extended deterministic Newton backtracking

For each Newton direction test, in order,

\[
\alpha=2^{-m},\qquad m=0,1,\ldots,40.
\]

Accept the first alpha that strictly reduces the Euclidean residual norm. No alpha outside this frozen sequence is allowed.

### R3. Newton/Krylov budget

Keep the same analytic directional derivative of

`div[j(x) grad chi]`

and the same deterministic Fourier preconditioner. Increase only the maximum Newton iteration count from `40` to `60` per continuation step. GMRES settings remain unchanged.

The Newton convergence target remains `2e-10`, tighter than the final physical residual gate.

### R4. Later native times

As in NL1C6, solve native slices from largest z to smallest z. The preceding converged physical-time solution is the first initial condition. If that direct step fails, use the **same fixed fine zero-source continuation** `2^-24 ... 1` at that slice. No further solver route is allowed.

### R5. Resolution controls and alternate starts

The `Nx=512` controls and the two fixed alternate starts from NL1C6 use the repaired Newton backtracking. If a control direct solve fails, the only permitted fallback is the same fixed fine zero-source continuation.

## 5. Gates unchanged from NL1C6

The following gates are numerically identical to the original preregistration:

- exact NL1C5B artifact identity;
- requested k-mode relative match `<=1e-12`;
- at least eight native times in `0.2<=z<=1.5`;
- high-gradient regression `<=1e-10`;
- original coupled `R1 <=1e-10`;
- original coupled `R2 <=1e-8`;
- all reported fields finite;
- `Nx=256` versus `Nx=512` low-mode/`x_rms` discrepancy `<=5e-3`;
- alternate valid roots must agree with the continuation branch in low-mode chi to `<=1e-4`.

The primary resolution remains `Nx=256` for all 24 native times. The control remains `Nx=512` for the eight native times in `0.2<=z<=1.5`.

## 6. Classification

If the unchanged physical/numerical gates pass for all nine co-primary branches and no distinct residual-valid alternate root is found:

**NL1C6R_FULL_J_BARYONIC_RECLOSURE_PASS**

If the repaired deterministic solver still cannot satisfy the unchanged gates:

**NL1C6R_FULL_J_BARYONIC_RECLOSURE_FAIL**

If the equations are solved but a distinct residual-valid root is found by the frozen alternate-start audit:

**NL1C6R_FULL_J_MULTIBRANCH_REQUIRES_BOUNDARY_SELECTION**

A PASS repairs only the numerical globalization failure of NL1C6 and establishes the same limited scientific claim NL1C6 was intended to test: a single controlled periodic full-J baryonic quasistatic snapshot branch. It does not erase or relabel the historical NL1C6 FAIL.

## 7. Continuation rule

Only `NL1C6R_FULL_J_BARYONIC_RECLOSURE_PASS` permits the next eta=0 retarded-memory source/tangent test on the reclosed full native-time chi trajectory.
