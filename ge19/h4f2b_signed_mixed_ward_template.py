#!/usr/bin/env python3
"""H4F2b exact signed mixed spatial Ward coefficient: FORMAL subset only.

The coefficient is d_eta d_eps^2 of the universal Euler spatial-Ward
expression, on homogeneous eta-independent FLRW, including the full
background and first-order parent residuals. The frozen GE19
isotropic/anisotropy projection and S=-E_inhom sign are tested.
It does NOT instantiate six action-derived H4 source pieces and does
NOT prove their source identity, propagate Z21 or license lensing.
"""
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
BLOBS={
 "ge19/h4f2_predata_complete_mixed_h4_ward_parent_dictionary.json":"8097a4770ae8aed74cb4dd0721c1c9bd6907533c",
 "ge19/h4_structural_stage_b_geometric_ward_primitives.py":"5695cf064dcc32bf4385687cbe6052521f2e36b4",
 "docs/ge19_h4_structural_stage_a_source_row_ledger.md":"44d4f01a05aba26926d6a8e13a2b7aac995258d5",
 "docs/ge19_h4f1_longitudinal_bath_ward_valid_freeze.md":"5aa99f10383a253e934c0c2833230fa714c3ef1d",
}
def iszero(expr):
    return bool(sp.expand(expr.doit())==0)
