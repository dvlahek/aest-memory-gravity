#!/usr/bin/env python3
"""GE19 H4 Stage D: common GR-anchored NL0C/GE06 action normalization.

Analytic frozen-action audit. Compare plane GE06 analytic action to the
fully Y-completed spherical NL1C6 action under common invariant names.
The spherical/plane GR difference is the known unit-sphere curvature
term. Derive full Y scalar+aether source rows in the resulting common
raw Euler convention. No historical GE19 code is patched, no solver.
"""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
BLOBS={
 "ge19/h4_structural_stage_d_predata_global_y_normalization.json":
    "764d064c76d44bc597ab6c4f96044ba2a90433a5",
 "docs/ge19_h4_stagec_local_analytic_reproduction_freeze.md":
    "25d896278fe82c30c4d6475fbcabcac8879f0961",
 "docs/ge19_h4_stagec_y_raw_ge19_conventions_valid_freeze.md":
    "a22a762148cb30f4d52c494f9df377c4613941d1",
 "docs/nl0c_y_sector_weakly_nonlinear_result.md":
    "6fe02e60e4de34a247003c1f4ab449c159850e99",
 "nl1c6/spherical_self_gravity_g1_g10.py":
    "e3eeb820fa1826fb7ac29f3fce2fe0bdde8d564f",
 "ge06/analytic_aest_directional_source_generator.py":
    "a7afe0035054a9dca55d74a6497c081422114b4c",
 "docs/ge06_analytic_aest_directional_source_generator_implementation_lock.md":
    "962427b4a52ba084081f9328670f672c0109471e",
}


def blobs_exact():
    d={}
    for p,want in BLOBS.items():
        got=subprocess.check_output(
            ["git","rev-parse","HEAD:"+p],cwd=ROOT,text=True
        ).strip()
        d[p]={"expected_blob":want,"observed_blob":got,"exact":bool(got==want)}
    return d


def frozen_assignment(path,name):
    content=(ROOT/path).read_text()
    tree=ast.parse(content)
    found=[]
    for node in tree.body:
        if isinstance(node,(ast.Assign,ast.AnnAssign)):
            targets=node.targets if isinstance(node,ast.Assign) else [node.target]
            if any(isinstance(t,ast.Name) and t.id==name for t in targets):
                found.append(node.value)
    if len(found)!=1:
        raise RuntimeError(f"Nonunique frozen {path}:{name}: {len(found)}")
    return ast.unparse(found[0])


def eqzero(x):
    return bool(sp.simplify(x)==0)


