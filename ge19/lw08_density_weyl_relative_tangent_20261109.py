#!/usr/bin/env python3
"""LW08: SHA-locked source-level matter-vs-Weyl relative-tangent audit.

No new CLASS, no DES/ACT values, no projected observable. Motivated by an
already-seen LW06 exploratory alignment; NOT an independent blind discovery.
Calculates additive antisymmetric and symmetric cross-power response
without per-node ratios near transfer zeros.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw08_density_weyl_relative_tangent_predata_20261109.json"
PRE_BLOB="589d3cef1b66a52770db046463eb6d2be032cbfe"
TINY=1e-300

def require(ok, label):
    if not bool(ok):
        raise RuntimeError("GE19_LW08_"+label)

def digest(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for x in iter(lambda:f.read(1<<20),b""):
            h.update(x)
    return h.hexdigest()

def rel_l2(x, ref):
    return float(np.linalg.norm(x)/max(np.linalg.norm(ref),TINY))

def selftest():
    d=np.array([1.,-3.,4.]);w=np.array([2.,0.,-5.])
    td=np.array([.3,.4,.6]);tw=np.array([.7,.8,.9])
    s=td*w+d*tw
    a=d*tw-td*w
    require(np.array_equal(s+a,2*d*tw) and
            np.array_equal(s-a,2*td*w), "SELFTEST_SUM_DIFFERENCE")
    require(np.all(np.isfinite(a)),"SELFTEST_FINITE")
    print("GE19_LW08_ANTISYMMETRIC_SYMMETRIC_SYNTHETIC_PASS",flush=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--lw01-prefix",type=Path,default=ROOT/
        "results/ge19_linear_weyl_native_tangent_20261109_kgridfix")
    ap.add_argument("--lw06-prefix",type=Path,default=ROOT/
        "results/ge19_lw06_native_matter_weyl_cross_20261109_archive_replay")
    ap.add_argument("--output",type=Path,default=ROOT/
        "results/ge19_lw08_density_weyl_relative_tangent_20261109.json")
    args=ap.parse_args()
    if args.self_test:
        selftest()
        return
    require(subprocess.check_output(["git","hash-object",str(PRE)],
                text=True).strip()==PRE_BLOB,"PREDATA_BLOB_CHANGED")
    pre=json.loads(PRE.read_text())
    require(pre["classification"]==
        "GE19_LW08_SOURCE_RELATIVE_GEOMETRY_MATTER_RESPONSE_DIAGNOSTIC_PREDATA",
        "PREDATA_CLASSIFICATION_CHANGED")

    paths={
        "lw01_json":Path(str(args.lw01_prefix)+".json"),
        "lw01_npz":Path(str(args.lw01_prefix)+".npz"),
        "lw06_replay_json":Path(str(args.lw06_prefix)+".json"),
        "lw06_replay_npz":Path(str(args.lw06_prefix)+".npz"),
    }
    for label,p in paths.items():
        require(p.exists() and digest(p)==pre["parent_sha256"][label],
                "PARENT_SHA_"+label)
    j=json.loads(paths["lw01_json"].read_text())
    require(j["classification"]==
        "GE19_LINEAR_WEYL_NATIVE_SIGNED_TANGENT_NUMERICAL_PASS_OBSERVATIONAL_OPEN"
        and all(j["gates"].values()),"LW01_PARENT_NOT_PASS")
    j6=json.loads(paths["lw06_replay_json"].read_text())
    require(j6["classification"]==
        "GE19_LW06_NATIVE_MATTER_WEYL_SIGNED_CROSS_NUMERICAL_PASS_OBSERVATIONAL_OPEN",
        "LW06_PARENT_NOT_PASS")
    with np.load(paths["lw01_npz"],allow_pickle=False) as f:
        a={k:np.asarray(f[k]).copy() for k in f.files}
    with np.load(paths["lw06_replay_npz"],allow_pickle=False) as f:
        b={k:np.asarray(f[k]).copy() for k in f.files}
    k=a["k_native_h"];z=a["z_native"]
    mask=a["primary_mask"]
    ii=np.where(mask.any(axis=1))[0]
    jj=np.where(mask.any(axis=0))[0][::-1]
    lam=a["lambdas"]
    require(k.shape==(912,) and z.shape==(24,) and
            mask.shape==(912,24) and int(mask.sum())==2576 and
            ii.size==322 and jj.size==8 and
            np.array_equal(lam,pre["primary_gates"]["source_lambdas"]),
            "NATIVE_GRID_CHANGED")
    sl=np.ix_(ii,jj)
    d=a["matter_base"][sl];w=a["weyl_base"][sl]
    td=a["matter_tangents"][:,ii,:][:,:,jj]
    tw=a["weyl_tangents"][:,ii,:][:,:,jj]
    cos=67.3324639084866/100
    kphys=k[ii]*cos
    P=(2*np.pi**2/kphys**3)*2.1308864352626987e-9 * (
        kphys/0.05)**(0.9666229454895277-1)
    P=P[:,None]
    Dterm=P[None,:,:]*td*w[None,:,:]
    Wterm=P[None,:,:]*d[None,:,:]*tw
    S=Dterm+Wterm
    A=Wterm-Dterm
    Sm=S.mean(axis=0);Am=A.mean(axis=0)
    mprod=rel_l2(Sm-
      P*(a["matter_signed_mean"][sl]*w+
        d*a["weyl_signed_mean"][sl]),Sm)
    mreference=rel_l2(Sm-b["signed_cross_tangent_mean"],Sm)
    criteria=pre["primary_gates"]
    gates={
        "frozen_mean_product_rule":
            mprod<=criteria["product_rule_L2_error_max"],
        "cross_response_reconstructs_original_LW06":
            mreference<=criteria[
              "symmetric_reconstruction_vs_archived_LW06_L2_error_max"],
        "all_finite":bool(np.isfinite(S).all() and
                          np.isfinite(A).all() and
                          np.isfinite(P).all()),
        "native_primary_nodes":bool(int(mask.sum())==
                                  criteria["exact_primary_nodes"]),
    }
    result={
        "classification":(
            pre["interpretation"]["source_replay_pass"]
            if all(gates.values())
            else pre["interpretation"]["numerical_fail"]),
        "preregistration_git_blob_sha1":PRE_BLOB,
        "history":"LW06 posthoc near-alignment was seen before LW08 predata; not a blind independent check.",
        "parent_sha256":{s:digest(p) for s,p in paths.items()},
        "native_grid":[322,8],"native_nodes":2576,
        "w_over_matter_relative_source_tangent_algebraic":
            "A=P_R*(d_m*T_W-T_d*W); S=P_R*(T_d*W+d_m*T_W)",
        "antisymmetric_to_symmetric_mean_L2_ratio":
            rel_l2(Am,Sm),
        "alignment_cosine_between_mean_terms":
            float(np.sum(Dterm.mean(0)*Wterm.mean(0))/
                  (np.linalg.norm(Dterm.mean(0))*
                   np.linalg.norm(Wterm.mean(0)))),
        "symmetric_reconstruction_reference_relative_L2":mreference,
        "symmetric_reconstruction_product_rule_relative_L2":mprod,
        "by_lambda":[
            {"lambda_numeric":float(lam[i]),
             "antisymmetric_over_symmetric_L2":
                 rel_l2(A[i],S[i]),
             "antisymmetric_affinity_to_mean_relative_L2":
                 rel_l2(A[i]-Am,Am),
             "symmetric_affinity_to_mean_relative_L2":
                 rel_l2(S[i]-Sm,Sm)}
            for i in range(4)],
        "by_z":[{"z":float(z[jj[i]]),
                 "antisymmetric_over_symmetric_L2":
                 rel_l2(Am[:,i],Sm[:,i])}
                 for i in range(8)],
        "gates":gates,
        "antisymmetric_physical_response_numerically_certified":False,
        "reason_antisymmetric_not_certified":
            "Antisymmetric component is a small difference of aligned terms and has large across-lambda affinity; this is a diagnostic, not a preregistered anti-signal stability gate.",
        "gauge_invariant_observed_difference_certified":False,
        "model_history_memory_identified":False,
        "galaxy_galaxy_lensing_certified":False,
        "DES_ACT_observational_detection":False,
        "LW03_radial_FAIL_preserved":True,
        "LW04_time_sampling_PASS_preserved":True,
        "LW05_full_LOS_BLOCK_preserved":True,
        "H4_Z21_certified":False,
    }
    target=args.output.resolve()
    require(target.parent.is_dir() and not target.exists(),
            "OUTPUT_PREEXISTS_OR_DIR")
    target.write_text(json.dumps(result,indent=2,sort_keys=True,
                                 allow_nan=False)+"\n")
    print("GE19_LW08_CLASSIFICATION",result["classification"],flush=True)
    print("GE19_LW08_ANTISYMMETRIC_OVER_SYMMETRIC",
          result["antisymmetric_to_symmetric_mean_L2_ratio"],flush=True)
    print("GE19_LW08_OUTPUT",target,flush=True)

if __name__=="__main__":
    main()
