#!/usr/bin/env python3
"""Pre-run lock correction for the repaired power-lattice regression.

The preregistration wording was clarified before any regression data were run.
No grid, threshold, equation, stochastic draw, or classification rule changed.
This wrapper updates only the predata ancestry lock used by the implementation.
"""

from fullj_weyl import stochastic_tagged_power_lattice_kmask_regression as mod

mod.PREDATA_LOCK = "dde7ae43d974451b49f73df7473025812e906e83"
PREDATA_LOCK_CORRECTION_ONLY = True

if __name__ == "__main__":
    raise SystemExit(mod.main())