def derive():
    t,x,eps,eta=sp.symbols("t x eps eta",real=True)
    a=sp.Function("a")(t)
    names=("N","L","R","b","u","phi","T","rho","q")
    baseline={"N":sp.Integer(1),"L":a,"R":a,
              "b":sp.Integer(0),"u":sp.Integer(0),
              "phi":sp.Function("phi_0")(t),
              "T":sp.Function("T_0")(t),
              "rho":sp.Function("rho_0")(t),"q":sp.Integer(0)}
    def fn(prefix,n,k):
        return sp.Function(prefix+"_"+n+"_"+k)(t,x)
    E={n:{k:fn("E",n,k) for k in ("00","10","11","20","21")}
       for n in names}
    F={n:{k:fn("F",n,k) for k in ("10","11","20","21")}
       for n in names}
    field={n:baseline[n]+eps*(F[n]["10"]+eta*F[n]["11"])
           +eps**2*(F[n]["20"]+eta*F[n]["21"])/2 for n in names}
    euler={n:E[n]["00"]+eps*(E[n]["10"]+eta*E[n]["11"])
           +eps**2*(E[n]["20"]+eta*E[n]["21"])/2 for n in names}
    ward=sum((euler[n]*sp.diff(field[n],x) for n in names),sp.S.Zero)
    ward-=sp.diff(field["L"]*euler["L"]-
                  field["b"]*euler["b"],x)
    ward-=sp.diff(euler["b"],t)
    coefficient=sp.diff(sp.diff(ward,eps,2),eta).subs(
        {eps:0,eta:0}).doit()
    parents=sum((
        E[n]["00"]*sp.diff(F[n]["21"],x)
        +2*E[n]["10"]*sp.diff(F[n]["11"],x)
        +2*E[n]["11"]*sp.diff(F[n]["10"],x)
        for n in names),sp.S.Zero)
    boundary=(a*E["L"]["21"]+F["L"]["21"]*E["L"]["00"]
        +2*F["L"]["10"]*E["L"]["11"]
        +2*F["L"]["11"]*E["L"]["10"]
        -F["b"]["21"]*E["b"]["00"]
        -2*F["b"]["10"]*E["b"]["11"]
        -2*F["b"]["11"]*E["b"]["10"])
    expected=parents-sp.diff(boundary,x)-sp.diff(E["b"]["21"],t)
    exact=iszero(coefficient-expected)
    iso,aniso,el,er=sp.symbols("E_iso E_aniso E_L E_R")
    projected=sp.solve([iso-el-er,aniso-el+er/2],
                       [el,er],dict=True)[0]
    projection=bool(iszero(projected[el]-(iso+2*aniso)/3)
                    and iszero(projected[er]-(2*iso-2*aniso)/3))
    shell={E[n][k]:0 for n in names for k in ("00","10","11")}
    on_shell=expected.subs(shell).doit()
    on_shell_target=-sp.diff(E["b"]["21"],t)-sp.diff(
        a*E["L"]["21"],x)
    shell_exact=iszero(on_shell-on_shell_target)
    sb,si,sa=[sp.Function(n)(t,x) for n in ("S_b","S_iso","S_aniso")]
    lb,li,la=[sp.Function(n)(t,x) for n in ("Lin_b","Lin_iso","Lin_aniso")]
    split=on_shell_target.subs({
        E["b"]["21"]:lb-sb,
        E["L"]["21"]:(li+2*la-si-2*sa)/3
    }).doit()
    operator=-sp.diff(lb,t)-sp.diff(a*(li+2*la)/3,x)
    source=sp.diff(sb,t)+sp.diff(a*(si+2*sa)/3,x)
    signed=iszero(split-operator-source)
    return {
      "tests":{
        "mixed_epsilon2_eta1_coefficient_from_Ward_exact":exact,
        "GE19_isotropic_anisotropy_projection_exact":projection,
        "homogeneous_FLRW_all_lower_Euler_on_shell_reduction_exact":shell_exact,
        "frozen_rhs_S_minus_E_source_sign_exact":signed,
      },
      "row_order":["N","L_plus_R","u","phi","T","rho","b","L_minus_R_over2"],
      "Euler_fields":list(names),
      "derivative_convention":"d_eta d_epsilon^2 evaluated epsilon=eta=0 (NO extra factorial)",
      "signed_mixed_Ward":{
        "identity":"W21=Sum_i [E_i00 F_i21,x+2 E_i10 F_i11,x+2 E_i11 F_i10,x] - d_x B21 - d_t E_b21 =0",
        "B21":"a E_L21+L21 E_L00+2 L10 E_L11+2 L11 E_L10-b21 E_b00-2 b10 E_b11-2 b11 E_b10",
        "Euler_L_projection":"E_L=(E_iso+2 E_aniso)/3",
        "source_on_shell_conditional":"d_t S_b+(a/3)d_x(S_iso+2 S_aniso)=0 IF background,H1,Z11 Euler residuals vanish AND the linear operator has the same Ward identity",
        "six_piece_sign_ledger":"Every source piece contributes +d_t S_b,piece + (a/3)d_x(S_iso,piece+2 S_aniso,piece), with parent terms kept separately",
        "absent_direct_E20_term":"F_background,eta=0 and E_background,eta=0; corrected Z20/q20 still enter E21 through the source functional",
        "regularity":"Formal eta derivative assumes the frozen rescaled bath q and one-sided eta convention; original action has sqrt(eta) before rescaling",
      },
      "full_six_piece_source_action_coefficient_instantiated":False,
      "corrected_parent_common_grid_evaluated":False,
      "full_H4_Noether_derived":False,
    }
def main():
    p=argparse.ArgumentParser();p.add_argument("--json-out",required=True)
    args=p.parse_args()
    checks={}
    for path,want in BLOBS.items():
        got=subprocess.check_output(
            ["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True).strip()
        checks[path]={"expected":want,"observed":got,"exact":got==want}
    audit=derive()
    good=bool(all(z["exact"] for z in checks.values())
              and all(audit["tests"].values()))
    result={
      "classification":("GE19_H4F2B_SIGNED_MIXED_WARD_TEMPLATE_DERIVED_FULL_SOURCE_OPEN"
                        if good else "GE19_H4F2B_SIGNED_MIXED_WARD_TEMPLATE_UNRESOLVED"),
      "frozen_blobs":checks,"symbolic":audit,
      "all_restricted_analytic_gates_pass":good,
      "full_all_sector_H4_source_Noether_derived":False,
      "Z21_certified":False,"lensing_licensed":False,
      "next_route":"INSTANTIATE_ALL_SIX_H4_SOURCE_PIECES_WITH_SIGNED_PARENT_RESIDUALS",
    }
    out=Path(args.json_out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
    if not good:raise SystemExit(3)
if __name__=="__main__":main()
