# NL1C6D2N pre-result implementation clarification

Status: **LOCKED BEFORE THE FIRST D2N NORMALIZATION-AUDIT OUTPUT**.

This note does not change the corrected Exp normalization, any numerical gate, or any physical parameter. It only resolves the domain of the already existing background inverse routine before the first D2N result is generated.

The repository function

```text
aest_exp_Z_from_x(double x,...)
```

has the explicit contract `x > 0` and is used by the homogeneous cosmological background on the positive shift-charge branch. Therefore preregistered N4 is evaluated through the actual inverse routine only for

```text
Z in {0.1, 1, 2, 4}
```

with the unchanged gate

```text
max |Z_recovered-Z| / max(1,|Z|) <= 1e-12.
```

The negative points

```text
Z in {-4,-2,-1,-0.1}
```

remain in N3 and additionally verify the exact parity identities

```text
K(-Z)   = K(Z)
KQ(-Z)  = -KQ(Z)
KQQ(-Z) = KQQ(Z)
```

at normalized discrepancy `<=1e-14`.

No corrected-model output had been inspected when this domain clarification was written.
