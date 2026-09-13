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
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import aest_ulp_initial_amplitude_localization as amp
from fullj_weyl import corrected_class_spectral_fringe_bridge_identity as b
from fullj_weyl import corrected_class_spectral_fringe_k_ulp_forensics as ulp

PREDATA_LOCK = "63d673b0e7f6349a2a10c762aac970f301646abd"
POSTHOC_LOCK = "9e3d8e51fc3013894d071e3d1850177110866287"
PARENT_JSON = ROOT / "results/fullj_aest_ulp_initial_amplitude_localization.json"
PARENT_NPZ = ROOT / "results/fullj_aest_ulp_initial_amplitude_localization.npz"
Z = np.asarray([6.,5.,4.,3.,2.,1.5,1.,0.5,0.2], float)
PATH_PAIRS = amp.PAIRS
HELDOUT = (0.10000, 0.16125, 0.19500, 0.19875)
CALM = (0.09875, 0.10250, 0.10375)

INCOMPLETE = "FULLJ_AEST_STABLE_CHI_RESIDUAL_INCOMPLETE"
REF_MISMATCH = "FULLJ_AEST_STABLE_CHI_REFERENCE_MISMATCH"
REGRESSION = "FULLJ_AEST_STABLE_CHI_GROSS_REGRESSION"
PERSISTS = "FULLJ_AEST_STABLE_CHI_PATHOLOGY_PERSISTS"
IMPROVE = "FULLJ_AEST_STABLE_CHI_IMPROVEMENT_INSUFFICIENT"
HELD_FAIL = "FULLJ_AEST_STABLE_CHI_HELDOUT_CONTINUITY_FAIL"
IDENTITY_FAIL = "FULLJ_AEST_STABLE_CHI_IDENTITY_CONTROL_FAIL"
PASS = "FULLJ_AEST_STABLE_CHI_RESIDUAL_REFORMULATION_CERTIFIED"


