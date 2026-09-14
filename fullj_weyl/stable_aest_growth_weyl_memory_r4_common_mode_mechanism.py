#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import aest_ulp_initial_amplitude_localization as amp
from fullj_weyl import aest_stable_chi_precision_convergence as pc
from fullj_weyl import stable_aest_growth_weyl_memory_r3_scale_generality as r3

PREDATA_LOCK = "f742cfb33bd00ec8e1b637d7d1e7201d464fc433"
R3_POSTDATA_LOCK = "8094cf2a3a40659419e64ea0c45fd27491decae3"
R3_JSON = ROOT / "results/stable_aest_growth_weyl_memory_r3_scale_generality.json"
R2E_JSON = ROOT / "results/stable_aest_growth_weyl_memory_r2e_single_hook.json"
R1C_JSON = ROOT / "results/stable_aest_finite_memory_r1c.json"
HOST_JSON = ROOT / "results/fullj_aest_stable_chi_precision_floor.json"

R3_CLASS = "STABLE_AEST_GROWTH_WEYL_MEMORY_R3_SCALE_GENERALITY_CERTIFIED"
R2E_CLASS = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_ABSOLUTE_COMMON_MODE_CERTIFIED"
R1C_CLASS = "STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED"
HOST_CLASS = "FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED"

ANCHORS = (0.10000, 0.10125, 0.10250, 0.10375, 0.16500, 0.19750, 0.19875)
ETAS = (0.0, 0.005, 0.01)
TAU = 10.0
ORDER = 20
TOL = 3e-8
Z = np.asarray([6., 5., 4., 3., 2., 1.5, 1., 0.5, 0.2], float)
HI = np.where(Z >= 3.0)[0]
LATE = np.where(Z <= 2.0)[0]

CLS_INCOMPLETE = "STABLE_AEST_GROWTH_WEYL_MEMORY_R4_INCOMPLETE"
CLS_SOURCE = "STABLE_AEST_GROWTH_WEYL_MEMORY_R4_SOURCE_TOPOLOGY_FAIL"
CLS_BASIS = "STABLE_AEST_GROWTH_WEYL_MEMORY_R4_TRANSFER_BASIS_FAIL"
CLS_TAN = "STABLE_AEST_GROWTH_WEYL_MEMORY_R4_TANGENT_FAIL"
CLS_MODE = "STABLE_AEST_GROWTH_WEYL_MEMORY_R4_SINGLE_AMPLITUDE_MODE_CERTIFIED"
CLS_SLIP = "STABLE_AEST_GROWTH_WEYL_MEMORY_R4_COMMON_MODE_WITH_SLIP_RESPONSE"
CLS_UNRES = "STABLE_AEST_GROWTH_WEYL_MEMORY_R4_MECHANISM_UNRESOLVED"


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel(a, b) -> float:
    a = np.asarray(a, float); b = np.asarray(b, float)
    return float(np.linalg.norm(a-b) / max(float(np.linalg.norm(a)), float(np.linalg.norm(b)), 1e-300))


def cosine(a, b) -> float:
    a = np.asarray(a, float); b = np.asarray(b, float)
    na = float(np.linalg.norm(a)); nb = float(np.linalg.norm(b))
    if na <= 0.0 or nb <= 0.0:
        return float("nan")
    return float(np.dot(a, b)/(na*nb))


def rms(a) -> float:
    a = np.asarray(a, float)
    return float(np.sqrt(np.mean(a*a)))


def tag(kh: float) -> str:
    return pc.tag_of(float(kh))


def derivs_block(text: str) -> str:
    start = text.find("int perturbations_derivs(")
    if start < 0:
        return ""
    rest = text[start + 1:]
    m = re.search(r"\nint\s+perturbations_[A-Za-z0-9_]+\s*\(", rest)
    if m is None:
        return text[start:]
    return text[start:start + 1 + m.start()]


