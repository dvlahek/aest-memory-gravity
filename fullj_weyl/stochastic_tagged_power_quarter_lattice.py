#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# The validated physical-k repair must be active before the evolving-Weyl
# helpers are used.
from fullj_weyl import metric_projection_physical_kmask_repair as kmask
from fullj_weyl import stochastic_tagged_power_lattice_kmask_regression as reg

pl = reg.pl
poc = pl.poc
r2 = pl.r2
m = pl.m
static = pl.static

REG_FAIL_RESULT_LOCK = "9f5218629901643574373e32c84d137c9cda2494"
NPZ_AUDIT_LOCK = "97d72584aa5ed26028e8e60e1e6ef0ccd1919a21"
HISTORY_LOCK = "24292897672aea7a62620e766f014d7004e6d1d4"
KMASK_RESULT_LOCK = "20151ab785e923de20d720f3fdd8890576b6cc05"
PREDATA_LOCK = "3d309b51e44eb38569a7be263dbb14963ba4bd17"

PASS = "FULLJ_STOCHASTIC_TAGGED_POWER_QUARTER_LATTICE_PASS"
FAIL = "FULLJ_STOCHASTIC_TAGGED_POWER_QUARTER_LATTICE_FAIL"
INCOMPLETE = "FULLJ_STOCHASTIC_TAGGED_POWER_QUARTER_LATTICE_INCOMPLETE"

PARENT_NPZ = ROOT / "results/fullj_stochastic_tagged_power_lattice_kmask_regression.npz"
PARENT_JSON = ROOT / "results/fullj_stochastic_tagged_power_lattice_kmask_regression.json"
PARENT_NPZ_SHA256 = "83fb7462ec970bfef953e3804d11a81fd5843745347fe77c318c9e39b8e6e82d"
COEFF_HASH = "9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200"

B2 = (0, 1)
EPS = 0.05
NSTEP = 4096
CHECK_Z = np.asarray(pl.CHECK_Z, float)

WINDOWS = {
    "W1": {
        "parent": np.asarray([0.0925,0.0950,0.0975,0.1000,0.1025,0.1050,0.1075,0.1100,0.1125], float),
        "quarter": np.asarray([0.09375,0.09625,0.09875,0.10125,0.10375,0.10625,0.10875,0.11125], float),
    },
    "W2": {
        "parent": np.asarray([0.1550,0.1575,0.1600,0.1625,0.1650,0.1675,0.1700], float),
        "quarter": np.asarray([0.15625,0.15875,0.16125,0.16375,0.16625,0.16875], float),
    },
    "W3": {
        "parent": np.asarray([0.1900,0.1925,0.1950,0.1975,0.2000], float),
        "quarter": np.asarray([0.19125,0.19375,0.19625,0.19875], float),
    },
}
WINDOW_ORDER = ("W1", "W2", "W3")
K_QUARTER = np.concatenate([WINDOWS[w]["quarter"] for w in WINDOW_ORDER])
WINDOW_ID = np.concatenate([
    np.full(len(WINDOWS[w]["quarter"]), i, int) for i, w in enumerate(WINDOW_ORDER)
])

KF_Q = 0.00125
NX_Q = 1024
BOX_Q = 2.0 * np.pi / (KF_Q * float(static.h))

CANONICAL_GATE = 1.0e-10
METRIC_GATE = 1.0e-8
SAT_GATE = 2.0e-2
ALG_GATE = 1.0e-12
BG_RESPONSE_GATE = 1.0e-3
BG_POWER_GATE = 1.0e-3
POWER_L2_MAX_GATE = 5.0e-2
POWER_L2_MED_GATE = 2.5e-2
POWER_PEAK_GATE = 1.0e-1
SPIKE_FACTOR = 2.0
REFINE_TOL = 1.0e-12


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def idx(grid, value):
    q = np.where(np.isclose(np.asarray(grid, float), float(value), rtol=0.0, atol=5e-13))[0]
    if len(q) != 1:
        raise RuntimeError(f"nonunique/missing grid value {value}")
    return int(q[0])


