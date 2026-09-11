#!/usr/bin/env python3
from __future__ import annotations

import argparse, json, math, os, shutil, subprocess
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BASE_INI = ROOT / "v019/ini/aest_exp.ini"
BASE_PRECISION = ROOT / "v019p/pre/p3.pre"
R9_BASE = "6084a9626ad15316e552f6dfb073cd56aced645f"
PREDATA = "540006afd837ed1b276676cc889d408a05363155"
CLASS_SHA = "e85808324f51fc694d12e3ed7439552a3c3f9540"
KB, TAUH0, MEMORY_ORDER = 0.0665, 1.0, 39
THEORY_LMAX, TRIM_LMAX, ACT_REQUIRED_LMAX = 4000, 2998, 2999
ETA0_GATE, KMAX_GATE = 1.0e-8, 1.0e-2
KMAX_COMPARE, KMAX_FINAL = 2.4, 3.0
ETA_GRID = np.asarray([0.,1/256,1/128,1/64,1/32,1/16,1/8], dtype=float)
START = dict(H0=67.3324639084866, omega_b=0.022377376877682164,
             omega_cdm=0.12006705327635288, tau_reio=0.06174082364515668,
             n_s=0.9666229454895277, A_s=2.1308864352626987e-9)
COMPLETE = "ACT_DR6_FSTATE_CERTIFIED_LINEAR_ETA_SCAN_COMPLETE"
CERT_FAIL = "ACT_DR6_FSTATE_CERTIFICATION_FAIL"
INCOMPLETE = "ACT_DR6_FSTATE_INCOMPLETE"


def git_head():
    return subprocess.check_output(["git","rev-parse","HEAD"], cwd=ROOT, text=True).strip()


def ancestor(sha):
    return subprocess.run(["git","merge-base","--is-ancestor",sha,"HEAD"], cwd=ROOT,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def rel_l2(a,b):
    a,b=np.asarray(a,float),np.asarray(b,float)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),1e-300))


def make_pre(label,kmax):
    p=ROOT/"results"/f"act_dr6_fs_{label}.pre"
    p.write_text(BASE_PRECISION.read_text().rstrip()+
                 f"\n\n# nonredundant F-state certified direct-LOS route\nk_max_tau0_over_l_max = {float(kmax):.17g}\n")
    return p


def make_ini(text,root,memory,eta):
    repl=dict(START); repl["aest_KB"]=KB
    drop={"aest_enabled","aest_memory_enabled","aest_memory_order","aest_eta","aest_tau_H0",
          "want_lcmb_full_limber","l_switch_limber","z_max_pk","P_k_max_h/Mpc","P_k_max_1/Mpc"}
    out=[]; seen=set(); flags={"output":0,"lensing":0,"lmax":0}
    for line in text.splitlines():
        st=line.strip(); key=st.split("=",1)[0].strip() if "=" in st else None
        if key in drop or key=="non linear": continue
        if key=="root": out.append(f"root = {root}")
        elif key=="output": out.append("output = tCl,pCl,lCl"); flags["output"]=1
        elif key=="lensing": out.append("lensing = yes"); flags["lensing"]=1
        elif key=="l_max_scalars": out.append(f"l_max_scalars = {THEORY_LMAX}"); flags["lmax"]=1
        elif key in repl: out.append(f"{key} = {repl[key]:.17g}"); seen.add(key)
        else: out.append(line)
    missing=set(repl)-seen
    if missing: raise RuntimeError(f"missing CLASS parameters: {sorted(missing)}")
    if not flags["output"]: out.append("output = tCl,pCl,lCl")
    if not flags["lensing"]: out.append("lensing = yes")
    if not flags["lmax"]: out.append(f"l_max_scalars = {THEORY_LMAX}")
    out += ["# nonredundant F-state final linear ACT route","aest_enabled = yes",
            f"aest_memory_enabled = {'yes' if memory else 'no'}",f"aest_memory_order = {MEMORY_ORDER}",
            f"aest_eta = {float(eta):.17g}",f"aest_tau_H0 = {TAUH0:.17g}",
            "want_lcmb_full_limber = no"]
    return "\n".join(out)+"\n"


