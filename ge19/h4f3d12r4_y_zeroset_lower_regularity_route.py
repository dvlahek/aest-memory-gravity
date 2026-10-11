#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np

from ge19 import h4f3b_actual_corrected_six_piece_source as h4b
from ge19 import h4_stagee_versioned_y_source_rows as stagee
from ge19 import repair37_cancellation_safe_fd8_h4_z21_reclosure as old

ROOT = Path(__file__).resolve().parents[1]

PRE = ROOT / (
    "ge19/"
    "h4f3d12r4_predata_y_zeroset_lower_regularity_route.json"
)

PRE_CLASS = (
    "GE19_H4F3D12R4_PREDATA_Y_ZEROSET_LOWER_REGULARITY_ROUTE"
)

TINY = 1e-300


def require(cond, msg):
    if not cond:
        raise RuntimeError(msg)


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob(path):
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD:" + path],
        cwd=ROOT,
        text=True,
    ).strip()


def rel(a, b):
    aa = np.asarray(a)
    bb = np.asarray(b)
    return float(
        np.linalg.norm(aa - bb) /
        max(np.linalg.norm(aa), np.linalg.norm(bb), TINY)
    )


def verify_predata(pre):
    require(
        pre.get("classification") == PRE_CLASS,
        "D12R4 preregistration classification changed",
    )

    branch = subprocess.check_output(
        ["git", "branch", "--show-current"],
        cwd=ROOT,
        text=True,
    ).strip()

    require(
        branch == "physics-first-gravitational-elasticity",
        "wrong branch",
    )

    anc = subprocess.run(
        [
            "git", "merge-base", "--is-ancestor",
            pre["parent_HEAD"], "HEAD",
        ],
        cwd=ROOT,
    )
    require(
        anc.returncode == 0,
        "D12R4 prereg parent is not ancestor of execution HEAD",
    )

    blob_audit = {}
    for name, item in pre["frozen_git_blobs"].items():
        observed = git_blob(item["path"])
        blob_audit[name] = {
            "path": item["path"],
            "expected": item["blob"],
            "observed": observed,
            "exact": observed == item["blob"],
        }

    require(
        all(v["exact"] for v in blob_audit.values()),
        "D12R4 frozen Git dependency changed",
    )

    artifact_audit = {}
    for name, item in pre["frozen_artifacts"].items():
        path = ROOT / item["path"]
        require(path.is_file(), f"missing D12R4 artifact: {path}")
        observed = sha256(path)
        artifact_audit[name] = {
            "path": item["path"],
            "expected": item["sha256"],
            "observed": observed,
            "exact": observed == item["sha256"],
        }

    require(
        all(v["exact"] for v in artifact_audit.values()),
        "D12R4 frozen artifact changed",
    )

    d12r3 = json.loads(
        (
            ROOT /
            pre["frozen_artifacts"]["D12R3_result"]["path"]
        ).read_text()
    )

    require(
        d12r3.get("classification") ==
        "GE19_H4F3D12R3_NUMERICAL_BUDGET_ROUTE_PRELOCK_PASS_FULL_BUDGET_OPEN",
        "D12R3 prelock not PASS",
    )

    require(
        d12r3["inherited_certified_closures"][
            "D55_continuous_X10_PASS"
        ] is True,
        "continuous X10 certificate missing",
    )

    require(
        d12r3.get("candidate_full_Ward_residual_read") is False,
        "D12R3 unexpectedly read full Ward residual",
    )

    return blob_audit, artifact_audit


def exact_sign_change_mask(g):
    a = np.asarray(g[:-1], float)
    b = np.asarray(g[1:], float)

    return ((a < 0.0) & (b > 0.0)) | (
        (a > 0.0) & (b < 0.0)
    )


