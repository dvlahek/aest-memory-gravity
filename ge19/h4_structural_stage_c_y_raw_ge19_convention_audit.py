#!/usr/bin/env python3
"""GE19 H4 Stage C: exact raw NL0C Y-action versus GE19 Y-source conventions.

Symbolic structural audit only. Derive raw action-density Euler
coefficients on both strict-sign branches, independently check their
relation to the physical-space GE19 y2_source, and inspect frozen
GE06/GE19 source assembly without importing computational source modules.

No source coefficient is fitted, no H3/H4 solver is run, no historical
result is relabelled. The cross-sector global action normalization
remains open unless independently established from frozen sources.
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
    "ge19/h4_structural_stage_c_predata_y_raw_ge19_conventions.json":
        "cc43754e92eef83d025475a9c5f893aa6dd81ce4",
    "docs/ge19_h4_stageb_y_aether_row_gap_valid_freeze.md":
        "7b713928f3b3d453353089fd596da4896e509fdd",
    "ge19/h4_structural_stage_b_y_variational_row_audit.py":
        "a3a0973e973f552fabb40a3dff9dd612d47ed01a",
    "docs/nl0c_y_sector_weakly_nonlinear_result.md":
        "6fe02e60e4de34a247003c1f4ab449c159850e99",
    "ge06/analytic_aest_directional_source_generator.py":
        "a7afe0035054a9dca55d74a6497c081422114b4c",
    "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
        "e34d28a2062c748f48bc82fa928844b02631de25",
    "ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py":
        "45d203a092f9ac71cc612b15df5f0c0c630f5898",
}


def frozen_blobs():
    return {
        path:{
            "expected":want,
            "observed":(got:=subprocess.check_output(
                ["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True
            ).strip()),
            "exact":bool(got==want)
        }
        for path,want in BLOBS.items()
    }


def function_source(path,name):
    source=(ROOT/path).read_text()
    tree=ast.parse(source)
    functions=[
        n for n in tree.body
        if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))
        and n.name==name
    ]
    if len(functions)!=1:
        raise RuntimeError(f"Missing or nonunique frozen function: {path}::{name}")
    return ast.get_source_segment(source,functions[0]) or ""


def exact_zero(expr):
    return bool(sp.simplify(sp.factor(expr))==0)


def action_to_physical_y_audit():
    eps,eta=sp.symbols("eps eta",real=True)
    a,Q,beta,a0,lam=sp.symbols(
        "a Q beta a0 lam",positive=True,real=True
    )
    N,L,R,b,u,pt,px=sp.symbols(
        "N L R b u pt px",real=True
    )
    dn,dl,dr,db,du,dpt,dpx=sp.symbols(
        "dn dl dr db du dpt dpx",real=True
    )
    c=sp.Rational(2,3)/((1+beta)*a0)
    kappa=sp.factor(3*lam*c)
    X=sp.sinh(u)*(pt-b*px)/N+sp.cosh(u)*px/L
    volume=N*L*R**2
    perturbation={
        N:1+eps*dn,L:a+eps*dl,R:a+eps*dr,
        b:eps*db,u:eps*du,pt:Q+eps*dpt,px:eps*dpx
    }
    g=Q*du+dpx/a
    checks={
        "frozen_kappa_equals_2lam_over_beta_a0":exact_zero(
            kappa-2*lam/((1+beta)*a0)
        ),
        "first_order_gradient_exact":exact_zero(
            sp.diff(X.subs(perturbation),eps).subs(eps,0)-g
        ),
    }
    raw={}
    for name,branch_sign in (("positive",sp.Integer(1)),("negative",sp.Integer(-1))):
        # +/- X^3 implements |X|^3 on the open strict-sign branches.
        lag=-branch_sign*lam*c*volume*X**3
        eu2=sp.simplify(sp.diff(
            sp.diff(lag,u).subs(perturbation),eps,2
        ).subs(eps,0))
        flux2=sp.simplify(sp.diff(
            (-sp.diff(lag,px)).subs(perturbation),eps,2
        ).subs(eps,0))
        want_eu=-branch_sign*6*lam*c*a**3*Q*g**2
        want_flux=branch_sign*6*lam*c*a**2*g**2
        checks[f"{name}_raw_u_second_directional"]=exact_zero(eu2-want_eu)
        checks[f"{name}_raw_scalar_flux_second_directional"]=exact_zero(
            flux2-want_flux
        )
        checks[f"{name}_aether_scalar_flux_relation"]=exact_zero(
            eu2+a*Q*flux2
        )
        raw[name]={
            "raw_aether_second_directional":str(sp.factor(eu2)),
            "raw_scalar_EL_spatial_flux_second_directional":str(
                sp.factor(flux2)
            ),
        }

    # The absolute-flux expression combines the branches. The spatial
    # derivative acts on |g|g; a,Q and c vary with time only.
    xx=sp.symbols("x",real=True)
    f=sp.Function("f")(xx)
    physical_divergence=sp.diff(f,xx)/a
    frozen_code_y=kappa*physical_divergence
    raw_scalar_EL2=2*a**2*kappa*sp.diff(f,xx)
    raw_u_EL2=-2*a**3*Q*kappa*f
    checks["raw_scalar_EL2_equals_2_a3_frozen_y2"]=exact_zero(
        raw_scalar_EL2-2*a**3*frozen_code_y
    )
    checks["raw_aether_EL2_equals_minus_2_a3_Q_kappa_flux"]=exact_zero(
        raw_u_EL2+2*a**3*Q*kappa*f
    )
    checks["raw_u_EL2_plus_aQ_scalar_flux2_zero"]=exact_zero(
        raw_u_EL2+a*Q*2*a**2*kappa*f
    )
    g10,g11=sp.symbols("g10 g11",real=True)
    # The map g -> |g|g has derivative 2|g|h for any real g,
    # with the unique continuous extension at g=0.
    f10=sp.Function("f10")(xx)
    f11=sp.Function("f11")(xx)
    # Directional flux: 2*|g10|*g11.
    gabs=sp.symbols("gabs",nonnegative=True,real=True)
    dflux=2*gabs*g11
    eta_raw_scalar=2*a**2*kappa*sp.diff(
        2*sp.Function("h")(xx),xx
    )
    eta_code_y=kappa*sp.diff(
        2*sp.Function("h")(xx),xx
    )/a
    checks["H4_eta_tangent_same_2_a3_scalar_relation"]=exact_zero(
        eta_raw_scalar-2*a**3*eta_code_y
    )
    checks["H4_eta_tangent_aether_flux_identity"]=exact_zero(
        -2*a**3*Q*kappa*dflux+
        a*Q*(2*a**2*kappa*dflux)
    )
    return {
        "checks":checks,
        "branch_primitive_rows":raw,
        "frozen_y2_physical_coefficient":str(kappa),
        "frozen_scalar_y2":"kappa/a * d_x(|g|g)",
        "raw_scalar_EL_second_directional":"2*a^3 * frozen_scalar_y2",
        "raw_aether_EL_second_directional":"-2*a^3*Q*kappa*|g|g",
        "normalized_aether_Y2_if_common_a3_convention":"-Q*kappa*|g|g",
        "H4_eta_tangent_normalized_aether_if_common_a3_convention":
            "-2*Q*kappa*|g10|*g11",
        "geometric_volume_ratio_raw_EL2_to_code_2Y2":"a^3",
        "strict_sign_branch_and_zero_set":"Real X, eps->0+; flux |g|g is C^1 and derivative 2|g|h, including at g=0.",
        "global_action_prefactor_between_NL0C_and_GE06":"NOT_DERIVED_IN_THIS_AUDIT",
    }


def code_convention_checks():
    p="ge19/repair07_window_retarded_reduced_h3_z20_particular.py"
    h3ga=function_source(p,"assemble_ga_local")
    h3main=function_source(p,"main_and_constraints")
    h3src=function_source(p,"source_real_reduced")
    h3other=function_source(p,"source_real")
    y2=function_source(p,"y2_source")
    y2red=function_source(p,"y2_source_from_reduced")
    h4=function_source(
        "ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py",
        "assemble_nonmemory"
    )
    ge06=(ROOT/"ge06/analytic_aest_directional_source_generator.py").read_text()
    checks={
        "GE06_action_explicit_volume_density":
            "grav=N*L*R**2*" in ge06 and "aest=N*L*R**2*" in ge06,
        "GE06_raw_EL_assembly_no_a3_division":
            (
                '"u":pd["u_f"]-Dt@pd["u_t"]-dx(pd["u_x"])' in h3ga
                and '"phi":-Dt@pd["phi_t"]-dx(pd["phi_x"])' in h3ga
                and "a**3" not in h3ga and "/bg[" not in h3ga
            ),
        "GE19_raw_row_stack_no_a3_division":
            (
                "ga[\"u\"],ga[\"phi\"]" in h3main
                and "np.stack" in h3main
                and "a**3" not in h3main
            ),
        "GE19_y2_physical_divergence_over_a":
            (
                "div=np.fft.ifft(" in y2 and
                ".real/a[:,None]" in y2 and
                "return (2.0*(2.0-KB)/((1.0+beta)*A0_MPC_INV))*div" in y2
            ),
        "GE19_y2_reduced_physical_divergence_over_a":
            (
                "div=spectral_dx(flux,kfund)/a" in y2red
                and "return (2.0*(2.0-KB)/((1.0+beta)*A0_MPC_INV))*div" in y2red
            ),
        "H3_reduced_scalar_Y_rhs_no_a3_conversion":
            (
                "rhs=-qmain" in h3src and
                "rhs[3] += -2.0*y" in h3src and
                "rhs[2]" not in h3src
            ),
        "H3_alternate_scalar_Y_rhs_no_a3_conversion":
            (
                "rhs=-qmain" in h3other and
                "rhs[3] += -2.0*y" in h3other and
                "rhs[2]" not in h3other
            ),
        "H4_scalar_DY_rhs_no_a3_conversion":
            (
                "main[3]=-2.0*fm" in h4 and
                "main[2]" not in h4 and
                "con=np.zeros((2," in h4
            ),
    }
    return checks


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--json-out",required=True)
    args=parser.parse_args()
    blobs=frozen_blobs()
    symbolic=action_to_physical_y_audit()
    source=code_convention_checks()
    passed=bool(
        all(v["exact"] for v in blobs.values())
        and all(symbolic["checks"].values())
        and all(source.values())
    )
    classification=(
        "GE19_H4_STAGEC_RAW_Y_VOLUME_FACTOR_ESTABLISHED_GLOBAL_NORMALIZATION_OPEN"
        if passed else
        "GE19_H4_STAGEC_ACTION_TO_GE19_MAPPING_UNRESOLVED"
    )
    report={
        "classification":classification,
        "predata_classification":
            "GE19_H4_STRUCTURAL_STAGE_C_PREDATA_Y_ACTION_DENSITY_TO_GE19_SOURCE_CONVENTION",
        "analytic_scope_only":True,
        "frozen_blob_controls":blobs,
        "symbolic_action_to_physical_source":symbolic,
        "frozen_GE19_implementation_conventions":source,
        "all_subset_gates_pass":passed,
        "global_action_prefactor_independently_proven":False,
        "complete_Y_source_dictionary_licensed":False,
        "H3_H4_numerical_solver_performed":False,
        "previous_science_results_relabelled":False,
        "Z21_window_local_particular_certified":False,
        "lensing_licensed":False,
        "next_route":(
            "DERIVE_GLOBAL_ACTION_NORMALIZATION_AND_VERSION_COMPLETE_Y_SOURCE_ROWS"
            if passed else
            "RESOLVE_FROZEN_ACTION_OR_SOURCE_CONVENTION_BINDING"
        ),
        "claim_boundary":"The a^3 ratio is exact for the action-density source versus existing physical y2_source. Do not directly patch H3/H4 until the global NL0C-to-GE06 action prefactor and complete Y aether/scalar row signs are independently fixed."
    }
    p=Path(args.json_out)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True,allow_nan=False))
    if not passed:
        raise SystemExit(3)


if __name__=="__main__":
    main()