def action_normalization_proof():
    nl0c=(ROOT/"docs/nl0c_y_sector_weakly_nonlinear_result.md").read_text()
    nls="nl1c6/spherical_self_gravity_g1_g10.py"
    ge6="ge06/analytic_aest_directional_source_generator.py"
    syms={name:sp.Symbol(name) for name in (
        "N L R KB E C C2 X Xinv K Kfun Js kL kR Rx Nx Rr Nr"
    ).split()}
    ge_aest=sp.sympify(frozen_assignment(ge6,"aest"),locals=syms)
    nl_aest=sp.sympify(frozen_assignment(nls,"aest"),locals=syms)
    ge_grav=sp.sympify(frozen_assignment(ge6,"grav"),locals=syms)
    nl_grav=sp.sympify(frozen_assignment(nls,"grav"),locals=syms)

    N,L,R,KB,E,C,C2,X,Xinv,K,Kfun,Js,kL,kR,Rx,Nx,Rr,Nr=(
        syms[n] for n in (
          "N L R KB E C C2 X Xinv K Kfun Js kL kR Rx Nx Rr Nr"
        ).split()
    )
    vol=N*L*R**2
    matched=nl_aest.xreplace({C2:C,X:Xinv,K:Kfun})
    curvature=nl_grav.xreplace({Rr:Rx,Nr:Nx})-ge_grav
    k1,k2=sp.symbols("k1 k2")
    eh_kinetic=k1**2+2*k2**2-(k1+2*k2)**2

    covariant_anchor=(
        r"S_{\mathcal J}" in nl0c
        and r"-\frac{1}{16\pi\tilde G}" in nl0c
        and r"\sqrt{-g}\,(2-K_B)\mathcal J(\mathcal Y)" in nl0c
    )
    checks={
      "NL0C_explicit_EH_normalized_covariant_J_sector":covariant_anchor,
      "GE06_raw_analytic_and_NL1C6_full_same_EH_normalized_aest":
          eqzero(matched-ge_aest+C*vol*Js),
      "GE06_vs_NL1C6_GR_curvature_only_difference":
          eqzero(curvature-2*N*L),
      "EH_ADM_kinetic_exact":eqzero(
          eh_kinetic+4*k1*k2+2*k2**2
      ),
      "GE06_GR_kinetic_canonical_coefficient":
          eqzero(ge_grav.subs({
              Rx:0,Nx:0
          })-vol*(-4*kL*kR-2*kR**2)),
      "NL1C6_full_action_single_unscaled_sum":
          frozen_assignment(nls,"lag")=="aest + grav + mem",
      "GE06_analytic_action_single_unscaled_sum":
          frozen_assignment(ge6,"lag")=="sp.expand(grav + aest)",
      "NL1C6_C2_equals_2_minus_KB":
          frozen_assignment(nls,"C2")=="2 - KB",
      "GE06_C_symbol_matches_2_minus_KB_in_frozen_lock":
          ("C=2-KB" in (ROOT/
          "docs/ge06_analytic_aest_directional_source_generator_implementation_lock.md"
          ).read_text()),
    }
    return {
        "checks":checks,
        "normalization":"NL0C and NL1C6 full Y sector share a single canonical Einstein-Hilbert action normalization with GE06 memory-off analytic sector; relative NL0C-to-GE06 raw action prefactor = 1",
        "NL1C6_minus_GE06_analytic_sector":"-N*L*R**2*C*J(Y)",
        "NL1C6_minus_GE06_GR_sector":
            "2*N*L (unit-sphere curvature; absent in plane geometry)",
        "relative_Y_sector_action_prefactor_in_GE06_raw_units":"1",
        "physical_common_1_over_16piG_cancels_in_raw_EL_equations":True,
    }


