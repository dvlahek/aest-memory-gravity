#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np

from ge19 import h4f3d9_exact_original_fd4_fd8_stencil_budget_compiler as d9

ROOT = Path(__file__).resolve().parents[1]
PRE = ROOT / "ge19/h4f3d12r3_predata_full_ward_numerical_budget_prelock.json"

EXPECTED_PRE_CLASS = (
    "GE19_H4F3D12R3_PREDATA_FULL_WARD_NUMERICAL_BUDGET_PRELOCK"
)

def require(v, msg):
    if not v:
        raise RuntimeError(msg)

def sha256(path):
    path = Path(path)
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def git_blob(rel):
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD:" + rel],
        cwd=ROOT,
        text=True,
    ).strip()

def load_json(path):
    return json.loads(Path(path).read_text())

def verify_predata(pre):
    require(pre["classification"] == EXPECTED_PRE_CLASS,
            "D12R3 preregistration classification changed")

    require(
        subprocess.check_output(
            ["git", "branch", "--show-current"], cwd=ROOT, text=True
        ).strip() == "physics-first-gravitational-elasticity",
        "wrong branch",
    )

    dirty = subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=ROOT, text=True
    ).strip()
    require(not dirty, "working tree must be clean for D12R3 execution")

    blob_report = {}
    for name, item in pre["frozen_git_blobs"].items():
        got = git_blob(item["path"])
        blob_report[name] = {
            "path": item["path"],
            "expected": item["blob"],
            "observed": got,
            "exact": got == item["blob"],
        }
    require(all(x["exact"] for x in blob_report.values()),
            "D12R3 frozen Git dependency changed")

    artifact_report = {}
    for name, item in pre["frozen_artifacts"].items():
        p = ROOT / item["path"]
        require(p.is_file(), f"missing frozen artifact: {p}")
        got = sha256(p)
        artifact_report[name] = {
            "path": item["path"],
            "expected": item["sha256"],
            "observed": got,
            "exact": got == item["sha256"],
        }
    require(all(x["exact"] for x in artifact_report.values()),
            "D12R3 frozen physical artifact changed")

    return blob_report, artifact_report

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", required=True)
    args = ap.parse_args()

    pre = load_json(PRE)
    blobs, artifacts = verify_predata(pre)

    paths = {
        k: ROOT / v["path"]
        for k, v in pre["frozen_artifacts"].items()
    }

    h4 = load_json(paths["H4F3B_json"])
    d1j = load_json(paths["D1_json"])
    d4j = load_json(paths["D4_json"])
    d10 = load_json(paths["D10R1_json"])
    d12 = load_json(paths["D12R2_json"])
    d55 = load_json(paths["D55CR11F_json"])

    require(
        h4.get("classification") ==
        "GE19_H4F3B_ACTUAL_CORRECTED_SIX_SOURCE_PASS_FULL_WARD_OPEN",
        "corrected H4F3B source certificate missing",
    )
    require(h4.get("gates") and all(v is True for v in h4["gates"].values()),
            "H4F3B source gate not fully PASS")

    require(
        d1j.get("classification") ==
        "GE19_H4F3D1_CANONICAL_OPERATOR_WARD_COMPILER_PASS",
        "D1 canonical operator compiler not PASS",
    )
    require(
        d4j.get("classification") ==
        "GE19_H4F3D4_FULL_FORMAL_ETA_WARD_LEDGER_PASS_ACTUAL_GRID_OPEN",
        "D4 formal Ward ledger not PASS",
    )
    require(
        d10.get("classification") ==
        "GE19_H4F3D10R1_LOSSLESS_ARCHIVE_KNOWN_NONBATH_DIAGNOSTIC_PASS_FULL_OPEN",
        "D10R1 lossless parent/boundary archive not PASS",
    )
    require(
        d12.get("classification") ==
        "GE19_H4F3D12R2_EXACT_BACKGROUND_ONSHELL_ELIMINATION_PASS_F21_INDEPENDENT",
        "D12R2 background closure not PASS",
    )
    require(
        d12.get("arbitrary_unknown_state_elimination", {}).get(
            "E00_times_dchi_F21_exact_zero_without_F21"
        ) is True,
        "D12R2 F21-independent E00 elimination missing",
    )
    require(
        d12.get("arbitrary_unknown_state_elimination", {}).get(
            "L21_EL00_minus_b21_Eb00_exact_zero_without_L21_b21"
        ) is True,
        "D12R2 L21/b21 background boundary elimination missing",
    )

    require(
        d55.get("classification") ==
        "GE19_D55CR11F_CONTINUUM_BATH_AND_GE05_ONSHELL_CLOSURE_PASS_H4_OPEN",
        "D55CR11F continuum bath closure not PASS",
    )
    for key in (
        "continuous_X10_certified",
        "continuum_bath_quadrature_certified",
        "GE05_bath_onshell_certified",
    ):
        require(d55.get(key) is True, f"D55CR11F missing {key}=true")

    # Reproduce the ORIGINAL D9 source-derived stencil constants.
    locks, _, _ = d9.source_lock()
    require(all(v["exact"] for v in locks.values()),
            "D9 original stencil source lock changed")

    fd4 = d9.exact_stencil(d9.fd4_original_rows(), 4)
    fd8 = d9.exact_stencil(d9.fd8_original_rows(), 8)

    k4 = float(fd4["max_Taylor_remainder_factor_float_report_only"])
    k8 = float(fd8["max_Taylor_remainder_factor_float_report_only"])

    with np.load(paths["H4F3B_npz"], allow_pickle=False) as z:
        x128 = np.asarray(z["x_primary"], float)
        x64 = np.asarray(z["x_control"], float)

    require(x128.shape == (128,), "H4F3B primary grid changed")
    require(x64.shape == (64,), "H4F3B control grid changed")

    h128 = float((x128[-1] - x128[0]) / 127.0)
    h64 = float((x64[-1] - x64[0]) / 63.0)

    require(np.allclose(np.diff(x128), h128, rtol=1e-9, atol=1e-13),
            "Nt128 grid not uniform")
    require(np.allclose(np.diff(x64), h64, rtol=1e-9, atol=1e-13),
            "Nt64 grid not uniform")

    stencil_prefactors = {
        "Nt128": {
            "h": h128,
            "h4_K4_max": h128**4 * k4,
            "h8_K8_max": h128**8 * k8,
        },
        "Nt64": {
            "h": h64,
            "h4_K4_max": h64**4 * k4,
            "h8_K8_max": h64**8 * k8,
        },
        "interpretation":
            "Multiply only by independently certified physical M5/M9 "
            "suprema. These prefactors are not themselves a Ward tolerance."
    }

    inherited = {
        "formal_Ward_D4_PASS": True,
        "corrected_H4F3B_six_source_PASS": True,
        "canonical_operator_D1_PASS": True,
        "D10R1_lossless_known_parent_boundary_PASS": True,
        "D12R2_background_unknown_state_elimination_PASS": True,
        "D55_continuous_X10_PASS": True,
        "D55_continuum_bath_quadrature_PASS": True,
        "D55_GE05_bath_onshell_PASS": True,
        "D9_exact_FD4_FD8_stencil_constants_reproduced": True,
    }

    # These are intentionally NOT inferred from any observed combined Ward.
    open_obligations = {
        "physical_operator_and_source_M5_M9_envelopes_certified": False,
        "Y_zero_set_lower_regularity_modulus_for_FD8_certified": False,
        "nonbath_parent_and_lower_boundary_discretization_budget_certified": False,
        "operation_level_roundoff_propagation_bound_certified": False,
    }

    report = {
        "classification":
            "GE19_H4F3D12R3_NUMERICAL_BUDGET_ROUTE_PRELOCK_PASS_FULL_BUDGET_OPEN",
        "preregistration": EXPECTED_PRE_CLASS,
        "execution_HEAD": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "frozen_git_dependency_audit": blobs,
        "frozen_artifact_audit": artifacts,
        "inherited_certified_closures": inherited,
        "original_D9_FD4": fd4,
        "original_D9_FD8": fd8,
        "physical_grid_stencil_prefactors": stencil_prefactors,
        "remaining_budget_obligations": open_obligations,
        "D55_supersedes_old_first_order_bath_open_status": True,
        "D12R2_supersedes_old_background_F21_open_status": True,
        "candidate_full_Ward_residual_read": False,
        "registered_hotspot_full_Ward_defect_read": False,
        "B_total_defined": False,
        "full_physical_FD4_FD8_structural_budget_complete": False,
        "full_Ward_execution_licensed": False,
        "full_original_H4_Ward_certified": False,
        "H4_Z21_solve_performed": False,
        "Z21_certified": False,
        "lensing_licensed": False,
        "threshold_changed": False,
        "source_coefficients_changed": False,
        "observational_tuning": False,
        "next_route":
            "CERTIFY_PHYSICAL_M5_M9_PLUS_Y_ZEROSET_MODULUS_PLUS_"
            "NONBATH_PARENT_BOUNDARY_BUDGET_PLUS_ROUNDOFF_THEN_FREEZE_B_TOTAL",
        "claim_boundary":
            "Pre-residual numerical-budget route freeze only. Exact original "
            "FD4/FD8 stencil constants and all already-certified corrected "
            "physics parents are bound before any integrated Ward residual "
            "is evaluated. Background F21/L21/b21 and first-order GE05 bath "
            "are no longer blockers. The full physical structural tolerance "
            "is still open until independent derivative, Y-zero-set, "
            "nonbath-parent/boundary and floating-point bounds are frozen."
    }

    out = Path(args.json_out).resolve()
    if out.exists():
        raise RuntimeError("D12R3 output exists; no overwrite")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    print(json.dumps(report, indent=2, sort_keys=True))
    print("GE19_H4F3D12R3_NUMERICAL_BUDGET_PRELOCK_PASS")

if __name__ == "__main__":
    main()
