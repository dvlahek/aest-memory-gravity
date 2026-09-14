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
from fullj_weyl import aest_stable_chi_precision_convergence as pc
from fullj_weyl import stable_aest_finite_memory_r1 as r1

PREDATA_LOCK = "1543d7bd47eca7401b046b84f5f929298da92e1e"
POSTDATA_LOCK = "bfc94abbbddeacc0d803cfeaaadbbdb7bd2e9e72"
R1_JSON = ROOT / "results/stable_aest_finite_memory_r1.json"
R1_NPZ = ROOT / "results/stable_aest_finite_memory_r1.npz"
HOST_JSON = ROOT / "results/fullj_aest_stable_chi_precision_floor.json"
R1_CLASS = "STABLE_AEST_FINITE_MEMORY_R1_ETA_SMOOTHNESS_FAIL"
HOST_CLASS = "FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED"

Z = np.asarray([6.,5.,4.,3.,2.,1.5,1.,0.5,0.2], float)
ANCHORS = (0.10000, 0.16500, 0.19750)
ETAS = (0.0025, 0.005, 0.01)
TAUS = (1.0, 10.0)
PRIMARY_TOL = 1e-7
TIGHT_TOL = 3e-8
ORDER = 16

INCOMPLETE = "STABLE_AEST_FINITE_MEMORY_R1B_INCOMPLETE"
BASE_FAIL = "STABLE_AEST_FINITE_MEMORY_R1B_MATCHED_BASELINE_FAIL"
ETA_FAIL = "STABLE_AEST_FINITE_MEMORY_R1B_ETA_TANGENT_FAIL"
TOL_FAIL = "STABLE_AEST_FINITE_MEMORY_R1B_TOLERANCE_FAIL"
UNRESOLVED = "STABLE_AEST_FINITE_MEMORY_R1B_RESPONSE_UNRESOLVED"
TAU_FAIL = "STABLE_AEST_FINITE_MEMORY_R1B_RELAXATION_TIME_FAIL"
PASS = "STABLE_AEST_FINITE_MEMORY_R1B_MATCHED_TANGENT_CERTIFIED"


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git","merge-base","--is-ancestor",sha,"HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel(a,b) -> float:
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    return float(np.linalg.norm(aa-bb)/max(float(np.linalg.norm(aa)),float(np.linalg.norm(bb)),1e-300))


def cosine(a,b) -> float:
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    na=float(np.linalg.norm(aa)); nb=float(np.linalg.norm(bb))
    if na <= 1e-300 or nb <= 1e-300:
        return float("nan")
    return float(np.dot(aa,bb)/(na*nb))


def amplitude(delta,base) -> float:
    dd=np.asarray(delta,float); bb=np.asarray(base,float)
    return float(np.linalg.norm(dd)/max(float(np.linalg.norm(bb)),1e-300))


def source_audit_ok() -> bool:
    root=os.environ.get("AEST_STABLE_CLASS_ROOT","")
    if not root:
        return False
    root=Path(root)
    files=[root/"include/background.h", root/"include/perturbations.h", root/"source/perturbations.c"]
    if not all(p.is_file() for p in files):
        return False
    text="\n".join(p.read_text() for p in files)
    req=(
        "FULLJ_AEST_STABLE_CHI_RESIDUAL_V1",
        "double chi_aest = Q_aest*s_aest;",
        "aest_memory_enabled",
        "aest_eta",
        "aest_tau_H0",
        "aest_memory_order",
        "E_rhs_aest -= 0.5*Q_aest*Bchi_aest",
    )
    return all(x in text for x in req) and text.count("double chi_aest = Q_aest*s_aest;") >= 2


def run_case(kh: float, eta: float, tau: float, tol: float):
    bits=pc.bits_for_anchor(kh)
    p,pos=amp.make_params(kh,int(bits))
    p["tol_perturbations_integration"]=float(tol)
    p["aest_memory_enabled"]="yes"
    p["aest_eta"]=float(eta)
    p["aest_tau_H0"]=float(tau)
    p["aest_memory_order"]=int(ORDER)
    raw,nh=amp.raw_target(p,pos,True)
    vals=r1.extract(raw)
    finite=all(np.all(np.isfinite(v)) for v in vals.values())
    return vals,int(nh),int(pos),int(bits),bool(finite)


