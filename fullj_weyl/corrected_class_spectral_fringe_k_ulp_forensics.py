#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
from scipy.interpolate import CubicSpline

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import corrected_class_spectral_fringe_parameter_factorization as pf
from fullj_weyl import corrected_class_spectral_fringe_bridge_identity as b

PREDATA_LOCK = "f37f3a9209c010493cafabf5d1b53e96b78cd55e"
PF_JSON = ROOT / "results/fullj_corrected_class_spectral_fringe_parameter_factorization.json"
PF_NPZ = ROOT / "results/fullj_corrected_class_spectral_fringe_parameter_factorization.npz"

INCOMPLETE = "FULLJ_CLASS_FRINGE_K_ULP_FORENSICS_INCOMPLETE"
CONTEXT = "FULLJ_CLASS_FRINGE_K_LIST_CONTEXT_DEPENDENCE"
GENERIC = "FULLJ_CLASS_FRINGE_GENERIC_CLASS_ULP_SENSITIVITY"
AEST_ULP = "FULLJ_CLASS_FRINGE_AEST_ULP_SENSITIVITY_CERTIFIED"
NOT_REPRO = "FULLJ_CLASS_FRINGE_AEST_ULP_SENSITIVITY_NOT_REPRODUCED"

GLOBAL_GATE = 2.0e-5
PERK_GATE = 5.0e-5
GR_ULP_GATE = 1.0e-6
AEST_MATERIAL_GATE = 5.0e-3
SELECTED = np.asarray([0.10125, 0.10250, 0.16250, 0.16500, 0.19750], float)


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel(a, c) -> float:
    aa=np.asarray(a,complex); cc=np.asarray(c,complex)
    return float(np.linalg.norm(aa-cc)/max(float(np.linalg.norm(aa)),float(np.linalg.norm(cc)),1e-300))


def per_k_rel(a, c):
    aa=np.asarray(a); cc=np.asarray(c)
    return [rel(aa[i],cc[i]) for i in range(aa.shape[0])]


def cmp(a, c):
    pp=per_k_rel(a,c)
    return rel(a,c), float(max(pp)), pp


def tokens(text: str):
    return [q.strip() for q in str(text).split(",") if q.strip()]


def join_tokens(ts):
    return ", ".join(str(x) for x in ts)


def eval_field_at_a(raw, names, z, required=True):
    key=None
    for name in names:
        if name in raw:
            key=name; break
    if key is None:
        if required:
            raise RuntimeError(f"missing field among {names}; available={sorted(raw.keys())}")
        return None
    akey=b.base.d2a.pick(raw,"a",("scale factor",))
    aa=np.asarray(raw[akey],float)
    yy=np.asarray(raw[key],float)
    ax,vy=b.clean_xy(aa,yy)
    sp=CubicSpline(ax,vy,bc_type="not-a-knot")
    at=1.0/(1.0+np.asarray(z,float))
    out=np.asarray(sp(at),float)
    if not np.all(np.isfinite(out)):
        raise RuntimeError(f"nonfinite field {key}")
    return out


def eval_fields(pars, pos: int, z, aest: bool):
    p=dict(pars)
    p["aest_enabled"]="yes" if aest else "no"
    hs=b.run_histories(p)
    if pos >= len(hs):
        raise RuntimeError(f"target positional index {pos} outside returned history count {len(hs)}")
    raw=hs[pos]
    phi=eval_field_at_a(raw,("phi",),z)
    psi=eval_field_at_a(raw,("psi",),z)
    out={"phi":phi,"psi":psi,"W":phi+psi,"n_histories":len(hs)}
    if aest:
        alpha=eval_field_at_a(raw,("alpha_aest","alpha"),z,required=False)
        E=eval_field_at_a(raw,("E_aest","E"),z,required=False)
        if alpha is not None: out["alpha_aest"]=alpha
        if E is not None: out["E_aest"]=E
    return out


def float_bits(x: float) -> int:
    a=np.asarray([np.float64(x)],dtype=np.float64)
    return int(a.view(np.uint64)[0])


def bits_float(u: int) -> float:
    a=np.asarray([np.uint64(u)],dtype=np.uint64)
    return float(a.view(np.float64)[0])


