#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import stable_aest_observable_projection_r5b_derivative_zero as r5b
from fullj_weyl import stable_aest_desi_dr1_r9b2b_source_state_extraction as r9b2b

PREFIT_LOCK = "bb15759f23246d3b7af734ff7f7cb2052f44d651"
R9B2C_POSTDATA_LOCK = "7c4cc8a0a9f2a59a91cbb288a157f880d630f309"
R9B2C_IMPL_LOCK = "cb15af792b6d2deca3c495a47f75238986e85c00"
R9B2B_POSTDATA_LOCK = "3101581468bc8a5b85eb2b34c33df22418f1ce88"
R9B2A_POSTDATA_LOCK = "00d06aa140fc8e9097be3df62ecd6013f0c8b312"

ZEFF = np.asarray([
    0.29536404346937617, 0.5096288678782911, 0.7057956472488681,
    0.9185851971138159, 1.3170658832980264, 1.4905017757527006,
], float)
TOL = 3.0e-8
TAU = 10.0
REL_GATE = 5.0e-3
MATERIAL_GATE = 5.0e-2
NODE_RATIO_GATE = 4.0
DENSE_PK = 80.0
DENSE_BAO = 560.0

PASS = "STABLE_AEST_DESI_DR1_R9B2D_DENSE_K_FORENSIC_INHERITANCE_DEFECT_CERTIFIED"
CFG_FAIL = "STABLE_AEST_DESI_DR1_R9B2D_CONFIGURATION_ISOLATION_FAIL"
SEP_FAIL = "STABLE_AEST_DESI_DR1_R9B2D_KGRID_SEPARATION_NOT_REPRODUCED"
GR_FAIL = "STABLE_AEST_DESI_DR1_R9B2D_GR_KGRID_CONTROL_FAIL"
DEFAULT_FAIL = "STABLE_AEST_DESI_DR1_R9B2D_DEFAULT_GRID_AEST_UNRESOLVED"
CAUSE_FAIL = "STABLE_AEST_DESI_DR1_R9B2D_DENSE_GRID_CAUSE_NOT_REPRODUCED"
INTERNAL_FAIL = "STABLE_AEST_DESI_DR1_R9B2D_INTERNAL_SOLUTION_KGRID_SENSITIVE"
RUN_FAIL = "STABLE_AEST_DESI_DR1_R9B2D_RUN_FAIL"


