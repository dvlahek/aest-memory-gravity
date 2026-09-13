#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
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

PREDATA_LOCK = "167a556247e334a4a3652d61b365a4d8af3b523f"
PARENT_JSON = ROOT / "results/fullj_aest_stable_chi_residual.json"
Z = np.asarray([6.,5.,4.,3.,2.,1.5,1.,0.5,0.2], float)
TOLS = (1e-5, 3e-6, 1e-6, 3e-7)
PATH_PAIRS = amp.PAIRS
CALM = (0.09875, 0.10250, 0.10375)
HELD = (0.10000, 0.16125, 0.19500, 0.19875)
UNIQUE = (0.09875, 0.10000, 0.10125, 0.10250, 0.10375, 0.16125, 0.16500, 0.19500, 0.19750, 0.19875)

INCOMPLETE = "FULLJ_AEST_STABLE_CHI_PRECISION_AUDIT_INCOMPLETE"
NOT_CONV = "FULLJ_AEST_STABLE_CHI_NOT_PRECISION_CONVERGED"
ULP_FAIL = "FULLJ_AEST_STABLE_CHI_ULP_RECOVERY_NOT_ROBUST"
IDENT_FAIL = "FULLJ_AEST_STABLE_CHI_IDENTITY_NOT_ROBUST"
RESOLVED = "FULLJ_AEST_STABLE_CHI_NUMERICALLY_RESOLVED_COORDINATE"
EQUIV = "FULLJ_AEST_STABLE_CHI_EQUIVALENT_CONVERGED_SOLUTION"


