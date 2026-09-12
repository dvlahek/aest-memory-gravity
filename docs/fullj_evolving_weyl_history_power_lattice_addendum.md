# Full-J evolving Weyl history addendum: stochastic tagged power-lattice FAIL

This addendum continues the canonical history in `docs/fullj_evolving_weyl_history.md`, whose locked chain currently runs through the stochastic response-kernel POC PASS. It preserves the next completed milestone without changing any historical classification.

## Stochastic tagged power-lattice adequacy

- kernel POC PASS result: `2a5f884a50b7b30b90ddff01721914626dbde20f`
- history through kernel POC: `6eea250e82c2ed2b161a776594948062a6d77743`
- power-lattice preregistration: `30630042acc41b1978f7ac8a0be2b736ababbc0b`
- implementation: `97c044793d415d021c863e6bc4377fcfaf50fc4a`
- runner / science-run head: `dba8df537e2753c783faedfa04768b12caa5111b`
- locked result FAIL: `b1a66aaa6e1a37919c8287908995ee2aea79eb4e`

Frozen construction:

- complete Stage-A lattice `k/h=0.030,0.035,...,0.200 Mpc^-1`
- Stage-A geometry `kF/h=0.005`, `NX=256`
- Stage-B preregistered adaptive half-lattice geometry `kF/h=0.0025`, `NX=512`
- same physical real-space grid spacing across Stage A and Stage B
- Gaussian hash `9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200`
- 176/176 new runs finite.

Passed gates: provenance, Stage-A solver/constraints, Stage-A saturation, complete-lattice algebra/background convergence, Stage-B solver/constraints/saturation.

Failed gates: half-lattice power interpolation accuracy and unresolved selected-interval power spike veto.

Key values:

- Stage-A saturation max `4.686860739225767e-05`
- Stage-B saturation max `4.305454091526383e-05`
- new-node B2->B4 response global `1.4972561232033347e-08`
- new-node B2->B4 power global `1.2008620017571966e-08`
- power half-lattice L2 median `0.003328742986623499`
- power half-lattice L2 max `0.3086377990034805`
- power half-lattice peak max `0.18662232403879295`
- maximum direct midpoint spike ratio `11.436423060133826`.

The interpolation error is tiny at high redshift and grows late: the primary power L2 is about `0.0301` at `z=1`, `0.0966` at `z=0.5`, and `0.3086` at `z=0.2`. The strongest direct spike is at `z=0.2`, `k/h=0.0975`.

## Interpretation lock

Do not reinterpret this FAIL as a failure of the stochastic tagged response. Solver health, constraints, broadband saturation, background convergence, scalar diagonal reduction, and direct power algebra remain clean. The result says that the 0.005 power lattice does not predict preregistered half-lattice values at late time.

However, Stage B necessarily uses a doubled periodic box to represent half-lattice modes exactly. Same physical dx does not by itself prove box-length invariance. Before attributing the half-lattice discrepancy to genuine sub-0.005 radial structure, perform a bounded same-k box-doubling audit: rerun selected shared k values in the Stage-B geometry and compare directly with their locked Stage-A responses and powers.

If box-doubling invariance passes, finer/adaptive bounded radial power sampling is justified. If it fails, periodic embedding dependence must be understood before any continuum power claim.

All continuous-power, LOS, ACT, and observational licenses remain false.
