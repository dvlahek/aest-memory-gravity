# MCMG growth-Weyl memory consistency relation

## Status

Post-R3 analytic derivation. This note is written after the held-out generality result `MCMG_GROWTH_WEYL_MEMORY_GENERALITY_PASS` and does not retroactively alter any preregistered gate.

## Setup

Let the causal memory operator act on a scalar source P(t) as

    M[P](t) = integral_0^infinity K(s) P(t-s) ds,

with

    K(s) >= 0,
    integral_0^infinity K(s) ds = 1,

and finite moments

    mu_n = integral_0^infinity s^n K(s) ds.

The MCMG pure-memory deformation uses

    P_eff = (1-eta) P + eta M[P].

The linear matter-growth amplitude D changes self-consistently with eta. In the scalar baseline used in R2-R3,

    P = D/a.

Let D_0 and P_0=D_0/a denote the eta=0 GR solution. Define relative responses

    g = D/D_0 - 1,
    w = P_eff/P_0 - 1.

## Proposition 1: exact tangent backreaction cancellation

Assume the self-consistent solution is differentiable in eta at eta=0. Write

    D = D_0 [1 + eta G + O(eta^2)],

so that

    P = P_0 [1 + eta G + O(eta^2)].

Because the memory operator is linear,

    M[P] = M[P_0] + O(eta).

Then

    P_eff
      = P + eta(M[P]-P)
      = P_0 + eta[P_0 G + M[P_0]-P_0] + O(eta^2).

Therefore

    (partial g / partial eta)_{eta=0} = G,

while

    (partial w / partial eta)_{eta=0}
      = G + [M[P_0]-P_0]/P_0.

Subtracting gives the exact tangent identity

    d/deta (w-g)|_{eta=0}
      = [M[P_0]-P_0]/P_0.

Thus the first-order growth backreaction cancels from the difference between the Weyl and growth responses. The remaining quantity is the causal memory lag evaluated on the GR source.

This identity does not require a specific kernel shape. It requires only the pure-memory coupling above and differentiability of the self-consistent solution at eta=0.

## Proposition 2: causal first-moment law

If P_0 is sufficiently smooth over the support of K, Taylor expansion gives

    P_0(t-s)
      = P_0(t)
        - s dP_0/dt
        + s^2/2 d^2P_0/dt^2
        - ... .

After integration,

    M[P_0]-P_0
      = -mu_1 dP_0/dt
        + mu_2/2 d^2P_0/dt^2
        - mu_3/6 d^3P_0/dt^3
        + ... .

Hence

    d/deta (w-g)|_{eta=0}
      = -mu_1 d ln P_0/dt
        + mu_2/2 (d^2P_0/dt^2)/P_0
        + O(mu_3).

Using x=H0 t and u=H0 mu_1,

    1/u * d/deta (w-g)|_{eta=0}
      = -d ln P_0/dx + O(mu_2/mu_1).

For a one-parameter kernel family whose width scales with mu_1, mu_2=O(mu_1^2), so the correction to the scaled relation is O(u).

The leading term depends only on the first causal moment, not on the detailed kernel shape.

## Corollary: growth-Weyl memory consistency relation

In the joint tangent and short-memory limit,

    (w-g)/(eta u)
      -> -d ln P_GR/d(H0 t).

Equivalently, the direct memory observable

    H_mem(z) = [w(z)-g(z)]/eta

is the normalized retarded lag of the GR potential source, and

    H_mem(z)/u

approaches the logarithmic decay rate of that source.

This is the MCMG consistency relation.

## Physical meaning

The relation separates two effects that are otherwise mixed in modified-gravity fits:

1. growth backreaction changes D and therefore both matter growth and the metric source;
2. causal memory adds a direct lag between the instantaneous source and the Weyl response.

Their difference removes the first contribution at linear order in eta. The surviving quantity probes the finite response time itself.

Therefore MCMG does not predict two arbitrary functions for growth and lensing. The difference between their responses is constrained by a causal time-response law.

## Connection to R1-R3

R1 established the first-moment limit for four distinct causal kernels on a prescribed GR source.

R2 established the exact tangent cancellation numerically in the self-consistent growth system and showed that the relation remains accurate at finite eta.

R3 held out both kernel shape and cosmological background. Across four kernels and five backgrounds it found:

- all seven generality gates passed;
- maximum tangent-versus-passive-lag relative L2 error: 1.8170306336539354e-08;
- maximum first-moment error at u=0.005: 0.010288138764102665;
- maximum kernel-collapse disagreement at u=0.005: 0.005178801828408899;
- maximum finite-amplitude relation relative L2 error at eta=+-0.5 and u=0.02: 0.004104171344558881;
- maximum nested-GR relative L2 error: 1.1623732185339783e-11.

The held-out backgrounds were:

    (Omega_m0,w) =
      (0.315,-1.0),
      (0.27,-1.0),
      (0.36,-1.0),
      (0.315,-0.9),
      (0.315,-1.1).

The held-out kernels were exponential, Erlang-2, Erlang-4, and bi-exponential.

## Claim boundary

The theorem above is a structural result inside the MCMG pure-memory construction. It is not by itself evidence that gravity in nature has a nonzero response time.

The next requirements for a broad physics claim are:

1. embed or recover the same relation in at least one independent relativistic host theory;
2. project the relation to observables with no independent growth and lensing memory amplitudes;
3. test if one causal-memory parameter set consistently accounts for both sectors;
4. compare against instantaneous modified-gravity alternatives and the nested GR limit.

AeST can serve as the first independent host realization once its current numerical ULP/stability issue is resolved.