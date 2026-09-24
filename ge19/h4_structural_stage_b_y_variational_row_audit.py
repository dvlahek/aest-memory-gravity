#!/usr/bin/env python3
"""GE19 structural Stage B: NL0C Y^(3/2) variational source-row coverage.

Derive second-directional and eta-tangent scalar/aether rows from the
frozen covariant Y action in the longitudinal 3+1 reduction. Check the
frozen H3/H4 explicit Y2 source assignments without altering them.

This is an analytic source-contract audit, NOT an H4 Noether certificate,
Z21 solve, physical normalization fit or retrospective relabeling.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp

ROOT=Path(__file__).resolve().parents[1]

FROZEN_BLOBS={
    "docs/nl0c_y_sector_weakly_nonlinear_result.md":
        "6fe02e60e4de34a247003c1f4ab449c159850e99",
    "docs/nl1b2_directional_second_order_eta_tangent_result.md":
        "67b580f62118773ea4a41b84f5a8cc18f2174f47",
    "ge06/analytic_aest_directional_source_generator.py":
        "a7afe0035054a9dca55d74a6497c081422114b4c",
    "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
        "e34d28a2062c748f48bc82fa928844b02631de25",
    "ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py":
        "45d203a092f9ac71cc612b15df5f0c0c630f5898",
    "docs/ge19_h4_structural_stage_a_source_row_ledger.md":
        "44d4f01a05aba26926d6a8e13a2b7aac995258d5",
    "ge19/h4_structural_stage_b_y_variational_row_predata.json":
        "bb325a7b77be1b87b8d53c9f1462db479e36903d",
}


def check_blobs():
    out={}
    for path,want in FROZEN_BLOBS.items():
        got=subprocess.check_output(
            ["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True
        ).strip()
        out[path]={"expected":want,"observed":got,"exact":bool(got==want)}
    return out


def exact_zero(expr):
    return bool(sp.simplify(expr)==0)


def analytic_y_rows():
    eps,eta=sp.symbols("eps eta",real=True)
    a,Q,lam,c=sp.symbols("a Q lam c",positive=True,real=True)
    N,L,R,b,u,pt,px=sp.symbols(
        "N L R b u pt px",real=True
    )
    du,dpt,dpx,dn,dl,dr,db=sp.symbols(
        "du dpt dpx dn dl dr db",real=True
    )
    xphi=sp.sinh(u)*(pt-b*px)/N+sp.cosh(u)*px/L
    vol=N*L*R**2
    # On each strict-sign branch, |X|^3 = sign(X)*X^3.
    lplus=-lam*c*vol*xphi**3
    lminus=+lam*c*vol*xphi**3
    perturbation={
        N:1+eps*dn,L:a+eps*dl,R:a+eps*dr,b:eps*db,
        u:eps*du,pt:Q+eps*dpt,px:eps*dpx,
    }
    background={N:1,L:a,R:a,b:0,u:0,pt:Q,px:0}
    g=Q*du+dpx/a
    check={}

    x1=sp.simplify(
        sp.diff(xphi.subs(perturbation),eps).subs(eps,0)
    )
    check["first_order_X_equals_Qdu_plus_dpx_over_a"]=exact_zero(x1-g)
    check["background_X_zero"]=exact_zero(xphi.subs(background))

    rows={}
    for branch,lag,sign in (
        ("positive_X",lplus,1),("negative_X",lminus,-1)
    ):
        eu=sp.diff(lag,u)
        # E_phi includes -partial_x dL/dphi_x. Report the spatial
        # Euler flux, never silently normalize by the 3+1 volume.
        phi_flux=-sp.diff(lag,px)
        phi_time_flux=-sp.diff(lag,pt)

        eu2=sp.simplify(sp.diff(
            eu.subs(perturbation),eps,2
        ).subs(eps,0))
        phi_flux2=sp.simplify(sp.diff(
            phi_flux.subs(perturbation),eps,2
        ).subs(eps,0))
        phi_time_flux2=sp.simplify(sp.diff(
            phi_time_flux.subs(perturbation),eps,2
        ).subs(eps,0))

        want_eu=-sign*6*lam*c*a**3*Q*g**2
        want_phi_flux=sign*6*lam*c*a**2*g**2
        check[branch+"_aether_second_directional_exact"]=exact_zero(eu2-want_eu)
        check[branch+"_scalar_spatial_flux_second_directional_exact"]=exact_zero(
            phi_flux2-want_phi_flux
        )
        check[branch+"_scalar_temporal_flux_second_directional_zero"]=exact_zero(
            phi_time_flux2
        )
        metrics={}
        for name,var in (("N",N),("L",L),("R",R),("b",b)):
            val=sp.simplify(sp.diff(
                sp.diff(lag,var).subs(perturbation),eps,2
            ).subs(eps,0))
            metrics[name]=bool(exact_zero(val))
        check[branch+"_all_metric_second_directional_zero"]=bool(all(metrics.values()))
        rows[branch]={
            "aether_second_directional_action_density":str(sp.factor(eu2)),
            "scalar_spatial_EL_flux_second_directional_action_density":
                str(sp.factor(phi_flux2)),
            "scalar_temporal_EL_flux_second_directional_action_density":
                str(sp.factor(phi_time_flux2)),
            "metric_second_directional_zero_by_row":metrics,
        }

    du10,du11,px10,px11=sp.symbols(
        "du10 du11 px10 px11",real=True
    )
    g10=Q*du10+px10/a
    g11=Q*du11+px11/a
    tangent={du:du10+eta*du11,dpx:px10+eta*px11}
    eu21_plus=sp.simplify(sp.diff(
        (-6*lam*c*a**3*Q*g**2).subs(tangent),eta
    ).subs(eta,0))
    phiflux21_plus=sp.simplify(sp.diff(
        (6*lam*c*a**2*g**2).subs(tangent),eta
    ).subs(eta,0))
    check["H4_eta_tangent_aether_positive_X_exact"]=exact_zero(
        eu21_plus+12*lam*c*a**3*Q*g10*g11
    )
    check["H4_eta_tangent_scalar_flux_positive_X_exact"]=exact_zero(
        phiflux21_plus-12*lam*c*a**2*g10*g11
    )
    check["aether_vs_scalar_spatial_flux_H3_relation"]=exact_zero(
        -6*lam*c*a**3*Q*g**2+
        a*Q*(6*lam*c*a**2*g**2)
    )
    check["aether_vs_scalar_spatial_flux_H4_relation"]=exact_zero(
        eu21_plus+a*Q*phiflux21_plus
    )

    # The invariant small-gradient coefficient is frozen in NL0C.
    beta,a0,KB=sp.symbols("beta a0 KB",positive=True,real=True)
    coeff=sp.Rational(2,3)/((1+beta)*a0)
    h3_eu=sp.factor((-6*lam*c*a**3*Q*g**2).subs(
        {lam:2-KB,c:coeff}
    ))
    h4_eu=sp.factor(eu21_plus.subs(
        {lam:2-KB,c:coeff}
    ))
    # 2-KB need not be positive for formal algebra; physical
    # frozen branch KB=0.1 gives nonzero 2-KB.
    return {
        "checks":check,
        "branches":rows,
        "first_order_gradient":"g = Q du + dpx/a",
        "H3_generic_aether_second_directional_positive_branch":str(h3_eu),
        "H3_generic_aether_second_directional_all_branches":
            "-6*lam*c*a**3*Q*Abs(g)*g",
        "H4_generic_aether_eta_tangent_all_branches":
            "-12*lam*c*a**3*Q*Abs(g10)*g11",
        "H4_generic_aether_eta_tangent_positive_branch":str(h4_eu),
        "H3_scalar_EL_spatial_flux_all_branches":
            "+6*lam*c*a**2*Abs(g)*g",
        "H4_scalar_EL_spatial_flux_all_branches":
            "+12*lam*c*a**2*Abs(g10)*g11",
        "zero_set_directional_continuation":
            "D(Abs(g)*g)[h]=2*Abs(g)*h for all real g including g=0; no delta distribution arises from the continuous flux.",
        "volume_normalization_warning":
            "These are raw reduced action-density Euler coefficients/fluxes; do not compare directly to GE19 y2_source output without independently proving its division by volume and sign conventions."
    }


def function_source(text,name):
    tree=ast.parse(text)
    matches=[n for n in tree.body
             if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))
             and n.name==name]
    if len(matches)!=1:
        raise RuntimeError(f"cannot uniquely locate frozen function {name}")
    return ast.get_source_segment(text,matches[0]) or ""


def source_coverage():
    h3=(ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py").read_text()
    h4=(ROOT/"ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py").read_text()
    ge06=(ROOT/"ge06/analytic_aest_directional_source_generator.py").read_text()
    nl0c=(ROOT/"docs/nl0c_y_sector_weakly_nonlinear_result.md").read_text()
    r3=function_source(h3,"source_real_reduced")
    r3_other=function_source(h3,"source_real")
    r4=function_source(h4,"assemble_nonmemory")
    check={
        "NL0C_action_contains_Y_three_halves":
            "Y^{3/2}" in nl0c,
        "NL0C_action_has_covariant_negative_J_sector":
            "S_{\\mathcal J}" in nl0c and "(2-K_B)\\mathcal J" in nl0c,
        "GE06_analytic_generator_explicitly_excludes_nonanalytic_Y":
            "nonanalytic Y sector is deliberately excluded" in ge06,
        "H3_reduced_Y_is_inserted_only_in_scalar_main_row3":
            (
                "rhs[3] += -2.0*y" in r3 and
                "ypiece[3]=-2.0*y" in r3 and
                "rhs[2]" not in r3 and
                "ypiece[2]" not in r3 and
                "rhscon=-qcon" in r3
            ),
        "H3_alternate_Y_is_inserted_only_in_scalar_main_row3":
            (
                "rhs[3] += -2.0*y" in r3_other and
                "ypiece[3]=-2.0*y" in r3_other and
                "rhs[2]" not in r3_other and
                "ypiece[2]" not in r3_other and
                "rhscon=-qcon" in r3_other
            ),
        "H4_DY2_is_inserted_only_in_scalar_main_row3":
            (
                "dy=dy2_real(" in r4 and
                "main[3]=-2.0*fm" in r4 and
                "con=np.zeros((2," in r4 and
                "main[2]" not in r4
            ),
        "H4_all_six_source_pieces_explicit":
            all(f'"{name}"' in function_source(h4,"build_source_config")
                for name in (
                    "2Q_GE06_cross","2Q_GE07_cross",
                    "2Q_Lambda_cross","2DY2",
                    "2M1_GE05_mapped","2M2_GE05_mapped"
                )),
    }
    return check


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()

    blobs=check_blobs()
    analysis=analytic_y_rows()
    coverage=source_coverage()
    exact=bool(
        all(v["exact"] for v in blobs.values())
        and all(analysis["checks"].values())
        and all(coverage.values())
    )
    # The null action variation at background is consistent with the
    # previously frozen linear theory. The nonzero aether H3/H4 row
    # follows at the first nonlinear physical order, not at H1.
    classified=(
        "GE19_H4_STAGEB_Y_AETHER_SOURCE_ROW_COVERAGE_GAP_CONFIRMED"
        if exact else
        "GE19_H4_STAGEB_Y_SOURCE_ROW_VARIATION_OR_BINDING_UNRESOLVED"
    )
    report={
        "classification":classified,
        "predata_classification":
            "GE19_H4_STRUCTURAL_STAGE_B_Y_SECTOR_VARIATIONAL_SOURCE_COVERAGE_PREDATA",
        "audit_scope":
            "Frozen NL0C Y^(3/2) action second directional and eta-tangent Euler source-row coverage versus explicit frozen GE19 H3/H4 Y insertions.",
        "analytic_audit_only":True,
        "frozen_blob_controls":blobs,
        "action_variational_rows":analysis,
        "frozen_explicit_source_coverage":coverage,
        "all_analytic_and_coverage_checks_pass":exact,
        "frozen_GE19_H3_H4_variational_completeness_for_Y_sector":
            "NOT_ESTABLISHED; EXPLICIT_AETHER_Y_ROW_ABSENT" if exact else "UNRESOLVED",
        "existing_certifications_relabelled":False,
        "H4_Z21_solve_performed":False,
        "full_H4_Noether_identity_derived":False,
        "Z21_window_local_particular_certified":False,
        "lensing_licensed":False,
        "routing":{
            "next_route":(
                "FREEZE_Y_SOURCE_ROW_COVERAGE_GAP_AND_DERIVE_SEPARATELY_VERSIONED_FULL_VARIATIONAL_DICTIONARY"
                if exact else
                "RESOLVE_Y_VARIATIONAL_OR_FROZEN_SOURCE_BINDING"
            ),
            "science_H4_reclosure_licensed":False,
        },
        "claim_boundary":
            "An explicit frozen GE19 source-row coverage gap relative to the chosen NL0C covariant Y action is an action-to-implementation finding; it does not show the full H4 Noether identity fails or authorize retuning historical results. The exact raw-to-GE19 normalization and parent reclosure require a separately versioned derivation."
    }
    out=Path(args.json_out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True,allow_nan=False))
    if not exact:
        raise SystemExit(3)


if __name__=="__main__":
    main()
