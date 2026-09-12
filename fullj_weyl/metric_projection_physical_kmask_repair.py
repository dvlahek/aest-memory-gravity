#!/usr/bin/env python3
from __future__ import annotations

"""Geometry-invariant repair of the evolving-Weyl metric projection mask.

Historical R2 used integer Fourier indices 1<=|n|<=32 on the original
kF/h=0.01 geometry.  Later tagged campaigns changed BOX while preserving the
integer mask, unintentionally changing the physical projection cutoff.  This
module preserves the original physical meaning, 0<|k|/h<=0.32, and monkey
patches only r0.metric_correction.  No field equation or science threshold is
changed.
"""

import numpy as np

from fullj_weyl import evolving_flrw_weyl_bridge as r0

m = r0.m
static = r0.static

ORIGINAL_KF_H = 0.01
METRIC_KMAX_H = float(r0.NMAX) * ORIGINAL_KF_H
ROUND_TOL_H = 5.0e-13
HISTORICAL_METRIC_CORRECTION = r0.metric_correction


def physical_k_grid_h(nx: int, box: float | None = None) -> np.ndarray:
    if box is None:
        box = float(static.BOX)
    kk = 2.0 * np.pi * np.fft.fftfreq(int(nx), d=float(box) / int(nx))
    return np.abs(kk) / float(static.h)


def physical_mask(nx: int, box: float | None = None) -> np.ndarray:
    kh = physical_k_grid_h(int(nx), box)
    return (kh > ROUND_TOL_H) & (kh <= METRIC_KMAX_H + ROUND_TOL_H)


def historical_index_mask(nx: int) -> np.ndarray:
    modes = np.minimum(np.arange(int(nx)), int(nx) - np.arange(int(nx)))
    return (modes >= 1) & (modes <= int(r0.NMAX))


def original_r2_mask_identity(nx: int = 128) -> dict:
    original_box = 2.0 * np.pi / (ORIGINAL_KF_H * float(static.h))
    old = historical_index_mask(int(nx))
    new = physical_mask(int(nx), original_box)
    mismatch = int(np.count_nonzero(old != new))
    return {
        "nx": int(nx),
        "original_kF_h": float(ORIGINAL_KF_H),
        "metric_kmax_h": float(METRIC_KMAX_H),
        "mismatch_count": mismatch,
        "identical": bool(mismatch == 0),
    }


def metric_correction_physical_kmask(data, tau, corr, nx):
    """Exact historical metric correction with only the mask made physical-k invariant."""
    bg = r0.fluid_background(data, tau)
    a = bg["a"]
    Hconf = a * bg["H"]

    kk = 2.0 * np.pi * np.fft.fftfreq(nx, d=static.BOX / nx)
    k2 = kk * kk
    mask = physical_mask(nx, float(static.BOX))

    rh = np.fft.fft(np.asarray(corr["delta_rho"], float))
    qh = np.fft.fft(np.asarray(corr["q_momentum"], float))
    sh = np.fft.fft(np.asarray(corr["shear"], float))

    xh = np.zeros(nx, complex)
    ph = np.zeros(nx, complex)
    ps = np.zeros(nx, complex)
    xh[mask] = 1.5 * a**2 * qh[mask] / k2[mask]
    ph[mask] = -(
        1.5 * a**2 * rh[mask] + 3.0 * Hconf * xh[mask]
    ) / k2[mask]
    ps[mask] = ph[mask] - 4.5 * a**2 * sh[mask] / k2[mask]

    rH = k2[mask] * ph[mask] + 3.0 * Hconf * xh[mask] + 1.5 * a**2 * rh[mask]
    rM = k2[mask] * xh[mask] - 1.5 * a**2 * qh[mask]
    rS = k2[mask] * (ps[mask] - ph[mask]) + 4.5 * a**2 * sh[mask]

    sH = max(
        float(np.linalg.norm(k2[mask] * ph[mask])),
        float(np.linalg.norm(3.0 * Hconf * xh[mask])),
        float(np.linalg.norm(1.5 * a**2 * rh[mask])),
        1.0e-300,
    )
    sM = max(
        float(np.linalg.norm(k2[mask] * xh[mask])),
        float(np.linalg.norm(1.5 * a**2 * qh[mask])),
        1.0e-300,
    )
    sS = max(
        float(np.linalg.norm(k2[mask] * (ps[mask] - ph[mask]))),
        float(np.linalg.norm(4.5 * a**2 * sh[mask])),
        1.0e-300,
    )

    phi = np.fft.ifft(ph).real
    psi = np.fft.ifft(ps).real
    return {
        "phi": phi,
        "psi": psi,
        "weyl": phi + psi,
        "X": np.fft.ifft(xh).real,
        "constraint": {
            "hamiltonian": float(np.linalg.norm(rH) / sH),
            "momentum": float(np.linalg.norm(rM) / sM),
            "shear": float(np.linalg.norm(rS) / sS),
        },
    }


# Runtime repair. R1/R2 call r0.metric_correction dynamically, so replacing
# this one module attribute propagates through the existing bridge without
# editing historical locked source files.
r0.metric_correction = metric_correction_physical_kmask
REPAIR_ACTIVE = True


if __name__ == "__main__":
    print(original_r2_mask_identity())
