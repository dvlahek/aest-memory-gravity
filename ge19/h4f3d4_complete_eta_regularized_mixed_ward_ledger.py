#!/usr/bin/env python3
"""H4F3d4: full FORMAL signed mixed spatial Ward ledger with eta-rescaled bath.

Derive a single off-shell d_eta d_epsilon^2 identity from the complete
nonbath GE19 Euler field list, plus the PHYSICAL (not naive integer-eta)
NL0B bath product 2 eta sum_j E_GE05,qj qj,x. Project the full L/shift
Euler rows onto the frozen GE19 canonical operator and six RHS pieces.

The exact proof is formal/action-level: it does NOT independently compute
all actual first-order parent Euler residual arrays or physical FD errors.
No actual-grid structural PASS and no Z21 science solve are claimed.
"""
from __future__ import annotations

import argparse,json,subprocess
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
PINS={
 "ge19/h4f3d4_predata_complete_eta_regularized_mixed_ward_ledger.json":
   "cc921c4086d914274738a29f2b7b5c6961ab56b0",
 "ge19/h4f3d3_predata_eta_regularized_bath_ward_parent.json":
   "ff7720381ddd09c7c073e106b2f35065ac3d1d6f",
 "ge19/h4f3d3_eta_regularized_bath_ward_parent.py":
   "fb340b957c31e34d35f1ebd9404a53b59d29c102",
 "ge19/h4f2b_signed_mixed_ward_template.py":
   "ab783ffe8242d8ff455647df8664a074f725ee81",
 "ge19/h4f3d1_frozen_canonical_operator_ward.py":
   "60786ac14c9478801c5df9ccf458ead9a34ac827",
 "ge19/h4f3d2_dust_bath_parent_euler_currents.py":
   "42b2405759402195ffb371056d9e48b70dcded71",
 "ge19/h4f2h_physical_time_source_ward_bridge.py":
   "65ce1e68a2f77e063c4bb8848d770abb4baeeebf",
 "ge19/h4f2g_action_completed_six_piece_source_ledger.py":
   "d9778da0bb6cc52a15015238810c79978527ffc5",
 "ge19/h4f3b_actual_corrected_six_piece_source.py":
   "0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c",
 "ge19/h4f3d_predata_actual_operator_all_parent_ward_closure.json":
   "f1bd4eb52b7da96ac2d50ed9136e3e1a74635f51",
}
PIECES=(
 "2Q_GE06_cross","2Q_GE07_cross","2Q_Lambda_cross",
 "2DY2_action_complete_Y_u_and_phi","2M1_GE05_mapped",
 "2M2_GE05_mapped"
)
NONBATH=("N","L","R","b","u","phi","T","rho")

def exact(e):
    return bool(sp.expand(e.doit())==0)

