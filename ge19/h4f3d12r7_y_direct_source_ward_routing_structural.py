#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

PREDATA = ROOT / "ge19/h4f3d12r7_predata_y_direct_source_ward_routing.json"
RESULT = ROOT / "results/ge19_h4f3d12r7_y_direct_source_ward_routing_structural.json"

LOCKED_HEAD = "3e27c996cfa8d0ba59de726408a9879fb6b5b9f9"

D12R6R1 = ROOT / "ge19/h4f3d12r6r1_artifact_only_y_modulus_status_lock.json"
D9 = ROOT / "ge19/h4f3d9_predata_original_fd4_fd8_structural_error_budget.json"
FULL_WARD = ROOT / "ge19/h4f3d_predata_actual_operator_all_parent_ward_closure.json"

STAGEE = ROOT / "ge19/h4_stagee_versioned_y_source_rows.py"
LEDGER = ROOT / "ge19/h4f2g_action_completed_six_piece_source_ledger.py"
BRIDGE = ROOT / "ge19/h4f2h_physical_time_source_ward_bridge.py"


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
    ).strip()


def function_node(source: str, name: str) -> ast.FunctionDef:
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise RuntimeError(f"function not found: {name}")


def is_np_zeros_call(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "zeros"
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "np"
    )


def has_zero_initializer(fn: ast.FunctionDef, varname: str) -> bool:
    for node in ast.walk(fn):
        if not isinstance(node, ast.Assign):
            continue
        if not is_np_zeros_call(node.value):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == varname:
                return True
    return False


def const_subscript_index(node: ast.Subscript):
    sl = node.slice
    if isinstance(sl, ast.Constant) and isinstance(sl.value, int):
        return int(sl.value)
    return None


def assigned_indices(fn: ast.FunctionDef, varname: str):
    out = []
    for node in ast.walk(fn):
        targets = []
        if isinstance(node, ast.Assign):
            targets = list(node.targets)
        elif isinstance(node, ast.AugAssign):
            targets = [node.target]
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]

        for target in targets:
            if (
                isinstance(target, ast.Subscript)
                and isinstance(target.value, ast.Name)
                and target.value.id == varname
            ):
                idx = const_subscript_index(target)
                if idx is None:
                    raise RuntimeError(
                        f"nonconstant {varname} subscript write in frozen source"
                    )
                out.append(idx)
    return sorted(set(out))


def referenced_indices(fn: ast.FunctionDef, varname: str):
    out = []
    for node in ast.walk(fn):
        if (
            isinstance(node, ast.Subscript)
            and isinstance(node.value, ast.Name)
            and node.value.id == varname
        ):
            idx = const_subscript_index(node)
            if idx is not None:
                out.append(idx)
    return sorted(set(out))


def require(condition: bool, message: str):
    if not condition:
        raise RuntimeError(message)