def run_class(cr,label,memory,eta,kmax):
    ini=cr/f"obs_act_fs_{label}.ini"; root=f"output/obs_act_fs_{label}_"
    ini.write_text(make_ini(BASE_INI.read_text(),root,memory,eta))
    shutil.copy2(ini,ROOT/"results"/f"act_dr6_fs_{label}.ini")
    pre=make_pre(label,kmax)
    env=os.environ.copy(); env["OMP_NUM_THREADS"]="1"
    for n in ("AEST_TANGENT_FORCE_FILE","AEST_TANGENT_LAMBDA","AEST_TANGENT_TRACE_FILE","AEST_OFFLINE_TRACE_FILE","AEST_TANGENT_ALLOW_K_MISS"):
        env.pop(n,None)
    log=ROOT/"results"/f"act_dr6_fs_class_{label}.log"
    with log.open("w") as fh:
        p=subprocess.run([str(cr/"class"),ini.name,str(pre)],cwd=cr,env=env,stdout=fh,stderr=subprocess.STDOUT)
    if p.returncode:
        raise RuntimeError(f"CLASS failed for {label}:\n"+"\n".join(log.read_text(errors="replace").splitlines()[-80:]))
    src=cr/"output"/f"obs_act_fs_{label}__cl.dat"
    if not src.exists() or not src.stat().st_size: raise RuntimeError(f"missing _cl.dat for {label}")
    dst=ROOT/"results"/f"act_dr6_fs_{label}__cl.dat"; shutil.copy2(src,dst); return dst


def load_ckk(path,label):
    a=np.loadtxt(path)
    if a.ndim!=2 or a.shape[1]<6: raise RuntimeError(f"bad CLASS pCl shape for {label}: {a.shape}")
    er=np.asarray(a[:,0],int); dp=np.asarray(a[:,5],float)
    ell=np.arange(2,ACT_REQUIRED_LMAX+1,dtype=int); pos={int(L):i for i,L in enumerate(er)}
    if not er.size or int(er[-1])<ACT_REQUIRED_LMAX or any(int(L) not in pos for L in ell):
        raise RuntimeError(f"{label}: insufficient/missing L support")
    d=dp[np.asarray([pos[int(L)] for L in ell])]; phys=(np.pi/2)*ell*(ell+1)*d
    if not np.all(np.isfinite(phys)): raise FloatingPointError(f"{label}: nonfinite Ckk")
    if np.any(phys<=0): raise FloatingPointError(f"{label}: non-positive Ckk first={ell[phys<=0][:20].tolist()}")
    c=np.zeros(ACT_REQUIRED_LMAX+1); c[ell]=phys
    s=dict(ell_min=2,ell_max=ACT_REQUIRED_LMAX,n_multipoles=int(ell.size),ckk_min=float(phys.min()),ckk_max=float(phys.max()))
    print(f"FS_CKK_FINITE label={label} N={ell.size} L=2..{ACT_REQUIRED_LMAX} min={s['ckk_min']:.12e} max={s['ckk_max']:.12e}",flush=True)
    return c,s


def act_eval(data,c):
    bm=np.asarray(data["binmat_act"],float); b=bm@np.asarray(c[:bm.shape[1]],float)
    obs=np.asarray(data["data_binned_clkk"],float); ci=np.asarray(data["cinv"],float); d=obs-b
    chi=float(d@ci@d)
    if not math.isfinite(chi) or not np.all(np.isfinite(b)): raise FloatingPointError("nonfinite ACT result")
    return chi,b,obs


