# NL1C7B4 Repair01 implementation lock

Status: **IMPLEMENTATION LOCKED BEFORE OFFICIAL REPAIR01 RUN**

Pre-data Repair01 commit: `95f37bfe7be2757ab3cf4c00087da010017be679`.

Implementation:

- `nl1c7b/initial_constraint_certification_repair01.py`
- blob: `253a0ae2a19a597f06358704ea276c9005973af3`

Historical B4 domain result remains immutable:

- run `35211367954`
- artifact `10492575332`
- SHA256 `9fdf56fd2c2b224c934cc15be31d5d27076971b50ab2961849c151939d60ef74`
- freeze `d42e22945e2ca6acaf412741198e4b8c6659598a`.

Repair01 changes only the representation of the exact Exp K contribution. It derives the K-sector lapse/shift identities from the frozen nonlinear scalar dictionary, evaluates all non-K GR/AeST-Y/dust/standard-background contributions directly, and uses the preregistered triangle lower bound on the original normalized residual. The original `1e-7` gate is unchanged.

No state projection, Q linearization, K clipping, Y-branch selection, scale selection, finite eta, or nonlinear trajectory is permitted.