def frozen_blobs():
    d={}
    for path,want in PINS.items():
        got=subprocess.check_output(
            ["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True
        ).strip()
        d[path]={"expected":want,"observed":got,"exact":got==want}
    return d

def action_and_implementation_binding():
    src=(ROOT/"ge19/h4f3d3_eta_regularized_bath_ward_parent.py").read_text()
    template=(ROOT/"ge19/h4f2b_signed_mixed_ward_template.py").read_text()
    op=(ROOT/"ge19/h4f3d1_frozen_canonical_operator_ward.py").read_text()
    currents=(ROOT/"ge19/h4f3d2_dust_bath_parent_euler_currents.py").read_text()
    source=(ROOT/"ge19/h4f2g_action_completed_six_piece_source_ledger.py").read_text()
    clock=(ROOT/"ge19/h4f2h_physical_time_source_ward_bridge.py").read_text()
    actual=(ROOT/"ge19/h4f3b_actual_corrected_six_piece_source.py").read_text()
    return {
      "H4F3d3_physical_bath_factor_2eta":
         "physical_mapped_ward=2*eta*E*qx" in src,
      "H4F2b_original_all_nonbath_mixed_template":
         "E[n][\"00\"]*sp.diff(F[n][\"21\"],x)" in template,
      "H4F3d1_frozen_actual_Cmat_full_momentum_operator":
         "EL=EL_non-H*(D@pL)" in op
         and "ward=-Eshift_time-1j*float(k)*a*EL" in op,
      "H4F3d2_actual_GE07_GE05_parent_currents":
         '"E_rho10":"2*a**3*(dTt-dN), no rho0 multiplier"' in currents
         and '"eta_regularization_not_assumed"' in currents,
      "H4F2g_actual_six_source_family_names":
         all(('"'+name+'"') in source for name in PIECES),
      "H4F2h_actual_physical_clock_source_schemes":
         '"fd8"' in clock and '"fd4"' in clock
         and "hh[:,None]*(derivative@f[6])" in clock,
      "H4F3b_actual_corrected_source_not_manufactured":
         "per_beta,diag=actual_case_source(" in actual
         and 'save[f"{name}_total_rows"]' in actual,
    }

def complete_formal_mixed():
    t,x,eps,eta=sp.symbols("t x eps eta",real=True)
    a=sp.Function("a")(t)
    baseline={
      "N":sp.Integer(1),"L":a,"R":a,"b":sp.Integer(0),
      "u":sp.Integer(0),"phi":sp.Function("phi0")(t),
      "T":sp.Function("T0")(t),"rho":sp.Function("rho0")(t),
    }
    def F(prefix,name,order):
        return sp.Function(prefix+"_"+name+"_"+order)(t,x)
    E={n:{p:F("E",n,p) for p in ("00","10","11","20","21")}
       for n in NONBATH}
    fields={n:{p:F("f",n,p) for p in ("10","11","20","21")}
            for n in NONBATH}
    field={
        n:baseline[n]+eps*(fields[n]["10"]+eta*fields[n]["11"])
          +eps**2*(fields[n]["20"]+eta*fields[n]["21"])/2
        for n in NONBATH
    }
    euler={
        n:E[n]["00"]+eps*(E[n]["10"]+eta*E[n]["11"])
          +eps**2*(E[n]["20"]+eta*E[n]["21"])/2
        for n in NONBATH
    }
    # q is a regularized scalar only. Its PHYSICAL action carries 2*eta
    # after the frozen GE05->GE06 Euler normalization (H4F3d3).
    eq10=F("Eq","q","10");eq11=F("Eq","q","11")
    eq20=F("Eq","q","20");eq21=F("Eq","q","21")
    q10=F("q","q","10");q11=F("q","q","11")
    q20=F("q","q","20");q21=F("q","q","21")
    eqred=eps*(eq10+eta*eq11)+eps**2*(eq20+eta*eq21)/2
    qred=eps*(q10+eta*q11)+eps**2*(q20+eta*q21)/2

    ward=sum((euler[n]*sp.diff(field[n],x)
              for n in NONBATH),sp.S.Zero)
    ward+=2*eta*eqred*sp.diff(qred,x)
    ward-=sp.diff(field["L"]*euler["L"]-
                  field["b"]*euler["b"],x)
    ward-=sp.diff(euler["b"],t)
    mixed=sp.diff(sp.diff(ward,eps,2),eta).subs(
        {eps:0,eta:0}).doit()
    nonbath_parent=sum(
        (E[n]["00"]*sp.diff(fields[n]["21"],x)
         +2*E[n]["10"]*sp.diff(fields[n]["11"],x)
         +2*E[n]["11"]*sp.diff(fields[n]["10"],x))
        for n in NONBATH
    )
    bath_parent=4*eq10*sp.diff(q10,x)
    lower_boundary=(
        fields["L"]["21"]*E["L"]["00"]
        +2*fields["L"]["10"]*E["L"]["11"]
        +2*fields["L"]["11"]*E["L"]["10"]
        -fields["b"]["21"]*E["b"]["00"]
        -2*fields["b"]["10"]*E["b"]["11"]
        -2*fields["b"]["11"]*E["b"]["10"]
    )
    parent=nonbath_parent+bath_parent-sp.diff(lower_boundary,x)
    expected=(parent-sp.diff(a*E["L"]["21"],x)
              -sp.diff(E["b"]["21"],t))

    test={
        "full_action_mixed_eps2_eta1_exact_with_eta_bath":
             exact(mixed-expected),
        "bath_normalization_exact_plus_four":
             exact(sp.diff(sp.diff(
                  2*eta*eqred*sp.diff(qred,x),eps,2),eta
                  ).subs({eps:0,eta:0})-bath_parent),
        "bath_q20_or_q11_do_not_enter_direct_mixed_parent":
             not mixed.has(eq20) and not mixed.has(q20)
             and not mixed.has(eq11) and not mixed.has(q11)
             and not mixed.has(eq21) and not mixed.has(q21),
        "bath_first_order_on_shell_conditional_vanish":
             exact(bath_parent.subs(eq10,0)),
        "bath_missing_term_is_not_identically_zero":
             not exact(bath_parent),
        "full_nonbath_lower_parent_and_boundary_kept":
             all(mixed.has(E[n]["10"]) and mixed.has(E[n]["11"])
                 for n in NONBATH),
        "nonbath_background_E00_F21_kept":
             all(mixed.has(E[n]["00"]) for n in NONBATH),
    }
    # A generic scalar homogeneous T0/rho0 background need not satisfy
    # its Euler equations; only explicit verified on-shell substitutions
    # eliminate these terms.
    shell={E[n][order]:0 for n in NONBATH
           for order in ("00","10","11")}
    shell[eq10]=0
    on_shell=mixed.subs(shell).doit()
    on_shell_expected=(
         -sp.diff(a*E["L"]["21"],x)-sp.diff(E["b"]["21"],t))
    test["conditional_all_parent_on_shell_exact"]=exact(
        on_shell-on_shell_expected
    )

    # Independently retain original GE19 source decomposition in
    # the canonical L Euler projection, before any FD approximation.
    SB=[F("Sb",name,"21") for name in PIECES]
    SI=[F("Si",name,"21") for name in PIECES]
    SA=[F("Sa",name,"21") for name in PIECES]
    sb=sum(SB,sp.S.Zero)
    si=sum(SI,sp.S.Zero)
    sa=sum(SA,sp.S.Zero)
    lb,li,la=[F("Lin",name,"21") for name in ("b","iso","aniso")]
    split=expected.subs({
         E["b"]["21"]:lb-sb,
         E["L"]["21"]:(li+2*la-si-2*sa)/3
    }).doit()
    operator=-sp.diff(lb,t)-sp.diff(a*(li+2*la)/3,x)
    source=sum((sp.diff(SB[i],t)
        +sp.diff(a*(SI[i]+2*SA[i])/3,x)
        for i in range(len(PIECES))),sp.S.Zero)
    test["operator_plus_six_source_plus_all_parent_exact"]=exact(
        split-operator-source-parent
    )
    no_eta_parent=parent-bath_parent
    test["omitting_explicit_eta_bath_parent_negative_control"]=(
        not exact(split-operator-source-no_eta_parent)
    )
    test["source_ward_is_not_standalone_zero_identity"]=(
        not exact(source)
    )
    test["zero_parent_noether_reduces_to_operator_plus_source"]=exact(
        (split-parent)-operator-source
    )

    return test,{
      "exact_full_formal_identity":
       "W21 = Sum_i!=q(E_i00*f_i21,x +2E_i10*f_i11,x +2E_i11*f_i10,x)+4Sum_j E_qj10,GE05*q_j10,x -d_x(B21)-d_t(E_b21)=0",
      "B21":
       "a*E_L21 + L21*E_L00 +2L10*E_L11+2L11*E_L10 -b21*E_b00-2b10*E_b11-2b11*E_b10",
      "complete_residual_split":
       "W_operator + W_six_source + W_all_parent =0",
      "linear_operator":
       "-H*FD4_x[(Cmat10+Cmat11)w] -ik*a{[Cmat6+2(Cmat12+Cmat13)]w/3-H*FD4_x[Cmat14*w]}",
      "source_six_piece":
       "Sum_p[H*D_p S_b,p +ik*a(S_iso,p+2 S_aniso,p)/3], D_p=FD8 for GE06/GE07/Lambda/Y; FD4 for GE05 M1/M2",
      "signed_all_parent":
       "Sum_i!=q(E_i00*f_i21,x+2E_i10*f_i11,x+2E_i11*f_i10,x)+4Sum_j E_qj10,GE05*q_j10,x -d_x[ L21 E_L00+2L10 E_L11+2L11 E_L10-b21 E_b00-2b10 E_b11-2b11 E_b10]",
      "explicit_q20_parent_product":
       "zero at mixed eps2 eta1 because regular q background and E_q00 vanish; corrected q20 still enters actual six-piece M1 source",
      "on_shell":"W_parent=0 only after independently verified background,H1,Z11 and first-order per-node bath equations plus stated boundary regularity",
      "actual_parent_grid_evaluated":False,
      "FD4_FD8_structural_tolerance_preregistered":False,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()
    pins=frozen_blobs()
    binds=action_and_implementation_binding()
    tests,ledger=complete_formal_mixed()
    passed=bool(all(x["exact"] for x in pins.values())
                and all(binds.values()) and all(tests.values()))
    out={
      "classification":(
        "GE19_H4F3D4_FULL_FORMAL_ETA_WARD_LEDGER_PASS_ACTUAL_GRID_OPEN"
        if passed else
        "GE19_H4F3D4_FORMAL_MIXED_WARD_LEDGER_UNRESOLVED"
      ),
      "predata_classification":
        "GE19_H4F3D4_PREDATA_COMPLETE_ETA_REGULARIZED_MIXED_WARD_LEDGER",
      "frozen_blobs":pins,
      "action_and_actual_implementation_bindings":binds,
      "exact_signed_full_formal_ward_gates":tests,
      "full_formal_ledger":ledger,
      "all_formal_gates_pass":passed,
      "actual_H4F3b_corrected_parent_arrays_loaded":False,
      "all_actual_parent_residuals_evaluated":False,
      "FD4_FD8_physical_structural_threshold_frozen":False,
      "full_physical_H4F3d_structural_PASS":False,
      "H4_Z21_solve_performed":False,"Z21_certified":False,
      "lensing_licensed":False,
      "next_route":(
        "ONE_ACTUAL_COMMON_GRID_OPERATOR_SIX_SOURCE_ALL_PARENT_WARD_TEST"
        if passed else "FREEZE_FORMAL_WARD_GATE_DEFECT"
      ),
    }
    p=Path(args.json_out);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True,allow_nan=False))
    if not passed:
        raise SystemExit(3)

if __name__=="__main__":
    main()