def complete_y_raw_rows():
    eps,eta=sp.symbols("eps eta",real=True)
    a,Q,KB,beta,a0=sp.symbols(
        "a Q KB beta a0",positive=True,real=True
    )
    # C=2-KB is not presumed positive by the symbolic derivation.
    C=2-KB
    kappa=2*C/((1+beta)*a0)
    c=sp.Rational(2,3)/((1+beta)*a0)
    sign=sp.symbols("sign",real=True)
    N,L,R,b,u,pt,px=sp.symbols("N L R b u pt px",real=True)
    dn,dl,dr,db,du,dpt,dpx=sp.symbols(
        "dn dl dr db du dpt dpx",real=True
    )
    g=Q*du+dpx/a
    x=sp.sinh(u)*(pt-b*px)/N+sp.cosh(u)*px/L
    lag=-sign*C*c*N*L*R**2*x**3
    sub={
        N:1+eps*dn,L:a+eps*dl,R:a+eps*dr,
        b:eps*db,u:eps*du,pt:Q+eps*dpt,px:eps*dpx,
    }
    def second(partial):
        return sp.simplify(
            sp.diff(partial.subs(sub),eps,2).subs(eps,0)
        )
    eu=second(sp.diff(lag,u))
    ephi_flux=second(-sp.diff(lag,px))
    ephi_tflux=second(-sp.diff(lag,pt))
    metric={name:eqzero(second(sp.diff(lag,var)))
            for name,var in (("N",N),("L",L),("R",R),("b",b))}
    checks={
      "aether_raw_second_directional":
          eqzero(eu+sign*2*a**3*Q*kappa*g**2),
      "scalar_raw_spatial_flux_second_directional":
          eqzero(ephi_flux-sign*2*a**2*kappa*g**2),
      "scalar_raw_temporal_flux_zero":eqzero(ephi_tflux),
      "all_Y_metric_and_shift_second_directional_zero":
          bool(all(metric.values())),
      "aether_scalar_flux_relation":
          eqzero(eu+a*Q*ephi_flux),
      "positive_branch_sign":eqzero(
          eu.subs(sign,1)+2*a**3*Q*kappa*g**2
      ),
      "negative_branch_sign":eqzero(
          eu.subs(sign,-1)-2*a**3*Q*kappa*g**2
      ),
    }
    g10,g11=sp.symbols("g10 g11",real=True)
    f=sign*(g10+eta*g11)**2
    df=sp.diff(f,eta).subs(eta,0)
    checks["H4_eta_flux_strict_branches"]=eqzero(
        df-2*sign*g10*g11
    )
    checks["H3_scalar_source_volume_factor"]=eqzero(
        2*a**2*kappa-2*a**3*kappa/a
    )
    checks["H4_scalar_source_volume_factor"]=eqzero(
        4*a**2*kappa-2*a**3*2*kappa/a
    )
    return {
      "checks":checks,
      "metric_second_directional_zero_by_row":metric,
      "g":"Q*u10+phi10_x/a",
      "kappa":"2*(2-KB)/((1+beta)*a0)",
      "branch_flux":"sign(g)*g**2 = Abs(g)*g",
      "Y_H3_raw_EL_aether":"-2*a**3*Q*kappa*Abs(g)*g",
      "Y_H3_raw_EL_scalar":"2*a**3*kappa/a*d_x(Abs(g)*g)",
      "Y_H3_raw_EL_shift_and_metric":"0",
      "Y_H3_GE19_raw_RHS_aether":"+2*a**3*Q*kappa*Abs(g)*g",
      "Y_H3_GE19_raw_RHS_scalar":"-2*a**3*kappa/a*d_x(Abs(g)*g)",
      "Y_H4_GE19_raw_RHS_aether":
          "+4*a**3*Q*kappa*Abs(g10)*g11",
      "Y_H4_GE19_raw_RHS_scalar":
          "-4*a**3*kappa/a*d_x(Abs(g10)*g11)",
      "Y_H4_GE19_raw_RHS_shift_and_metric":"0",
      "nonanalytic_branch_rule":
          "Use eps->0+ directional coefficient and D(Abs(g)*g)[h]=2Abs(g)h, including g=0. No globally bilinear F2 kernel is introduced.",
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()
    locks=blobs_exact()
    action=action_normalization_proof()
    rows=complete_y_raw_rows()
    passed=bool(
        all(v["exact"] for v in locks.values())
        and all(action["checks"].values())
        and all(rows["checks"].values())
    )
    classification=(
        "GE19_H4_STAGED_COMMON_GR_NORMALIZATION_AND_Y_ROWS_DERIVED"
        if passed else
        "GE19_H4_STAGED_ACTION_NORMALIZATION_OR_VARIATION_UNRESOLVED"
    )
    report={
        "classification":classification,
        "predata_classification":
            "GE19_H4_STRUCTURAL_STAGE_D_PREDATA_GLOBAL_Y_NORMALIZATION",
        "all_analytic_gates_pass":passed,
        "frozen_blob_controls":locks,
        "common_action_normalization":action,
        "complete_Y_sector_raw_source_rows":rows,
        "theory_change_or_fit_performed":False,
        "historical_results_relabelled":False,
        "numerical_H3_H4_Z21_solve_performed":False,
        "integrated_parent_reclosure_performed":False,
        "full_H4_Noether_identity_derived":False,
        "window_local_particular_Z21_certified":False,
        "lensing_licensed":False,
        "next_route":(
          "FREEZE_VERSIONED_ALL_Y_ROW_DICTIONARY_THEN_PREREGISTER_PARENT_RECLOSURE"
          if passed else
          "FREEZE_AND_LOCALIZE_GLOBAL_ACTION_PROOF_OBLIGATION"
        ),
        "claim_boundary":
          "Exact GR-anchored relative Y-sector action normalization and Y-only raw source-row formulas do not certify the full H4 Noether identity, any corrected parent or Z21. Old H3/H4 solver sources remain untouched."
    }
    p=Path(args.json_out)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True,allow_nan=False))
    if not passed:
        raise SystemExit(3)


if __name__=="__main__":
    main()
