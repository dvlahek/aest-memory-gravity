#!/usr/bin/env python3
"""Exact integrable-jet coefficient ledger for frozen GE19 linear Ward.

Proof of 16 equivalent coefficient obligations, plus source-bound dust-only
nonzero lapse Ward coefficient. Does NOT check that actual production Cmat
satisfies all 16 or certify full H4 Ward / Z21 / lensing.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
PINS={
    "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
        "e34d28a2062c748f48bc82fa928844b02631de25",
    "ge19/h4f3d1_frozen_canonical_operator_ward.py":
        "60786ac14c9478801c5df9ccf458ead9a34ac827",
    "ge19/h4f3d2_dust_bath_parent_euler_currents.py":
        "42b2405759402195ffb371056d9e48b70dcded71",
    "ge07/pressureless_matter_directional_source_generator.py":
        "cde8da77a80799cef00fc7c09c3633310fc9e3d4",
    "ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py":
        "dbfa43ae11dbd3cfeeb1994a30237e9374dbb3e7",
}
TINY_GATE="ACTUAL_16_CMAT_JET_COEFFICIENTS_NOT_EVALUATED"

def verify_original():
    pins={}
    for path,expected in PINS.items():
        observed=subprocess.check_output(
            ["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True).strip()
        if observed!=expected:
            raise RuntimeError("GIT_BLOB_MISMATCH "+path+" "+observed)
        pins[path]={"blob":expected,"match":True}
    r7=(ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py").read_text()
    d1=(ROOT/"ge19/h4f3d1_frozen_canonical_operator_ward.py").read_text()
    d2=(ROOT/"ge19/h4f3d2_dust_bath_parent_euler_currents.py").read_text()
    expected={
        "canonical_w_order":
            "w=(N,dr,S,u,phi,T,Sdot,udot,phidot,Tdot)" in r7,
        "full_shift_Euler_row":
            "Eb=products[:,10]+products[:,11]" in d1,
        "independent_L_projection":
            "EL_non=(iso+2*aniso)/3" in d1,
        "retained_L_time_momentum":
            "EL=EL_non-H*(D@pL)" in d1,
        "retained_shift_time_derivative":
            "Eshift_time=H*(D@Eb)" in d1,
        "GE07_first_shift_row":
            '"E_b10":"-2*a**3*rho0*dTx"' in d2,
        "GE07_first_L_row":
            '"E_L10":"2*a**2*rho0*(dTt-dN)"' in d2,
    }
    if not all(expected.values()):
        raise RuntimeError("SOURCE_ROW_BINDING_MISMATCH "+str(expected))
    return pins,expected

def analytic_gate():
    t,k=sp.symbols("t k",real=True)
    a=sp.Function("a")(t)
    # Actual w has 6 fields and 4 already-entered first time derivatives;
    # its 10 time derivatives therefore are NOT independent.
    N,dr,S,u,phi,T=[sp.Function(n)(t)
                    for n in ("N","dr","S","u","phi","T")]
    w=[N,dr,S,u,phi,T,sp.diff(S,t),sp.diff(u,t),
       sp.diff(phi,t),sp.diff(T,t)]
    B=[sp.Function("B"+str(j))(t) for j in range(10)]
    P=[sp.Function("P"+str(j))(t) for j in range(10)]
    J=[sp.Function("J"+str(j))(t) for j in range(10)]
    # B = C10+C11, P=C14, J=(C6+2(C12+C13))/3.
    U=[-sp.diff(B[j],t)-sp.I*k*a*J[j]+sp.I*k*a*sp.diff(P[j],t)
       for j in range(10)]
    V=[-B[j]+sp.I*k*a*P[j] for j in range(10)]
    W=(-sp.diff(sum(B[j]*w[j] for j in range(10)),t)
       -sp.I*k*a*(sum(J[j]*w[j] for j in range(10))
                 -sp.diff(sum(P[j]*w[j] for j in range(10)),t)))
    expanded=sum(U[j]*w[j]+V[j]*sp.diff(w[j],t)
                 for j in range(10))
    if sp.expand(W-expanded)!=0:
        raise RuntimeError("OPERATOR_PRODUCT_RULE_FAIL")

    jets=[
        (N,U[0]),(dr,U[1]),(S,U[2]),(u,U[3]),
        (phi,U[4]),(T,U[5]),
        (sp.diff(N,t),V[0]),(sp.diff(dr,t),V[1]),
        (sp.diff(S,t,2),V[6]),(sp.diff(u,t,2),V[7]),
        (sp.diff(phi,t,2),V[8]),(sp.diff(T,t,2),V[9]),
        (sp.diff(S,t),U[6]+V[2]),
        (sp.diff(u,t),U[7]+V[3]),
        (sp.diff(phi,t),U[8]+V[4]),
        (sp.diff(T,t),U[9]+V[5]),
    ]
    if len(jets)!=16 or len(set(z for z,_ in jets))!=16:
        raise RuntimeError("NOT_16_INDEPENDENT_JETS")
    reconstructed=sum(z*c for z,c in jets)
    if sp.expand(W-reconstructed)!=0:
        raise RuntimeError("INTEGRABLE_JET_DECOMPOSITION_FAIL")
    if any(sp.expand(sp.diff(W,z)-c)!=0 for z,c in jets):
        raise RuntimeError("INDEPENDENT_JET_COEFFICIENT_FAIL")

    # Dust-only source-derived values under D=a^3 varrho0=3C:
    # E_b,10 = -2 D (ik) T ; E_L,10 = 2D/a (dot T-N).
    D=sp.symbols("D",positive=True)
    bd=[sp.S.Zero]*10
    pd=[sp.S.Zero]*10
    jd=[sp.S.Zero]*10
    bd[5]=-2*D*sp.I*k
    jd[0]=-2*D/a
    jd[9]=2*D/a
    ud=[-sp.diff(bd[j],t)-sp.I*k*a*jd[j] for j in range(10)]
    vd=[-bd[j] for j in range(10)]
    dust=sum(ud[j]*w[j]+vd[j]*sp.diff(w[j],t)
             for j in range(10))
    if sp.expand(dust-2*sp.I*k*D*N)!=0:
        raise RuntimeError("DUST_NONZERO_N_LAPSE_COEFFICIENT_FAIL")
    if sp.expand(dust.subs(D,3*sp.Symbol("C"))-
                 6*sp.I*k*sp.Symbol("C")*N)!=0:
        raise RuntimeError("DUST_C_NORMALIZATION_FAIL")
    if sp.expand(dust.subs({N:0}))!=0:
        raise RuntimeError("DUST_NEGATIVE_CONTROL_FAIL")

    return {
        "formal_product_rule_identity":True,
        "exact_16_integrable_jet_coefficients":True,
        "independent_jet_groups":{
            "fields_U0_to_U5":6,
            "lapse_and_density_time_derivatives_V0_V1":2,
            "four_second_derivatives_V6_to_V9":4,
            "dynamic_first_derivatives_U6_to_U9_plus_V2_to_V5":4,
        },
        "dust_only_syzygy": "2*I*k*D*N = 6*I*k*C*N",
        "dust_source_derived_reduction_exact":True,
        "combined_GE06_plus_Lambda_required_lapse_term":
            "-6*I*k*C*N",
        "production_Cmat_16_coefficients_evaluated":False,
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--json-out",type=Path)
    args=parser.parse_args()
    pins,bindings=verify_original()
    gates=analytic_gate()
    report={
        "classification":
            "GE19_CMAT_INTEGRABLE_JET_FORMAL_CONTRACT_PASS_ACTUAL_CMAT_OPEN",
        "source_blob_locks":pins,"source_row_bindings":bindings,
        "analytic_results":gates,
        "claim_boundary":
            "Exact integrable-jet coefficient decomposition of the canonical "
            "linear Ward operator plus dust-only nonzero lapse Ward term. "
            "Does not evaluate the 16 conditions on the actual production "
            "Cmat with analytic background derivatives, establish the full "
            "action-coupled numerical Noether identity, or certify Z21.",
        "full_H4_Ward_certified":False,
        "Z21_certified":False,
        "lensing_licensed":False,
        "physical_Ward_error_budget_frozen":False,
        "next_gate":
            "VERIFY_ALL_16_SOURCE_DERIVED_CMAT_COEFFICIENTS_ON_REPAIR13_ONSHELL_BACKGROUND"
    }
    if args.json_out is not None:
        if args.json_out.exists():
            raise RuntimeError("OUTPUT_EXISTS_NO_OVERWRITE "+str(args.json_out))
        args.json_out.parent.mkdir(parents=True,exist_ok=True)
        args.json_out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print("GE19_16_INTEGRABLE_JET_COEFFICIENT_LEDGER_EXACT_PASS")
    print("GE19_GE07_DUST_UNCANCELLED_6IKC_N_COEFFICIENT_EXACT_PASS")
    print("ACTUAL_CMAT_16_COEFFICIENTS_OPEN FULL_H4_WARD_CERTIFIED=false")
if __name__=="__main__":
    main()