def source_topology():
    root = os.environ.get("AEST_STABLE_CLASS_ROOT", "")
    if not root:
        return False, {"reason": "AEST_STABLE_CLASS_ROOT missing"}
    pc_path = Path(root) / "source" / "perturbations.c"
    if not pc_path.is_file():
        return False, {"reason": "perturbations.c missing"}
    text = pc_path.read_text()
    body = derivs_block(text)
    eta_mul = body.count("Bchi_aest *= pba->aest_eta;")
    closure = body.count("E_rhs_aest -= 0.5*Q_aest*Bchi_aest;")
    eta_refs = body.count("pba->aest_eta")
    external = body.count("aest_tangent_external_force")
    checks = {
        "stable_marker": "FULLJ_AEST_STABLE_CHI_RESIDUAL_V1" in text,
        "stable_chi_rhs": "double chi_aest = Q_aest*s_aest;" in body,
        "alpha_rhs": "dy[pv->index_pt_alpha_aest] = a*(E_aest-psi_aest);" in body,
        "stable_s_rhs": "3.*cad2_aest*a_prime_over_a*(s_aest-alpha_aest)" in body,
        "physical_eta_multiply_once": eta_mul == 1,
        "physical_memory_closure_once": closure == 1,
        "physical_eta_rhs_reference_once": eta_refs == 1,
        "diagnostic_external_force_absent": external == 0,
    }
    meta = {"checks": checks, "eta_multiply_count": eta_mul, "closure_count": closure,
            "eta_reference_count_in_derivs": eta_refs, "external_force_count_in_derivs": external}
    return bool(all(checks.values())), meta


def run_case(kh: float, eta: float):
    from classy import Class

    bits = pc.bits_for_anchor(float(kh))
    p, pos = amp.make_params(float(kh), int(bits))
    p["tol_perturbations_integration"] = float(TOL)
    p["aest_memory_enabled"] = "yes"
    p["aest_memory_order"] = int(ORDER)
    p["aest_eta"] = float(eta)
    p["aest_tau_H0"] = float(TAU)
    p["output"] = "mTk,vTk"
    p["z_max_pk"] = max(float(p.get("z_max_pk", 0.0)), 6.5)

    c = Class(); c.set(p); c.compute()
    try:
        h = r3.classy_h(c)
        D=[]; P=[]; S=[]; W=[]; domains=[]; keys=[]
        for z in Z:
            tr = c.get_transfer(z=float(z), output_format="class")
            missing = [x for x in ("d_m", "phi", "psi") if x not in tr]
            if missing:
                raise RuntimeError(f"missing transfer fields {missing}; keys={sorted(tr.keys())}")
            kg, kkey = r3.k_h_from_transfer(tr, h)
            dm, klo, khi, nk = r3.interp_transfer_field(kg, tr["d_m"], kh)
            ph, _, _, _ = r3.interp_transfer_field(kg, tr["phi"], kh)
            ps, _, _, _ = r3.interp_transfer_field(kg, tr["psi"], kh)
            D.append(dm); P.append(ph); S.append(ps); W.append(ph+ps)
            domains.append((klo,khi,nk)); keys.append(kkey)
        D=np.asarray(D,float); P=np.asarray(P,float); S=np.asarray(S,float); W=np.asarray(W,float)
        finite = bool(np.all(np.isfinite(D)) and np.all(np.isfinite(P)) and np.all(np.isfinite(S)) and np.all(np.isfinite(W)))
        denom = bool(np.all(np.abs(D)>1e-300) and np.all(np.abs(P)>1e-300) and np.all(np.abs(S)>1e-300) and np.all(np.abs(W)>1e-300))
        domain_ok = bool(all(d[0] <= kh <= d[1] and d[2] >= 4 for d in domains))
        keys_ok = bool(len(set(keys)) == 1)
        return {"D":D,"P":P,"S":S,"W":W,"finite":finite,"denom":denom,
                "basis_pass":bool(finite and denom and domain_ok and keys_ok),
                "bits":int(bits),"target_pos":int(pos),"h":float(h),
                "k_key":keys[0] if keys else None,
                "min_k_h":float(min(d[0] for d in domains)),
                "max_k_h":float(max(d[1] for d in domains)),
                "min_k_count":int(min(d[2] for d in domains))}
    finally:
        c.struct_cleanup(); c.empty()