def audit_case(bg, h1, dh1, z11, dz11):
    nt = len(bg["x"])

    first_real, _, first_space = old.r7.reduced_state_real(
        bg,
        h1,
        h4b.SOURCE_NX_Y,
        dh1,
    )

    tangent_real, _, tangent_space = old.r7.reduced_state_real(
        bg,
        z11,
        h4b.SOURCE_NX_Y,
        dz11,
    )

    kfund = float(
        old.r7.g9.K_REQ[0] /
        old.r7.FOURIER_N[0]
    )

    by_beta = []

    for beta in old.r7.BETAS:
        out = stagee.source_h4(
            bg["a"],
            bg["Q_action"],
            first_real["u20"],
            first_space["phi20"],
            tangent_real["u20"],
            tangent_space["phi20"],
            old.r7.KB,
            old.r7.A0_MPC_INV,
            float(beta),
            kfund,
        )

        by_beta.append(
            (
                float(beta),
                np.asarray(out["gradient10"], float),
                np.asarray(out["gradient11"], float),
            )
        )

    g0 = by_beta[0][1]
    g1 = by_beta[0][2]

    require(
        g0.shape == g1.shape,
        "Y g10/g11 real-space shape mismatch",
    )

    require(
        g0.shape[0] == nt,
        "Y gradient time grid mismatch",
    )

    beta_g0_exact = all(
        np.array_equal(g0, q[1])
        for q in by_beta[1:]
    )

    beta_g1_exact = all(
        np.array_equal(g1, q[2])
        for q in by_beta[1:]
    )

    require(
        beta_g0_exact and beta_g1_exact,
        "Y gradient unexpectedly depends on beta",
    )

    # Independent mode-space X10/X11 construction.
    X10 = np.asarray(
        old.r24.first_order_X_modes(
            old.r7,
            bg,
            h1,
        ),
        complex,
    )

    X11 = np.asarray(
        old.r24.first_order_X_modes(
            old.r7,
            bg,
            z11,
        ),
        complex,
    )

    nx = g0.shape[1]
    modes = np.asarray(old.r7.FOURIER_N, int)

    fg0 = np.fft.fft(g0, axis=-1) / nx
    fg1 = np.fft.fft(g1, axis=-1) / nx

    g0_modes = fg0[:, modes].T
    g1_modes = fg1[:, modes].T

    x10_rel = rel(g0_modes, X10)
    x11_rel = rel(g1_modes, X11)

    require(
        x10_rel <= 1e-12,
        f"Stage-E g10 does not reproduce X10 modes: {x10_rel}",
    )

    require(
        x11_rel <= 1e-12,
        f"Stage-E g11 does not reproduce tangent X11 modes: {x11_rel}",
    )

    crossing = exact_sign_change_mask(g0)
    exact_zero = g0 == 0.0

    cross_idx = np.argwhere(crossing)
    zero_idx = np.argwhere(exact_zero)

    witnesses = []

    for row in cross_idx[:20]:
        i = int(row[0])
        j = int(row[1])

        witnesses.append({
            "kind": "strict_sign_change",
            "time_left_index": i,
            "time_right_index": i + 1,
            "space_index": j,
            "x_left": float(bg["x"][i]),
            "x_right": float(bg["x"][i + 1]),
            "g10_left": float(g0[i, j]),
            "g10_right": float(g0[i + 1, j]),
            "g11_left_report_only": float(g1[i, j]),
            "g11_right_report_only": float(g1[i + 1, j]),
        })

    for row in zero_idx[:max(0, 20 - len(witnesses))]:
        i = int(row[0])
        j = int(row[1])

        witnesses.append({
            "kind": "exact_node_zero",
            "time_index": i,
            "space_index": j,
            "x": float(bg["x"][i]),
            "g10": 0.0,
            "g11_report_only": float(g1[i, j]),
        })

    return {
        "Nt": nt,
        "realspace_nx": int(nx),
        "beta_gradient_invariance_exact":
            bool(beta_g0_exact and beta_g1_exact),
        "StageE_g10_vs_independent_X10_modes_relative_L2":
            x10_rel,
        "StageE_g11_vs_independent_X11_modes_relative_L2":
            x11_rel,
        "strict_time_sign_change_count":
            int(len(cross_idx)),
        "exact_zero_node_count":
            int(len(zero_idx)),
        "min_abs_g10_grid_report_only":
            float(np.min(np.abs(g0))),
        "max_abs_g10_grid_report_only":
            float(np.max(np.abs(g0))),
        "max_abs_g11_grid_report_only":
            float(np.max(np.abs(g1))),
        "witnesses_first_20":
            witnesses,
    }


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument(
        "--results-dir",
        required=True,
    )

    ap.add_argument(
        "--repair26-trace",
        required=True,
    )

    ap.add_argument(
        "--json-out",
        required=True,
    )

    args = ap.parse_args()

    out = Path(args.json_out).resolve()

    if out.exists():
        raise RuntimeError(
            "D12R4 output exists; no overwrite"
        )

    pre = json.loads(PRE.read_text())

    blobs, artifacts = verify_predata(pre)

    rd = Path(args.results_dir).resolve()
    trace = Path(args.repair26_trace).resolve()

    code_lock = h4b.code_lock()
    files, parent_hashes = h4b.frozen_inputs(
        rd,
        trace,
    )

    require(
        all(x["exact"] for x in code_lock.values()),
        "H4F3B code lock changed",
    )

    require(
        all(
            x["exact"]
            for k, x in parent_hashes.items()
            if k != "Repair26_R1_trace"
        ),
        "H4F3B corrected parent hash changed",
    )

    cases = []

    total_crossings = 0
    total_exact_zeros = 0

    with (
        np.load(files["r13"], allow_pickle=False) as r13,
        np.load(files["h3fn"], allow_pickle=False) as h3f,
        np.load(files["z11"], allow_pickle=False) as z11,
    ):
        bgs, _, _, _, _, _, _, _, _ = old.build_context(
            rd,
            r13,
        )

        for nt, label in (
            (128, "primary"),
            (64, "control"),
        ):
            for tag in old.r7.C_TAGS:
                bg = bgs[(nt, tag)]

                x = np.asarray(
                    h3f["x_" + label],
                    float,
                )

                require(
                    np.array_equal(
                        x,
                        np.asarray(bg["x"], float),
                    ),
                    "H3F/background clock mismatch",
                )

                require(
                    np.array_equal(
                        x,
                        np.asarray(
                            z11["x_" + label],
                            float,
                        ),
                    ),
                    "Z11/background clock mismatch",
                )

                h1 = np.asarray(
                    h3f[f"{tag}_H1_{label}"],
                    complex,
                )

                dh1 = np.asarray(
                    h3f[f"{tag}_H1dot_{label}"],
                    complex,
                )

                tangent = np.asarray(
                    z11[f"{tag}_Z11_{label}"],
                    complex,
                )

                tangent_dot = np.asarray(
                    z11[f"{tag}_Z11dot_{label}"],
                    complex,
                )

                audit = audit_case(
                    bg,
                    h1,
                    dh1,
                    tangent,
                    tangent_dot,
                )

                audit["C"] = tag
                audit["grid_label"] = label

                total_crossings += (
                    audit[
                        "strict_time_sign_change_count"
                    ]
                )

                total_exact_zeros += (
                    audit[
                        "exact_zero_node_count"
                    ]
                )

                cases.append(audit)

    require(
        len(cases) == 6,
        "expected six unique C x Nt Y-gradient cases",
    )

    all_mode_bind = all(
        q[
            "StageE_g10_vs_independent_X10_modes_relative_L2"
        ] <= 1e-12
        and
        q[
            "StageE_g11_vs_independent_X11_modes_relative_L2"
        ] <= 1e-12
        for q in cases
    )

    all_beta_invariant = all(
        q["beta_gradient_invariance_exact"]
        for q in cases
    )

    zero_witness = bool(
        total_crossings > 0 or
        total_exact_zeros > 0
    )

    if zero_witness:
        classification = (
            "GE19_H4F3D12R4_Y_ZEROSET_ROUTE_PASS_"
            "LOWER_REGULARITY_REQUIRED"
        )

        next_route = (
            "CERTIFY_STENCILWISE_M0_M1_L0_L1_FOR_Y_"
            "LOWER_REGULARITY_MODULUS_THEN_COMBINE_WITH_"
            "NON_Y_M5_M9_PARENT_BOUNDARY_AND_ROUNDOFF"
        )
    else:
        classification = (
            "GE19_H4F3D12R4_Y_ZEROSET_ROUTE_PASS_"
            "NO_DISCRETE_WITNESS_CONTINUUM_SEPARATION_OPEN"
        )

        next_route = (
            "CERTIFY_CONTINUUM_G10_SEPARATION_FROM_ZERO_OR_"
            "FALL_BACK_TO_LOWER_REGULARITY_MODULUS"
        )

    report = {
        "classification": classification,
        "preregistration": PRE_CLASS,
        "execution_HEAD": subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            text=True,
        ).strip(),

        "frozen_git_dependency_audit":
            blobs,

        "frozen_artifact_audit":
            artifacts,

        "H4F3B_code_lock":
            code_lock,

        "H4F3B_parent_hashes":
            parent_hashes,

        "analytic_result": {
            "H4_Y_flux":
                "F_Y=2*abs(g10)*g11",

            "generic_global_C9_not_available_across_"
            "unresolved_g10_zero_set":
                True,

            "safe_lower_regularity_modulus":
                "|F_Y(t)-F_Y(s)| <= "
                "2*(M1*L0+M0*L1)*|t-s|",

            "modulus_constants_not_yet_certified":
                True,

            "strict_sign_change_plus_continuous_X10_"
            "implies_continuum_zero":
                True,

            "simple_zero_with_nonzero_g11_generic_"
            "counterexample":
                "g10=A*(t-t0), g11=B gives "
                "F_Y=2*abs(A)*B*|t-t0|, "
                "whose left/right first derivatives differ "
                "for A*B != 0."
        },

        "unique_C_Nt_cases":
            cases,

        "unique_C_Nt_case_count":
            len(cases),

        "physical_beta_cohort_count":
            len(cases) * len(old.r7.BETAS),

        "all_18_beta_C_Nt_cohorts_covered":
            len(cases) * len(old.r7.BETAS) == 18,

        "all_beta_gradient_invariance_exact":
            all_beta_invariant,

        "all_StageE_gradients_bound_to_"
        "independent_mode_X10_X11":
            all_mode_bind,

        "strict_sign_change_count_total":
            int(total_crossings),

        "exact_zero_node_count_total":
            int(total_exact_zeros),

        "actual_zero_set_witness_found":
            zero_witness,

        "zero_threshold_used":
            False,

        "D55_continuous_X10_certificate_inherited":
            True,

        "Y_global_C9_FD8_Taylor_route_licensed":
            False,

        "Y_lower_regularity_route_selected":
            zero_witness,

        "Y_zero_set_lower_regularity_modulus_"
        "numerically_certified":
            False,

        "candidate_full_Ward_residual_read":
            False,

        "registered_hotspot_full_Ward_defect_read":
            False,

        "B_total_defined":
            False,

        "full_Ward_execution_licensed":
            False,

        "full_original_H4_Ward_certified":
            False,

        "H4_Z21_solve_performed":
            False,

        "Z21_certified":
            False,

        "lensing_licensed":
            False,

        "threshold_changed":
            False,

        "source_coefficients_changed":
            False,

        "observational_tuning":
            False,

        "next_route":
            next_route,

        "claim_boundary":
            "Y zero-set regularity route decision only. "
            "Stage-E real-space g10 is independently tied "
            "to the certified X10 mode representation and "
            "all original C x Nt x beta cohorts are covered. "
            "Strict sign changes use no numerical zero threshold. "
            "If present they prove a continuum zero by continuity, "
            "so a blanket global C9 Y assumption is forbidden. "
            "The lower-regularity Lipschitz modulus formula is "
            "frozen, but its physical M0/M1/L0/L1 constants are "
            "not yet certified. No integrated H4 Ward residual, "
            "B_total, Z21 or observable is evaluated."
    }

    require(
        all_mode_bind,
        "Stage-E gradient/mode binding failed",
    )

    require(
        all_beta_invariant,
        "beta invariance of Y gradients failed",
    )

    out.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    out.write_text(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        ) + "\n"
    )

    print("CLASSIFICATION =", classification)
    print("UNIQUE_C_NT_CASES =", len(cases))
    print(
        "PHYSICAL_C_BETA_NT_COHORTS =",
        len(cases) * len(old.r7.BETAS),
    )
    print(
        "STRICT_SIGN_CHANGES =",
        total_crossings,
    )
    print(
        "EXACT_ZERO_NODES =",
        total_exact_zeros,
    )
    print(
        "ZEROSET_WITNESS =",
        zero_witness,
    )
    print(
        "LOWER_REGULARITY_ROUTE =",
        zero_witness,
    )
    print("NEXT =", next_route)
    print(
        "GE19_H4F3D12R4_Y_ZEROSET_ROUTE_PASS"
    )


if __name__ == "__main__":
    main()