def rel_complex(a, b):
    aa = np.asarray(a, complex); bb = np.asarray(b, complex)
    return float(np.linalg.norm(aa-bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


def rel_real(a, b):
    aa = np.asarray(a, float); bb = np.asarray(b, float)
    return float(np.linalg.norm(aa-bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


def load_parent():
    if not PARENT_NPZ.exists() or not PARENT_JSON.exists():
        raise FileNotFoundError("missing repaired-regression parent JSON/NPZ")
    digest = sha256_file(PARENT_NPZ)
    if digest != PARENT_NPZ_SHA256:
        raise RuntimeError(f"parent NPZ SHA256 mismatch: {digest}")

    meta = json.loads(PARENT_JSON.read_text())
    if meta.get("classification") != "FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_KMASK_REGRESSION_FAIL":
        raise RuntimeError("parent JSON does not preserve repaired-regression FAIL")
    gates = meta.get("gates", {})
    for name in (
        "KR_G1_provenance_and_frozen_identity",
        "KR_G2_overlap_reuse_certification",
        "KR_G3_stageA_repaired_health_and_saturation",
        "KR_G4_repaired_hybrid_power_sanity",
        "KR_G5_stageB_repaired_health_and_saturation",
    ):
        if gates.get(name) is not True:
            raise RuntimeError(f"parent true gate not preserved: {name}")
    for name in (
        "KR_G6_repaired_half_lattice_power_interpolation_accuracy",
        "KR_G7_no_unresolved_repaired_half_lattice_power_spike",
    ):
        if gates.get(name) is not False:
            raise RuntimeError(f"parent failed gate not preserved: {name}")

    q = np.load(PARENT_NPZ)
    required = {
        "redshifts", "K_full", "selected_half", "response_hybrid_B2", "response_half_new"
    }
    if not required.issubset(set(q.files)):
        raise RuntimeError(f"parent NPZ missing keys {sorted(required-set(q.files))}")
    z = np.asarray(q["redshifts"], float)
    kfull = np.asarray(q["K_full"], float)
    khalf = np.asarray(q["selected_half"], float)
    afull = np.asarray(q["response_hybrid_B2"], complex)
    ahalf = np.asarray(q["response_half_new"], complex)
    if not np.allclose(z, CHECK_Z, rtol=0.0, atol=5e-13):
        raise RuntimeError("parent redshift grid mismatch")
    if afull.shape != (2, len(kfull), len(CHECK_Z)) or ahalf.shape != (2, len(khalf), len(CHECK_Z)):
        raise RuntimeError(f"parent response shapes mismatch {afull.shape} {ahalf.shape}")
    if not np.all(np.isfinite(afull)) or not np.all(np.isfinite(ahalf)):
        raise RuntimeError("nonfinite parent response")
    return meta, digest, kfull, khalf, afull, ahalf


def parent_response_at(kh, kfull, khalf, afull, ahalf):
    q = np.where(np.isclose(kfull, float(kh), rtol=0.0, atol=5e-13))[0]
    if len(q) == 1:
        return np.asarray(afull[:, int(q[0]), :], complex)
    q = np.where(np.isclose(khalf, float(kh), rtol=0.0, atol=5e-13))[0]
    if len(q) == 1:
        return np.asarray(ahalf[:, int(q[0]), :], complex)
    raise RuntimeError(f"required local parent node missing: {kh}")


def health_ok(rec: dict) -> bool:
    return bool(
        rec.get("finite", False)
        and float(rec.get("canonical_max", np.inf)) <= CANONICAL_GATE
        and all(float(v) <= METRIC_GATE for v in rec.get("metric_max", {}).values())
    )


def append_rows(rows, bgid, kh, window, T):
    if T is None:
        return
    for iz, z in enumerate(CHECK_Z):
        rows.append({
            "window": window,
            "background": int(bgid),
            "k_h_Mpc_inv": float(kh),
            "z": float(z),
            "T_real": float(np.real(T[iz])),
            "T_imag": float(np.imag(T[iz])),
            "P_tag": float(abs(T[iz])**2),
        })


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_stochastic_tagged_power_quarter_lattice.json")
    ap.add_argument("--npz-out", default="results/fullj_stochastic_tagged_power_quarter_lattice.npz")
    ap.add_argument("--csv-out", default="results/fullj_stochastic_tagged_power_quarter_lattice.csv")
    args = ap.parse_args()

    ancestry = {
        "repaired_regression_fail_result_lock": is_ancestor(REG_FAIL_RESULT_LOCK),
        "npz_audit_lock": is_ancestor(NPZ_AUDIT_LOCK),
        "history_lock": is_ancestor(HISTORY_LOCK),
        "physical_kmask_repair_result_lock": is_ancestor(KMASK_RESULT_LOCK),
        "predata_lock": is_ancestor(PREDATA_LOCK),
    }
    _, gcoef, coeff_digest = poc.coeff_draw()
    identity = kmask.original_r2_mask_identity(128)
    expected_quarter = np.asarray([
        0.09375,0.09625,0.09875,0.10125,0.10375,0.10625,0.10875,0.11125,
        0.15625,0.15875,0.16125,0.16375,0.16625,0.16875,
        0.19125,0.19375,0.19625,0.19875,
    ], float)
    exact_modes = all(abs(round(float(k)/KF_Q)*KF_Q-float(k)) <= 5e-13 for k in K_QUARTER)
    frozen = bool(
        coeff_digest == COEFF_HASH
        and B2 == (0,1)
        and EPS == pl.EPS == 0.05
        and NSTEP == pl.NSTEP == 4096
        and abs(float(kmask.METRIC_KMAX_H)-0.32) < 1e-15
        and identity.get("mismatch_count") == 0
        and abs(KF_Q-0.00125) < 1e-15 and NX_Q == 1024
        and len(K_QUARTER) == 18 and np.allclose(K_QUARTER, expected_quarter, rtol=0.0, atol=5e-14)
        and exact_modes
    )

    print("FULLJ_QUARTER_LATTICE_START", flush=True)
    print("FULLJ_QUARTER_LATTICE_ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)
    print("FULLJ_QUARTER_LATTICE_COEFFICIENT_SHA256=" + coeff_digest, flush=True)
    print("FULLJ_QUARTER_LATTICE_ORIGINAL_IDENTITY=" + json.dumps(identity, sort_keys=True), flush=True)
    print("FULLJ_QUARTER_LATTICE_GEOMETRY kF_h=%.6f NX=%d box_Mpc=%.12e" % (KF_Q, NX_Q, BOX_Q), flush=True)
    print("FULLJ_QUARTER_LATTICE_NODES=" + json.dumps(K_QUARTER.tolist()), flush=True)
    print("FULLJ_QUARTER_LATTICE_TOTAL_RUNS=72", flush=True)

    try:
        parent_meta, parent_digest, kfull, khalf, afull, ahalf = load_parent()
        parent_by_window = {}
        for w in WINDOW_ORDER:
            kp = WINDOWS[w]["parent"]
            arr = np.stack([parent_response_at(k, kfull, khalf, afull, ahalf) for k in kp], axis=1)
            if arr.shape != (2, len(kp), len(CHECK_Z)) or not np.all(np.isfinite(arr)):
                raise RuntimeError(f"bad complete parent window {w}: {arr.shape}")
            parent_by_window[w] = arr
    except Exception as exc:
        out = {
            "classification": INCOMPLETE,
            "diagnostic_complete": False,
            "ancestry": ancestry,
            "frozen_setup": frozen,
            "reason": str(exc),
        }
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("FULLJ_QUARTER_LATTICE_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3

    if not all(ancestry.values()) or not frozen:
        out = {
            "classification": INCOMPLETE,
            "diagnostic_complete": False,
            "ancestry": ancestry,
            "frozen_setup": frozen,
            "parent_npz_sha256": parent_digest,
        }
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("FULLJ_QUARTER_LATTICE_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3

    Aquarter = np.full((2, len(K_QUARTER), len(CHECK_Z)), np.nan+1j*np.nan, complex)
    all_runs = []
    response_rows = []
    run_index = 0

    old_kmpc = np.asarray(m.K_MPC, float).copy()
    old_kh = np.asarray(getattr(m, "K_H", pl.radial.K0), float).copy()
    try:
        for iq, kh in enumerate(K_QUARTER):
            w = WINDOW_ORDER[int(WINDOW_ID[iq])]
            mode_h = poc.target_modes(float(kh))
            m.K_H = mode_h.copy()
            m.K_MPC = mode_h * float(static.h)
            data = r2.r0.prepare_bridge_data()
            for ib, bgid in enumerate(B2):
                pair = {}; meta = None
                for sign in (+1, -1):
                    run_index += 1
                    rec, wh, mm = pl.run_signed_geom(
                        data, mode_h, gcoef[bgid], bgid, float(kh), sign,
                        KF_Q, NX_Q, BOX_Q, "quarter00125",
                    )
                    rec["run_index"] = int(run_index)
                    rec["window"] = w
                    all_runs.append(rec)
                    print(
                        f"FULLJ_QUARTER_LATTICE_RUN {run_index:03d}/72 window={w} bg={bgid} "
                        f"k_h={kh:.5f} sign={sign:+d} "
                        + (f"canonical={rec['canonical_max']:.3e} satMax={rec['sat_max']:.3e}"
                           if rec.get("finite") else f"finite=False reason={rec.get('reason','unknown')}"),
                        flush=True,
                    )
                    if wh is not None:
                        pair[sign] = wh; meta = mm
                if len(pair) == 2:
                    T = pl.pair_response(pair, meta)
                    Aquarter[ib, iq, :] = T
                    append_rows(response_rows, bgid, kh, w, T)
    finally:
        m.K_MPC = old_kmpc
        m.K_H = old_kh

    Pquarter = np.abs(Aquarter)**2
    Pdirect = np.mean(Pquarter, axis=0)
    Tdirect = np.mean(Aquarter, axis=0)
    back = np.real(Aquarter)**2 + np.imag(Aquarter)**2
    alg = float(np.linalg.norm(Pquarter-back) / max(float(np.linalg.norm(Pquarter)), 1e-300))
    bg_t = rel_complex(Aquarter[0], Aquarter[1])
    bg_p = rel_real(Pquarter[0], Pquarter[1])

    parent_power_by_window = {
        w: np.mean(np.abs(parent_by_window[w])**2, axis=0) for w in WINDOW_ORDER
    }
    parent_transfer_by_window = {
        w: np.mean(parent_by_window[w], axis=0) for w in WINDOW_ORDER
    }

    Ppred0025 = np.full_like(Pdirect, np.nan, float)
    Tpred0025 = np.full_like(Tdirect, np.nan+1j*np.nan, complex)
    window_metrics = []
    power_l2 = []
    power_peak = []
    transfer_desc = []
    spike_failures = []
    spike_max_ratio = 0.0
    interp_nonneg = True

    offset = 0
    for w in WINDOW_ORDER:
        kp = WINDOWS[w]["parent"]
        kq = WINDOWS[w]["quarter"]
        pp = parent_power_by_window[w]
        tp = parent_transfer_by_window[w]
        sl = slice(offset, offset+len(kq))
        for iz, z in enumerate(CHECK_Z):
            pred = pl.power_interp(kp, pp[:, iz], kq)
            tpred = pl.complex_interp(kp, tp[:, iz], kq)
            direct = Pdirect[sl, iz]
            Ppred0025[sl, iz] = pred
            Tpred0025[sl, iz] = tpred
            ep = rel_real(pred, direct)
            epeak = float(np.max(np.abs(pred-direct)) / max(float(np.max(direct)), 1e-300))
            et = rel_complex(tpred, Tdirect[sl, iz])
            power_l2.append(ep); power_peak.append(epeak); transfer_desc.append(et)
            window_metrics.append({
                "window": w, "z": float(z), "power_L2": ep,
                "power_peak": epeak, "transfer_L2_descriptive": et,
            })
            if not np.all(np.isfinite(pred)) or np.any(pred < 0.0):
                interp_nonneg = False
            pmax = float(np.max(pp[:, iz])); floor = 1e-14*pmax
            for j, kh in enumerate(kq):
                right = int(np.searchsorted(kp, kh)); left = right-1
                den = max(float(pp[left, iz]), float(pp[right, iz]), floor, 1e-300)
                ratio = float(direct[j]/den)
                spike_max_ratio = max(spike_max_ratio, ratio)
                if float(direct[j]) > SPIKE_FACTOR*max(float(pp[left, iz]), float(pp[right, iz])) + floor:
                    spike_failures.append({
                        "window": w, "z": float(z), "k_h_Mpc_inv": float(kh),
                        "direct_power": float(direct[j]),
                        "left_power": float(pp[left, iz]), "right_power": float(pp[right, iz]),
                        "ratio": ratio,
                    })
        offset += len(kq)

    # Coarse 0.005 prediction at the exact same new quarter controls.
    P005 = np.mean(np.abs(afull)**2, axis=0)
    Ppred005 = np.full_like(Pdirect, np.nan, float)
    refine_rows = []
    improve_nonworse = True
    improve_late = True
    e005_by_z = []; e0025_by_z = []
    for iz, z in enumerate(CHECK_Z):
        p005 = pl.power_interp(kfull, P005[:, iz], K_QUARTER)
        Ppred005[:, iz] = p005
        e005 = rel_real(p005, Pdirect[:, iz])
        e0025 = rel_real(Ppred0025[:, iz], Pdirect[:, iz])
        e005_by_z.append(e005); e0025_by_z.append(e0025)
        nonworse = bool(e0025 <= e005 + REFINE_TOL)
        improve_nonworse = improve_nonworse and nonworse
        late_required = bool(np.isclose(z, 0.5, rtol=0, atol=1e-12) or np.isclose(z, 0.2, rtol=0, atol=1e-12))
        strict = bool(e0025 < e005) if late_required else None
        if late_required:
            improve_late = improve_late and bool(strict)
        refine_rows.append({
            "z": float(z), "E_005": e005, "E_0025": e0025,
            "nonworse": nonworse, "late_strict_required": late_required,
            "late_strict_improvement": strict,
        })

    all_finite = bool(len(all_runs) == 72 and np.all(np.isfinite(Aquarter)) and all(r.get("finite", False) for r in all_runs))
    health = bool(all_finite and all(health_ok(r) for r in all_runs))
    canonical_max = float(max([r.get("canonical_max", np.inf) for r in all_runs], default=np.inf))
    metric_max = {k: float(max([r.get("metric_max", {}).get(k, np.inf) for r in all_runs], default=np.inf)) for k in ("hamiltonian","momentum","shear")}
    sat_max = float(max([r.get("sat_max", np.inf) for r in all_runs], default=np.inf))

    gates = {
        "QL_G1_provenance_and_frozen_identity": bool(all(ancestry.values()) and frozen and parent_digest == PARENT_NPZ_SHA256),
        "QL_G2_solver_constraint_health": bool(health),
        "QL_G3_broadband_saturated_closure": bool(sat_max <= SAT_GATE),
        "QL_G4_quarter_stochastic_algebra_sanity": bool(
            all_finite and np.all(np.isfinite(Pquarter)) and np.all(Pquarter >= 0.0)
            and alg <= ALG_GATE and bg_t <= BG_RESPONSE_GATE and bg_p <= BG_POWER_GATE
        ),
        "QL_G5_absolute_quarter_power_interpolation_accuracy": bool(
            interp_nonneg and max(power_l2) <= POWER_L2_MAX_GATE
            and float(np.median(power_l2)) <= POWER_L2_MED_GATE
            and max(power_peak) <= POWER_PEAK_GATE
        ),
        "QL_G6_no_new_unresolved_quarter_power_spike": bool(len(spike_failures) == 0),
        "QL_G7_refinement_improves_over_005": bool(improve_nonworse and improve_late),
    }
    classification = PASS if all(gates.values()) else FAIL

    summary = {
        "runs_expected": 72,
        "runs_finite": int(sum(bool(r.get("finite", False)) for r in all_runs)),
        "canonical_max": canonical_max,
        "metric_max": metric_max,
        "broadband_saturation_max": sat_max,
        "background_response_relative_L2": bg_t,
        "background_power_relative_L2": bg_p,
        "power_identity_relative_L2": alg,
        "quarter_power_L2_max": float(max(power_l2)),
        "quarter_power_L2_median": float(np.median(power_l2)),
        "quarter_power_peak_max": float(max(power_peak)),
        "spike_max_ratio": float(spike_max_ratio),
        "spike_failure_count": int(len(spike_failures)),
        "refinement_nonworse_all_z": bool(improve_nonworse),
        "refinement_strict_late": bool(improve_late),
        "E005_by_z": [float(x) for x in e005_by_z],
        "E0025_by_z": [float(x) for x in e0025_by_z],
    }

    out = {
        "classification": classification,
        "diagnostic_complete": True,
        "ancestry": ancestry,
        "frozen_setup": frozen,
        "parent_npz_sha256": parent_digest,
        "coefficient_sha256": coeff_digest,
        "metric_kmax_h": float(kmask.METRIC_KMAX_H),
        "geometry": {"kF_h": KF_Q, "NX": NX_Q, "box_Mpc": BOX_Q},
        "quarter_nodes": K_QUARTER.tolist(),
        "window_metrics": window_metrics,
        "refinement_by_z": refine_rows,
        "spike_failures": spike_failures,
        "gates": gates,
        "summary": summary,
        "STOCHASTIC_TAGGED_LOCAL_QUARTER_LATTICE_TESTED": bool(classification == PASS),
        "STOCHASTIC_TAGGED_LOCAL_0025_POWER_RESOLUTION_SUPPORTED": bool(classification == PASS),
        "STOCHASTIC_TAGGED_BOUNDED_POWER_INTERPOLANT_TESTED": False,
        "THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED": False,
        "THREE_D_CONTINUOUS_WEYL_POWER_LICENSED": False,
        "EVOLVING_WEYL_POWER_LICENSED": False,
        "ACT_LIKELIHOOD_LICENSED": False,
        "OBSERVATIONAL_CLAIM_LICENSED": False,
    }

    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
    np.savez_compressed(
        args.npz_out,
        redshifts=CHECK_Z,
        quarter_nodes=K_QUARTER,
        quarter_window_id=WINDOW_ID,
        response_quarter_B2=Aquarter,
        power_quarter_B2=Pquarter,
        power_direct_mean=Pdirect,
        power_pred_0025=Ppred0025,
        power_pred_005=Ppred005,
        transfer_pred_0025=Tpred0025,
        K_full=kfull,
        response_hybrid_B2=afull,
    )
    with open(args.csv_out, "w", newline="") as f:
        fields = ["window","background","k_h_Mpc_inv","z","T_real","T_imag","P_tag"]
        wr = csv.DictWriter(f, fieldnames=fields); wr.writeheader(); wr.writerows(response_rows)

    print("FULLJ_QUARTER_LATTICE_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_QUARTER_LATTICE_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("FULLJ_QUARTER_LATTICE_CLASSIFICATION=" + classification, flush=True)
    print("STOCHASTIC_TAGGED_LOCAL_QUARTER_LATTICE_TESTED=" + str(classification == PASS), flush=True)
    print("STOCHASTIC_TAGGED_LOCAL_0025_POWER_RESOLUTION_SUPPORTED=" + str(classification == PASS), flush=True)
    return 0 if classification == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
