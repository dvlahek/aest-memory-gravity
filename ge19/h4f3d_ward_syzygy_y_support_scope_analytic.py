#!/usr/bin/env python3
"""GE19 analytic scope lemmas; not full H4 certification.

Checks the first-order homogeneous-background spatial Ward syzygy and
vanishing direct source-Ward projection for Stage E H4 Y support.
The source-support premise is audited from the frozen Stage E generator.
No physical Cmat/parent arrays and no Z21 solver are evaluated.
"""
from __future__ import annotations

from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]


def exact(expr):
    return sp.simplify(sp.expand(expr.doit())) == 0


def main():
    x, t, eps = sp.symbols("x t eps", real=True)
    a = sp.Function("a")(t)
    names = ("N", "L", "R", "b", "u", "phi", "T", "rho")
    base = {
        "N": sp.Integer(1), "L": a, "R": a, "b": sp.Integer(0),
        "u": sp.Integer(0), "phi": sp.Function("phi0")(t),
        "T": sp.Function("T0")(t), "rho": sp.Function("rho0")(t),
    }
    f = {n: sp.Function("f_" + n)(t, x) for n in names}
    e0 = {n: sp.Function("E0_" + n)(t, x) for n in names}
    e1 = {n: sp.Function("E1_" + n)(t, x) for n in names}
    F = {n: base[n] + eps * f[n] for n in names}
    E = {n: e0[n] + eps * e1[n] for n in names}
    ward = (
        sum(E[n] * sp.diff(F[n], x) for n in names)
        - sp.diff(F["L"] * E["L"] - F["b"] * E["b"], x)
        - sp.diff(E["b"], t)
    )
    linear = sp.diff(ward, eps).subs(eps, 0).doit()
    expected = (
        sum(e0[n] * sp.diff(f[n], x) for n in names)
        - sp.diff(a * e1["L"] + f["L"] * e0["L"] - f["b"] * e0["b"], x)
        - sp.diff(e1["b"], t)
    )
    assert exact(linear - expected), "linear Ward coefficient sign/factor"
    shell = {e0[n]: 0 for n in names}
    reduced = linear.subs(shell).doit()
    assert exact(reduced + sp.diff(a * e1["L"], x) + sp.diff(e1["b"], t))
    assert exact(sp.diff(a * e1["L"], x) - a * sp.diff(e1["L"], x))

    iso, aniso, eb = (sp.Function(s)(t, x)
                      for s in ("Lin_iso", "Lin_aniso", "Lin_b"))
    si, sa, sb = (sp.Function(s)(t, x)
                  for s in ("Source_iso", "Source_aniso", "Source_b"))
    lin_l = (iso + 2 * aniso) / 3
    src_l = (si + 2 * sa) / 3
    total = -sp.diff(eb - sb, t) - sp.diff(a * (lin_l - src_l), x)
    op = -sp.diff(eb, t) - sp.diff(a * lin_l, x)
    source = sp.diff(sb, t) + sp.diff(a * src_l, x)
    assert exact(total - op - source), "signed source/operator split"

    # Frozen Stage E support: _rhs creates zero main rows except u,phi,
    # and zero independent shift/anisotropy constraints.
    stage = (ROOT / "ge19/h4_stagee_versioned_y_source_rows.py").read_text()
    assert "main=np.zeros((6,flux.shape[0],flux.shape[1]),float)" in stage
    assert "constraints=np.zeros((2,flux.shape[0],flux.shape[1]),float)" in stage
    assert "main[2]=2.0*aa**3*qq*kappa*projected" in stage
    assert "main[3]=-2.0*aa**2*kappa*div_x" in stage
    yu, yphi = sp.symbols("Y_u Y_phi")
    yr = [sp.Integer(0), sp.Integer(0), yu, yphi,
          sp.Integer(0), sp.Integer(0), sp.Integer(0), sp.Integer(0)]
    yward = sp.diff(yr[6], t) + sp.diff(a * (yr[1] + 2 * yr[7]) / 3, x)
    assert exact(yward), "Y source support projection must vanish"

    print("GE19_H4_LINEAR_WARD_SYZYGY_FORMAL_SCOPE_PASS")
    print("GE19_H4_STAGEE_DIRECT_SOURCE_WARD_SUPPORT_ZERO_PASS")
    print("NO_PHYSICAL_OPERATOR_OR_PARENT_ARRAY_EVALUATED")
    print("FULL_H4_WARD_CERTIFIED=false Z21_CERTIFIED=false LENSING_LICENSED=false")


if __name__ == "__main__":
    main()
