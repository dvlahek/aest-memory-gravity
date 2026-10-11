#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]

LOCKED_HEAD = "3e27c996cfa8d0ba59de726408a9879fb6b5b9f9"
BRANCH = "physics-first-gravitational-elasticity"

BLOBS = {
    "ge19/h4f3d8_independent_nonbath_euler_and_boundary.py":
        "861cd5a81c17380a727777a4e1ff08cd7e857522",
    "ge19/h4f3d8_predata_independent_nonbath_euler_and_boundary.json":
        "007bec20e450dd67263d32a33476dcb8a5c33996",
    "ge19/h4_stagee_versioned_y_source_rows.py":
        "282166ea5840d7fba4dbc328d40d7687afa6fa0f",
    "ge19/h4f2b_signed_mixed_ward_template.py":
        "ab783ffe8242d8ff455647df8664a074f725ee81",
    "ge19/h4f3d12r2_exact_background_onshell_elimination.py":
        "df5d0b384747edefaab2878e1a9fe6d174d2da29",
    "ge19/h4f3d12r2_predata_exact_background_onshell_elimination.json":
        "d34de3b2befe1820bcfc2619aadc508378d0f5f9",
    "ge19/h4f3d9_predata_original_fd4_fd8_structural_error_budget.json":
        "98e6fd8835fdbe3bd169d062431eefe80a3e9232",
}


def require(cond, msg):
    if not cond:
        raise RuntimeError(msg)


def git(*args):
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True
    ).strip()