def ulp_grid(x0: float, x1: float, max_points: int=17):
    b0=float_bits(x0); b1=float_bits(x1)
    lo=min(b0,b1); hi=max(b0,b1)
    lo2=max(1,lo-1); hi2=hi+1
    count=hi2-lo2+1
    if count <= max_points:
        bits=list(range(lo2,hi2+1))
    else:
        bits=[int(round(v)) for v in np.linspace(lo2,hi2,max_points)]
        bits += [lo2,hi2,b0,b1]
        bits=sorted(set(bits))
    vals=[bits_float(u) for u in bits]
    if not all(np.isfinite(vals)) or not all(v>0 for v in vals):
        raise RuntimeError("invalid ULP ladder")
    return bits,vals,b0,b1


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",default="results/fullj_corrected_class_spectral_fringe_k_ulp_forensics.json")
    ap.add_argument("--npz-out",default="results/fullj_corrected_class_spectral_fringe_k_ulp_forensics.npz")
    args=ap.parse_args()

    print("FULLJ_CLASS_FRINGE_K_ULP_FORENSICS_START",flush=True)
    if not PF_JSON.exists() or not PF_NPZ.exists():
        out={"classification":INCOMPLETE,"diagnostic_complete":False,"reason":"missing parameter-factorization result"}
        Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("FULLJ_CLASS_FRINGE_K_ULP_FORENSICS_CLASSIFICATION="+INCOMPLETE,flush=True)
        return 3

    pj=json.loads(PF_JSON.read_text())
    pq=np.load(PF_NPZ)
    anchors=np.asarray(pq["anchors"],float)
    z=np.asarray(pq["redshifts"],float)
    C00=np.asarray(pq["C00"],float)
    C01=np.asarray(pq["C01"],float)
    frozen=bool(
        is_ancestor(PREDATA_LOCK)
        and pj.get("classification")=="FULLJ_CLASS_FRINGE_K_SERIALIZATION_DEPENDENCE"
        and pj.get("diagnostic_complete") is True
        and all(bool(v) for v in pj.get("gates",{}).values())
        and C00.shape==(15,9) and C01.shape==(15,9)
        and np.all(np.isfinite(C00)) and np.all(np.isfinite(C01))
    )

    T=np.full_like(C00,np.nan)
    O=np.full_like(C00,np.nan)
    token_rows=[]

    for ik,kh in enumerate(anchors):
        mode_h=np.asarray(b.sd.poc.target_modes(float(kh)),float)
        q=np.where(np.isclose(mode_h,float(kh),rtol=0,atol=5e-13))[0]
        if len(q)!=1: raise RuntimeError(f"target {kh} not unique in bridge list")
        pos=int(q[0])
        p00,_=b.r3_params(mode_h)
        p11=b.bridge_params(mode_h)
        t00=tokens(p00["k_output_values"]); t11=tokens(p11["k_output_values"])
        if len(t00)!=len(t11) or pos>=len(t00): raise RuntimeError("token list mismatch")

        tt=list(t00); tt[pos]=t11[pos]
        ot=list(t11); ot[pos]=t00[pos]
        pT=dict(p00); pT["k_output_values"]=join_tokens(tt)
        pO=dict(p00); pO["k_output_values"]=join_tokens(ot)
        T[ik],_=pf.eval_target(pT,pos,z)
        O[ik],_=pf.eval_target(pO,pos,z)

        parsed00=np.asarray([float(x) for x in t00],float)
        parsed11=np.asarray([float(x) for x in t11],float)
        changed=[int(i) for i in range(len(t00)) if parsed00[i]!=parsed11[i]]
        target_changed=bool(parsed00[pos]!=parsed11[pos])
        token_rows.append({
            "k_h":float(kh),"target_pos":pos,"target_changed":target_changed,
            "changed_token_indices":changed,
            "target_15":t00[pos],"target_historical":t11[pos],
            "target_abs_delta_1_per_Mpc":float(abs(parsed11[pos]-parsed00[pos])),
        })
        print(
            f"FULLJ_CLASS_FRINGE_K_ULP_TOKEN {ik+1:02d}/15 k_h={kh:.5f} "
            f"pos={pos} target_changed={target_changed} changed={changed}",flush=True
        )

    eT,mT,pTrel=cmp(T,C01)
    eO,mO,pOrel=cmp(O,C00)
    g1=frozen
    g2=bool(eT<=GLOBAL_GATE and mT<=PERK_GATE and eO<=GLOBAL_GATE and mO<=PERK_GATE)

    ulp_rows=[]
    npz_payload={"anchors":anchors,"redshifts":z,"T_target_only":T,"O_others_only":O,"C00":C00,"C01":C01}
    max_gr=0.0; max_ae=0.0; base_repro=[]

    for kh in SELECTED:
        ii=np.where(np.isclose(anchors,float(kh),rtol=0,atol=5e-13))[0]
        if len(ii)!=1: raise RuntimeError(f"selected anchor {kh} not found")
        ia=int(ii[0])
        mode_h=np.asarray(b.sd.poc.target_modes(float(kh)),float)
        pos=int(np.where(np.isclose(mode_h,float(kh),rtol=0,atol=5e-13))[0][0])
        p00,_=b.r3_params(mode_h); p11=b.bridge_params(mode_h)
        t00=tokens(p00["k_output_values"]); t11=tokens(p11["k_output_values"])
        x15=float(t00[pos]); x17=float(t11[pos])
        bits,vals,b15,b17=ulp_grid(x15,x17,17)

        aest_W=[]; gr_W=[]; aest_phi=[]; aest_psi=[]; gr_phi=[]; gr_psi=[]
        alpha_rows=[]; E_rows=[]
        for jj,(ub,x) in enumerate(zip(bits,vals)):
            tx=list(t00); tx[pos]=format(x,".17g")
            p=dict(p00); p["k_output_values"]=join_tokens(tx)
            ae=eval_fields(p,pos,z,True)
            gr=eval_fields(p,pos,z,False)
            aest_W.append(ae["W"]); gr_W.append(gr["W"])
            aest_phi.append(ae["phi"]); aest_psi.append(ae["psi"])
            gr_phi.append(gr["phi"]); gr_psi.append(gr["psi"])
            if "alpha_aest" in ae: alpha_rows.append(ae["alpha_aest"])
            if "E_aest" in ae: E_rows.append(ae["E_aest"])
            print(
                f"FULLJ_CLASS_FRINGE_K_ULP_POINT k_h={kh:.5f} {jj+1:02d}/{len(vals):02d} "
                f"bits={ub} k_Mpc={x:.17g}",flush=True
            )

        aest_W=np.asarray(aest_W,float); gr_W=np.asarray(gr_W,float)
        aest_phi=np.asarray(aest_phi,float); aest_psi=np.asarray(aest_psi,float)
        gr_phi=np.asarray(gr_phi,float); gr_psi=np.asarray(gr_psi,float)
        ibase=bits.index(b15); ihist=bits.index(b17)
        ae_rel=[rel(aest_W[j],aest_W[ibase]) for j in range(len(bits))]
        gr_rel=[rel(gr_W[j],gr_W[ibase]) for j in range(len(bits))]
        adj=[rel(aest_W[j+1],aest_W[j]) for j in range(len(bits)-1)]
        adj_sum=float(sum(adj)); concentration=float(max(adj)/adj_sum) if adj_sum>0 else 0.0
        ae_max=float(max(ae_rel)); gr_max=float(max(gr_rel))
        max_ae=max(max_ae,ae_max); max_gr=max(max_gr,gr_max)
        base_rel=rel(aest_W[ibase],C00[ia]); base_repro.append(base_rel)
        row={
            "k_h":float(kh),"target_pos":pos,
            "target_15_token":t00[pos],"target_historical_token":t11[pos],
            "k15_Mpc":x15,"k17_Mpc":x17,"bit15":int(b15),"bit17":int(b17),
            "endpoint_ulp_distance":int(abs(b17-b15)),
            "ladder_points":len(bits),"ladder_bits":[int(u) for u in bits],
            "ladder_k_Mpc":[float(x) for x in vals],
            "aest_rel_from_15":[float(x) for x in ae_rel],
            "gr_rel_from_15":[float(x) for x in gr_rel],
            "aest_endpoint_relL2":float(rel(aest_W[ihist],aest_W[ibase])),
            "gr_endpoint_relL2":float(rel(gr_W[ihist],gr_W[ibase])),
            "aest_max_relL2":ae_max,"gr_max_relL2":gr_max,
            "aest_adjacent_relL2":[float(x) for x in adj],
            "jump_concentration":concentration,
            "base_vs_locked_C00_relL2":float(base_rel),
            "aest_W_z0p2":[float(x) for x in aest_W[:,-1]],
            "gr_W_z0p2":[float(x) for x in gr_W[:,-1]],
        }
        ulp_rows.append(row)
        key=str(f"{kh:.5f}").replace(".","p")
        npz_payload[f"bits_{key}"]=np.asarray(bits,np.uint64)
        npz_payload[f"k_Mpc_{key}"]=np.asarray(vals,float)
        npz_payload[f"aest_W_{key}"]=aest_W
        npz_payload[f"gr_W_{key}"]=gr_W
        npz_payload[f"aest_phi_{key}"]=aest_phi
        npz_payload[f"aest_psi_{key}"]=aest_psi
        npz_payload[f"gr_phi_{key}"]=gr_phi
        npz_payload[f"gr_psi_{key}"]=gr_psi
        if alpha_rows: npz_payload[f"aest_alpha_{key}"]=np.asarray(alpha_rows,float)
        if E_rows: npz_payload[f"aest_E_{key}"]=np.asarray(E_rows,float)
        print(
            f"FULLJ_CLASS_FRINGE_K_ULP_ANCHOR k_h={kh:.5f} ulp_distance={abs(b17-b15)} "
            f"ae_max={ae_max:.6e} gr_max={gr_max:.6e} jump_concentration={concentration:.6f}",flush=True
        )

    max_base_repro=float(max(base_repro)) if base_repro else float("inf")
    g1=bool(g1 and max_base_repro<=PERK_GATE)
    g3=bool(max_gr<=GR_ULP_GATE)
    g4=bool(max_ae>AEST_MATERIAL_GATE)

    if not g1:
        classification=INCOMPLETE
    elif not g2:
        classification=CONTEXT
    elif not g3:
        classification=GENERIC
    elif g4:
        classification=AEST_ULP
    else:
        classification=NOT_REPRO

    gates={
        "UF_G1_provenance_parent_and_base_identity":g1,
        "UF_G2_target_token_locality":g2,
        "UF_G3_matched_GR_ULP_continuity":g3,
        "UF_G4_AeST_material_ULP_sensitivity":g4,
    }
    summary={
        "target_only_T_vs_C01_global_relative_L2":eT,
        "target_only_T_vs_C01_per_k_max":mT,
        "others_only_O_vs_C00_global_relative_L2":eO,
        "others_only_O_vs_C00_per_k_max":mO,
        "selected_base_vs_locked_C00_max_relative_L2":max_base_repro,
        "max_AeST_ULP_relative_L2":float(max_ae),
        "max_GR_ULP_relative_L2":float(max_gr),
        "selected_anchors":SELECTED.tolist(),
    }
    out={
        "classification":classification,"diagnostic_complete":True,"predata_lock":PREDATA_LOCK,
        "gates":gates,"summary":summary,"token_rows":token_rows,"ulp_rows":ulp_rows,
        "thresholds":{
            "global":GLOBAL_GATE,"per_k":PERK_GATE,
            "GR_ULP_continuity":GR_ULP_GATE,"AeST_material_ULP":AEST_MATERIAL_GATE,
        },
        "interpretation":{
            "historical_R3_reclassified":False,
            "parameter_factorization_reclassified":False,
            "equation_level_followup_licensed":False,
            "new_physics_claim_licensed":False,
            "source_level_or_stability_followup_required":classification==AEST_ULP,
        },
    }
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out,**npz_payload)
    print("FULLJ_CLASS_FRINGE_K_ULP_FORENSICS_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("FULLJ_CLASS_FRINGE_K_ULP_FORENSICS_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("FULLJ_CLASS_FRINGE_K_ULP_FORENSICS_CLASSIFICATION="+classification,flush=True)
    return 0


if __name__=="__main__":
    raise SystemExit(main())