def tangent(xe, x0, eta):
    return (np.asarray(xe,float)-np.asarray(x0,float))/(float(eta)*np.asarray(x0,float))


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/stable_aest_growth_weyl_memory_r4_common_mode_mechanism.json")
    ap.add_argument("--npz-out", default="results/stable_aest_growth_weyl_memory_r4_common_mode_mechanism.npz")
    args=ap.parse_args()

    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R4_START", flush=True)

    required=(R3_JSON,R2E_JSON,R1C_JSON,HOST_JSON)
    if not all(p.exists() for p in required):
        out={"classification":CLS_INCOMPLETE,"diagnostic_complete":False,"reason":"missing parent json"}
        Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("STABLE_AEST_GROWTH_WEYL_MEMORY_R4_CLASSIFICATION="+CLS_INCOMPLETE,flush=True)
        return 3

    r3j=json.loads(R3_JSON.read_text()); r2e=json.loads(R2E_JSON.read_text())
    r1c=json.loads(R1C_JSON.read_text()); host=json.loads(HOST_JSON.read_text())
    g1=bool(ancestor(PREDATA_LOCK) and ancestor(R3_POSTDATA_LOCK)
            and r3j.get("classification")==R3_CLASS
            and r2e.get("classification")==R2E_CLASS
            and r1c.get("classification")==R1C_CLASS
            and host.get("classification")==HOST_CLASS)

    g2, source_meta = source_topology()
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R4_SOURCE "+json.dumps(source_meta,sort_keys=True),flush=True)

    vals={}; run_rows=[]; arrays={"redshifts":Z}; basis_all=True
    for kh in ANCHORS:
        for eta in ETAS:
            try:
                v=run_case(kh,eta); vals[(kh,eta)]=v
                basis_all &= v["basis_pass"]
                t=tag(kh); et=f"{eta:.3f}".replace(".","p")
                for key in ("D","P","S","W"):
                    arrays[f"{key}_{t}_e{et}"]=v[key]
                row={k:v[k] for k in ("bits","target_pos","h","k_key","min_k_h","max_k_h","min_k_count","finite","denom","basis_pass")}
                row.update({"k_h":kh,"eta":eta}); run_rows.append(row)
                print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R4_RUN k_h={kh:.5f} eta={eta:.3g} finite={v['finite']} basis={v['basis_pass']}",flush=True)
            except Exception as e:
                basis_all=False; run_rows.append({"k_h":kh,"eta":eta,"finite":False,"basis_pass":False,"error":repr(e)})
                print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R4_RUN_FAIL k_h={kh:.5f} eta={eta:.3g} error={e!r}",flush=True)

    g3=bool(basis_all and len(vals)==len(ANCHORS)*len(ETAS))
    cells=[]; tan_strict_count=0; tan_loose_all=True; amp_strict_count=0; amp_loose_all=True
    slip_strict_count=0; slip_loose_all=True; late_count=0

    if g3:
        for kh in ANCHORS:
            t=tag(kh); b=vals[(kh,0.0)]
            tang={}
            tan_metrics={}; strict=True; loose=True
            for eta,label in ((0.005,"005"),(0.01,"01")):
                ve=vals[(kh,eta)]
                for key in ("D","P","S","W"):
                    tang[(key,label)]=tangent(ve[key],b[key],eta)
                    arrays[f"T{key}{label}_{t}"]=tang[(key,label)]
            for key in ("D","P","S","W"):
                e=rel(tang[(key,"005")],tang[(key,"01")]); c=cosine(tang[(key,"005")],tang[(key,"01")])
                tan_metrics[f"E_{key}"]=e; tan_metrics[f"C_{key}"]=c
                strict &= bool(e<=.02 and c>=.999)
                loose &= bool(e<=.05 and c>=.995)
            tan_strict_count += int(strict); tan_loose_all &= loose

            TD=tang[("D","01")]; TP=tang[("P","01")]; TS=tang[("S","01")]; TW=tang[("W","01")]
            bphi=rel(TP,TD); bpsi=rel(TS,TD); bwd=rel(TW,TD); bslip=rel(TP,TS)
            amp_strict=bool(bphi<=.01 and bpsi<=.01 and bwd<=.01)
            amp_loose=bool(bphi<=.05 and bpsi<=.05 and bwd<=.05)
            slip_strict=bool(bslip<=.01); slip_loose=bool(bslip<=.05)
            amp_strict_count += int(amp_strict); amp_loose_all &= amp_loose
            slip_strict_count += int(slip_strict); slip_loose_all &= slip_loose

            fD=rms(TD[LATE])/max(rms(TD[HI]),1e-300); fW=rms(TW[LATE])/max(rms(TW[HI]),1e-300)
            late_nonzero=all(np.isfinite(np.linalg.norm(x[LATE])) and float(np.linalg.norm(x[LATE]))>0.0 for x in (TD,TP,TS,TW))
            late_pass=bool(late_nonzero and fD>=2.0 and fW>=2.0)
            late_count += int(late_pass)

            row={"k_h":kh,**tan_metrics,"tangent_strict":strict,"tangent_loose":loose,
                 "B_phiD":bphi,"B_psiD":bpsi,"B_WD":bwd,"B_slip":bslip,
                 "amplitude_strict":amp_strict,"amplitude_loose":amp_loose,
                 "slip_strict":slip_strict,"slip_loose":slip_loose,
                 "F_late_D":fD,"F_late_W":fW,"late_pass":late_pass,
                 "norm_D01":float(np.linalg.norm(TD)),"norm_phi01":float(np.linalg.norm(TP)),
                 "norm_psi01":float(np.linalg.norm(TS)),"norm_W01":float(np.linalg.norm(TW))}
            cells.append(row)
            print("STABLE_AEST_GROWTH_WEYL_MEMORY_R4_CELL "+json.dumps(row,sort_keys=True),flush=True)

    g4=bool(g3 and tan_strict_count>=6 and tan_loose_all)
    g5=bool(g4 and amp_strict_count>=6 and amp_loose_all)
    g6=bool(g4 and slip_strict_count>=6 and slip_loose_all)
    g7=bool(g4 and late_count==len(ANCHORS))

    gates={"R4_G1_provenance_and_parent_lock":g1,
           "R4_G2_single_channel_source_topology":g2,
           "R4_G3_transfer_basis_and_finite_run_validity":g3,
           "R4_G4_individual_finite_eta_tangent_consistency":g4,
           "R4_G5_single_amplitude_metric_matter_response":g5,
           "R4_G6_slip_invariance":g6,
           "R4_G7_late_time_activation":g7}

    if not g1: cls=CLS_INCOMPLETE
    elif not g2: cls=CLS_SOURCE
    elif not g3: cls=CLS_BASIS
    elif not g4: cls=CLS_TAN
    elif g5 and g6 and g7: cls=CLS_MODE
    elif g5 and (not g6) and g7: cls=CLS_SLIP
    else: cls=CLS_UNRES

    summary={"classification":cls,"run_count":len(run_rows),"tangent_strict_count":tan_strict_count,
             "amplitude_strict_count":amp_strict_count,"slip_strict_count":slip_strict_count,
             "late_pass_count":late_count}
    if cells:
        summary.update({"max_B_phiD":float(max(r["B_phiD"] for r in cells)),
                        "max_B_psiD":float(max(r["B_psiD"] for r in cells)),
                        "max_B_WD":float(max(r["B_WD"] for r in cells)),
                        "max_B_slip":float(max(r["B_slip"] for r in cells))})

    out={"classification":cls,"diagnostic_complete":True,"predata_lock":PREDATA_LOCK,
         "r3_parent_classification":r3j.get("classification"),"source_topology":source_meta,
         "settings":{"anchors":ANCHORS,"etas":ETAS,"tau_H0":TAU,"memory_order":ORDER,
                     "tol_perturbations_integration":TOL,"redshifts":Z.tolist(),
                     "science_method":"direct physical finite-eta; separate phi and psi; no diagnostic variational forcing"},
         "runs":run_rows,"cells":cells,"gates":gates,"summary":summary,
         "interpretation":{"single_direct_memory_channel_licensed":bool(g2),
                           "single_amplitude_mode_licensed":cls==CLS_MODE,
                           "common_mode_with_slip_response":cls==CLS_SLIP,
                           "observable_projection_licensed":cls in (CLS_MODE,CLS_SLIP),
                           "observational_claim_licensed":False,
                           "positive_growth_weyl_separation_licensed":False}}
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out,**arrays)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R4_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R4_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R4_CLASSIFICATION="+cls,flush=True)
    return 0 if cls in (CLS_MODE,CLS_SLIP) else 1


if __name__ == "__main__":
    raise SystemExit(main())
