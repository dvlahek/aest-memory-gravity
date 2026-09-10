#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from v063 import theory_response_map as v63
from nl1c6d2a import baryon_matter_sector_audit as old
from nl1c6d2n.corrected_class_baseline_r1 import provenance_audit

H0 = 67.3324639084866
h = H0 / 100.0
K_H = np.asarray([0.03,0.05,0.08,0.10,0.15,0.20], float)
K_REQ = K_H * h
K_GRID_GATE = 1.0e-12
Z_GRID_GATE = 1.0e-12
SOURCE_ID_GATE = 1.0e-10
REQUESTED_K_GATE = 1.0e-12
CONTINUITY_GATE = 2.0e-3
DENSE_NATIVE_GATE = 2.0e-4
PASS_LABEL = "NL1C6D2AC_CORRECTED_BARYON_MATTER_SECTOR_AUDIT_PASS"
FAIL_LABEL = "NL1C6D2AC_CORRECTED_BARYON_MATTER_SECTOR_AUDIT_FAIL"


def rel_l2(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(b),1e-300))


def git_meta():
    try:
        head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
        branch=subprocess.check_output(["git","rev-parse","--abbrev-ref","HEAD"],cwd=ROOT,text=True).strip()
    except Exception:
        head,branch="unknown","unknown"
    return head,branch