def is_ancestor(sha: str) -> bool:
    return subprocess.run(["git","merge-base","--is-ancestor",sha,"HEAD"], cwd=ROOT,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def rel(a,b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    return float(np.linalg.norm(aa-bb)/max(float(np.linalg.norm(aa)),float(np.linalg.norm(bb)),1e-300))


def tag_of(kh: float) -> str:
    return f"{kh:.5f}".replace(".","p")


def target_setup(kh: float):
    mode_h=np.asarray(b.sd.poc.target_modes(float(kh)),float)
    q=np.where(np.isclose(mode_h,float(kh),rtol=0,atol=5e-13))[0]
    if len(q)!=1:
        raise RuntimeError(f"target {kh} not unique")
    pos=int(q[0]); p00,_=b.r3_params(mode_h); tt=amp.tokens(p00["k_output_values"])
    return pos,p00,tt


def direct_bits(kh: float):
    pos,_,tt=target_setup(kh)
    x=float(tt[pos])
    return int(ulp.float_bits(x))


def bits_for_anchor(kh: float):
    for _,(pkh,ba,_) in PATH_PAIRS.items():
        if abs(float(kh)-float(pkh)) < 5e-13:
            return int(ba)
    return direct_bits(kh)


def raw_for(kh: float, bits: int, tol: float):
    p,pos=amp.make_params(kh,int(bits))
    p["tol_perturbations_integration"] = float(tol)
    raw,nh=amp.raw_target(p,pos,True)
    return raw,int(nh),int(pos),float(ulp.bits_float(int(bits)))


def field_at_z(raw,names):
    at=1.0/(1.0+Z)
    return amp.interp(raw,names,at)[0]


def W_at_z(raw):
    return field_at_z(raw,("phi",))+field_at_z(raw,("psi",))


def dense_s_identity(raw,k_mpc: float):
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


def collect(mode: str, out_npz: Path, out_json: Path):
    stable=(mode=="stable")
    arrays={}; rows=[]; identities=[]; held=[]
    for tol in TOLS:
        tl=f"{tol:.0e}".replace("-","m")
        for kh in UNIQUE:
            bits=bits_for_anchor(kh)
            raw,nh,pos,kval=raw_for(kh,bits,tol)
            W=W_at_z(raw); tag=tag_of(kh)
            arrays[f"W_{tl}_{tag}"]=W
            rows.append({"tol":tol,"k_h":kh,"bits":bits,"n_histories":nh,"target_pos":pos})
            if stable and tol==TOLS[-1] and any(abs(kh-v[0])<5e-13 for v in PATH_PAIRS.values()):
                sid,n=dense_s_identity(raw,kval)
                identities.append({"k_h":kh,"s_identity_relL2":sid,"point_count":n})
        print(f"FULLJ_AEST_STABLE_CHI_PRECISION_COLLECT mode={mode} tol={tol:.1e} anchors={len(UNIQUE)}",flush=True)

    if stable:
        tol=TOLS[-1]; tl=f"{tol:.0e}".replace("-","m")
        for kh in HELD:
            ba=direct_bits(kh); bb=ba+1
            rawA,_,_,_=raw_for(kh,ba,tol); rawB,_,_,_=raw_for(kh,bb,tol)
            WA=W_at_z(rawA); WB=W_at_z(rawB); wr=rel(WA,WB)
            held.append({"k_h":kh,"bits_A":ba,"bits_B":bb,"W_relL2":wr})
            arrays[f"held_A_{tl}_{tag_of(kh)}"]=WA; arrays[f"held_B_{tl}_{tag_of(kh)}"]=WB
            print(f"FULLJ_AEST_STABLE_CHI_PRECISION_HELD k_h={kh:.5f} W={wr:.6e}",flush=True)

    np.savez_compressed(out_npz,redshifts=Z,**arrays)
    meta={"mode":mode,"tolerances":list(TOLS),"anchors":list(UNIQUE),"rows":rows,
          "heldout":held,"identities":identities}
    out_json.write_text(json.dumps(meta,indent=2,sort_keys=True)+"\n")
    return 0


def tie_ge(a: float,b: float) -> bool:
    # Accept a>=b, or a numerical tie within 2% relative / 1e-12 absolute.
    if a>=b: return True
    return abs(a-b) <= max(1e-12,0.02*max(abs(a),abs(b),1e-300))


def aggregate(old_npz: Path, stable_npz: Path, stable_json: Path, out_json: Path, out_npz: Path):
    if not PARENT_JSON.exists():
        raise RuntimeError("missing stable-chi parent result")
    parent=json.loads(PARENT_JSON.read_text())
    O=np.load(old_npz); S=np.load(stable_npz); sm=json.loads(stable_json.read_text())
    g1=bool(is_ancestor(PREDATA_LOCK) and parent.get("classification")=="FULLJ_AEST_STABLE_CHI_REFERENCE_MISMATCH")

    anchor_rows=[]; stable_tight=[]; stable_mono=0; old_mono=0; dos=[]
    arrays={}
    tight=TOLS[-1]
    for kh in UNIQUE:
        tag=tag_of(kh); cS=[]; cO=[]
        WSt=np.asarray(S[f"W_{f'{tight:.0e}'.replace('-','m')}_{tag}"],float)
        WOt=np.asarray(O[f"W_{f'{tight:.0e}'.replace('-','m')}_{tag}"],float)
        for tol in TOLS[:-1]:
            tl=f"{tol:.0e}".replace("-","m")
            cS.append(rel(S[f"W_{tl}_{tag}"],WSt)); cO.append(rel(O[f"W_{tl}_{tag}"],WOt))
        cs1,cs2,cs3=cS; co1,co2,co3=cO
        smono=bool(tie_ge(cs1,cs2) and tie_ge(cs2,cs3)); omono=bool(tie_ge(co1,co2) and tie_ge(co2,co3))
        stable_mono+=int(smono); old_mono+=int(omono)
        d=rel(WOt,WSt); dos.append(d); stable_tight.append(cs3)
        anchor_rows.append({"k_h":kh,"C_stable_1e5":cs1,"C_stable_3e6":cs2,"C_stable_1e6":cs3,
                            "stable_monotone":smono,"C_old_1e5":co1,"C_old_3e6":co2,"C_old_1e6":co3,
                            "old_monotone":omono,"D_old_stable_tight":d})
        arrays[f"W_old_tight_{tag}"]=WOt; arrays[f"W_stable_tight_{tag}"]=WSt
        print(f"FULLJ_AEST_STABLE_CHI_PRECISION_ANCHOR k_h={kh:.5f} Cs={cs3:.3e} Co={co3:.3e} D={d:.3e} smono={smono} omono={omono}",flush=True)

    g2=bool(sum(v<=2e-3 for v in stable_tight)>=8 and max(stable_tight)<=1e-2 and float(np.median(stable_tight))<=5e-4)
    g3=bool(stable_mono>=8)
    held=sm.get("heldout",[]); hvals=[float(x["W_relL2"]) for x in held]
    g5=bool(len(hvals)==4 and sum(v<=1e-4 for v in hvals)>=3 and max(hvals)<=1e-3)
    ids=sm.get("identities",[]); ivals=[float(x["s_identity_relL2"]) for x in ids]
    g6=bool(len(ivals)==4 and sum(v<=1e-4 for v in ivals)>=3)

    gates={"PC_G1_provenance_and_parent_lock":g1,
           "PC_G2_stable_tight_tolerance_convergence":g2,
           "PC_G3_stable_convergence_trend":g3,
           "PC_G5_stable_adjacent_ULP_preservation":g5,
           "PC_G6_stable_residual_identity":g6}
    medD=float(np.median(dos))
    if not g1: classification=INCOMPLETE
    elif not g2 or not g3: classification=NOT_CONV
    elif not g5: classification=ULP_FAIL
    elif not g6: classification=IDENT_FAIL
    elif medD>1e-2: classification=RESOLVED
    else: classification=EQUIV

    summary={"classification":classification,"anchor_count":len(UNIQUE),"stable_monotone_count":stable_mono,
             "old_monotone_count":old_mono,"median_stable_C_1e6":float(np.median(stable_tight)),
             "max_stable_C_1e6":float(max(stable_tight)),"median_D_old_stable_tight":medD,
             "max_D_old_stable_tight":float(max(dos)),"max_heldout_W_relL2":float(max(hvals)) if hvals else None,
             "max_identity_relL2":float(max(ivals)) if ivals else None}
    out={"classification":classification,"diagnostic_complete":True,"predata_lock":PREDATA_LOCK,
         "parent_classification":parent.get("classification"),"gates":gates,"summary":summary,
         "anchors":anchor_rows,"heldout":held,"identities":ids,
         "interpretation":{"historical_R3_reclassified":False,"new_physics_claim_licensed":False,
                            "physical_instability_claim_licensed":False,
                            "stable_AeST_host_followup_licensed":classification in (RESOLVED,EQUIV)}}
    out_json.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(out_npz,redshifts=Z,**arrays)
    print("FULLJ_AEST_STABLE_CHI_PRECISION_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("FULLJ_AEST_STABLE_CHI_PRECISION_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("FULLJ_AEST_STABLE_CHI_PRECISION_CLASSIFICATION="+classification,flush=True)
    return 0 if classification in (RESOLVED,EQUIV) else 1


def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd",required=True)
    c=sub.add_parser("collect"); c.add_argument("--mode",choices=("old","stable"),required=True); c.add_argument("--npz-out",required=True); c.add_argument("--json-out",required=True)
    a=sub.add_parser("aggregate"); a.add_argument("--old-npz",required=True); a.add_argument("--stable-npz",required=True); a.add_argument("--stable-json",required=True); a.add_argument("--json-out",required=True); a.add_argument("--npz-out",required=True)
    args=ap.parse_args()
    if args.cmd=="collect": return collect(args.mode,Path(args.npz_out),Path(args.json_out))
    return aggregate(Path(args.old_npz),Path(args.stable_npz),Path(args.stable_json),Path(args.json_out),Path(args.npz_out))


if __name__=="__main__":
    raise SystemExit(main())