def is_ancestor(sha: str) -> bool:
    return subprocess.run(["git","merge-base","--is-ancestor",sha,"HEAD"], cwd=ROOT,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def rel(a,b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    return float(np.linalg.norm(aa-bb)/max(float(np.linalg.norm(aa)),float(np.linalg.norm(bb)),1e-300))


def target_setup(kh: float):
    mode_h=np.asarray(b.sd.poc.target_modes(float(kh)),float)
    q=np.where(np.isclose(mode_h,float(kh),rtol=0,atol=5e-13))[0]
    if len(q)!=1:
        raise RuntimeError(f"target {kh} not unique")
    pos=int(q[0])
    p00,_=b.r3_params(mode_h)
    tt=amp.tokens(p00["k_output_values"])
    return mode_h,pos,p00,tt


def direct_bits(kh: float):
    _,pos,_,tt=target_setup(kh)
    x=float(tt[pos])
    return ulp.float_bits(x),x,pos


def raw_for_bits(kh: float, bits: int):
    p,pos=amp.make_params(kh,int(bits))
    raw,nh=amp.raw_target(p,pos,True)
    return raw,int(nh),int(pos),ulp.bits_float(int(bits))


def field_at_z(raw, names):
    at=1.0/(1.0+Z)
    return amp.interp(raw,names,at)[0]


def fields_z(raw, require_s=False):
    phi=field_at_z(raw,("phi",)); psi=field_at_z(raw,("psi",))
    out={"W":phi+psi,"alpha":field_at_z(raw,("alpha_aest","alpha")),"E":field_at_z(raw,("E_aest","E"))}
    if require_s:
        out["s"]=field_at_z(raw,("s_aest",))
    return out


def interp_parent_to_z(a, y):
    aa=np.asarray(a,float); yy=np.asarray(y,float)
    at=1.0/(1.0+Z)
    return np.interp(at,aa,yy)


def dense_s_identity(raw, k_mpc: float):
    akey=b.base.d2a.pick(raw,"a",("scale factor",))
    alpha_key=amp.field_key(raw,("alpha_aest","alpha"))
    s_key=amp.field_key(raw,("s_aest",))
    theta_key=amp.field_key(raw,("theta_cdm",))
    a=np.asarray(raw[akey],float); alpha=np.asarray(raw[alpha_key],float)
    s=np.asarray(raw[s_key],float); theta=np.asarray(raw[theta_key],float)
    good=np.isfinite(a)&np.isfinite(alpha)&np.isfinite(s)&np.isfinite(theta)&(a>0)
    a=a[good]; alpha=alpha[good]; s=s[good]; theta=theta[good]
    tp=a*theta/(float(k_mpc)**2)
    scale=np.abs(tp)+np.abs(alpha)
    mask=np.abs(s) >= 1e-8*np.maximum(scale,1e-300)
    if np.count_nonzero(mask)<8:
        return float("inf"),int(np.count_nonzero(mask))
    return rel(s[mask],(tp+alpha)[mask]),int(np.count_nonzero(mask))


def make_reference(out_json: Path, out_npz: Path):
    if not PARENT_JSON.exists() or not PARENT_NPZ.exists():
        raise RuntimeError("missing parent amplitude result")
    pj=json.loads(PARENT_JSON.read_text()); pq=np.load(PARENT_NPZ)
    if pj.get("classification")!="FULLJ_AEST_ULP_LATE_EVOLUTION_DIVERGENCE":
        raise RuntimeError("wrong parent classification")

    payload={}; rows=[]; max_repro=0.0
    for tag,(kh,ba,bb) in PATH_PAIRS.items():
        parent_a=np.asarray(pq[f"a_{tag}"],float)
        parent_zA=interp_parent_to_z(parent_a,pq[f"W_A_{tag}"])
        parent_zB=interp_parent_to_z(parent_a,pq[f"W_B_{tag}"])
        parent_rel=rel(parent_zA,parent_zB)
        rr=[]
        for ep,bits in (("A",ba),("B",bb)):
            raw,_,_,_=raw_for_bits(kh,bits)
            wz=fields_z(raw)["W"]
            pref=parent_zA if ep=="A" else parent_zB
            e=rel(wz,pref); rr.append(e); max_repro=max(max_repro,e)
            payload[f"path_parent_W_{ep}_{tag}"]=pref
        rows.append({"tag":tag,"k_h":float(kh),"parent_W_z_relL2":parent_rel,
                     "reproduce_A_relL2":rr[0],"reproduce_B_relL2":rr[1]})

    calm=[]
    for kh in CALM:
        bits,_,_=direct_bits(kh)
        raw,_,_,_=raw_for_bits(kh,bits)
        W=fields_z(raw)["W"]
        tag=f"{kh:.5f}".replace(".","p")
        payload[f"calm_W_{tag}"]=W
        calm.append({"k_h":float(kh),"bits":int(bits),"tag":tag})

    out={"parent_classification":pj["classification"],"pathological":rows,"calm":calm,
         "max_parent_reproduction_relL2":float(max_repro),"redshifts":Z.tolist()}
    out_json.parent.mkdir(parents=True,exist_ok=True)
    out_json.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(out_npz,**payload)
    print("FULLJ_AEST_STABLE_CHI_REFERENCE_SUMMARY="+json.dumps({"max_parent_reproduction_relL2":max_repro},sort_keys=True),flush=True)
    return 0


def source_audit_ok():
    root=os.environ.get("AEST_STABLE_CLASS_ROOT","")
    if not root:
        return False
    ph=Path(root)/"include/perturbations.h"; pc=Path(root)/"source/perturbations.c"
    if not ph.is_file() or not pc.is_file():
        return False
    h=ph.read_text(); s=pc.read_text()
    req=[
        "FULLJ_AEST_STABLE_CHI_RESIDUAL_V1","index_pt_s_aest",
        "double chi_aest = Q_aest*s_aest;",
        "3.*cad2_aest*a_prime_over_a*(s_aest-alpha_aest)",
        "dy[pv->index_pt_alpha_aest] = a*(E_aest-psi_aest);",
        "dy[pv->index_pt_E_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest;",
    ]
    return all(x in (h+s) for x in req) and s.count("double chi_aest = Q_aest*s_aest;")==2


def run_stable(ref_json: Path, ref_npz: Path, out_json: Path, out_npz: Path):
    rj=json.loads(ref_json.read_text()); rq=np.load(ref_npz)
    pj=json.loads(PARENT_JSON.read_text())
    g1=bool(is_ancestor(PREDATA_LOCK) and is_ancestor(POSTHOC_LOCK) and source_audit_ok()
            and pj.get("classification")=="FULLJ_AEST_ULP_LATE_EVOLUTION_DIVERGENCE")
    g2=bool(float(rj["max_parent_reproduction_relL2"])<=2e-5)

    payload={}; calm_rows=[]
    for c in rj["calm"]:
        kh=float(c["k_h"]); bits=int(c["bits"]); tag=c["tag"]
        raw,_,_,_=raw_for_bits(kh,bits); W=fields_z(raw,True)["W"]
        e=rel(W,rq[f"calm_W_{tag}"])
        calm_rows.append({"k_h":kh,"relL2":e}); payload[f"calm_stable_W_{tag}"]=W
    calm_vals=[x["relL2"] for x in calm_rows]
    g3=bool(sum(x<=5e-3 for x in calm_vals)>=2 and max(calm_vals)<=2e-2)

    parent_map={r["tag"]:r for r in rj["pathological"]}
    path_rows=[]; improvements=[]; path_pass=0; identity_pass=0
    for tag,(kh,ba,bb) in PATH_PAIRS.items():
        vals={}; rawA=None; kA=None
        for ep,bits in (("A",ba),("B",bb)):
            raw,_,pos,kval=raw_for_bits(kh,bits); f=fields_z(raw,True); vals[ep]=f
            for n,v in f.items(): payload[f"path_{n}_{ep}_{tag}"]=v
            if ep=="A": rawA=raw; kA=kval
        wrel=rel(vals["A"]["W"],vals["B"]["W"])
        arel=rel(vals["A"]["alpha"],vals["B"]["alpha"])
        erel=rel(vals["A"]["E"],vals["B"]["E"])
        ok=bool(wrel<=1e-4 and arel<=1e-3 and erel<=1e-3); path_pass+=int(ok)
        parent_rel=float(parent_map[tag]["parent_W_z_relL2"])
        imp=parent_rel/max(wrel,1e-300); improvements.append(imp)
        sid,nmask=dense_s_identity(rawA,kA); identity_pass+=int(sid<=1e-4)
        path_rows.append({"tag":tag,"k_h":float(kh),"W_relL2":wrel,"alpha_relL2":arel,"E_relL2":erel,
                          "parent_W_z_relL2":parent_rel,"improvement":imp,
                          "s_identity_relL2":sid,"s_identity_point_count":nmask})
        print(f"FULLJ_AEST_STABLE_CHI_PATH k_h={kh:.5f} W={wrel:.6e} alpha={arel:.6e} E={erel:.6e} improvement={imp:.3e} sid={sid:.3e}",flush=True)

    g4=bool(path_pass>=3 and max(r["W_relL2"] for r in path_rows)<=1e-3)
    g5=bool(float(np.median(improvements))>=1e3 and sum(x>=1e2 for x in improvements)>=3)

    held_rows=[]; held_pass=0
    for kh in HELDOUT:
        b0,_,_=direct_bits(kh); b1=int(b0)+1
        fvals={}
        for ep,bits in (("A",b0),("B",b1)):
            raw,_,_,_=raw_for_bits(kh,bits); fvals[ep]=fields_z(raw,True)
        wr=rel(fvals["A"]["W"],fvals["B"]["W"]); held_pass+=int(wr<=1e-4)
        held_rows.append({"k_h":float(kh),"bits_A":int(b0),"bits_B":int(b1),"W_relL2":wr})
        print(f"FULLJ_AEST_STABLE_CHI_HELDOUT k_h={kh:.5f} W={wr:.6e}",flush=True)
    g6=bool(held_pass>=3 and max(r["W_relL2"] for r in held_rows)<=1e-3)
    g7=bool(identity_pass>=3)

    gates={
        "SR_G1_provenance_and_exact_reformulation_audit":g1,
        "SR_G2_unmodified_reference_reproduction":g2,
        "SR_G3_calm_control_regression":g3,
        "SR_G4_pathological_pair_continuity_recovery":g4,
        "SR_G5_material_improvement_over_parent":g5,
        "SR_G6_heldout_adjacent_ULP_continuity":g6,
        "SR_G7_residual_state_consistency":g7,
    }
    if not g1: classification=INCOMPLETE
    elif not g2: classification=REF_MISMATCH
    elif not g3: classification=REGRESSION
    elif not g4: classification=PERSISTS
    elif not g5: classification=IMPROVE
    elif not g6: classification=HELD_FAIL
    elif not g7: classification=IDENTITY_FAIL
    else: classification=PASS

    summary={
        "classification":classification,"pathological_pass_count":int(path_pass),
        "heldout_pass_count":int(held_pass),"identity_pass_count":int(identity_pass),
        "median_improvement":float(np.median(improvements)),"min_improvement":float(min(improvements)),
        "max_stable_pathological_W_relL2":float(max(r["W_relL2"] for r in path_rows)),
        "max_heldout_W_relL2":float(max(r["W_relL2"] for r in held_rows)),
        "max_calm_regression_relL2":float(max(calm_vals)),
    }
    out={"classification":classification,"diagnostic_complete":True,"predata_lock":PREDATA_LOCK,
         "posthoc_lock":POSTHOC_LOCK,"gates":gates,"summary":summary,
         "pathological":path_rows,"heldout":held_rows,"calm":calm_rows,
         "interpretation":{
             "historical_R3_reclassified":False,"new_physics_claim_licensed":False,
             "physical_instability_claim_licensed":False,
             "stable_AeST_host_followup_licensed":bool(classification==PASS),
         }}
    out_json.parent.mkdir(parents=True,exist_ok=True); out_json.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(out_npz,redshifts=Z,**payload)
    print("FULLJ_AEST_STABLE_CHI_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("FULLJ_AEST_STABLE_CHI_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("FULLJ_AEST_STABLE_CHI_CLASSIFICATION="+classification,flush=True)
    return 0 if classification==PASS else 1


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=("reference","stable"),required=True)
    ap.add_argument("--reference-json",default="results/fullj_aest_stable_chi_reference.json")
    ap.add_argument("--reference-npz",default="results/fullj_aest_stable_chi_reference.npz")
    ap.add_argument("--json-out",default="results/fullj_aest_stable_chi_residual.json")
    ap.add_argument("--npz-out",default="results/fullj_aest_stable_chi_residual.npz")
    args=ap.parse_args()
    if args.mode=="reference":
        return make_reference(Path(args.reference_json),Path(args.reference_npz))
    return run_stable(Path(args.reference_json),Path(args.reference_npz),Path(args.json_out),Path(args.npz_out))


if __name__=="__main__":
    raise SystemExit(main())