def parent_mem_key(name: str, kh: float, eta: float, tau: float) -> str:
    return f"mem_{name}_e{r1.key_eta(eta)}_t{r1.key_tau(tau)}_{pc.tag_of(kh)}"


def parent_zero_key(name: str, kh: float) -> str:
    return f"eta0_{name}_{pc.tag_of(kh)}"


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",default="results/stable_aest_finite_memory_r1b.json")
    ap.add_argument("--npz-out",default="results/stable_aest_finite_memory_r1b.npz")
    args=ap.parse_args()

    print("STABLE_AEST_FINITE_MEMORY_R1B_START",flush=True)
    if not R1_JSON.exists() or not R1_NPZ.exists() or not HOST_JSON.exists():
        out={"classification":INCOMPLETE,"diagnostic_complete":False,"reason":"missing R1 or host parent files"}
        Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("STABLE_AEST_FINITE_MEMORY_R1B_CLASSIFICATION="+INCOMPLETE,flush=True)
        return 3

    r1j=json.loads(R1_JSON.read_text()); host=json.loads(HOST_JSON.read_text()); P=np.load(R1_NPZ)
    expected=[]
    for tau in TAUS:
        for eta in ETAS:
            for kh in ANCHORS:
                expected.append(parent_mem_key("W",kh,eta,tau))
    for kh in ANCHORS:
        expected.append(parent_zero_key("W",kh))
    g1=bool(
        is_ancestor(PREDATA_LOCK) and is_ancestor(POSTDATA_LOCK)
        and r1j.get("classification")==R1_CLASS and r1j.get("diagnostic_complete") is True
        and host.get("classification")==HOST_CLASS and host.get("diagnostic_complete") is True
        and source_audit_ok() and all(k in P for k in expected)
        and abs(float(r1j.get("settings",{}).get("tol_perturbations_integration",0))-PRIMARY_TOL)<1e-20
        and int(r1j.get("settings",{}).get("memory_order",0))==ORDER
    )

    arrays={"redshifts":Z}
    primary_zero={}
    new_rows=[]

    # Primary matched eta=0. tau=10 is frozen R1 parent data; tau=1 is newly generated.
    for kh in ANCHORS:
        tag=pc.tag_of(kh)
        z10={name:np.asarray(P[parent_zero_key(name,kh)],float) for name in ("W","delta","alpha","E","s")}
        primary_zero[(kh,10.0)]=z10
        for name,v in z10.items(): arrays[f"primary_eta0_{name}_t10_{tag}"]=v
        print(f"STABLE_AEST_FINITE_MEMORY_R1B_PRIMARY_ZERO_REUSE k_h={kh:.5f} tau=10",flush=True)

        vals,nh,pos,bits,finite=run_case(kh,0.0,1.0,PRIMARY_TOL)
        primary_zero[(kh,1.0)]={name:vals[name] for name in ("W","delta","alpha","E","s")}
        for name,v in primary_zero[(kh,1.0)].items(): arrays[f"primary_eta0_{name}_t1_{tag}"]=v
        new_rows.append({"k_h":kh,"tau_H0":1.0,"eta":0.0,"tol":PRIMARY_TOL,"finite":finite,"histories":nh})
        print(f"STABLE_AEST_FINITE_MEMORY_R1B_PRIMARY_ZERO k_h={kh:.5f} tau=1 finite={finite} histories={nh} pos={pos}",flush=True)

    # Primary matched tangents from frozen R1 finite-eta histories.
    primary_q={}
    eta_rows=[]; eta_strict=0; eta_loose_all=True
    for tau in TAUS:
        for kh in ANCHORS:
            q={}
            for eta in ETAS:
                W=np.asarray(P[parent_mem_key("W",kh,eta,tau)],float)
                d=W-primary_zero[(kh,tau)]["W"]
                q[eta]=d/eta
                tag=pc.tag_of(kh)
                arrays[f"primary_dW_e{r1.key_eta(eta)}_t{r1.key_tau(tau)}_{tag}"]=d
                arrays[f"primary_qW_e{r1.key_eta(eta)}_t{r1.key_tau(tau)}_{tag}"]=q[eta]
            e1=rel(q[0.0025],q[0.005]); e2=rel(q[0.005],q[0.01]); mx=max(e1,e2)
            strict=bool(mx<=0.05); loose=bool(mx<=0.10)
            eta_strict+=int(strict); eta_loose_all &= loose
            primary_q[(kh,tau)]=q
            eta_rows.append({"k_h":kh,"tau_H0":tau,"E_25_50":e1,"E_50_100":e2,"max_E":mx,"strict_pass":strict,"loose_pass":loose})
            print(f"STABLE_AEST_FINITE_MEMORY_R1B_ETA k_h={kh:.5f} tau={tau:.0f} E25_50={e1:.3e} E50_100={e2:.3e} strict={strict}",flush=True)

    # Tight matched pairs eta=0 and eta=.01 for both taus.
    tight={}; all_new_finite=True
    for tau in TAUS:
        for kh in ANCHORS:
            for eta in (0.0,0.01):
                vals,nh,pos,bits,finite=run_case(kh,eta,tau,TIGHT_TOL)
                tight[(kh,tau,eta)]=vals
                all_new_finite &= finite
                tag=pc.tag_of(kh)
                for name in ("W","delta","alpha","E","s"):
                    arrays[f"tight_{name}_e{r1.key_eta(eta)}_t{r1.key_tau(tau)}_{tag}"]=vals[name]
                new_rows.append({"k_h":kh,"tau_H0":tau,"eta":eta,"tol":TIGHT_TOL,"finite":finite,"histories":nh})
                print(f"STABLE_AEST_FINITE_MEMORY_R1B_TIGHT k_h={kh:.5f} tau={tau:.0f} eta={eta:.3g} finite={finite} histories={nh} pos={pos}",flush=True)

    # G2: finite baselines; reused tau=10 primary is exact parent reuse (reproduction error zero by construction).
    primary_tau1_finite=all(r["finite"] for r in new_rows if r["tol"]==PRIMARY_TOL and r["eta"]==0.0)
    tight_zero_finite=all(r["finite"] for r in new_rows if r["tol"]==TIGHT_TOL and r["eta"]==0.0)
    tau10_repro=[{"k_h":kh,"W_relL2":0.0,"exact_parent_reuse":True} for kh in ANCHORS]
    g2=bool(primary_tau1_finite and tight_zero_finite and all_new_finite)

    # G3 eta tangent.
    g3=bool(eta_strict>=5 and eta_loose_all)

    # G4 tolerance reproducibility and G5 response resolution.
    tol_rows=[]; tol_strict=0; tol_loose_all=True; response_cells=0; nonzero_all=True
    tight_q={}
    for tau in TAUS:
        for kh in ANCHORS:
            dT=tight[(kh,tau,0.01)]["W"]-tight[(kh,tau,0.0)]["W"]
            qT=dT/0.01; qP=primary_q[(kh,tau)][0.01]
            tight_q[(kh,tau)]=qT
            ct=rel(qP,qT); cs=cosine(qP,qT)
            strict=bool(np.isfinite(cs) and ct<=0.10 and cs>=0.99)
            loose=bool(np.isfinite(cs) and ct<=0.20 and cs>=0.95)
            tol_strict+=int(strict); tol_loose_all &= loose
            ampM=amplitude(dT,tight[(kh,tau,0.0)]["W"])
            nz=bool(np.all(np.isfinite(qT)) and float(np.linalg.norm(qT))>1e-300)
            nonzero_all &= nz
            response_cells += int(ampM>=1e-12)
            tag=pc.tag_of(kh)
            arrays[f"tight_dW_t{r1.key_tau(tau)}_{tag}"]=dT
            arrays[f"tight_qW_t{r1.key_tau(tau)}_{tag}"]=qT
            tol_rows.append({"k_h":kh,"tau_H0":tau,"C_tol":ct,"cosine":cs,"strict_pass":strict,"loose_pass":loose,"A_M_W":ampM,"nonzero":nz})
            print(f"STABLE_AEST_FINITE_MEMORY_R1B_TOL k_h={kh:.5f} tau={tau:.0f} C={ct:.3e} cos={cs:.9f} A={ampM:.3e} strict={strict}",flush=True)
    g4=bool(tol_strict>=5 and tol_loose_all)
    g5=bool(nonzero_all and response_cells>=4)

    # G6 matched tangent relaxation-time dependence.
    tau_rows=[]; tau_pass=0
    for kh in ANCHORS:
        tt=rel(tight_q[(kh,10.0)],tight_q[(kh,1.0)])
        finite=bool(np.isfinite(tt))
        passed=bool(finite and tt>=0.02)
        tau_pass+=int(passed)
        tau_rows.append({"k_h":kh,"T_tau":tt,"finite":finite,"pass":passed})
        print(f"STABLE_AEST_FINITE_MEMORY_R1B_TAU k_h={kh:.5f} T_tau={tt:.3e} pass={passed}",flush=True)
    g6=bool(tau_pass>=2 and all(r["finite"] for r in tau_rows))

    gates={
        "R1B_G1_provenance_and_parent_lock":g1,
        "R1B_G2_matched_eta0_regularity":g2,
        "R1B_G3_primary_eta_tangent_consistency":g3,
        "R1B_G4_tight_tolerance_tangent_reproducibility":g4,
        "R1B_G5_nonzero_matched_coupling_response":g5,
        "R1B_G6_relaxation_time_dependence":g6,
    }
    if not g1: classification=INCOMPLETE
    elif not g2: classification=BASE_FAIL
    elif not g3: classification=ETA_FAIL
    elif not g4: classification=TOL_FAIL
    elif not g5: classification=UNRESOLVED
    elif not g6: classification=TAU_FAIL
    else: classification=PASS

    summary={
        "classification":classification,
        "anchor_count":len(ANCHORS),
        "new_run_count":len(new_rows),
        "eta_strict_pass_count":eta_strict,
        "tol_strict_pass_count":tol_strict,
        "resolved_response_cell_count":response_cells,
        "tau_dependence_pass_count":tau_pass,
        "max_primary_eta_tangent_error":float(max(r["max_E"] for r in eta_rows)),
        "max_tolerance_tangent_error":float(max(r["C_tol"] for r in tol_rows)),
        "min_tolerance_cosine":float(min(r["cosine"] for r in tol_rows)),
        "min_matched_A_W":float(min(r["A_M_W"] for r in tol_rows)),
        "min_T_tau":float(min(r["T_tau"] for r in tau_rows)),
    }
    out={
        "classification":classification,"diagnostic_complete":True,
        "predata_lock":PREDATA_LOCK,"r1_parent_classification":r1j.get("classification"),
        "host_parent_classification":host.get("classification"),
        "settings":{"anchors":list(ANCHORS),"etas_primary":list(ETAS),"taus_H0":list(TAUS),"primary_tol":PRIMARY_TOL,"tight_tol":TIGHT_TOL,"memory_order":ORDER,"redshifts":Z.tolist()},
        "gates":gates,"summary":summary,"eta_tangent":eta_rows,"tolerance_tangent":tol_rows,"tau_dependence":tau_rows,"new_runs":new_rows,"tau10_primary_baseline_reuse":tau10_repro,
        "interpretation":{"historical_R1_reclassified":False,"historical_results_reclassified":False,"observational_claim_licensed":False,"new_physics_claim_licensed":False,"permanent_elasticity_loss_claim_licensed":False,"stable_AeST_growth_Weyl_memory_followup_licensed":classification==PASS},
    }
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out,**arrays)
    print("STABLE_AEST_FINITE_MEMORY_R1B_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_FINITE_MEMORY_R1B_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("STABLE_AEST_FINITE_MEMORY_R1B_CLASSIFICATION="+classification,flush=True)
    return 0 if classification==PASS else 1

if __name__=="__main__":
    raise SystemExit(main())
