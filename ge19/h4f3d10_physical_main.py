#!/usr/bin/env python3
"""D10 isolated-local physical driver. Restricted actual nonbath first-order only."""
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
import numpy as np
from ge19 import h4f3d10_actual_nonbath_first_order_known_boundary as pre
from ge19 import h4f3d10_nonbath_first_order_local_partials as local
from ge19 import h4f3d10_known_parent_boundary_assembly as signed

ROOT=Path(__file__).resolve().parents[1]
HELPERS={
"ge19/h4f3d10_actual_nonbath_first_order_known_boundary.py":
"c570546caa301ec6899b4e669b663726fd4fdc2f",
"ge19/h4f3d10_nonbath_first_order_local_partials.py":
"4c3968d7186e27f15b10992198d7bccedf207bfb",
"ge19/h4f3d10_known_parent_boundary_assembly.py":
"d3a43a0ebbd78e03f2313592bdb1455977cb1d1c"}

def helper_lock():
    z={}
    for p,want in HELPERS.items():
        head=subprocess.check_output(["git","rev-parse","HEAD:"+p],cwd=ROOT,text=True).strip()
        work=subprocess.check_output(["git","hash-object",str(ROOT/p)],cwd=ROOT,text=True).strip()
        z[p]={"expected":want,"head":head,"worktree":work,"exact":want==head==work}
    if not all(v["exact"] for v in z.values()):raise RuntimeError("D10 helper blob mismatch")
    return z

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--results-dir",required=True)
    a.add_argument("--repair26-trace",required=True)
    a.add_argument("--json-out",required=True)
    a.add_argument("--npz-out",required=True)
    args=a.parse_args()
    rd=Path(args.results_dir).resolve()
    trace=Path(args.repair26_trace).resolve()
    outj=Path(args.json_out).resolve()
    outn=Path(args.npz_out).resolve()
    if outj.exists() or outn.exists():raise RuntimeError("D10 outputs exist; no overwrite")
    helpers=helper_lock()
    pins=pre.locks()
    paths=pre.physical_paths(rd,trace)
    files,parents=pre.s.frozen_inputs(rd,trace)
    if not all(parents[k]["exact"] for k in pre.s.REQUIRED):
        raise RuntimeError("D10 certified H3F/H3G/Repair13/Z11 parent mismatch")
    save={}
    rows=[]
    with (np.load(files["r13"],allow_pickle=False) as r13,
          np.load(files["h3fn"],allow_pickle=False) as h3f,
          np.load(files["z11"],allow_pickle=False) as z11,
          np.load(paths["source_npz"],allow_pickle=False) as six):
        bgs,_,m6,m7,_,_,_,_,_=pre.old.build_context(rd,r13)
        for nt,label in ((128,"primary"),(64,"control")):
            x=np.asarray(six["x_"+label],float)
            if x.shape!=(nt,):raise RuntimeError("D10 wrong original grid")
            for par in (h3f,z11):
                if not np.array_equal(x,np.asarray(par["x_"+label],float)):
                    raise RuntimeError("D10 parent clock mismatch")
            save["x_"+label]=x
            for tag in pre.old.r7.C_TAGS:
                bg=bgs[(nt,tag)]
                if not np.array_equal(x,np.asarray(bg["x"],float)):
                    raise RuntimeError("D10 background x clock mismatch")
                h1=np.asarray(h3f[tag+"_H1_"+label],complex)
                dh1=np.asarray(h3f[tag+"_H1dot_"+label],complex)
                z=np.asarray(z11[tag+"_Z11_"+label],complex)
                dz=np.asarray(z11[tag+"_Z11dot_"+label],complex)
                if (h1.shape!=(6,6,nt) or z.shape!=(6,6,nt)
                    or dh1.shape!=(6,4,nt) or dz.shape!=(6,4,nt)
                    or not all(np.isfinite(q).all() for q in (h1,dh1,z,dz))):
                    raise RuntimeError("D10 original physical first-order parent invalid")
                kfund=float(pre.old.r7.g9.K_REQ[0]/pre.old.r7.FOURIER_N[0])
                def dx(q):return pre.old.r7.spectral_dx(q,kfund)
                dx.kfund=kfund
                schemes={}
                f10=f11=x10=x11=None
                for scheme,mat in (
                    ("FD4",pre.old.r7.fd4_matrix(nt,float(x[0]),float(x[-1]))),
                    ("FD8",pre.old.fd8_matrix(nt,float(x[0]),float(x[-1])))):
                    Dt=np.asarray(bg["H"],float)[:,None]*mat
                    aa,bb,ea=local.evaluate(pre.old,bg,tag,m6,m7,h1,dh1,Dt)
                    cc,dd,eb=local.evaluate(pre.old,bg,tag,m6,m7,z,dz,Dt)
                    if f10 is None:f10,x10,f11,x11=aa,bb,cc,dd
                    else:
                        if any(not np.array_equal(f10[n],aa[n])
                               or not np.array_equal(f11[n],cc[n])
                               or not np.array_equal(x10[n],bb[n])
                               or not np.array_equal(x11[n],dd[n])
                               for n in pre.FN):
                            raise RuntimeError("D10 original fields differ between time schemes")
                    schemes[scheme]=(ea,eb)
                arrays,diags,error,passed=signed.evaluate_pair(
                    f10,x10,f11,x11,schemes,dx)
                for name,arr in arrays.items():save[label+"_"+tag+"_"+name]=arr
                rows.append({"C":tag,"Nt":nt,"original_2048_R1_nodes_unchanged":True,
                  "original_positive_modes":list(map(int,pre.old.r7.FOURIER_N)),
                  "eight_actual_nonbath_fields":list(pre.FN),
                  "schemes":diags,
                  "archive_only_max_FFT_relative":error,
                  "unknown_E00_times_F21_and_L21_boundary_retained":True,
                  "no_physical_on_shell_smallness_gate":True,
                  "pass":passed})
    ok=bool(len(rows)==6 and all(q["pass"] for q in rows)
            and all(np.isfinite(x).all() for x in save.values()))
    report={
       "classification":("GE19_H4F3D10_ACTUAL_NONBATH_FIRST_ORDER_KNOWN_BOUNDARY_DIAGNOSTIC_PASS_FULL_OPEN"
                         if ok else "GE19_H4F3D10_ACTUAL_PARENT_INTERFACE_UNRESOLVED"),
       "frozen_helper_blobs":helpers,"original_code_blobs":pins,
       "original_physical_input_sha256":{k:pre.digest(p) for k,p in paths.items()},
       "original_certified_parent_hashes":parents,
       "cases":rows,"all_six_actual_nonbath_cases_complete":len(rows)==6,
       "archive_only_array_assembly_checks_pass":ok,
       "actual_background_E00_F21_evaluated":False,
       "actual_L21_EL00_minus_b21_Eb00_evaluated":False,
       "actual_complete_H4_Ward_evaluated":False,
       "original_H4F3d7r1_bath_on_shell_asserted":False,
       "complete_FD4_FD8_physical_error_budget_certified":False,
       "Z21_certified":False,"lensing_licensed":False,
       "claim_boundary":"Physical original H3F H1 and Repair32B Z11 nonbath first-order Euler plus known signed boundary, original FD4 and FD8 report separately. The unknown Z21-dependent E00/F21 and L21/b21 terms and full H4 Noether remain OPEN."}
    outj.parent.mkdir(parents=True,exist_ok=True)
    outn.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    np.savez_compressed(outn,**save)
    print(json.dumps(report,indent=2,sort_keys=True,allow_nan=False))
    if not ok:raise SystemExit(2)

if __name__=="__main__":main()