def ancestor(sha: str) -> bool:
    return subprocess.run(["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def rel(a: float, b: float) -> float:
    aa=float(a); bb=float(b)
    return abs(aa-bb)/max(abs(aa),abs(bb),1e-300)


def params_dense():
    p, _, _ = r5b.build_params(0.0, TOL)
    p["aest_tau_H0"] = TAU
    p["output"] = "mPk,mTk,vTk"
    p["z_max_pk"] = max(2.3, float(np.max(ZEFF))+0.25)
    p["P_k_max_h/Mpc"] = 5.0
    p.pop("non_linear", None); p.pop("lensing", None)
    p.pop("l_max_scalars", None); p.pop("k_output_values", None)
    return p


def params_default():
    p = dict(params_dense())
    p.pop("k_per_decade_for_pk", None)
    p.pop("k_per_decade_for_bao", None)
    return p


def gr_variant(p):
    q = dict(p)
    q["aest_enabled"] = "no"
    q["aest_memory_enabled"] = "no"
    q["aest_eta"] = 0.0
    return q


def config_isolation():
    d=params_dense(); n=params_default()
    dense_exact = (float(d.get("k_per_decade_for_pk", -1)) == DENSE_PK and
                   float(d.get("k_per_decade_for_bao", -1)) == DENSE_BAO)
    default_absent = ("k_per_decade_for_pk" not in n and "k_per_decade_for_bao" not in n)
    keys=set(d)|set(n); diff={}
    for k in sorted(keys):
        if d.get(k, "<MISSING>") != n.get(k, "<MISSING>"):
            diff[k] = {"dense": d.get(k, "<MISSING>"), "default": n.get(k, "<MISSING>")}
    only_two = set(diff) == {"k_per_decade_for_pk", "k_per_decade_for_bao"}
    return bool(dense_exact and default_absent and only_two), diff


def node_count(c):
    _, k, _ = c.get_transfer_and_k_and_z(output_format="class", h_units=True)
    k=np.asarray(k,float)
    keep=np.isfinite(k)&(k>=1e-4)&(k<=5.0)
    return int(np.count_nonzero(keep))


def run_model(params, internal=False):
    from classy import Class
    c=Class(); c.set(params); c.compute()
    try:
        As=float(params["A_s"]); ns=float(params["n_s"])
        rows=[]
        for z in ZEFF:
            rr=r9b2b._source_state_at_z(c,float(z),As,ns)
            if internal:
                si=float(c.sigma(8.0,float(z),h_units=True))
                fp=float(c.effective_f_sigma8(float(z),z_step=0.1))/si
                rr.update({"sigma8_internal":si,"legacy_growth_proxy":fp,
                           "rel_sigma8_source_vs_internal":rel(rr["sigma8_dd_source"],si),
                           "rel_f_source_vs_internal_proxy":rel(rr["f_source"],fp)})
            rows.append(rr)
            print("R9B2D_POINT "
                  f"z={z:.9f} sdd={rr['sigma8_dd_source']:.9g} "
                  f"stt={rr['sigma8_tt_source']:.9g} f={rr['f_source']:.9g}" +
                  (f" si={rr['sigma8_internal']:.9g} proxy={rr['legacy_growth_proxy']:.9g}"
                   if internal else ""), flush=True)
        return {"n_k":node_count(c),"rows":rows}
    finally:
        c.struct_cleanup(); c.empty()


def rowmap(x):
    return {float(r["z"]):r for r in x["rows"]}


def physical(r):
    return bool(r["finite_positive"] and 0.1<r["sigma8_dd_source"]<2.0 and 0.05<r["f_source"]<2.0)


def main() -> int:
    outpath=ROOT/"results/stable_aest_desi_dr1_r9b2d_kgrid_inheritance.json"
    print("STABLE_AEST_DESI_DR1_R9B2D_START",flush=True)
    d1_prov=all(ancestor(x) for x in (PREFIT_LOCK,R9B2C_POSTDATA_LOCK,R9B2C_IMPL_LOCK,R9B2B_POSTDATA_LOCK,R9B2A_POSTDATA_LOCK))
    d1_cfg,diff=config_isolation()
    d1=bool(d1_prov and d1_cfg)
    print("STABLE_AEST_DESI_DR1_R9B2D_CONFIG="+json.dumps(diff,sort_keys=True),flush=True)
    if not d1:
        out={"classification":CFG_FAIL,"diagnostic_complete":False,"science_evaluated":False,
             "gates":{"R9B2D_D1_provenance_and_configuration_isolation":False},"parameter_diff":diff}
        outpath.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("STABLE_AEST_DESI_DR1_R9B2D_CLASSIFICATION="+CFG_FAIL,flush=True); return 3
    try:
        pd=params_dense(); pn=params_default()
        print("STABLE_AEST_DESI_DR1_R9B2D_RUN=AEST_DENSE",flush=True); ad=run_model(pd,True)
        print("STABLE_AEST_DESI_DR1_R9B2D_RUN=AEST_DEFAULT",flush=True); an=run_model(pn,True)
        print("STABLE_AEST_DESI_DR1_R9B2D_RUN=GR_DENSE",flush=True); gd=run_model(gr_variant(pd),False)
        print("STABLE_AEST_DESI_DR1_R9B2D_RUN=GR_DEFAULT",flush=True); gn=run_model(gr_variant(pn),False)
    except Exception as exc:
        out={"classification":RUN_FAIL,"diagnostic_complete":False,"science_evaluated":False,"error":repr(exc)}
        outpath.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print(f"STABLE_AEST_DESI_DR1_R9B2D_RUN_FAIL error={exc!r}",flush=True)
        print("STABLE_AEST_DESI_DR1_R9B2D_CLASSIFICATION="+RUN_FAIL,flush=True); return 2

    node_ratio=float(ad["n_k"])/max(float(an["n_k"]),1.0)
    d2=bool(node_ratio>=NODE_RATIO_GATE)

    gdm=rowmap(gd); gnm=rowmap(gn); grmax={"sigma8_dd":0.0,"sigma8_tt":0.0,"f":0.0}; d3=True
    for z in gdm:
        a=gdm[z]; b=gnm[z]
        grmax["sigma8_dd"]=max(grmax["sigma8_dd"],rel(a["sigma8_dd_source"],b["sigma8_dd_source"]))
        grmax["sigma8_tt"]=max(grmax["sigma8_tt"],rel(a["sigma8_tt_source"],b["sigma8_tt_source"]))
        grmax["f"]=max(grmax["f"],rel(a["f_source"],b["f_source"]))
        d3 &= physical(a) and physical(b)
    d3=bool(d3 and max(grmax.values())<=REL_GATE)

    adm=rowmap(ad); anm=rowmap(an)
    d4=True
    for r in an["rows"]:
        d4 &= bool(physical(r) and r["rel_sigma8_source_vs_internal"]<=REL_GATE and
                   r["rel_f_source_vs_internal_proxy"]<=REL_GATE)

    dense_default={"sigma8_dd":0.0,"f":0.0}; dense_unphysical=False
    for z in adm:
        a=adm[z]; b=anm[z]
        dense_default["sigma8_dd"]=max(dense_default["sigma8_dd"],rel(a["sigma8_dd_source"],b["sigma8_dd_source"]))
        dense_default["f"]=max(dense_default["f"],rel(a["f_source"],b["f_source"]))
        dense_unphysical |= not physical(a)
    d5=bool(d4 and (dense_unphysical or max(dense_default.values())>=MATERIAL_GATE))

    internal={"sigma8":0.0,"growth_proxy":0.0}
    for z in adm:
        a=adm[z]; b=anm[z]
        internal["sigma8"]=max(internal["sigma8"],rel(a["sigma8_internal"],b["sigma8_internal"]))
        internal["growth_proxy"]=max(internal["growth_proxy"],rel(a["legacy_growth_proxy"],b["legacy_growth_proxy"]))
    d6=bool(max(internal.values())<=REL_GATE)

    gates={
        "R9B2D_D1_provenance_and_configuration_isolation":d1,
        "R9B2D_D2_node_count_separation":d2,
        "R9B2D_D3_GR_sampling_invariance":d3,
        "R9B2D_D4_DEFAULT_AeST_eta0_closure":d4,
        "R9B2D_D5_DENSE_pathology_reproduction":d5,
        "R9B2D_D6_internal_solution_invariance":d6,
    }
    if not d2: classification=SEP_FAIL
    elif not d3: classification=GR_FAIL
    elif not d4: classification=DEFAULT_FAIL
    elif not d6: classification=INTERNAL_FAIL
    elif not d5: classification=CAUSE_FAIL
    else: classification=PASS

    metrics={"rel_gate":REL_GATE,"material_gate":MATERIAL_GATE,"node_ratio_gate":NODE_RATIO_GATE,
             "n_k_AeST_dense":ad["n_k"],"n_k_AeST_default":an["n_k"],"node_ratio_dense_over_default":node_ratio,
             "GR_dense_vs_default_max_rel":grmax,"AeST_dense_vs_default_max_rel":dense_default,
             "AeST_internal_dense_vs_default_max_rel":internal,"dense_has_unphysical_source_point":bool(dense_unphysical),
             "default_max_rel_sigma8_source_vs_internal":max(r["rel_sigma8_source_vs_internal"] for r in an["rows"]),
             "default_max_rel_f_source_vs_internal_proxy":max(r["rel_f_source_vs_internal_proxy"] for r in an["rows"])}
    out={"classification":classification,"diagnostic_complete":True,"science_evaluated":False,"desi_data_loaded":False,
         "gates":gates,"metrics":metrics,"parameter_diff":diff,
         "AeST_dense":ad,"AeST_default":an,"GR_dense":gd,"GR_default":gn,
         "interpretation":{"historical_failures_reclassified":False,"desi_detection_claim_licensed":False,
                           "dense_k_inheritance_defect_certified":classification==PASS,
                           "raw_solver_history_followup_required":classification==DEFAULT_FAIL}}
    outpath.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("STABLE_AEST_DESI_DR1_R9B2D_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2D_METRICS="+json.dumps(metrics,sort_keys=True),flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2D_CLASSIFICATION="+classification,flush=True)
    return 0 if classification==PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