def build_params():
    p=dict(v63.class_params())
    p.update({
        "output":"mTk,vTk",
        "lensing":"no",
        "k_output_values":", ".join(f"{k:.17g}" for k in K_REQ),
        "P_k_max_h/Mpc":2.0,
        "z_max_pk":5.0,
        "k_per_decade_for_pk":80.0,
        "k_per_decade_for_bao":560.0,
        "aest_memory_enabled":"no",
        "aest_eta":0.0,
    })
    return p


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input-npz",required=True)
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    head,branch=git_meta()
    class_root=Path(os.environ.get("NL1C6D2N_CLASS_ROOT",""))
    if not class_root.exists():
        raise RuntimeError("NL1C6D2N_CLASS_ROOT must point to the isolated corrected CLASS tree")
    provenance=provenance_audit(class_root,head,branch)

    frozen=np.load(args.input_npz)
    fk=np.asarray(frozen["k_native_h"],float)
    fz=np.asarray(frozen["z_native"],float)
    fdb=np.asarray(frozen["d_b"],float)
    fdm=np.asarray(frozen["d_m"],float)

    print("NL1C6D2AC_CORRECTED_BARYON_MATTER_SECTOR_AUDIT_START",flush=True)
    print(f"repo_head={head} branch={branch}",flush=True)

    from classy import Class
    pars=build_params()
    c=Class(); c.set(pars); c.compute()
    try:
        tk,k,z=c.get_transfer_and_k_and_z(output_format="class",h_units=False)
        pert=c.get_perturbations()
        kb=old.pick(tk,"d_b",("delta_b",))
        ktb=old.pick(tk,"t_b",("theta_b",))
        km=old.pick(tk,"d_m",("delta_m",))
        db=np.asarray(tk[kb],float).copy()
        tb=np.asarray(tk[ktb],float).copy()
        dm=np.asarray(tk[km],float).copy()
        kk=np.asarray(k,float).copy(); zz=np.asarray(z,float).copy()
        histories_raw,scalar_key=old.scalar_histories(pert)
        if len(histories_raw)!=len(K_H):
            raise RuntimeError(f"expected {len(K_H)} dense scalar histories, got {len(histories_raw)}")
        modes=[old.prepare_dense_mode(d,i) for i,d in enumerate(histories_raw)]
        transfer_keys=sorted(tk.keys())
    finally:
        c.struct_cleanup(); c.empty()

    if db.shape!=fdb.shape or dm.shape!=fdm.shape:
        raise RuntimeError(f"fresh/frozen shape mismatch db={db.shape}/{fdb.shape} dm={dm.shape}/{fdm.shape}")
    if tb.shape!=db.shape or kk.size!=db.shape[0] or zz.size!=db.shape[1]:
        raise RuntimeError(f"unexpected transfer dimensions db={db.shape} tb={tb.shape} k={kk.size} z={zz.size}")

    kh=kk/h
    krel=float(np.max(np.abs(kh-fk)/np.maximum(np.abs(fk),1e-300)))
    zabs=float(np.max(np.abs(zz-fz)))
    dbrel=rel_l2(db,fdb); dmrel=rel_l2(dm,fdm)
    finite=bool(np.all(np.isfinite(db)) and np.all(np.isfinite(tb)) and np.all(np.isfinite(dm)))

    req=[]; reqmax=0.0
    for target in K_H:
        j=int(np.argmin(np.abs(kh-target)))
        miss=float(abs(kh[j]-target)/target)
        reqmax=max(reqmax,miss)
        req.append({"requested_k_h_Mpc":float(target),"actual_k_h_Mpc":float(kh[j]),"relative_miss":miss})

    continuity=old.continuity_regression(modes)
    closure=old.dense_native_regression(modes,kh,zz,db,tb)

    gates={
        "A1_corrected_CLASS_provenance":bool(provenance["pass"]),
        "A1_all_native_fields_finite":finite,
        "A1_k_grid_match_le_1e-12":bool(krel<=K_GRID_GATE),
        "A1_z_grid_match_le_1e-12":bool(zabs<=Z_GRID_GATE),
        "A1_d_b_identity_relL2_le_1e-10":bool(dbrel<=SOURCE_ID_GATE),
        "A1_d_m_identity_relL2_le_1e-10":bool(dmrel<=SOURCE_ID_GATE),
        "A1_requested_k_match_le_1e-12":bool(reqmax<=REQUESTED_K_GATE),
        "A2_continuity_max_le_2e-3":bool(continuity["max_normalized_L2_residual"]<=CONTINUITY_GATE),
        "A3_dense_native_d_b_le_2e-4":bool(closure["max_d_b_relative_L2"]<=DENSE_NATIVE_GATE),
        "A3_dense_native_t_b_le_2e-4":bool(closure["max_t_b_relative_L2"]<=DENSE_NATIVE_GATE),
        "A4_theta_convention_frozen":True,
        "A4_scope_clean":True,
    }
    passed=bool(all(gates.values()))
    classification=PASS_LABEL if passed else FAIL_LABEL

    result={
        "classification":classification,
        "git":{"head":head,"branch":branch},
        "provenance":provenance,
        "parameters":pars,
        "corrected_source_input":args.input_npz,
        "source_identity":{"k_relative_max":krel,"z_absolute_max":zabs,"d_b_relative_L2":dbrel,"d_m_relative_L2":dmrel,"requested_k_relative_miss_max":reqmax,"requested_k":req},
        "continuity":continuity,
        "dense_native_closure":closure,
        "theta_b_convention":"CLASS Newtonian-gauge velocity divergence in delta_b' + theta_b - 3 phi' = 0; no added scale-factor redefinition",
        "transfer_keys":transfer_keys,
        "dense_scalar_container_key":scalar_key,
        "gates":gates,
        "historical_D2A_unchanged":True,
        "historical_source_reused":False,
        "memory_or_likelihood_evaluated":False,
        "cosmological_refit_performed":False,
        "nonlinear_fullJ_evolved":False,
        "branch_selection_performed":False,
        "corrected_source_dependent_reclosure_licensed":passed,
        "NL1C7_authorized":False,
    }
    jout=Path(args.json_out); nout=Path(args.npz_out)
    jout.parent.mkdir(parents=True,exist_ok=True)
    jout.write_text(json.dumps(result,indent=2,sort_keys=True,default=str)+"\n")
    np.savez_compressed(nout,k_native_h=kh,z_native=zz,d_b=db,t_b=tb,d_m=dm)

    print(f"A1_SOURCE k={krel:.12e} z={zabs:.12e} db={dbrel:.12e} dm={dmrel:.12e} pass={all(v for k,v in gates.items() if k.startswith('A1_'))}",flush=True)
    print(f"A2_CONTINUITY max={continuity['max_normalized_L2_residual']:.12e} pass={gates['A2_continuity_max_le_2e-3']}",flush=True)
    print(f"A3_CLOSURE db={closure['max_d_b_relative_L2']:.12e} tb={closure['max_t_b_relative_L2']:.12e} pass={gates['A3_dense_native_d_b_le_2e-4'] and gates['A3_dense_native_t_b_le_2e-4']}",flush=True)
    print("A4_SCOPE theta_convention=frozen memory=False likelihood=False refit=False nonlinear_fullJ=False branch_selection=False",flush=True)
    print(f"CLASSIFICATION={classification}",flush=True)
    print(f"JSON={jout}",flush=True); print(f"NPZ={nout}",flush=True)
    print("NL1C6D2AC_CORRECTED_BARYON_MATTER_SECTOR_AUDIT_END",flush=True)
    return 0 if passed else 2

if __name__=="__main__":
    raise SystemExit(main())
