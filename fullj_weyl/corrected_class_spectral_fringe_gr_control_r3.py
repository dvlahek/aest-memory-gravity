#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import corrected_class_spectral_fringe_gr_control as base

SERIALIZATION_REPAIR_LOCK = "b691d6ef9e6fa061d7fca842bfc71cfbe81978c1"
INPUT_REPAIR_LOCK = "b16eed79f9fc730d651ed75b44ed161bf8b4a69d"
RUNTIME_REPAIR_LOCK = "1812f015682a946125e747f81b97b902dcf1bec0"
DENSE_RUNTIME_SOURCE_SHA = "4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f"
CLASS_HEAD = "e85808324f51fc694d12e3ed7439552a3c3f9540"
EXPECTED_REMOVED_LMAX = 2500
SERIALIZATION_SIGDIG = 15
CLASS_ARGUMENT_LIMIT = 1024
SERIALIZED_KH_ABS_GATE = 1.0e-12


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def json_out_from_argv() -> Path:
    args = sys.argv[1:]
    if "--json-out" in args:
        i = args.index("--json-out")
        if i + 1 < len(args):
            return Path(args[i + 1])
    return ROOT / "results/fullj_corrected_class_spectral_fringe_gr_control.json"


def serialize_requested_k(k_h):
    kh = np.asarray(k_h, float)
    vals_mpc = kh * base.cb.h
    text = ", ".join(f"{x:.{SERIALIZATION_SIGDIG}g}" for x in vals_mpc)
    pieces = [q.strip() for q in text.split(",")]
    parsed_mpc = np.asarray([float(q) for q in pieces], float)
    parsed_kh = parsed_mpc / base.cb.h
    if len(text) >= CLASS_ARGUMENT_LIMIT:
        raise RuntimeError(
            f"serialized k_output_values length {len(text)} >= CLASS limit {CLASS_ARGUMENT_LIMIT}"
        )
    if len(pieces) != len(kh):
        raise RuntimeError(f"serialized k count {len(pieces)} != requested {len(kh)}")
    max_abs_kh = float(np.max(np.abs(parsed_kh - kh))) if kh.size else 0.0
    if max_abs_kh > SERIALIZED_KH_ABS_GATE:
        raise RuntimeError(
            f"serialized physical-k displacement {max_abs_kh:.16e} exceeds gate {SERIALIZED_KH_ABS_GATE:.16e}"
        )
    return text, {
        "significant_digits": SERIALIZATION_SIGDIG,
        "string_length": len(text),
        "argument_limit": CLASS_ARGUMENT_LIMIT,
        "value_count": len(pieces),
        "max_abs_k_h_Mpc_displacement": max_abs_kh,
        "displacement_gate": SERIALIZED_KH_ABS_GATE,
    }


def repaired_run_direct_class(k_h, aest_enabled: bool):
    from classy import Class

    kh = np.asarray(k_h, float)
    k_text, serialization = serialize_requested_k(kh)
    pars = dict(base.cb.build_params())
    pars.update({
        "output": "mTk,vTk",
        "lensing": "no",
        "k_output_values": k_text,
        "P_k_max_h/Mpc": 0.30,
        "z_max_pk": 6.5,
        "aest_memory_enabled": "no",
        "aest_eta": 0.0,
        "aest_enabled": "yes" if aest_enabled else "no",
    })

    removed_lmax = pars.pop("l_max_scalars", None)
    if removed_lmax != EXPECTED_REMOVED_LMAX:
        raise RuntimeError(f"unexpected inherited l_max_scalars={removed_lmax!r}")
    if pars.get("output") != "mTk,vTk":
        raise RuntimeError(f"direct spectroscopy output changed: {pars.get('output')!r}")
    if "l_max_scalars" in pars:
        raise RuntimeError("l_max_scalars still present after transfer-input repair")

    print(
        "FULLJ_DIRECT_CLASS_FRINGE_R3_SERIALIZATION "
        f"n={serialization['value_count']} chars={serialization['string_length']} "
        f"max_abs_dkh={serialization['max_abs_k_h_Mpc_displacement']:.16e} "
        f"aest_enabled={aest_enabled}",
        flush=True,
    )

    c = Class()
    c.set(pars)
    c.compute()
    try:
        pert = c.get_perturbations()
        histories, scalar_key = base.d2a.scalar_histories(pert)
        if len(histories) != len(kh):
            raise RuntimeError(f"history count {len(histories)} != requested {len(kh)}")

        out = np.full((len(kh), len(base.CHECK_Z)), np.nan, float)
        cover = []
        for i, raw in enumerate(histories):
            akey = base.d2a.pick(raw, "a", ("scale factor",))
            pkey = base.d2a.pick(raw, "phi")
            pskey = base.d2a.pick(raw, "psi")
            aa = np.asarray(raw[akey], float)
            phi = np.asarray(raw[pkey], float)
            psi = np.asarray(raw[pskey], float)
            sp, xs = base.unique_spline_x(aa, phi + psi)
            at = 1.0 / (1.0 + base.CHECK_Z)
            ok = bool(
                float(np.min(xs)) <= float(np.min(at)) + 1e-12
                and float(np.max(xs)) >= float(np.max(at)) - 1e-12
            )
            cover.append(ok)
            if not ok:
                raise RuntimeError(f"history {i} lacks z=6..0.2 coverage")
            out[i, :] = sp(at)

        return {
            "W": out,
            "all_finite": bool(np.all(np.isfinite(out))),
            "coverage": bool(all(cover)),
            "scalar_key": scalar_key,
            "parameters": pars,
            "transfer_input_repair": {
                "removed_key": "l_max_scalars",
                "removed_value": removed_lmax,
                "output": pars["output"],
            },
            "k_serialization_repair": serialization,
        }
    finally:
        c.struct_cleanup()
        c.empty()


