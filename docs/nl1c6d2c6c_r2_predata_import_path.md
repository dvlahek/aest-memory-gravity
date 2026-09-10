# NL1C6D2C6C-R2 pre-data declaration — direct-script import-path repair

## Trigger

D2C6C-R1 Actions run `34458281699` on implementation commit `f5679a71066e68a6e43beb6e2635f687e3084be9` completed the corrected tau1 CLASS build and the linear eta=0 variational reference generation, but failed before entering `c.main()` with

`ModuleNotFoundError: No module named 'nl1c6d2c6c'`

when `nl1c6d2c6c/r1_tau1_parser_compat.py` was executed directly. No `C2_BRIDGE`, `C3_LINEAR`, member, `GATES=`, or D2C6C `CLASSIFICATION=` line was produced. The run is therefore a historical technical failure, not a physics/numerical gate result.

## Frozen repair

R2 may change only Python import-path bootstrapping in `nl1c6d2c6c/r1_tau1_parser_compat.py` by adding the repository root to `sys.path` before importing `nl1c6d2c6c.eta0_nonlinear_memory_tangent`.

The intended implementation is equivalent to the already used direct-script pattern in the D2C6A/D2C6B code:

```python
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
```

No other source file, equation, parameter, threshold, discretization, bath node/weight, CLASS patch, trajectory member, prehistory rule, response diagnostic, or gate may change in R2.

## Frozen scientific scope

All D2C6C preregistration remains exactly as locked in `fe34cbfb651f4e27fd05479f48c5832dd23863c2`, including:

- physical `eta=0` only;
- all 27 D2C6B nonlinear trajectory members;
- `tau H0=1`;
- primary bath order 39 and order-47 control;
- full retarded prehistory;
- stable canonical state `(alpha,chi,P_chi,S_c)`;
- the same C1-C8 numerical thresholds and continuation rule.

The D2C6C-R1 tau1 parser compatibility repair remains in force and is not modified.

## Classification rule

A subsequent run may be interpreted as a D2C6C physics/numerical result only if it successfully enters the D2C6C main program and reaches the preregistered gate evaluation. Any further failure before gate evaluation remains technical and must not be reclassified as physical evidence.