def save_fail(jout,nout,h,anc,cert,obs,arrays):
    result={"classification":CERT_FAIL,"observational_claim_licensed":False,
            "act_physics_interpretation_licensed":False,"exploratory":True,"head":h,"ancestry":anc,
            "class_upstream_sha":CLASS_SHA,"numerical_representation":"nonredundant_F_state",
            "certification":cert,"eta_scan_executed":False}
    jout.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(nout,ell=np.arange(ACT_REQUIRED_LMAX+1),data_binned_clkk=obs,**arrays)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--class-root",required=True)
    ap.add_argument("--json-out",default="results/act_dr6_fstate_certified_eta_scan.json")
    ap.add_argument("--npz-out",default="results/act_dr6_fstate_certified_eta_scan.npz")
    args=ap.parse_args(); cr=Path(args.class_root).resolve(); jout=Path(args.json_out); nout=Path(args.npz_out); jout.parent.mkdir(parents=True,exist_ok=True)
    try:
        import act_dr6_lenslike as alike
        h=git_head(); anc={"r9_base":ancestor(R9_BASE),"fstate_predata":ancestor(PREDATA)}
        print("ACT_DR6_FSTATE_FINAL_START",flush=True); print("HEAD="+h,flush=True); print("ANCESTRY="+json.dumps(anc,sort_keys=True),flush=True)
        print(f"MODEL AeST Exp KB={KB} tauH0={TAUH0} memory_order={MEMORY_ORDER}",flush=True)
        print("NUMERICAL_REPRESENTATION=nonredundant_F_state",flush=True)
        print(f"DIRECT_LOS_FINAL k_max_tau0_over_l_max={KMAX_FINAL} full_limber=False",flush=True)
        print("ETA_GRID="+",".join(f"{x:.12e}" for x in ETA_GRID),flush=True)
        if not all(anc.values()): raise RuntimeError(f"missing ancestry: {anc}")
        if not (cr/"class").exists(): raise RuntimeError("CLASS executable missing")
        data=alike.load_data("act_baseline",lens_only=True,like_corrections=False,trim_lmax=TRIM_LMAX,version="v1.2")
        print(f"ACT_DR6_NBINS={len(data['data_binned_clkk'])}",flush=True)

        p=run_class(cr,"eta0_off_k30",False,0.,KMAX_FINAL); off,offs=load_ckk(p,"eta0_off_k30"); offchi,offb,obs=act_eval(data,off)
        p=run_class(cr,"eta0_on_k30",True,0.,KMAX_FINAL); on,on_s=load_ckk(p,"eta0_on_k30"); onchi,onb,_=act_eval(data,on)
        eta0rel=rel_l2(on[2:],off[2:]); eta0pass=eta0rel<=ETA0_GATE
        print(f"FS_ETA0_REG relL2={eta0rel:.12e} gate={ETA0_GATE:.1e} pass={eta0pass}",flush=True)

        p=run_class(cr,"eta0_on_k24",True,0.,KMAX_COMPARE); k24,k24s=load_ckk(p,"eta0_on_k24"); k24chi,k24b,_=act_eval(data,k24)
        krel=rel_l2(onb,k24b); kpass=krel<=KMAX_GATE
        print(f"FS_KMAX_CERT chi2_k24={k24chi:.12e} chi2_k30={onchi:.12e} binned_relL2={krel:.12e} gate={KMAX_GATE:.1e} pass={kpass}",flush=True)
        cert={"pass":bool(eta0pass and kpass),
              "eta0_memory_on_off":{"rel_l2":eta0rel,"gate":ETA0_GATE,"pass":bool(eta0pass),"off_chi2":offchi,"on_chi2":onchi},
              "kmax":{"k24_chi2":k24chi,"k30_chi2":onchi,"binned_rel_l2":krel,"gate":KMAX_GATE,"pass":bool(kpass),"k24_spectrum":k24s,"k30_spectrum":on_s}}
        if not cert["pass"]:
            save_fail(jout,nout,h,anc,cert,obs,{"eta0_off_k30":off,"eta0_on_k30":on,"eta0_on_k24":k24,"eta0_off_binned":offb,"eta0_on_binned":onb,"eta0_k24_binned":k24b})
            print("FS_CERTIFICATION=FAIL",flush=True); print("CLASSIFICATION="+CERT_FAIL,flush=True); return 2
        print("FS_CERTIFICATION=PASS",flush=True)
        print("ACT_PHYSICS_INTERPRETATION_LICENSED=True",flush=True)

        rows=[]; spectra=[]; bins=[]
        for i,eta in enumerate(ETA_GRID):
            if i==0: c,s,chi,b=on,on_s,onchi,onb
            else:
                p=run_class(cr,f"eta_{i:02d}_k30",True,float(eta),KMAX_FINAL)
                c,s=load_ckk(p,f"eta_{i:02d}_k30"); chi,b,_=act_eval(data,c)
            shift=rel_l2(c[2:],on[2:]); row={"index":int(i),"eta":float(eta),"chi2":float(chi),"spectrum_rel_l2_vs_eta0":shift,"ckk_min":s["ckk_min"],"ckk_max":s["ckk_max"]}; rows.append(row); spectra.append(c); bins.append(b)
            print(f"FS_ACT_POINT {i+1:02d}/{len(ETA_GRID):02d} eta={eta:.12e} chi2={chi:.12e} relL2={shift:.12e}",flush=True)
        chi0=rows[0]["chi2"]
        for r in rows: r["delta_chi2_vs_eta0"]=float(r["chi2"]-chi0)
        best=min(rows,key=lambda r:r["chi2"]); bests={"grid_index":best["index"],"eta":best["eta"],"chi2":best["chi2"],"delta_chi2_vs_eta0":best["delta_chi2_vs_eta0"],"at_boundary":best["index"] in (0,len(ETA_GRID)-1)}
        result={"classification":COMPLETE,"observational_claim_licensed":False,"act_physics_interpretation_licensed":True,"exploratory":True,"eta_scan_executed":True,
                "head":h,"ancestry":anc,"class_upstream_sha":CLASS_SHA,"numerical_representation":"nonredundant_F_state",
                "model":{"aest_model":"Exp","KB":KB,"tauH0":TAUH0,"memory_order":MEMORY_ORDER,"theory":"linear"},
                "final_route":{"want_lcmb_full_limber":False,"k_max_tau0_over_l_max":KMAX_FINAL,"lmax_scalars":THEORY_LMAX},
                "act":{"variant":"act_baseline","lens_only":True,"like_corrections":False,"version":"v1.2","trim_lmax":TRIM_LMAX,"nbins":int(obs.size)},
                "certification":cert,"eta_grid":ETA_GRID.tolist(),"rows":rows,"best_grid_point":bests,
                "interpretation_scope":"Exploratory linear ACT DR6 physics is licensed only because the frozen eta0 identity and kmax convergence gates passed. Nonlinear/Halofit publication-level claim remains unlicensed."}
        jout.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
        np.savez_compressed(nout,ell=np.arange(ACT_REQUIRED_LMAX+1),eta=ETA_GRID,data_binned_clkk=obs,clkk=np.stack(spectra),binned_theory=np.stack(bins),chi2=np.asarray([r["chi2"] for r in rows]),eta0_off_k30=off,eta0_on_k24=k24)
        print("FS_BEST "+json.dumps(bests,sort_keys=True),flush=True); print("CLASSIFICATION="+COMPLETE,flush=True); print("OBSERVATIONAL_CLAIM_LICENSED=False",flush=True); return 0
    except Exception as exc:
        result={"classification":INCOMPLETE,"observational_claim_licensed":False,"act_physics_interpretation_licensed":False,"error":f"{type(exc).__name__}: {exc}"}
        jout.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n"); print("FS_ERROR="+result["error"],flush=True); print("CLASSIFICATION="+INCOMPLETE,flush=True); return 1


if __name__=="__main__":
    raise SystemExit(main())