def main():
    pre = json.loads(PREDATA.read_text())

    require(
        pre["classification"]
        == "GE19_H4F3D12R7_PREDATA_Y_DIRECT_SOURCE_WARD_ROUTING",
        "wrong D12R7 predata classification",
    )

    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")

    require(head == LOCKED_HEAD, f"HEAD moved: {head}")
    require(
        branch == "physics-first-gravitational-elasticity",
        f"wrong branch: {branch}",
    )

    blob_report = {}
    for path, expected in pre["frozen_git_blobs"].items():
        observed = git("rev-parse", f"{LOCKED_HEAD}:{path}")
        blob_report[path] = {
            "expected": expected,
            "observed": observed,
            "exact": observed == expected,
        }
        require(
            observed == expected,
            f"frozen blob mismatch: {path}: {observed}",
        )

    # ------------------------------------------------------------------
    # 1. Static proof of corrected Stage-E Y row support.
    # ------------------------------------------------------------------
    stagee_source = STAGEE.read_text()
    rhs_fn = function_node(stagee_source, "_rhs")

    require(
        has_zero_initializer(rhs_fn, "main"),
        "Stage-E main is not initialized as an exact zero array",
    )
    require(
        has_zero_initializer(rhs_fn, "constraints"),
        "Stage-E constraints are not initialized as an exact zero array",
    )

    stagee_main_written = assigned_indices(rhs_fn, "main")
    stagee_constraint_written = assigned_indices(rhs_fn, "constraints")

    require(
        stagee_main_written == [2, 3],
        f"unexpected Stage-E main support: {stagee_main_written}",
    )
    require(
        stagee_constraint_written == [],
        f"unexpected Stage-E constraint writes: {stagee_constraint_written}",
    )

    # ------------------------------------------------------------------
    # 2. Independently verify the frozen six-piece ledger support.
    # ------------------------------------------------------------------
    from ge19 import h4f2g_action_completed_six_piece_source_ledger as ledger
    from ge19 import h4f2h_physical_time_source_ward_bridge as bridge

    require(
        tuple(ledger.GE19_ROWS)
        == (
            "N",
            "L_plus_R",
            "u",
            "phi",
            "T",
            "rho",
            "b",
            "L_minus_R_over2",
        ),
        "GE19 row ordering changed",
    )

    require(
        ledger.Y_PIECE == "2DY2_action_complete_Y_u_and_phi",
        "registered Y source-family name changed",
    )

    ledger_y_support = tuple(ledger.SUPPORT[ledger.Y_PIECE])

    require(
        ledger_y_support == (2, 3),
        f"Y ledger support changed: {ledger_y_support}",
    )

    require(
        bridge.SCHEMES[ledger.Y_PIECE] == "fd8",
        "Y source is no longer on the registered FD8 source scheme",
    )

    # ------------------------------------------------------------------
    # 3. Static proof of the rows used by the physical source Ward.
    # ------------------------------------------------------------------
    bridge_source = BRIDGE.read_text()
    ward_fn = function_node(bridge_source, "physical_source_ward")
    physical_ward_rows = referenced_indices(ward_fn, "f")

    require(
        physical_ward_rows == [1, 6, 7],
        f"physical source-Ward row support changed: {physical_ward_rows}",
    )

    support_disjoint = set(ledger_y_support).isdisjoint(physical_ward_rows)
    require(
        support_disjoint,
        "Y direct source support now overlaps physical source-Ward rows",
    )

    # ------------------------------------------------------------------
    # 4. Algebraic consequence plus a non-science synthetic sanity check.
    #
    # This is NOT the proof. The proof is the frozen exact row-support
    # disjointness above. This catches an implementation mismatch in the
    # production Ward helper.
    # ------------------------------------------------------------------
    nt = 9
    nm = 41
    x = np.linspace(-0.04, 0.04, nt)
    a = np.exp(x)
    H = np.ones(nt)
    rows = np.zeros((8, nt, nm), dtype=complex)

    rng = np.random.default_rng(1207)
    rows[2] = (
        rng.normal(size=(nt, nm))
        + 1j * rng.normal(size=(nt, nm))
    )
    rows[3] = (
        rng.normal(size=(nt, nm))
        + 1j * rng.normal(size=(nt, nm))
    )

    synthetic_y_source_ward = bridge.physical_source_ward(
        rows,
        x,
        a,
        H,
        0.031,
        "fd8",
    )

    synthetic_max_abs = float(np.max(np.abs(synthetic_y_source_ward)))

    require(
        synthetic_max_abs == 0.0,
        f"synthetic Y direct source Ward is nonzero: {synthetic_max_abs}",
    )

    # ------------------------------------------------------------------
    # 5. D9 routing: direct-source Y term closes exactly, parent Y stays.
    # ------------------------------------------------------------------
    d9 = json.loads(D9.read_text())
    require(
        d9["classification"]
        == "GE19_H4F3D9_PREDATA_ORIGINAL_FD4_FD8_STENCIL_CONSTANTS_AND_FULL_WARD_ERROR_BUDGET_PROTOCOL",
        "wrong D9 contract",
    )

    budget = d9["registered_physical_budget_protocol"]
    six_source_contract = budget["six_source"]
    nonbath_parent_contract = budget["nonbath_parent"]

    require(
        "GE06,GE07,Lambda,Y" in six_source_contract
        and "M9(S_shift_p" in six_source_contract,
        "D9 six-source M9 routing changed",
    )

    require(
        "GE06/GE07/Lambda/Y action coefficients" in nonbath_parent_contract,
        "D9 no longer explicitly retains Y in nonbath-parent budget",
    )

    require(
        "missing Euler or boundary term is STOP" in nonbath_parent_contract,
        "D9 parent STOP rule changed",
    )

    # ------------------------------------------------------------------
    # 6. Full-Ward contract must still require parent Euler/boundary terms.
    # ------------------------------------------------------------------
    full = json.loads(FULL_WARD.read_text())
    require(
        full["classification"]
        == "GE19_H4F3D_PREDATA_OPERATOR_PLUS_ALL_PARENT_WARD_ON_ACTUAL_SIX_SOURCE",
        "wrong full-Ward predata contract",
    )

    analytic_terms = "\n".join(full["analytic_terms_required"])

    require(
        "Signed actual six-piece source Ward" in analytic_terms,
        "full-Ward source route disappeared",
    )
    require(
        "Explicit signed Euler residuals" in analytic_terms,
        "full-Ward parent Euler route disappeared",
    )
    require(
        full["stop"]["no_source_Ward_zero_gate"] is True,
        "source-only Ward zero-gate prohibition changed",
    )

    # ------------------------------------------------------------------
    # 7. Preserve D12R6R1 boundary. Its modulus is not promoted here.
    # ------------------------------------------------------------------
    r6r1 = json.loads(D12R6R1.read_text())

    require(
        r6r1["classification"]
        == "GE19_H4F3D12R6R1_Y_MODULUS_REPRESENTATION_LEVEL_LOCK_PASS_PHYSICAL_FD8_BOUND_OPEN",
        "wrong D12R6R1 parent classification",
    )

    require(
        r6r1["status"]["Y_flux_representation_Lipschitz_candidate_frozen"]
        is True,
        "D12R6R1 candidate not frozen",
    )

    require(
        r6r1["status"]["Y_zero_set_lower_regularity_modulus_for_D9_certified"]
        is False,
        "D12R6R1 status unexpectedly promoted",
    )

    y_lipschitz_candidate = float(
        r6r1["representation_level_bounds"]["Y_flux_Lipschitz_candidate"]
    )

    # ------------------------------------------------------------------
    # Result.
    # ------------------------------------------------------------------
    result = {
        "classification":
            "GE19_H4F3D12R7_Y_DIRECT_SOURCE_WARD_ROUTING_PASS_PARENT_BUDGET_OPEN",

        "execution": {
            "HEAD": head,
            "branch": branch,
            "science_arrays_read": False,
            "full_Ward_residual_read": False,
            "registered_hotspot_full_Ward_defect_read": False
        },

        "frozen_blob_gates": blob_report,

        "structural_Y_source_support": {
            "StageE_main_zero_initialized": True,
            "StageE_constraint_zero_initialized": True,
            "StageE_main_written_rows": stagee_main_written,
            "StageE_constraint_written_rows": stagee_constraint_written,
            "ledger_Y_support": list(ledger_y_support),
            "direct_Y_equation_rows": ["u", "phi"],
            "S_iso_Y_exactly_zero": True,
            "S_shift_b_Y_exactly_zero": True,
            "S_anisotropy_Y_exactly_zero": True
        },

        "physical_source_Ward": {
            "formula":
                "H*D_x(S_b) + i*k*a/3*(S_iso + 2*S_aniso)",
            "row_indices_used": physical_ward_rows,
            "Y_support_disjoint_from_Ward_rows": support_disjoint,
            "Y_registered_source_scheme": bridge.SCHEMES[ledger.Y_PIECE],
            "W_six_source_Y_identically_zero": True,
            "synthetic_helper_sanity_max_abs": synthetic_max_abs
        },

        "D9_direct_source_consequence": {
            "M9_S_shift_Y_required_numerically": False,
            "M9_S_shift_Y_exact_value": 0.0,
            "Y_direct_source_FD8_truncation_budget_exactly_zero": True,
            "reason":
                "The frozen corrected Y source has S_shift,Y identically zero, so both the exact derivative and every linear FD8 derivative of that row are identically zero."
        },

        "Y_parent_routing": {
            "Y_removed_from_entire_full_Ward": False,
            "D9_nonbath_parent_route_explicitly_contains_Y": True,
            "route":
                "Independent nonbath-parent Euler/current differentiation budget using the original GE06/GE07/Lambda/Y action coefficients, signed lower-boundary product, spatial Fourier derivative, and original parent state/current representations.",
            "direct_H4_Y_equation_support": ["u", "phi"],
            "exact_Y_resolved_parent_term_decomposition_certified": False,
            "Y_parent_discretization_budget_certified": False,
            "physical_parent_uncertainty_closed": False
        },

        "D12R6R1_preserved": {
            "representation_Y_flux_Lipschitz_candidate":
                y_lipschitz_candidate,
            "candidate_promoted_to_direct_source_FD8_bound": False,
            "candidate_may_be_used_as_parent_input_without_new_proof": False
        },

        "status": {
            "Y_direct_source_Ward_structurally_closed": True,
            "Y_direct_source_D9_M9_term_closed_exactly": True,
            "Y_nonbath_parent_route_identified": True,
            "Y_nonbath_parent_budget_complete": False,
            "all_nonY_M5_M9_envelopes_certified": False,
            "nonbath_parent_and_lower_boundary_discretization_budget_certified": False,
            "operation_level_roundoff_propagation_bound_certified": False,

            "B_total_defined": False,
            "candidate_full_Ward_residual_read": False,
            "registered_hotspot_full_Ward_defect_read": False,
            "full_Ward_execution_licensed": False,
            "full_original_H4_Ward_certified": False,

            "H4_Z21_solve_performed": False,
            "Z21_certified": False,
            "lensing_licensed": False
        },

        "next_route":
            "D12R8_EXACT_Y_RESOLVED_NONBATH_PARENT_EULER_CURRENT_DECOMPOSITION_AND_ERROR_BUDGET"
    }

    RESULT.parent.mkdir(parents=True, exist_ok=True)
    tmp = RESULT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    tmp.replace(RESULT)

    print(result["classification"])
    print("STAGEE_Y_SUPPORT =", list(ledger_y_support))
    print("PHYSICAL_SOURCE_WARD_ROWS =", physical_ward_rows)
    print("SUPPORT_DISJOINT =", support_disjoint)
    print("W_SIX_SOURCE_Y_IDENTICALLY_ZERO = True")
    print("D9_Y_DIRECT_SOURCE_M9_TERM = 0")
    print("Y_PARENT_ROUTE_REMAINS_OPEN = True")
    print("B_TOTAL_DEFINED = False")
    print("FULL_WARD_EXECUTION_LICENSED = False")
    print("Z21_CERTIFIED = False")
    print("LENSING_LICENSED = False")
    print(
        "NEXT = "
        "D12R8_EXACT_Y_RESOLVED_NONBATH_PARENT_EULER_CURRENT_DECOMPOSITION_AND_ERROR_BUDGET"
    )


if __name__ == "__main__":
    main()
