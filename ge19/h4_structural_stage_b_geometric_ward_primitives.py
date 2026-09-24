#!/usr/bin/env python3
"""GE19 H4 structural Stage B: reduced spatial-Ward geometric primitives.

Analytic subset only. This checks the transformation law of the 1+1
longitudinal GE06/GE07/GE05 scalar/tetrad building blocks, the formal
Euler-Lagrange spatial-Ward integration-by-parts identity, the exact
isotropic/anisotropy row projection, and the GE05 memory-shift variation.

It does NOT certify the full NL0B bath covariant field transformation,
the nonanalytic Y2 zero-set treatment, the mixed H4 coefficient,
parent-equation cancellation, Z21 or lensing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp

ROOT=Path(__file__).resolve().parents[1]

FROZEN_BLOBS={
    "ge06/analytic_aest_directional_source_generator.py":
        "a7afe0035054a9dca55d74a6497c081422114b4c",
    "ge07/pressureless_matter_directional_source_generator.py":
        "cde8da77a80799cef00fc7c09c3633310fc9e3d4",
    "ge05/memory_directional_source_generator.py":
        "40837d77f89028da30c28899e2d0530a4401844e",
    "docs/nl0b_covariant_memory_completion_result.md":
        "d005b1c135fead856510aa76b6174fb9051fa552",
    "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
        "e34d28a2062c748f48bc82fa928844b02631de25",
    "docs/ge19_h4_structural_stage_a_source_row_ledger.md":
        "44d4f01a05aba26926d6a8e13a2b7aac995258d5",
    "ge19/h4_structural_stage_b_predata_action_noether_identity.json":
        "11123763b2f5bf06ac6f704acffdea0b4eb34f1d",
}

def frozen_blob_controls():
    checks={}
    for path,want in FROZEN_BLOBS.items():
        got=subprocess.check_output(
            ["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True
        ).strip()
        checks[path]={"expected_blob":want,"observed_blob":got,
                      "exact":bool(got==want)}
    return checks


def rational_zero(expr):
    return sp.factor(sp.cancel(sp.expand(expr)))==0


def build_reduced_diffeo_checks():
    t,x,eps=sp.symbols("t x eps",real=True)
    xi=sp.Function("xi")(t,x)
    symbols={
        name:sp.Function(name)(t,x)
        for name in ("N","L","R","b","u","phi","T","q","rho")
    }
    N,L,R,b,u,phi,T,q,rho=(
        symbols[name]
        for name in ("N","L","R","b","u","phi","T","q","rho")
    )
    # The reduced per-node GE05 q variable is treated as an x-scalar
    # in this restricted primitive check. The full covariant bath
    # vector/projector transformation remains a separate obligation.
    delta={f:xi*sp.diff(f,x) for f in symbols.values()}
    delta[L]=sp.diff(xi*L,x)
    delta[b]=sp.diff(xi,t)+xi*sp.diff(b,x)-b*sp.diff(xi,x)

    substitution={}
    for field,variation in delta.items():
        for coordinate in (t,x):
            dfield=sp.diff(field,coordinate)
            substitution[dfield]=dfield+eps*sp.diff(variation,coordinate)
        substitution[field]=field+eps*variation

    ch,sh=sp.cosh(u),sp.sinh(u)
    kl=(sp.diff(L,t)-b*sp.diff(L,x)-L*sp.diff(b,x))/(N*L)
    kr=(sp.diff(R,t)-b*sp.diff(R,x))/(N*R)
    sigma=(sp.diff(phi,t)-b*sp.diff(phi,x))/N
    qinv=ch*sigma+sh*sp.diff(phi,x)/L
    xinv=sh*sigma+ch*sp.diff(phi,x)/L
    E=ch*(
        (sp.diff(u,t)-b*sp.diff(u,x))/N+
        sp.diff(N,x)/(N*L)
    )+sh*(kl+sp.diff(u,x)/L)
    aq=ch*(sp.diff(q,t)-b*sp.diff(q,x))/N+sh*sp.diff(q,x)/L
    dust_w=(sp.diff(T,t)-b*sp.diff(T,x))/N
    dust_v=sp.diff(T,x)/L

    primitives={
        "invariant_volume_density":(N*L*R**2,True),
        "GE06_kL":(kl,False),
        "GE06_kR":(kr,False),
        "GE06_sigma":(sigma,False),
        "GE06_Qinv":(qinv,False),
        "GE06_Xinv":(xinv,False),
        "GE06_E":(E,False),
        "GE05_reduced_Aq":(aq,False),
        "GE07_dust_W":(dust_w,False),
        "GE07_dust_V":(dust_v,False),
    }
    checks={}
    for name,(expr,is_density) in primitives.items():
        varied=sp.diff(expr.xreplace(substitution),eps).subs(eps,0)
        expected=xi*sp.diff(expr,x)
        if is_density:
            expected+=sp.diff(xi,x)*expr
        checks[name]=bool(rational_zero(varied-expected))

    # Formal Ward identity from Euler-Lagrange variations after
    # integration by parts. This checks the geometric sign and the
    # longitudinal metric/shift density terms only; it is not the
    # frozen complete H4 coefficient.
    EN,EL,ER,Eb=(
        sp.Function(name)(t,x)
        for name in ("EN","EL","ER","Eb")
    )
    field_equations={
        name:sp.Function("E_"+name)(t,x)
        for name in ("u","phi","T","q","rho")
    }
    scalar_contraction=sum(
        field_equations[name]*sp.diff(symbols[name],x)
        for name in field_equations
    )
    common=(
        EN*sp.diff(N,x)+EL*sp.diff(L,x)+
        ER*sp.diff(R,x)+Eb*sp.diff(b,x)+scalar_contraction
    )
    boundary_x=L*EL-b*Eb
    ward=common-sp.diff(boundary_x,x)-sp.diff(Eb,t)
    el_variation=xi*common+sp.diff(xi,x)*boundary_x+sp.diff(xi,t)*Eb
    integrated_form=(
        xi*ward+sp.diff(xi*boundary_x,x)+sp.diff(xi*Eb,t)
    )
    checks["formal_EL_Ward_integration_by_parts"]=bool(
        rational_zero(el_variation-integrated_form)
    )
    eiso,eaniso=sp.symbols("E_isotropic E_anisotropy")
    recovered_L=(eiso+2*eaniso)/3
    recovered_R=(2*eiso-2*eaniso)/3
    checks["isotropic_anisotropy_to_EL_ER_projection"]=bool(
        sp.simplify(recovered_L+recovered_R-eiso)==0
        and sp.simplify(recovered_L-sp.Rational(1,2)*recovered_R-eaniso)==0
    )
    return checks


def exact_ge05_shift_variation():
    N,L,R,b,u=sp.symbols("N L R b u",real=True)
    pt,px,qt,qx,q=sp.symbols("pt px qt qx q",real=True)
    om,sw=sp.symbols("om sw",positive=True,real=True)
    ch,sh=sp.cosh(u),sp.sinh(u)
    aq=ch*(qt-b*qx)/N+sh*qx/L
    xphi=sh*(pt-b*px)/N+ch*px/L
    completed=om*q-sw*xphi
    lag=N*L*R**2*sp.Rational(1,4)*(aq**2-completed**2)
    claimed=-(L*R**2)*sp.Rational(1,2)*(
        aq*ch*qx+completed*sw*sh*px
    )
    exact=bool(sp.simplify(sp.diff(lag,b)-claimed)==0)

    eps,a,Q=sp.symbols("eps a Q",real=True)
    dN,dL,dR,db,du,dpt,dpx,dqt,dqx,dq=sp.symbols(
        "dN dL dR db du dpt dpx dqt dqx dq",real=True
    )
    expansion={
        N:1+eps*dN,L:a+eps*dL,R:a+eps*dR,
        b:eps*db,u:eps*du,pt:Q+eps*dpt,
        px:eps*dpx,qt:eps*dqt,qx:eps*dqx,q:eps*dq
    }
    second=sp.simplify(sp.diff(claimed.subs(expansion),eps,2).subs(eps,0))
    second_exact=bool(sp.simplify(second+a**3*dqt*dqx)==0)
    return {
        "exact_shift_partial_identity":exact,
        "second_directional_shift_coefficient_exact":second_exact,
        "frozen_second_directional_shift_coefficient":str(second),
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--json-out",required=True)
    args=parser.parse_args()
    blobs=frozen_blob_controls()
    checks=build_reduced_diffeo_checks()
    ge05=exact_ge05_shift_variation()
    passed=bool(
        all(v["exact"] for v in blobs.values())
        and all(checks.values())
        and ge05["exact_shift_partial_identity"]
        and ge05["second_directional_shift_coefficient_exact"]
    )
    report={
        "classification":(
            "GE19_H4_STAGEB_GEOMETRIC_WARD_PRIMITIVES_COMPLETE"
            if passed else
            "GE19_H4_STAGEB_GEOMETRIC_WARD_PRIMITIVES_FAIL"
        ),
        "predata_classification":
            "GE19_H4_STRUCTURAL_STAGE_B_PREDATA_ACTION_NOETHER_IDENTITY",
        "scope":"Reduced 1+1 spatial-diffeomorphism primitive and formal Ward sign audit, plus frozen GE05 per-node exact shift variation. Full H4 action/parent/source identity is not derived.",
        "analytic_audit_only":True,
        "numerical_H4_Z21_solve_performed":False,
        "observational_data_used":False,
        "frozen_action_source_blob_controls":blobs,
        "reduced_diffeomorphism_checks":checks,
        "GE05_memory_shift_variation":ge05,
        "all_subset_gates_pass":passed,
        "full_covariant_bath_transformation_verified":False,
        "Y2_zero_set_completion_verified":False,
        "mixed_H4_source_Noether_coefficient_derived":False,
        "full_H4_Noether_certificate":False,
        "Z21_window_local_particular_certified":False,
        "lensing_licensed":False,
        "next_route":(
            "DERIVE_FULL_H4_ACTION_WARD_COEFFICIENT_AND_PARENT_RESIDUAL_DICTIONARY"
            if passed else
            "RESOLVE_REDUCED_GEOMETRIC_WARD_PRIMITIVE_FAILURE"
        ),
        "claim_boundary":"A PASS of this restricted geometric subset is not a full H4 source identity PASS. Bath covariant transformation, Y2 zero-set terms, exact H4 coefficient, parent equations, and continuum-to-discrete compatibility remain open."
    }
    out=Path(args.json_out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True,allow_nan=False))
    if not passed:
        raise SystemExit(3)


if __name__=="__main__":
    main()
