#!/usr/bin/env python3
"""GE19 H4F3d8: independent restricted nonbath Euler/boundary compiler.

This is an analytic source-bound derivative and sign compiler. It does NOT
import historical module-level generators, evaluate original physical
parents, establish an FD4/FD8 error budget, or claim full H4 Noether/Z21.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
PREDATA = ROOT / "ge19/h4f3d8_predata_independent_nonbath_euler_and_boundary.json"
PRE_BLOB = "007bec20e450dd67263d32a33476dcb8a5c33996"
PATHS = {
    "GE06_action": "ge06/analytic_aest_directional_source_generator.py",
    "GE07_action": "ge07/pressureless_matter_directional_source_generator.py",
    "Lambda_source": "ge19/repair14_self_consistent_reduced_h3_z20_particular.py",
    "NL0C_Y_source": "ge19/h4_stagee_versioned_y_source_rows.py",
    "H4F3d1_operator": "ge19/h4f3d1_frozen_canonical_operator_ward.py",
    "H4F3d2_dust_bath_currents": "ge19/h4f3d2_dust_bath_parent_euler_currents.py",
    "H4F3d4_complete_formal_ledger": "ge19/h4f3d4_complete_eta_regularized_mixed_ward_ledger.py",
    "H4F3d4_predata": "ge19/h4f3d4_predata_complete_eta_regularized_mixed_ward_ledger.json",
    "H4F3d7_original_interval_ODE_diagnostic":
        "ge19/h4f3d7_bath_fd4_vs_original_r1_interval_ode.py",
    "H4F3d_actual_full_predata":
        "ge19/h4f3d_predata_actual_operator_all_parent_ward_closure.json",
}
NONBATH = ("N", "L", "R", "b", "u", "phi", "T", "rho")


def zero(expr):
    return bool(sp.expand(sp.cancel(expr.doit())) == 0)


def git_blob(path, worktree=False):
    cmd = ["git", "hash-object", str(ROOT / path)] if worktree else [
        "git", "rev-parse", "HEAD:" + path
    ]
    return subprocess.check_output(cmd, cwd=ROOT, text=True).strip()


def source_lock():
    pred = json.loads(PREDATA.read_text())
    registered = pred["frozen_git_blobs"]
    if (pred["classification"] !=
            "GE19_H4F3D8_PREDATA_INDEPENDENT_NONBATH_EULER_AND_LOWER_BOUNDARY_COMPILER"):
        raise RuntimeError("H4F3d8 preregistration changed")
    if set(registered) != set(PATHS):
        raise RuntimeError("H4F3d8 preregistered source set changed")
    observations = {
        "predata": {
            "expected": PRE_BLOB,
            "head": git_blob(PREDATA.relative_to(ROOT).as_posix()),
            "worktree": git_blob(PREDATA.relative_to(ROOT).as_posix(), True),
        }
    }
    for label, rel in PATHS.items():
        observations[label] = {
            "file": rel,
            "expected": registered[label],
            "head": git_blob(rel),
            "worktree": git_blob(rel, True),
        }
    for item in observations.values():
        item["exact"] = (
            item["expected"] == item["head"] == item["worktree"]
        )
    return observations


def frozen_action_binding():
    # Read only: importing GE06/GE07 would execute historical result writers.
    ge06 = (ROOT / PATHS["GE06_action"]).read_text()
    ge07 = (ROOT / PATHS["GE07_action"]).read_text()
    lam = (ROOT / PATHS["Lambda_source"]).read_text()
    y = (ROOT / PATHS["NL0C_Y_source"]).read_text()
    d1 = (ROOT / PATHS["H4F3d1_operator"]).read_text()
    compact = lambda v: "".join(v.split())
    a = compact(ge06)
    d = compact(ge07)
    expected_jet = {
        "N": ("N_f", "N_x"),
        "L": ("L_f", "L_t", "L_x"),
        "R": ("R_f", "R_t", "R_x"),
        "b": ("b_f", "b_x"),
        "u": ("u_f", "u_t", "u_x"),
        "phi": ("phi_t", "phi_x"),
    }
    jet = all(
        ('"' + key + '":sp.diff(lag,' + var + ')') in a
        for key, var in (
            ("N_f", "N"), ("N_x", "Nx"),
            ("L_f", "L"), ("L_t", "Lt"), ("L_x", "Lx"),
            ("R_f", "R"), ("R_t", "Rt"), ("R_x", "Rx"),
            ("b_f", "b"), ("b_x", "bx"),
            ("u_f", "u"), ("u_t", "ut"), ("u_x", "ux"),
            ("phi_t", "pt"), ("phi_x", "px"),
        )
    )
    return {
        "GE06_exact_action_jet_partials_present": jet,
        "GE06_original_gravity_and_AeST_action_present":
            "lag=sp.expand(grav+aest)" in a
            and "grav=N*L*R**2*" in a
            and "aest=N*L*R**2*" in a,
        "GE07_frozen_action_present":
            "lag=sp.expand(N*L*R**2*varrho*(W**2-V**2-1))" in d,
        "Lambda_frozen_action_normalization_present":
            "L_lambda=-6rho_lambdaNLR^2" in compact(lam),
        "Y_original_real_flux_and_direction_present":
            "np.abs(g)*g" in y
            and "2.0*np.abs(g0)*g1" in y
            and "constraints=np.zeros((2,flux.shape[0],flux.shape[1]),float)" in y,
        "canonical_operator_keeps_complete_Cmat_product":
            "H*D4_x(C14 w)" in d1
            and "operator_ward_from_frozen_Cmat" in d1,
        "GE06_exact_jet_dictionary": expected_jet,
        "historical_module_imported": False,
    }


def independently_derive_mixed_parent():
    eps, eta = sp.symbols("eps eta", real=True)
    tests = {}
    definitions = {}
    for field in NONBATH:
        e00, e10, e11, e20, e21 = sp.symbols(
            "E_" + field + "_00 E_" + field + "_10 E_" + field +
            "_11 E_" + field + "_20 E_" + field + "_21"
        )
        f10, f11, f20, f21 = sp.symbols(
            "F_" + field + "_10_chi F_" + field + "_11_chi F_" +
            field + "_20_chi F_" + field + "_21_chi"
        )
        euler = (e00 + eps * (e10 + eta * e11)
                 + eps**2 * (e20 + eta * e21) / 2)
        gradient = (eps * (f10 + eta * f11)
                    + eps**2 * (f20 + eta * f21) / 2)
        actual = sp.diff(sp.diff(euler * gradient, eps, 2),
                         eta).subs({eps: 0, eta: 0})
        expected = e00 * f21 + 2 * e10 * f11 + 2 * e11 * f10
        tests[field + "_independent_mixed_parent_exact"] = zero(actual - expected)
        tests[field + "_background_E00_kept"] = zero(
            sp.diff(actual, e00) - f21)
        tests[field + "_both_cross_factors_2_kept"] = (
            zero(sp.diff(actual, e10) - 2 * f11)
            and zero(sp.diff(actual, e11) - 2 * f10))
        tests[field + "_no_direct_20_Euler_or_field_product"] = (
            zero(sp.diff(actual, e20))
            and zero(sp.diff(actual, f20))
            and zero(sp.diff(actual, e21)))
        tests[field + "_omitted_cross_negative_controls"] = (
            not zero(actual - (e00 * f21 + 2 * e10 * f11))
            and not zero(actual - (e00 * f21 + 2 * e11 * f10)))
        definitions[field] = "E00*F21_chi+2*E10*F11_chi+2*E11*F10_chi"
    return tests, definitions


def independently_derive_boundary():
    chi, eps, eta, a = sp.symbols("chi eps eta a", real=True)
    def f(name):
        return sp.Function(name)(chi)
    l10, l11, l20, l21 = (f("L" + i) for i in ("10", "11", "20", "21"))
    b10, b11, b20, b21 = (f("b" + i) for i in ("10", "11", "20", "21"))
    el00, el10, el11, el20, el21 = (
        f("EL" + i) for i in ("00", "10", "11", "20", "21"))
    eb00, eb10, eb11, eb20, eb21 = (
        f("Eb" + i) for i in ("00", "10", "11", "20", "21"))
    l = a + eps * (l10 + eta * l11) + eps**2 * (l20 + eta * l21)/2
    b = eps * (b10 + eta * b11) + eps**2 * (b20 + eta * b21)/2
    el = el00 + eps * (el10 + eta * el11) + eps**2 * (el20 + eta * el21)/2
    eb = eb00 + eps * (eb10 + eta * eb11) + eps**2 * (eb20 + eta * eb21)/2
    mixed = sp.diff(sp.diff(l * el - b * eb, eps, 2),
                    eta).subs({eps: 0, eta: 0}).doit()
    lower = (l21 * el00 + 2*l10*el11 + 2*l11*el10
             - b21*eb00 - 2*b10*eb11 - 2*b11*eb10)
    expected = a*el21 + lower
    return {
        "full_original_action_L_EL_minus_b_Eb_coefficient":zero(mixed-expected),
        "original_lower_boundary_spatial_derivative_exact":
            zero(sp.diff(mixed, chi)-sp.diff(a*el21+lower, chi)),
        "lower_boundary_keeps_both_independent_E00_products":
            bool(lower.has(el00) and lower.has(eb00)),
        "negative_control_wrong_shift_sign":
            not zero(mixed-(a*el21 + lower
                            + 2*(b21*eb00+2*b10*eb11+2*b11*eb10))),
        "negative_control_missing_first_L_cross":
            not zero(mixed-(expected-2*l10*el11)),
        "negative_control_missing_second_L_cross":
            not zero(mixed-(expected-2*l11*el10)),
        "negative_control_missing_first_shift_cross":
            not zero(mixed-(expected+2*b10*eb11)),
        "negative_control_missing_second_shift_cross":
            not zero(mixed-(expected+2*b11*eb10)),
    }, {
        "full_boundary": "a*EL21+L21*EL00+2L10*EL11+2L11*EL10"
                         "-b21*Eb00-2b10*Eb11-2b11*Eb10",
        "lower_boundary": "L21*EL00+2L10*EL11+2L11*EL10"
                          "-b21*Eb00-2b10*Eb11-2b11*Eb10",
        "nonbath_Ward_boundary_sign": "-partial_chi(lower_boundary)",
        "spatial_coordinate": "chi; xi=ln(a) is physical time grid, not chi",
    }


def independently_derive_dust():
    n,l,r,b,rho,tt,tx = sp.symbols(
        "N L R b rho Tt Tx", real=True, positive=True)
    w = (tt-b*tx)/n
    v = tx/l
    lag = n*l*r**2*rho*(w**2-v**2-1)
    jt = sp.diff(lag,tt)
    jx = sp.diff(lag,tx)
    erho = sp.diff(lag,rho)
    el = sp.diff(lag,l)
    eb = sp.diff(lag,b)
    eps = sp.symbols("eps",real=True)
    a,rho0 = sp.symbols("a rho0",positive=True,real=True)
    dn,dl,dr,db,drho,dtt,dtx = sp.symbols(
        "dN dL dR db drho dTt dTx",real=True)
    background = {
        n: 1+eps*dn, l: a+eps*dl, r: a+eps*dr,
        b: eps*db, rho: rho0+eps*drho,
        tt: 1+eps*dtt, tx: eps*dtx,
    }
    first = lambda expr: sp.diff(expr.subs(background, simultaneous=True),
                                  eps).subs(eps,0)
    return {
        "exact_frozen_GE07_T_time_current":
            zero(jt-2*l*r**2*rho*w),
        "exact_frozen_GE07_T_space_current":
            zero(jx+2*l*r**2*rho*b*w+2*n*r**2*rho*tx/l),
        "exact_frozen_GE07_rho_Euler":
            zero(erho-n*l*r**2*(w**2-v**2-1)),
        "GE07_E_rho10_has_NO_rho0_multiplier":
            zero(first(erho)-2*a**3*(dtt-dn)),
        "GE07_E_rho10_independent_of_rho0":
            zero(sp.diff(first(erho),rho0)),
        "GE07_E_L10_signed":
            zero(first(el)-2*a**2*rho0*(dtt-dn)),
        "GE07_E_b10_signed":
            zero(first(eb)+2*a**3*rho0*dtx),
        "GE07_T_current_time_first_signed":
            zero(first(jt)-2*a**3*rho0*(
                dl/a+2*dr/a+drho/rho0+dtt-dn)),
        "GE07_T_current_space_first_signed":
            zero(first(jx)+2*a**3*rho0*db+2*a*rho0*dtx),
    }, {
        "GE07_T_Euler": "-partial_t(J_T_time)-partial_chi(J_T_space)",
        "GE07_rho_Euler": "NLR^2*(W^2-V^2-1)",
        "GE07_E_rho10": "2 a^3 (delta Tt-delta N), no rho0 multiplier",
    }


def independently_derive_lambda():
    n,l,r,rl = sp.symbols("N L R rho_lambda",real=True)
    lag = -6*rl*n*l*r**2
    eps = sp.symbols("eps",real=True)
    a,dn,dl,dr = sp.symbols("a dN dL dR",real=True)
    first = lambda expr: sp.diff(expr.subs(
        {n:1+eps*dn,l:a+eps*dl,r:a+eps*dr},simultaneous=True),
        eps).subs(eps,0)
    en,el,er = (sp.diff(lag,v) for v in (n,l,r))
    return {
        "Lambda_action_exact_metric_lapse_Euler":
            zero(en+6*rl*l*r**2),
        "Lambda_action_exact_metric_L_Euler":
            zero(el+6*rl*n*r**2),
        "Lambda_action_exact_metric_R_Euler":
            zero(er+12*rl*n*l*r),
        "Lambda_first_lapse_Euler":
            zero(first(en)+6*rl*a**2*(dl+2*dr)),
        "Lambda_first_longitudinal_Euler":
            zero(first(el)+6*rl*(a**2*dn+2*a*dr)),
        "Lambda_first_transverse_Euler":
            zero(first(er)+12*rl*(a**2*dn+a*(dl+dr))),
        "Lambda_no_shift_or_other_derivative_current":
            zero(sp.diff(lag,sp.Symbol("b")))
            and zero(sp.diff(lag,sp.Symbol("L_t")))
            and zero(sp.diff(lag,sp.Symbol("phi"))),
    }, {"Lambda_action": "-6*rho_lambda*N*L*R^2",
        "Lambda_nonmetric_Euler": "0",
        "Lambda_spatial_or_temporal_currents": "0"}


def independent_Y_zero_set():
    eps,g,h = sp.symbols("eps g h",real=True)
    flux = lambda z: z*sp.Abs(z)
    test = [sp.limit(flux(eps*g)/eps,eps,0,dir=side)
            for side in ("+","-")]
    return {
        "NL0C_Y_first_order_zero_gradient_one_sided_plus":zero(test[0]),
        "NL0C_Y_first_order_zero_gradient_one_sided_minus":zero(test[1]),
        "NL0C_Y_flux_eta_tangent_at_nonzero_gradient":
            all(zero((sp.diff(flux(g+eps*h),eps).subs(eps,0)
                      -2*sp.Abs(g)*h).subs(g,g0))
                for g0 in (sp.Rational(2,3),-sp.Rational(2,3))),
        "NL0C_Y_global_C9_smoothness_not_assumed":True,
    }, {
        "mixed_Y_flux": "2*abs(g10)*g11, continuous at g10=0",
        "first_order_zero_set": "D(g abs(g)) at g=0 is 0",
        "FD8_global_9th_derivative_bound": "NOT ASSUMED; requires independent regularity bound"
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--json-out",required=True)
    args=parser.parse_args()
    locks=source_lock()
    bindings=frozen_action_binding()
    parents,parent_dictionary=independently_derive_mixed_parent()
    boundary,boundary_dictionary=independently_derive_boundary()
    dust,dust_dictionary=independently_derive_dust()
    lam,lam_dictionary=independently_derive_lambda()
    y,ydictionary=independent_Y_zero_set()
    maps=(parents,boundary,dust,lam,y)
    passed=bool(
        all(v["exact"] for v in locks.values())
        and all(v for k,v in bindings.items()
                if k not in ("GE06_exact_jet_dictionary","historical_module_imported"))
        and bindings["historical_module_imported"] is False
        and all(all(v is True for v in m.values()) for m in maps)
        and len(parent_dictionary)==len(NONBATH)
    )
    report={
        "classification":(
            "GE19_H4F3D8_RESTRICTED_NONBATH_EULER_BOUNDARY_COMPILER_PASS_ACTUAL_OPEN"
            if passed else
            "GE19_H4F3D8_RESTRICTED_NONBATH_EULER_BOUNDARY_COMPILER_FAIL"),
        "preregistration":
            "GE19_H4F3D8_PREDATA_INDEPENDENT_NONBATH_EULER_AND_LOWER_BOUNDARY_COMPILER",
        "git_source_blobs":locks,
        "source_bound_action_jet_dictionary":bindings,
        "independently_derived_eight_field_parent":parents,
        "eight_field_parent_dictionary":parent_dictionary,
        "independently_derived_lower_action_boundary":boundary,
        "lower_boundary_dictionary":boundary_dictionary,
        "GE07_dust_action_Euler_current_gates":dust,
        "GE07_dust_dictionary":dust_dictionary,
        "Lambda_action_Euler_gates":lam,
        "Lambda_dictionary":lam_dictionary,
        "NL0C_Y_zero_set_gates":y,
        "NL0C_Y_regularization_dictionary":ydictionary,
        "all_restricted_compiler_gates_pass":passed,
        "GE06_full_action_first_order_actual_Euler_arrays_derived":False,
        "all_physical_nonbath_parent_arrays_evaluated":False,
        "original_actual_H4F3b_NPZ_loaded":False,
        "FD4_FD8_physical_structural_error_budget_frozen":False,
        "full_actual_H4_Noether_structural_PASS":False,
        "H4_Z21_solve_performed":False,
        "Z21_certified":False,
        "lensing_licensed":False,
        "claim_boundary":"Independent RESTRICTED symbolic nonbath Ward parent, action lower boundary, source-bound GE06 jet dictionary, exact GE07 dust and Lambda Euler derivatives, Y zero-set regularity. No actual-grid GE06/Y parent residuals, complete all-sector structural error budget or physical H4 Noether claim.",
    }
    out=Path(args.json_out).resolve()
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True,allow_nan=False))
    if not passed:
        raise SystemExit(3)


if __name__=="__main__":
    main()
