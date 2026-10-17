#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import audited_certificates as ac


def save(fig: plt.Figure, outdir: Path, stem: str) -> None:
    fig.tight_layout()
    fig.savefig(outdir / f"{stem}.png", dpi=220, bbox_inches="tight")
    fig.savefig(outdir / f"{stem}.pdf", bbox_inches="tight")
    plt.close(fig)


def figure1_b0(outdir: Path) -> None:
    h = 1e-2
    beta = 2.0
    k = np.geomspace(1.0, 1e5, 500)
    bt = h**8 / 630.0 * k ** (9.0 - beta)
    bd = ac.FD8_L1 / h * k ** (-beta) + k ** (1.0 - beta)

    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    ax.loglog(k, bt, label="high-jet certificate")
    ax.loglog(k, bd, label="direct certificate")
    ax.set_xlabel(r"stiffness $\kappa$")
    ax.set_ylabel("certificate width")
    ax.set_title(r"B0: certificate separation ($h=10^{-2}$, $\beta=2$)")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend()
    save(fig, outdir, "figure1_b0_separation")


def figure2_b1_phase(outdir: Path) -> None:
    hs = np.geomspace(1e-3, 1e-1, 100)
    Rs = np.geomspace(3.0, 1e5, 180)
    Z = np.empty((len(hs), len(Rs)))
    for i, h in enumerate(hs):
        for j, R in enumerate(Rs):
            bd = ac.b1_direct(float(R), float(h))
            bt = ac.b1_taylor(float(R), float(h))
            Z[i, j] = math.log10(bt / bd)

    X, Y = np.meshgrid(Rs, hs)
    fig, ax = plt.subplots(figsize=(6.6, 4.7))
    mesh = ax.pcolormesh(X, Y, Z, shading="auto")
    rho = ac.asymptotic_rho_star("b1")
    ax.plot(rho / hs, hs, linewidth=2.0, label=rf"$R=\rho_*/h$, $\rho_*={rho:.4f}$")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"spectral cutoff $R$")
    ax.set_ylabel(r"grid spacing $h$")
    ax.set_title(r"B1 route phase diagram: $\log_{10}(B_T/B_D)$")
    fig.colorbar(mesh, ax=ax, label=r"$\log_{10}(B_T/B_D)$")
    ax.legend()
    save(fig, outdir, "figure2_b1_phase_diagram")


def figure3_memory_collapse(outdir: Path) -> None:
    hs = (0.1, 0.02, 0.005, 0.001)
    rhos = np.geomspace(1.001, 8.0, 300)

    fig, ax = plt.subplots(figsize=(6.6, 4.7))
    for h in hs:
        gamma = [ac.b2_taylor(rho / h, h) / ac.b2_direct(rho / h, h) for rho in rhos]
        ax.loglog(rhos, gamma, label=rf"B2 $h={h:g}$")
    asym = [ac.b2_asym_taylor(rho) / ac.b2_asym_direct(rho) for rho in rhos]
    ax.loglog(rhos, asym, linewidth=2.4, linestyle="--", label="B2 asymptotic")
    ax.axhline(1.0, linewidth=1.0)
    ax.axvline(ac.asymptotic_rho_star("b2"), linewidth=1.0, linestyle=":")
    ax.set_xlabel(r"$\rho=hR$")
    ax.set_ylabel(r"route ratio $\Gamma=B_T/B_D$")
    ax.set_title("B2 Maxwell transition collapse")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8)
    save(fig, outdir, "figure3a_b2_transition_collapse")

    fig, ax = plt.subplots(figsize=(6.6, 4.7))
    for h in hs:
        gamma = [ac.b3_taylor(rho / h, h) / ac.b3_direct(rho / h, h) for rho in rhos]
        ax.loglog(rhos, gamma, label=rf"B3 $h={h:g}$")
    asym = [ac.b3_asym_taylor(rho) / ac.b3_asym_direct(rho) for rho in rhos]
    ax.loglog(rhos, asym, linewidth=2.4, linestyle="--", label="B3 asymptotic")
    ax.axhline(1.0, linewidth=1.0)
    ax.axvline(ac.asymptotic_rho_star("b3"), linewidth=1.0, linestyle=":")
    ax.set_xlabel(r"$\rho=hR$")
    ax.set_ylabel(r"route ratio $\Gamma=B_T/B_D$")
    ax.set_title("B3 Volterra transition collapse")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8)
    save(fig, outdir, "figure3b_b3_transition_collapse")


def figure4_crossover_law(outdir: Path) -> None:
    hs = np.asarray([0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001])
    fig, ax = plt.subplots(figsize=(6.6, 4.7))
    for key, label in (("b1", "B1 continuum"), ("b2", "B2 Maxwell"), ("b3", "B3 Volterra")):
        R = np.asarray([ac.finite_crossover(key, float(h)) for h in hs])
        ax.loglog(hs, R, marker="o", label=label)
        rho = ac.asymptotic_rho_star(key)
        ax.loglog(hs, rho / hs, linestyle="--", alpha=0.65)
    href = hs
    ax.loglog(href, 1.0 / href, linestyle=":", linewidth=1.4, label=r"reference slope $-1$")
    ax.set_xlabel(r"grid spacing $h$")
    ax.set_ylabel(r"crossover cutoff $R_{\rm cross}$")
    ax.set_title(r"Cross-benchmark law $R_{\rm cross}=\Theta(h^{-1})$")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8)
    save(fig, outdir, "figure4_cross_benchmark_crossover")


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate audited core paper figures B0-B3.")
    ap.add_argument("--outdir", type=Path, default=Path("results/failure_aware_defect/figures"))
    args = ap.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    figure1_b0(args.outdir)
    figure2_b1_phase(args.outdir)
    figure3_memory_collapse(args.outdir)
    figure4_crossover_law(args.outdir)
    print("WROTE_FIGURES", args.outdir)


if __name__ == "__main__":
    main()
