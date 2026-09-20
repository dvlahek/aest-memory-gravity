# GE19 Repair02 execution — Exp-product implementation-failure freeze

## Status

The first locked GE19 Repair02 local science execution terminates before any valid Stage-A classification with

`GE19_REPAIR02_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_IMPLEMENTATION_FAIL`.

No reduced-H1 state and no Z20 state were constructed.

## Observed failure

The frozen-symbol tuple capture itself is no longer the problem.

The physical evaluation reaches the stable lambdified GE06 c1 functions and emits overflow in expressions containing the product

[
exp(Q_0^2/Z_0^2)
exp((Q_0+Z_0Z_b)^2/Z_0^2)
exp(-2Q_0(Q_0+Z_0Z_b)/Z_0^2).
]

The terminal exception is

`RuntimeError('non-finite stable GE06 partial c1:N_f')`.

## Exact algebraic identity

The product exponent is

[
rac{Q_0^2+(Q_0+Z_0Z_b)^2-2Q_0(Q_0+Z_0Z_b)}{Z_0^2}
=Z_b^2.
]

Therefore the complete product is exactly

[
exp(Z_b^2).
]

The failure is caused by evaluating the three algebraically separated exponential factors independently in floating point.

## Why Repair02 benign equivalence still passed

The GE06 benign audit uses `Q0=0.2` and `Z0=0.7`.

The individually separated exponentials remain numerically representable there, so Repair02 correctly reproduced the frozen GE06 source at machine precision:

- c1 source relative L2:
  `1.028882209897549e-15`;
- c2 source relative L2:
  `1.3610778770829969e-15`.

That control certified symbol capture and algebraic equivalence, but it could not detect physical-parameter overflow of algebraically separated exponential factors.

## Licensed Repair03

Repair03 may change only the symbolic numerical representation after the already frozen background substitution.

Before lambdify it must canonically combine products of exponential factors and simplify the combined exponent exactly.

In particular, all instances equivalent to

[
e^{a}e^{b}e^{c}
]

must be represented as

[
e^{operatorname{cancel}(operatorname{expand}(a+b+c))}
]

before numerical evaluation.

For the physical Exp background this must reduce the background factor to finite expressions in `exp(Zb**2)`.

## Mandatory pre-science controls

Repair03 must execute, before any science run:

1. stable-symbol contract PASS;
2. benign c1/c2 source equivalence <= `1e-10`;
3. physical-parameter symbolic audit:
   - no exponential argument may contain a negative power of `Z0` after canonicalization and the `Qb=Q0+Z0*Zb` substitution;
   - no exponential argument may contain `Q0`;
   - all remaining exponential arguments must be finite functions of `Zb` and perturbative symbols;
4. direct physical-background evaluation of every c1/c2 local partial on deterministic unit probes must be finite before Stage A.

No GE19 science threshold may change.

## Historical integrity

Original GE19, Repair01 and Repair02 classifications remain immutable implementation failures.

## Claim boundary

Repair02 carries no H1/H3 physical conclusion.
