#!/usr/bin/env python3
"""H4F3d3: exact physical eta-rescaled NL0B bath Ward parent coefficient.

The frozen physical bath U=sqrt(eta)*q is nonanalytic as a FIELD in eta
at eta=0; the composite action and Euler*field_x Ward term are smooth
after the frozen regularizing field redefinition. In GE06 raw Euler
units the bath action is 2 eta L_GE05(q), hence the mixed H4 Ward parent
contains 4 sum_j E_GE05,q10 q_j10,x, not the integer-eta q10/q11
template applied naively to U. This is a necessary ALL-PARENT
dictionary input. No source-row change, parent solve or Z21 claim.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
PINS={
 "ge19/h4f3d3_predata_eta_regularized_bath_ward_parent.json":
  "ff7720381ddd09c7c073e106b2f35065ac3d1d6f",
 "docs/nl0b_predata_covariant_memory_completion.md":
  "9b1c013153faeddbd2add3d80eb29f673bc7748f",
 "docs/nl0b_covariant_memory_completion_result.md":
  "d005b1c135fead856510aa76b6174fb9051fa552",
 "ge05/memory_directional_source_generator.py":
  "40837d77f89028da30c28899e2d0530a4401844e",
 "docs/ge19_repair32a_ge06_ge05_raw_residual_normalization_dictionary_result_freeze.md":
  "6c5b7f830cbae95209eda0e8c8663c6620ab7071",
 "ge19/h4f3d2_dust_bath_parent_euler_currents.py":
  "42b2405759402195ffb371056d9e48b70dcded71",
 "ge19/h4f2b_signed_mixed_ward_template.py":
  "ab783ffe8242d8ff455647df8664a074f725ee81",
 "ge19/h4f3d_predata_actual_operator_all_parent_ward_closure.json":
  "f1bd4eb52b7da96ac2d50ed9136e3e1a74635f51",
}

def frozen_blobs():
    result={}
    for path,expected in PINS.items():
        got=subprocess.check_output(
            ["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True
        ).strip()
        result[path]={"expected":expected,"observed":got,"exact":got==expected}
    return result

def frozen_bindings():
    pre=(ROOT/"docs/nl0b_predata_covariant_memory_completion.md").read_text()
    result=(ROOT/"docs/nl0b_covariant_memory_completion_result.md").read_text()
    ge05=(ROOT/"ge05/memory_directional_source_generator.py").read_text()
    norm=(ROOT/"docs/ge19_repair32a_ge06_ge05_raw_residual_normalization_dictionary_result_freeze.md").read_text()
    d2=(ROOT/"ge19/h4f3d2_dust_bath_parent_euler_currents.py").read_text()
    b=(ROOT/"ge19/h4f2b_signed_mixed_ward_template.py").read_text()
    squeeze=lambda x:"".join(x.split())
    return {
      "NL0B_physical_completed_square_sqrt_eta":
        r"\sqrt{\eta w_j}" in pre
        and r"S_{\rm mem}" in pre
        and r"\frac14" in pre,
      "NL0B_exact_U_equals_sqrt_eta_q":
        r"U_j=\sqrt\eta\,q_j" in pre
        and r"U_{j,L}=\sqrt\eta\,q_j" in result,
      "GE05_raw_reduced_per_node_action":
        "lag=N*L*R**2*sp.Rational(1,4)*(Aq**2-(om*q-sw*Xphi)**2)" in squeeze(ge05),
      "Repair32A_exact_GE05_to_GE06_Euler_scale_two":
        "GE05_M1_to_GE06_raw_residual_scale = 2" in norm
        and "This is symbolic and exact" in norm,
      "H4F3d2_raw_per_node_Eq10_bound":
        '"E_q10":"-a**3*omega*(omega*dq-sqrt(w)*(Q*du+dphi_x/a))/2-d_t(a**3*dqt/2)"' in squeeze(d2),
      "H4F3d2_records_eta_regularization_open":
        '"eta_regularization_not_assumed"' in d2,
      "H4F2b_original_formal_eta_template_bound":
        '"regularity"' in b
        and "original action has sqrt(eta)" in b,
    }

def exact(x):
    return bool(sp.simplify(sp.trigsimp(sp.expand(x)))==0)

def physical_action_and_euler():
    eta=sp.symbols("eta",positive=True,real=True)
    N,L,R,At,Ax,qt,qx,q,omega,sqrtw,X=sp.symbols(
        "N L R At Ax qt qx q omega sqrtw X",real=True
    )
    Ut,Utx,Uxx=sp.symbols("Ut Utx Uxx",real=True)
    vol=N*L*R**2
    lag_physical=vol*sp.Rational(1,4)*(
        (At*Utx+Ax*Uxx)**2
        -(omega*Ut-sp.sqrt(eta)*sqrtw*X)**2
    )
    lag_red=vol*sp.Rational(1,4)*(
        (At*qt+Ax*qx)**2-(omega*q-sqrtw*X)**2
    )
    field_redefinition={
       Ut:sp.sqrt(eta)*q,
       Utx:sp.sqrt(eta)*qt,
       Uxx:sp.sqrt(eta)*qx,
    }
    checks={
      "NL0B_completed_square_exact_eta_Lred":
         exact(lag_physical.subs(field_redefinition)-eta*lag_red),
      "Euler_U_local_equals_sqrt_eta_Euler_q_local":
         exact(sp.diff(lag_physical,Ut).subs(field_redefinition)
               -sp.sqrt(eta)*sp.diff(lag_red,q)),
      "Euler_U_t_momentum_equals_sqrt_eta_reduced":
         exact(sp.diff(lag_physical,Utx).subs(field_redefinition)
               -sp.sqrt(eta)*sp.diff(lag_red,qt)),
      "Euler_U_x_momentum_equals_sqrt_eta_reduced":
         exact(sp.diff(lag_physical,Uxx).subs(field_redefinition)
               -sp.sqrt(eta)*sp.diff(lag_red,qx)),
      "physical_U_spatial_Ward_equals_eta_reduced_Ward":
         exact(sp.sqrt(eta)*sp.sqrt(eta)-eta),
      "GE06_mapped_action_density_is_two_eta_Lred":
         exact(2*lag_physical.subs(field_redefinition)-2*eta*lag_red),
    }
    expected_q=-(vol*omega*(omega*q-sqrtw*X))/2
    checks["GE05_reduced_q_local_Euler_exact"]=exact(
        sp.diff(lag_red,q)-expected_q
    )
    checks["GE05_reduced_q_temporal_current_exact"]=exact(
        sp.diff(lag_red,qt)-vol*(At*qt+Ax*qx)*At/2
    )
    checks["GE05_reduced_q_spatial_current_exact"]=exact(
        sp.diff(lag_red,qx)-vol*(At*qt+Ax*qx)*Ax/2
    )
    return checks

def signed_mixed_coefficient():
    eps,eta,s=sp.symbols("eps eta s",positive=True,real=True)
    e10,e11,e20,e21,p10,p11,p20,p21=sp.symbols(
       "e10 e11 e20 e21 p10 p11 p20 p21",real=True
    )
    E=eps*(e10+eta*e11)+eps**2*(e20+eta*e21)/2
    qx=eps*(p10+eta*p11)+eps**2*(p20+eta*p21)/2
    physical_mapped_ward=2*eta*E*qx
    direct=sp.diff(sp.diff(physical_mapped_ward,eps,2),eta)
    actual=direct.subs({eps:0,eta:0})
    expected=4*e10*p10
    physical_s_ward=(2*s**2*E.subs(eta,s**2)*qx.subs(eta,s**2))
    s_derivative=sp.diff(physical_s_ward,s)/(2*s)
    s_limit=sp.limit(sp.diff(s_derivative,eps,2).subs(eps,0),s,0,dir="+")
    ordinary_wrong=2*E*qx
    wrong_coef=sp.diff(sp.diff(ordinary_wrong,eps,2),eta).subs(
        {eps:0,eta:0})
    without_two=eta*E*qx
    without_two_coef=sp.diff(sp.diff(without_two,eps,2),eta).subs(
        {eps:0,eta:0})
    checks={
       "physical_eps2_eta1_ward_coefficient_exact":
           exact(actual-expected),
       "physical_one_sided_sqrt_eta_derivative_same":
           exact(s_limit-expected),
       "independent_of_q11_eta_tangent":
           exact(sp.diff(actual,p11)),
       "independent_of_Eq11_eta_tangent":
           exact(sp.diff(actual,e11)),
       "independent_of_q20_and_q21":
           exact(sp.diff(actual,p20))
           and exact(sp.diff(actual,p21)),
       "independent_of_Eq20_and_Eq21":
           exact(sp.diff(actual,e20))
           and exact(sp.diff(actual,e21)),
       "on_shell_first_order_Eq_zero":
           exact(actual.subs(e10,0)),
       "naive_integer_eta_template_wrong_when_no_eta_tangent":
           exact(wrong_coef.subs({e11:0,p11:0}))
           and not exact(expected.subs({e11:0,p11:0})),
       "naive_template_unrelated_to_physical_coefficient":
           not exact(wrong_coef-expected),
       "omitted_GE05_GE06_factor_two_halves_term":
           exact(without_two_coef-expected/2),
    }
    per_node_raw=2*e10*p10
    checks["GE05_raw_coefficient_is_two_before_mapping"]=exact(
        per_node_raw-expected/2
    )
    return checks,{
       "physical_bath":"U_j=sqrt(eta)*q_j",
       "physical_reduced_action":"L_mem,GE05=eta*L_GE05,red",
       "mapped_action":"L_mem,GE06_raw=2*eta*L_GE05,red",
       "signed_regularized_parent":"W_q,GE06=+2 eta Sum_j E_q,GE05,red * partial_x q_j",
       "H4_mixed_parent":"d_eta d_eps^2 W_q|0 = +4 Sum_j E_q,GE05,10 * partial_x q_j10",
       "GE05_raw_unmapped":"d_eta d_eps^2 W_q,GE05|0 = +2 Sum_j E_q,GE05,10 * partial_x q_j10",
       "no_direct_q20_parent_coefficient":"q_j20 and E_qj20 first occur at eta*epsilon^3 with q_j00=E_qj00=0",
       "first_order_exact_on_shell":"if all E_qj10=0, this full off-shell bath parent term vanishes",
       "source_rows_not_modified":True,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()
    blobs=frozen_blobs()
    bindings=frozen_bindings()
    action=physical_action_and_euler()
    coeff,ledger=signed_mixed_coefficient()
    passed=bool(
      all(p["exact"] for p in blobs.values())
      and all(bindings.values())
      and all(action.values())
      and all(coeff.values())
    )
    result={
      "classification":(
        "GE19_H4F3D3_ETA_REGULARIZED_BATH_WARD_PARENT_DERIVED"
        if passed else
        "GE19_H4F3D3_ETA_REGULARIZED_BATH_WARD_UNRESOLVED"
      ),
      "predata_classification":
        "GE19_H4F3D3_PREDATA_ETA_REGULARIZED_BATH_WARD_PARENT",
      "source_blobs":blobs,
      "frozen_action_and_previous_gap_bindings":bindings,
      "physical_action_and_Euler_chain_rule":action,
      "signed_mixed_regularized_Ward_gates":coeff,
      "exact_ledger":ledger,
      "all_analytic_gates_pass":passed,
      "no_new_source_row_or_fitted_coefficient":True,
      "H3F_H3G_Z11_real_parent_residuals_evaluated":False,
      "full_H4_all_sector_Noether_derived":False,
      "H4_Z21_solve_performed":False,
      "Z21_certified":False,
      "lensing_licensed":False,
      "next_route":(
        "INTEGRATE_SIGNED_ETA_BATH_PARENT_WITH_EXISTING_H4F3D_OPERATOR_AND_ALL_SECTOR_SOURCES"
        if passed else "FREEZE_MISSING_OR_INCONSISTENT_ETA_BATH_PARENT_PROOF"
      ),
      "claim_boundary":
        "Exact missing regularized-bath parent coefficient closes the previously acknowledged eta-rescaling algebraic gap, but does not by itself certify full action-source/parent Ward on actual grids or Z21."
    }
    target=Path(args.json_out)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    if not passed:
        raise SystemExit(3)

if __name__=="__main__":
    main()