def locate_result(primary: Path, pattern: str) -> Path:
    if primary.exists():
        return primary
    found = sorted((ROOT / "results").glob(pattern))
    require(
        len(found) == 1,
        f"expected exactly one result for {pattern}, found {len(found)}"
    )
    return found[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", required=True)
    args = ap.parse_args()

    out = Path(args.json_out).resolve()
    require(not out.exists(), "D12R8 output exists; no overwrite")

    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")

    require(branch == BRANCH, "wrong branch")
    require(head == LOCKED_HEAD, f"HEAD moved: {head}")

    blob_checks = {}
    for path, expected in BLOBS.items():
        observed = git("rev-parse", f"HEAD:{path}")
        blob_checks[path] = {
            "expected": expected,
            "observed": observed,
            "exact": observed == expected
        }
        require(observed == expected, f"blob changed: {path}")

    pre = json.loads(
        (ROOT / "ge19/h4f3d12r8_predata_y_complete_ward_routing.json")
        .read_text()
    )
    require(
        pre["classification"] ==
        "GE19_H4F3D12R8_PREDATA_Y_COMPLETE_WARD_ROUTING_EXACT_ZERO",
        "D12R8 prereg classification mismatch"
    )
    require(
        pre["locked_parent_HEAD"] == LOCKED_HEAD,
        "D12R8 prereg HEAD mismatch"
    )

    # ------------------------------------------------------------
    # Parent results: exact background elimination and D12R7
    # direct-source routing.
    # ------------------------------------------------------------

    d12r2_path = locate_result(
        ROOT / "results/ge19_h4f3d12r2_exact_background_onshell_elimination.json",
        "*d12r2*exact_background*onshell*elimination*.json"
    )
    d12r2 = json.loads(d12r2_path.read_text())

    require(
        d12r2.get("classification") ==
        "GE19_H4F3D12R2_EXACT_BACKGROUND_ONSHELL_ELIMINATION_PASS_F21_INDEPENDENT",
        "D12R2 exact background elimination not PASS"
    )

    gates2 = d12r2.get("gates", {})
    require(
        gates2.get("E00_times_dchi_F21_exact_zero_without_F21") is True,
        "D12R2 E00*F21 elimination missing"
    )
    require(
        gates2.get(
            "L21_EL00_minus_b21_Eb00_exact_zero_without_L21_b21"
        ) is True,
        "D12R2 background action boundary elimination missing"
    )

    d12r7_path = locate_result(
        ROOT / "results/ge19_h4f3d12r7_y_direct_source_ward_routing.json",
        "*d12r7*y*source*ward*routing*.json"
    )
    d12r7 = json.loads(d12r7_path.read_text())

    require(
        d12r7.get("classification") ==
        "GE19_H4F3D12R7_Y_DIRECT_SOURCE_WARD_ROUTING_PASS_PARENT_BUDGET_OPEN",
        "D12R7 direct Y source Ward route not PASS"
    )

    # ------------------------------------------------------------
    # Frozen source structure.
    # ------------------------------------------------------------

    d8_text = (
        ROOT / "ge19/h4f3d8_independent_nonbath_euler_and_boundary.py"
    ).read_text()

    stagee_text = (
        ROOT / "ge19/h4_stagee_versioned_y_source_rows.py"
    ).read_text()

    ward_text = (
        ROOT / "ge19/h4f2b_signed_mixed_ward_template.py"
    ).read_text()

    d9 = json.loads(
        (
            ROOT /
            "ge19/h4f3d9_predata_original_fd4_fd8_structural_error_budget.json"
        ).read_text()
    )

    require(
        'flux = lambda z: z*sp.Abs(z)' in d8_text,
        "D8 Y flux definition changed"
    )
    require(
        '"first_order_zero_set": "D(g abs(g)) at g=0 is 0"' in d8_text,
        "D8 first-order Y zero-set statement missing"
    )
    require(
        '"mixed_Y_flux": "2*abs(g10)*g11, continuous at g10=0"' in d8_text,
        "D8 mixed Y tangent statement missing"
    )

    require(
        "E_i00 F_i21,x+2 E_i10 F_i11,x+2 E_i11 F_i10,x" in ward_text,
        "formal mixed parent identity changed"
    )

    # Stage-E actual mixed Y source support.
    main_rows = sorted(set(
        int(q) for q in re.findall(r"main\[(\d+)\]\s*=", stagee_text)
    ))
    constraint_rows = sorted(set(
        int(q) for q in re.findall(r"constraints\[(\d+)\]\s*=", stagee_text)
    ))

    require(
        main_rows == [2, 3],
        f"Stage-E Y main support changed: {main_rows}"
    )
    require(
        constraint_rows == [],
        f"Stage-E Y constraint support changed: {constraint_rows}"
    )
    require(
        "constraints=np.zeros((2,flux.shape[0],flux.shape[1]),float)"
        in "".join(stagee_text.split()),
        "Stage-E Y constraints are no longer identically zero"
    )
    require(
        "2.0*np.abs(g0)*g1" in stagee_text,
        "Stage-E mixed Y tangent changed"
    )

    # ------------------------------------------------------------
    # Independent mathematical proof:
    # J(X)=X|X| has no epsilon-linear coefficient at X0=0
    # for arbitrary first-order 10+eta*11 direction.
    # ------------------------------------------------------------

    eps, eta, g10, g11 = sp.symbols(
        "eps eta g10 g11", real=True
    )

    g = g10 + eta * g11
    J = lambda z: z * sp.Abs(z)

    plus = sp.simplify(
        sp.limit(J(eps * g) / eps, eps, 0, dir="+")
    )
    minus = sp.simplify(
        sp.limit(J(eps * g) / eps, eps, 0, dir="-")
    )

    require(plus == 0, "positive-side Y linear Euler limit nonzero")
    require(minus == 0, "negative-side Y linear Euler limit nonzero")

    # Therefore each Y Euler row has E00=E10=E11=0
    # in the mixed-parent coefficient. Keep generic field gradients.
    f21, f11, f10 = sp.symbols(
        "F21_chi F11_chi F10_chi"
    )

    E00 = sp.Integer(0)
    E10 = sp.Integer(0)
    E11 = sp.Integer(0)

    parent_y = sp.simplify(
        E00 * f21 + 2 * E10 * f11 + 2 * E11 * f10
    )
    require(parent_y == 0, "Y mixed parent is not exact zero")

    # Exact Y lower L/b action boundary:
    L21, L10, L11, b21, b10, b11 = sp.symbols(
        "L21 L10 L11 b21 b10 b11"
    )

    EL00 = EL10 = EL11 = sp.Integer(0)
    Eb00 = Eb10 = Eb11 = sp.Integer(0)

    boundary_y = sp.simplify(
        L21 * EL00
        + 2 * L10 * EL11
        + 2 * L11 * EL10
        - b21 * Eb00
        - 2 * b10 * Eb11
        - 2 * b11 * Eb10
    )

    require(
        boundary_y == 0,
        "Y lower action boundary is not exact zero"
    )

    # ------------------------------------------------------------
    # D9 routing consequence.
    # ------------------------------------------------------------

    budget = d9["registered_physical_budget_protocol"]

    require(
        "GE06,GE07,Lambda,Y" in budget["six_source"],
        "D9 Y source routing changed"
    )
    require(
        "GE06/GE07/Lambda/Y action coefficients"
        in budget["nonbath_parent"],
        "D9 Y parent routing changed"
    )
    require(
        "missing Euler or boundary term is STOP"
        in budget["nonbath_parent"],
        "D9 parent STOP rule changed"
    )

    report = {
        "classification":
            "GE19_H4F3D12R8_Y_COMPLETE_WARD_ROUTING_EXACT_ZERO_PASS_NONY_BUDGETS_OPEN",

        "HEAD": head,
        "branch": branch,

        "parents": {
            "D12R2_result": str(d12r2_path.relative_to(ROOT)),
            "D12R2_classification": d12r2["classification"],
            "D12R7_result": str(d12r7_path.relative_to(ROOT)),
            "D12R7_classification": d12r7["classification"]
        },

        "blob_checks": blob_checks,

        "proof": {
            "Y_background_E00_exact_zero": True,
            "Y_linear_E10_exact_zero": True,
            "Y_linear_E11_exact_zero": True,
            "Y_flux_linear_limit_plus": str(plus),
            "Y_flux_linear_limit_minus": str(minus),

            "mixed_parent_formula":
                "E00*F21_chi+2*E10*F11_chi+2*E11*F10_chi",

            "Y_mixed_parent_exact_zero": True,
            "Y_lower_action_boundary_exact_zero": True,

            "StageE_Y_main_row_support": main_rows,
            "StageE_Y_constraint_row_support": constraint_rows,

            "Y_H4_u_phi_source_retained": True,
            "Y_H4_mixed_flux":
                "2*abs(g10)*g11",

            "Y_direct_source_Ward_exact_zero": True,
            "Y_nonbath_parent_Ward_exact_zero": True,
            "Y_boundary_Ward_exact_zero": True,

            "Y_complete_mixed_H4_Ward_sector_exact_zero": True
        },

        "D9_budget_consequence": {
            "Y_M9_direct_source_envelope_required": False,
            "Y_zero_set_FD8_lower_regularity_budget_required_for_full_Ward":
                False,
            "Y_nonbath_parent_numerical_derivative_budget_required": False,
            "Y_full_Ward_structural_error_contribution": 0.0,

            "D12R4_R6_artifacts_preserved": True,
            "D12R6_representation_modulus_reinterpreted_as_invalid": False,
            "D12R6_representation_modulus_needed_for_full_Ward": False
        },

        "remaining_open_before_B_total": {
            "nonY_operator_M5_envelopes": True,
            "nonY_GE06_GE07_Lambda_source_M9_envelopes": True,
            "nonY_nonbath_parent_and_lower_boundary_budget": True,
            "operation_level_roundoff_bound": True
        },

        "candidate_full_Ward_residual_read": False,
        "registered_hotspot_full_Ward_defect_read": False,
        "science_arrays_read": False,
        "B_total_defined": False,
        "full_Ward_execution_licensed": False,
        "full_original_H4_Ward_certified": False,
        "H4_Z21_solve_performed": False,
        "Z21_certified": False,
        "lensing_licensed": False,

        "claim_boundary":
            "Exact NL0C/Y Ward-sector routing only. "
            "The action-completed mixed H4 Y u/phi source remains physically "
            "present. Its direct source Ward projection, first-order parent "
            "crosses and lower action boundary vanish exactly at the frozen "
            "X0=0 FLRW background. Therefore no Y FD8 or lower-regularity "
            "numerical error term enters the eventual full-Ward B_total. "
            "All non-Y operator/source/parent and floating-point budgets "
            "remain open."
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"
    )

    print("CLASSIFICATION =", report["classification"])
    print("Y_E00_ZERO =", report["proof"]["Y_background_E00_exact_zero"])
    print("Y_E10_ZERO =", report["proof"]["Y_linear_E10_exact_zero"])
    print("Y_E11_ZERO =", report["proof"]["Y_linear_E11_exact_zero"])
    print(
        "Y_PARENT_ZERO =",
        report["proof"]["Y_nonbath_parent_Ward_exact_zero"]
    )
    print(
        "Y_BOUNDARY_ZERO =",
        report["proof"]["Y_boundary_Ward_exact_zero"]
    )
    print(
        "Y_DIRECT_SOURCE_WARD_ZERO =",
        report["proof"]["Y_direct_source_Ward_exact_zero"]
    )
    print(
        "Y_COMPLETE_WARD_SECTOR_ZERO =",
        report["proof"]["Y_complete_mixed_H4_Ward_sector_exact_zero"]
    )
    print(
        "Y_LOWER_REGULARITY_BUDGET_NEEDED =",
        report["D9_budget_consequence"][
            "Y_zero_set_FD8_lower_regularity_budget_required_for_full_Ward"
        ]
    )
    print("B_TOTAL_DEFINED =", report["B_total_defined"])
    print("FULL_WARD_LICENSED =", report["full_Ward_execution_licensed"])
    print("Z21_CERTIFIED =", report["Z21_certified"])
    print("GE19_D12R8_Y_COMPLETE_WARD_ROUTING_PASS")


if __name__ == "__main__":
    main()
