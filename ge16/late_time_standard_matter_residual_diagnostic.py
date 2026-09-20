#!/usr/bin/env python3
"""GE16 diagnostic-only late-time standard-matter residual audit.

Consumes the frozen GE08 Repair01 artifact. No CLASS run and no new physics.
Distinguishes:
  (i) matched effective dust, retaining total standard density+momentum and
      dropping only standard pressure/shear;
  (ii) baryon-only replacement.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

ARTIFACT_ID=10598944561
ARTIFACT_DIGEST="sha256:d237aaf4b8f7314992de8dc1a0b432b4fb81eb80fe08352ac3f9d95cfc54982d"
PARENT_CLASS="GE08_REPAIR01_FULL_FIRST_ORDER_STATE_BRIDGE_PASS_MATTER_INCOMPLETE"
GE08_PRESSURE=4.0296809261404915e-7
GE08_SHEAR=5.717716788656946e-10
GE08_BARYON_DENSITY=1.3238516018121685e-3
TINY=1e-300


def unique_find(root:Path,name:str)->Path:
    hits=sorted(p for p in root.rglob(name) if p.is_file())
    if len(hits)!=1:
        raise RuntimeError(f"expected exactly one {name}, found {len(hits)}")
    return hits[0]


def relnorm(x,y=None):
    xx=np.asarray(x,float)
    if y is None:
        return float(np.linalg.norm(xx))
    yy=np.asarray(y,float)
    return float(np.linalg.norm(xx-yy)/max(np.linalg.norm(xx),np.linalg.norm(yy),TINY))


def safe_ratio_abs(num,den):
    return np.abs(np.asarray(num,float))/np.maximum(np.abs(np.asarray(den,float)),TINY)


def grouped(rows_key, vals):
    keys=np.asarray(rows_key)
    out=[]
    for key in sorted(np.unique(keys)):
        m=keys==key
        dr=vals["dr"][m]; dp=vals["dp"][m]; sh=vals["sh"][m]
        bd=vals["bd"][m]; bm=vals["bm"][m]; mom=vals["mom"][m]
        residual_dr=dr-bd
        residual_mom=mom-bm
        out.append({
            "key":float(key),
            "rows":int(np.sum(m)),
            "pressure_over_density_global_L2":float(np.linalg.norm(dp)/max(np.linalg.norm(dr),TINY)),
            "shear_over_density_global_L2":float(np.linalg.norm(sh)/max(np.linalg.norm(dr),TINY)),
            "pressure_over_density_pointwise_max":float(np.max(safe_ratio_abs(dp,dr))),
            "shear_over_density_pointwise_max":float(np.max(safe_ratio_abs(sh,dr))),
            "baryon_only_density_relative_L2":relnorm(dr,bd),
            "baryon_only_momentum_relative_L2":relnorm(mom,bm),
            "non_baryon_density_fraction_L2":float(np.linalg.norm(residual_dr)/max(np.linalg.norm(dr),TINY)),
            "non_baryon_momentum_fraction_L2":float(np.linalg.norm(residual_mom)/max(np.linalg.norm(mom),TINY)),
            "pressure_over_non_baryon_density_global_L2":float(np.linalg.norm(dp)/max(np.linalg.norm(residual_dr),TINY)),
            "shear_over_non_baryon_density_global_L2":float(np.linalg.norm(sh)/max(np.linalg.norm(residual_dr),TINY)),
        })
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--artifact-root",required=True)
    ap.add_argument("--artifact-meta-json",required=True)
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()

    root=Path(args.artifact_root)
    meta=json.loads(Path(args.artifact_meta_json).read_text())
    artifact_ok=bool(
        int(meta.get("id",-1))==ARTIFACT_ID
        and meta.get("digest")==ARTIFACT_DIGEST
        and meta.get("expired") is False
    )

    parent_json=unique_find(root,"ge08_repair01_full_first_order_state_bridge.json")
    parent_npz=unique_find(root,"ge08_repair01_full_first_order_state_bridge.npz")
    parent=json.loads(parent_json.read_text())
    parent_ok=parent.get("classification")==PARENT_CLASS

    d=np.load(parent_npz)
    required={
        "k","z","standard_delta_rho","standard_momentum","standard_delta_p",
        "standard_shear","baryon_delta_rho","delta_b","theta_b"
    }
    if not required.issubset(set(d.files)):
        raise RuntimeError(f"missing arrays: {sorted(required-set(d.files))}")

    k=np.asarray(d["k"],float)
    z=np.asarray(d["z"],float)
    dr=np.asarray(d["standard_delta_rho"],float)
    mom=np.asarray(d["standard_momentum"],float)
    dp=np.asarray(d["standard_delta_p"],float)
    sh=np.asarray(d["standard_shear"],float)
    bd=np.asarray(d["baryon_delta_rho"],float)
    db=np.asarray(d["delta_b"],float)
    tb=np.asarray(d["theta_b"],float)

    rho_b=bd/db
    bm=rho_b*tb
    residual_dr=dr-bd
    residual_mom=mom-bm

    pressure=float(np.linalg.norm(dp)/np.linalg.norm(dr))
    shear=float(np.linalg.norm(sh)/np.linalg.norm(dr))
    baryon_density=relnorm(dr,bd)
    baryon_momentum=relnorm(mom,bm)

    vals={"dr":dr,"mom":mom,"dp":dp,"sh":sh,"bd":bd,"bm":bm}
    per_k=grouped(k,vals)
    per_z=grouped(z,vals)

    global_diag={
        "matched_dust_pressure_over_density_global_L2":pressure,
        "matched_dust_shear_over_density_global_L2":shear,
        "matched_dust_pressure_over_density_pointwise_max":float(np.max(safe_ratio_abs(dp,dr))),
        "matched_dust_shear_over_density_pointwise_max":float(np.max(safe_ratio_abs(sh,dr))),
        "baryon_only_density_relative_L2":baryon_density,
        "baryon_only_momentum_relative_L2":baryon_momentum,
        "non_baryon_density_fraction_L2":float(np.linalg.norm(residual_dr)/np.linalg.norm(dr)),
        "non_baryon_momentum_fraction_L2":float(np.linalg.norm(residual_mom)/max(np.linalg.norm(mom),TINY)),
        "pressure_over_non_baryon_density_global_L2":float(np.linalg.norm(dp)/max(np.linalg.norm(residual_dr),TINY)),
        "shear_over_non_baryon_density_global_L2":float(np.linalg.norm(sh)/max(np.linalg.norm(residual_dr),TINY)),
    }

    finite=bool(all(
        np.all(np.isfinite(x))
        for x in (k,z,dr,mom,dp,sh,bd,db,tb,rho_b,bm,residual_dr,residual_mom)
    ))
    n_k=len(np.unique(k)); n_z=len(np.unique(z))
    gates={
        "artifact_digest_exact":artifact_ok,
        "parent_classification_exact":bool(parent_ok),
        "exactly_48_selected_rows":bool(len(k)==48),
        "exactly_6_k_modes":bool(n_k==6),
        "exactly_8_native_times":bool(n_z==8),
        "reproduce_GE08_global_pressure_ratio_abs_error_le_1e15":bool(abs(pressure-GE08_PRESSURE)<=1e-15),
        "reproduce_GE08_global_shear_ratio_abs_error_le_1e15":bool(abs(shear-GE08_SHEAR)<=1e-15),
        "reproduce_GE08_baryon_density_mismatch_abs_error_le_1e15":bool(abs(baryon_density-GE08_BARYON_DENSITY)<=1e-15),
        "all_quantities_finite":finite,
    }
    passed=bool(all(gates.values()))

    result={
        "classification":(
            "GE16_LATE_TIME_STANDARD_MATTER_RESIDUAL_DIAGNOSTIC_PASS"
            if passed else
            "GE16_LATE_TIME_STANDARD_MATTER_RESIDUAL_DIAGNOSTIC_FAIL"
        ),
        "predata_classification":"GE16_PREDATA_LATE_TIME_STANDARD_MATTER_RESIDUAL_DIAGNOSTIC",
        "scope":"Diagnostic-only decomposition of the frozen GE08 standard-sector residual. No approximation acceptance gate and no CLASS execution.",
        "artifact":{
            "id":ARTIFACT_ID,
            "digest":ARTIFACT_DIGEST,
            "metadata_exact":artifact_ok,
            "npz_sha256":hashlib.sha256(parent_npz.read_bytes()).hexdigest(),
        },
        "global":global_diag,
        "per_k":per_k,
        "per_z":per_z,
        "interpretation_boundary":{
            "matched_effective_dust":"retains exact standard-sector density and momentum; omits only pressure and shear",
            "baryon_only":"replaces the complete standard-sector density/momentum by baryons only",
            "approximation_licensed":False,
            "Z20_licensed":False,
        },
        "gates":gates,
        "claim_boundary":"PASS validates only this residual decomposition. It does not accept an effective-dust truncation budget or license Z20.",
    }

    Path(args.json_out).parent.mkdir(parents=True,exist_ok=True)
    Path(args.json_out).write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps(result,indent=2,allow_nan=False))
    if not passed:
        raise SystemExit(2)


if __name__=="__main__":
    main()
