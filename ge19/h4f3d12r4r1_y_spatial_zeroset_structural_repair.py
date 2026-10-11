#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import subprocess
from pathlib import Path

from ge19 import repair07_window_retarded_reduced_h3_z20_particular as r7
from ge19 import h4_stagee_versioned_y_source_rows as stagee

ROOT = Path(__file__).resolve().parents[1]

PRE = ROOT / (
    "ge19/"
    "h4f3d12r4r1_predata_y_spatial_zeroset_structural_repair.json"
)

PRE_CLASS = (
    "GE19_H4F3D12R4R1_PREDATA_Y_SPATIAL_ZEROSET_STRUCTURAL_REPAIR"
)

def require(x,msg):
    if not x:
        raise RuntimeError(msg)

def sha256(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()

def git_blob(p):
    return subprocess.check_output(
        ["git","rev-parse","HEAD:"+p],
        cwd=ROOT,text=True
    ).strip()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()

    out=Path(args.json_out).resolve()
    require(not out.exists(),"D12R4R1 output exists; no overwrite")

    pre=json.loads(PRE.read_text())
    require(pre["classification"]==PRE_CLASS,"wrong predata")

    require(
        subprocess.run(
            ["git","merge-base","--is-ancestor",
             pre["parent_HEAD"],"HEAD"],
            cwd=ROOT
        ).returncode==0,
        "preregistered parent is not ancestor"
    )

    locks={}
    for name,item in pre["frozen_git_blobs"].items():
        got=git_blob(item["path"])
        locks[name]={
            "path":item["path"],
            "expected":item["blob"],
            "observed":got,
            "exact":got==item["blob"],
        }

    require(
        all(q["exact"] for q in locks.values()),
        "frozen source changed"
    )

    d12path=ROOT/pre["D12R4_result"]["path"]

    require(
        sha256(d12path)==pre["D12R4_result"]["sha256"],
        "D12R4 result hash changed"
    )

    d12=json.loads(d12path.read_text())

    require(
        d12["classification"] ==
        "GE19_H4F3D12R4_Y_ZEROSET_ROUTE_PASS_"
        "NO_DISCRETE_WITNESS_CONTINUUM_SEPARATION_OPEN",
        "unexpected historical D12R4 classification"
    )

    require(
        d12["all_18_beta_C_Nt_cohorts_covered"] is True,
        "D12R4 cohort coverage missing"
    )

    require(
        d12[
            "all_StageE_gradients_bound_to_independent_mode_X10_X11"
        ] is True,
        "D12R4 Stage-E/X10 binding missing"
    )

    modes=tuple(int(m) for m in r7.FOURIER_N)

    require(
        modes==(3,5,8,10,15,20),
        "frozen Fourier support changed"
    )

    require(0 not in modes,"unexpected DC mode")

    recon=inspect.getsource(r7.reconstruct_positive_modes)
    real=inspect.getsource(r7.reduced_state_real)
    ys=inspect.getsource(stagee.source_h4)

    require(
        "for i,m in enumerate(FOURIER_N)" in recon,
        "positive-mode reconstruction changed"
    )

    require(
        "real[name]=reconstruct_positive_modes(coeff,nx)" in real,
        "reduced real-space reconstruction changed"
    )

    require(
        "spatial={name:spectral_dx(real[name],kfund)" in real,
        "spatial derivative reconstruction changed"
    )

    require(
        "g0=qq[:,None]*u0+p0/aa[:,None]" in ys,
        "Stage-E g10 formula changed"
    )

    require(
        "2.0*np.abs(g0)*g1" in ys,
        "Stage-E H4 Y flux changed"
    )

    # Exact structural argument:
    # 1. u10 is a finite sum of m in FOURIER_N only.
    # 2. d_chi phi10 preserves the same nonzero support.
    # 3. Q(t), a(t) are spatially homogeneous.
    # Therefore g10 has no m=0 coefficient and its spatial mean is zero.
    # A continuous real periodic zero-mean function has at least one zero.

    report={
        "classification":
            "GE19_H4F3D12R4R1_Y_SPATIAL_ZEROSET_"
            "STRUCTURAL_PASS_LOWER_REGULARITY_REQUIRED",

        "preregistration":PRE_CLASS,

        "execution_HEAD":
            subprocess.check_output(
                ["git","rev-parse","HEAD"],
                cwd=ROOT,text=True
            ).strip(),

        "frozen_source_audit":locks,

        "historical_D12R4_preserved":True,

        "historical_D12R4_time_sign_changes":d12[
            "strict_sign_change_count_total"
        ],

        "historical_D12R4_exact_nodes":d12[
            "exact_zero_node_count_total"
        ],

        "D12R4_did_not_test_spatial_adjacency":True,

        "Fourier_modes":list(modes),

        "zero_mode_present":False,

        "g10_spatial_mean_exactly_zero_by_representation":True,

        "g10_continuous_periodic_in_space":True,

        "spatial_zero_exists_for_every_time_slice":True,

        "global_abs_g10_positive_separation_possible":False,

        "Y_global_C9_FD8_Taylor_route_licensed":False,

        "Y_lower_regularity_route_selected":True,

        "safe_Y_modulus":
            "|F_Y(t)-F_Y(s)| <= "
            "2*(M1*L0+M0*L1)*|t-s|",

        "Y_M0_M1_L0_L1_numerically_certified":False,

        "candidate_full_Ward_residual_read":False,

        "B_total_defined":False,

        "full_Ward_execution_licensed":False,

        "Z21_certified":False,

        "lensing_licensed":False,

        "threshold_changed":False,

        "source_coefficients_changed":False,

        "observational_tuning":False,

        "next_route":
            "CERTIFY_Y_M0_M1_L0_L1_LOWER_REGULARITY_MODULUS_"
            "PLUS_NONY_M5_M9_PLUS_PARENT_BOUNDARY_PLUS_ROUNDOFF",

        "claim_boundary":
            "Artifact-only structural repair of the D12R4 route. "
            "The original D12R4 no-temporal-witness result is retained. "
            "Because the physical g10 representation has no spatial DC "
            "mode, its spatial mean is exactly zero and its periodic "
            "continuous field has a spatial zero at every time. "
            "Therefore global positive separation from zero cannot be "
            "the next route. No full Ward residual or Z21 is evaluated."
    }

    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(
        json.dumps(report,indent=2,sort_keys=True) + "\n"
    )

    print("CLASSIFICATION =",report["classification"])
    print("FOURIER_MODES =",report["Fourier_modes"])
    print(
        "SPATIAL_ZERO_EVERY_TIME =",
        report["spatial_zero_exists_for_every_time_slice"]
    )
    print(
        "GLOBAL_POSITIVE_SEPARATION =",
        report["global_abs_g10_positive_separation_possible"]
    )
    print(
        "LOWER_REGULARITY_ROUTE =",
        report["Y_lower_regularity_route_selected"]
    )
    print("NEXT =",report["next_route"])
    print("GE19_H4F3D12R4R1_STRUCTURAL_REPAIR_PASS")

if __name__=="__main__":
    main()
