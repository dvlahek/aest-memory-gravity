#!/usr/bin/env python3
"""Regression wrapper for the preregistered full-J mode-coupling Jacobian.

This does not change any physics equation, Jacobian definition, or preregistered
support threshold.  It only enforces that the three Jacobian snapshots are
extracted from the *same full z_pk request* used by the completed dense-map run,
then filters to z={0.25,0.5,1}.  Hard regression checks prevent a different
CLASS transfer realization from being analysed silently.
"""
from __future__ import annotations

import math
import numpy as np

from fullj_jacobian import mode_coupling_jacobian as jac

# Frozen values from the completed fullj-dense-reclosure-map run.
DENSE_DELTA_RMS = {
    0.25: 2.871804732026e01,
    0.50: 1.053860907840e01,
    1.00: 1.754686661334e00,
}
DENSE_NODE_RATIO_Z025_K06 = 0.1165387182751355
DELTA_RMS_RTOL = 5.0e-10
NODE_RATIO_RTOL = 5.0e-8

_ORIGINAL_EXTRACT = jac.poc.extract_baryon_transfers


def _fixed_configure() -> None:
    # This is the key regression fix: dense.configure_upstream() installs the
    # original ten-redshift dense request.  Do NOT replace poc.ZS by jac.ZS
    # before CLASS extraction.
    jac.dense.configure_upstream()
    if int(jac.MODE_NUM.max()) > int(np.floor(jac.NX / 3.0)):
        raise RuntimeError("Jacobian source mode exceeds dense 2/3 cutoff")


def _select_exact_dense_transfers():
    all_transfers, classy_module = _ORIGINAL_EXTRACT()

    selected = []
    for target in jac.ZS:
        matches = [tr for tr in all_transfers if abs(float(tr["z"]) - float(target)) < 1.0e-12]
        if len(matches) != 1:
            raise RuntimeError(
                f"dense-background extraction expected one z={target:g} row, got {len(matches)}"
            )
        selected.append(matches[0])

    # Hard regression against the already completed dense run.  These checks
    # happen before any nonlinear/Jacobian solve, so a background mismatch can
    # never be misclassified as a physical node/coupling result.
    for tr in selected:
        z = float(tr["z"])
        db = np.asarray(tr["d_b"], float)
        delta, source, _ = jac.base.source_for(db, z, jac.NX)
        got = float(np.sqrt(np.mean(delta * delta)))
        expected = DENSE_DELTA_RMS[z]
        rel = abs(got - expected) / max(abs(expected), 1.0e-300)
        ok = bool(rel <= DELTA_RMS_RTOL)
        print(
            f"FULLJ_JAC_DENSE_REG z={z:g} delta_rms={got:.12e} "
            f"expected={expected:.12e} rel={rel:.3e} pass={ok}",
            flush=True,
        )
        if not ok:
            raise RuntimeError(
                f"dense background mismatch at z={z:g}: rel={rel:.3e} > {DELTA_RMS_RTOL:.1e}"
            )

        if abs(z - jac.NODE_Z) < 1.0e-12:
            sh = np.fft.fft(source) / jac.NX
            iL, iN, iR = jac.ix(jac.NODE_LEFT), jac.ix(jac.NODE_K), jac.ix(jac.NODE_RIGHT)
            aL = abs(sh[int(jac.MODE_NUM[iL])])
            aN = abs(sh[int(jac.MODE_NUM[iN])])
            aR = abs(sh[int(jac.MODE_NUM[iR])])
            ratio = float(aN / max(math.sqrt(aL * aR), 1.0e-300))
            reln = abs(ratio - DENSE_NODE_RATIO_Z025_K06) / DENSE_NODE_RATIO_Z025_K06
            okn = bool(reln <= NODE_RATIO_RTOL)
            print(
                f"FULLJ_JAC_DENSE_NODE_REG z={z:g} nodeN={ratio:.12e} "
                f"expected={DENSE_NODE_RATIO_Z025_K06:.12e} rel={reln:.3e} pass={okn}",
                flush=True,
            )
            if not okn:
                raise RuntimeError(
                    f"dense node mismatch at z={z:g}: rel={reln:.3e} > {NODE_RATIO_RTOL:.1e}"
                )

    print(
        "FULLJ_JAC_DENSE_BASELINE_REGRESSION_PASS "
        f"full_z_count={len(all_transfers)} selected_z_count={len(selected)}",
        flush=True,
    )
    return selected, classy_module


# Patch only orchestration.  The preregistered tangent solver, metrics, gates,
# and classifications remain those in mode_coupling_jacobian.py.
jac.configure = _fixed_configure
jac.poc.extract_baryon_transfers = _select_exact_dense_transfers


if __name__ == "__main__":
    raise SystemExit(jac.main())
