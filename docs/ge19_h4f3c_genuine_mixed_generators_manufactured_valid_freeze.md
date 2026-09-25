# GE19 H4F3c — valid genuine frozen mixed generator manufactured runtime

## Classification and strict limit

`GE19_H4F3C_GENUINE_FROZEN_Q_LAMBDA_MANUFACTURED_RUNTIME_PASS`.

Dedicated GitHub Actions run [36096862132] completed **successfully**,
job `107950837089`. Its terminal marker was
`GE19_H4F3C_GENUINE_FROZEN_GENERATORS_MANUFACTURED_PASS`.

- preregistration:
  `ge19/h4f3c_predata_real_generator_manufactured_runtime.json`,
  blob `2fab9aafd16aa6ea6b11fa6dafff3f3394d97061`;
- implementation:
  `ge19/h4f3c_genuine_frozen_q_lambda_manufactured_selftest.py`,
  blob `be3b1d29f3f3a6110883ede801c99d121a2755ee`;
- workflow:
  `.github/workflows/ge19-h4f3c-genuine-frozen-mixed-generators.yml`,
  blob `bfcc469f34f6a0596d46ade27bec594bf2e45fbd`;
- execution commit:
  `c648bf59b753d8c4261510ca68a0543cae6cd739`;
- JSON:
  `results/ge19_h4f3c_genuine_frozen_q_lambda_manufactured.json`;
- JSON SHA-256:
  `5c0288cbf836dcc260e7d0029ae644cb733dd2e141a0128595c70633d2c57992`;
- artifact ID: `10848180381`.

The test executed the actual frozen GE06/GE07 mixed Q
symbolic generators and their direct/swapped Fourier
evaluators, plus the actual frozen Lambda source on
**manufactured Nt16 and Nt32 backgrounds/states**.
The generators were not mocked, and the original
symbolic polarization gates, evaluator shapes, finite
results, swapped symmetry and Lambda comparator
gates all passed.

This was an **engineering integration test, not a
calculation on certified physical parents**. It did
not consume the original Repair32B Z11 NPZ or
evaluate the full operator/parent H4 Ward identity
or solve Z21.

After this CI launch the user separately executed
the genuine H4F3b source on their complete exact
H3F/H3G/Z11/R13/R1 local scientific parent set,
and provided all four output files. The resulting
real-parent local source PASS is frozen in
`docs/ge19_h4f3b_actual_corrected_six_source_valid_local_freeze.md`.
The valid real-parent H4F3b result supersedes
H4F3c's *missing physical-source* execution
dependency, but the manufactured generator
PASS remains independent integration evidence.

**Full H4 Noether, Z21 and lensing remain open.**