def main() -> int:
    for label, sha in (
        ("runtime", RUNTIME_REPAIR_LOCK),
        ("input", INPUT_REPAIR_LOCK),
        ("serialization", SERIALIZATION_REPAIR_LOCK),
    ):
        if not is_ancestor(sha):
            print(f"FULLJ_DIRECT_CLASS_FRINGE_R3_{label.upper()}_REPAIR_LOCK_FAIL", flush=True)
            return 3

    class_root = Path(os.environ.get("NL1C6D2N_CLASS_ROOT", ""))
    if not class_root.is_dir() or not (class_root / ".git").exists():
        print("FULLJ_DIRECT_CLASS_FRINGE_R3_RUNTIME_ENV_MISSING", flush=True)
        return 3

    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=class_root, text=True).strip()
    src = class_root / "source/aest_memory.c"
    if not src.is_file():
        print("FULLJ_DIRECT_CLASS_FRINGE_R3_RUNTIME_SOURCE_MISSING", flush=True)
        return 3
    source_sha = base.sha256_file(src)
    if head != CLASS_HEAD or source_sha != DENSE_RUNTIME_SOURCE_SHA:
        print(
            "FULLJ_DIRECT_CLASS_FRINGE_R3_RUNTIME_PROVENANCE_FAIL "
            f"head={head} source_sha256={source_sha}",
            flush=True,
        )
        return 3

    base.cb.CORRECTED_SOURCE_SHA = DENSE_RUNTIME_SOURCE_SHA
    base.run_direct_class = repaired_run_direct_class

    dense_text, dense_meta = serialize_requested_k(base.K_DENSE)
    anchor_text, anchor_meta = serialize_requested_k(base.K_ANCHOR)
    if dense_meta["value_count"] != 51 or anchor_meta["value_count"] != 15:
        print("FULLJ_DIRECT_CLASS_FRINGE_R3_SERIALIZATION_COUNT_ASSERT_FAIL", flush=True)
        return 3

    probe = dict(base.cb.build_params())
    probe.update({"output": "mTk,vTk"})
    removed = probe.pop("l_max_scalars", None)
    if removed != EXPECTED_REMOVED_LMAX or probe.get("output") != "mTk,vTk" or "l_max_scalars" in probe:
        print("FULLJ_DIRECT_CLASS_FRINGE_R3_INPUT_REPAIR_ASSERT_FAIL", flush=True)
        return 3

    print(
        "FULLJ_DIRECT_CLASS_FRINGE_R3_SERIALIZATION_REPAIR_PASS "
        f"dense_n=51 dense_chars={len(dense_text)} "
        f"anchor_n=15 anchor_chars={len(anchor_text)} "
        f"dense_max_abs_dkh={dense_meta['max_abs_k_h_Mpc_displacement']:.16e} "
        "science_grid_or_gate_changed=False",
        flush=True,
    )
    print(
        "FULLJ_DIRECT_CLASS_FRINGE_R3_INPUT_REPAIR_PASS "
        "removed=l_max_scalars removed_value=2500 output=mTk,vTk science_grid_or_gate_changed=False",
        flush=True,
    )
    print(
        "FULLJ_DIRECT_CLASS_FRINGE_R3_RUNTIME_PROVENANCE_PASS "
        f"head={head} source_sha256={source_sha}",
        flush=True,
    )

    rc = int(base.main())

    out_path = json_out_from_argv()
    if out_path.exists():
        try:
            payload = json.loads(out_path.read_text())
            payload["k_serialization_repair"] = {
                "serialization_repair_lock": SERIALIZATION_REPAIR_LOCK,
                "input_repair_lock": INPUT_REPAIR_LOCK,
                "runtime_repair_lock": RUNTIME_REPAIR_LOCK,
                "historical_incomplete_preserved": True,
                "significant_digits": SERIALIZATION_SIGDIG,
                "CLASS_argument_limit": CLASS_ARGUMENT_LIMIT,
                "dense_string_length": dense_meta["string_length"],
                "dense_value_count": dense_meta["value_count"],
                "dense_max_abs_k_h_Mpc_displacement": dense_meta["max_abs_k_h_Mpc_displacement"],
                "anchor_string_length": anchor_meta["string_length"],
                "anchor_value_count": anchor_meta["value_count"],
                "anchor_max_abs_k_h_Mpc_displacement": anchor_meta["max_abs_k_h_Mpc_displacement"],
                "science_grid_or_gate_changed": False,
            }
            out_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        except Exception as exc:
            print(f"FULLJ_DIRECT_CLASS_FRINGE_R3_JSON_ANNOTATION_WARNING={exc}", flush=True)

    return rc


if __name__ == "__main__":
    raise SystemExit(main())
