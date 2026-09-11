#!/usr/bin/env python3
from __future__ import annotations

import argparse, json, math, os, shutil, subprocess
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BASE_INI = ROOT / "v019/ini/aest_exp.ini"
BASE_PRECISION = ROOT / "v019p/pre/p3.pre"
R8_EXECUTED_BASE = "a7293637d8c1b2f2d436697a6c1f24005cc9a15b"
R9_PREDATA_COMMIT = "5d74b5171c6a2cbd5cb82d7ae880e82b7987ce76"
CLASS_SHA = "e85808324f51fc694d12e3ed7439552a3c3f9540"
KB, TAUH0, MEMORY_ORDER = 0.0665, 1.0, 39
THEORY_LMAX, TRIM_LMAX, ACT_REQUIRED_LMAX = 4000, 2998, 2999
GR_BINNED_GATE = AEST_KMAX_BINNED_GATE = 1.0e-2
KMAX_COMPARE, KMAX_FINAL = 2.4, 3.0
ETA_GRID = np.asarray([0.,1/256,1/128,1/64,1/32,1/16,1/8], dtype=float)
START = dict(H0=67.3324639084866, omega_b=0.022377376877682164,
             omega_cdm=0.12006705327635288, tau_reio=0.06174082364515668,
             n_s=0.9666229454895277, A_s=2.1308864352626987e-9)
COMPLETE = "ACT_DR6_LENSING_EXPLORATORY_R9_DIRECT_LOS_CERTIFIED_ETA_SCAN_COMPLETE"
CERT_FAIL = "ACT_DR6_LENSING_EXPLORATORY_R9_DIRECT_LOS_CERTIFICATION_FAIL"
INCOMPLETE = "ACT_DR6_LENSING_EXPLORATORY_R9_DIRECT_LOS_INCOMPLETE"

def head():
    return subprocess.check_output(["git","rev-parse","HEAD"], cwd=ROOT, text=True).strip()

def ancestor(sha):
    return subprocess.run(["git","merge-base","--is-ancestor",sha,"HEAD"], cwd=ROOT,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

def rel_l2(a,b):
    a,b=np.asarray(a,float),np.asarray(b,float)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),1e-300))

def make_pre(label,kmax):
    lines=[BASE_PRECISION.read_text().rstrip(),"","# R9 certified direct-LOS route"]
    if kmax is not None: lines.append(f"k_max_tau0_over_l_max = {float(kmax):.17g}")
    p=ROOT/"results"/f"act_dr6_r9_{label}.pre"; p.write_text("\n".join(lines)+"\n"); return p

def make_ini(text, root, aest, memory, eta, full_limber):
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
    out += ["# R9 certified direct-LOS bridge", f"aest_enabled = {'yes' if aest else 'no'}",
            f"aest_memory_enabled = {'yes' if memory else 'no'}", f"aest_memory_order = {MEMORY_ORDER}",
            f"aest_eta = {float(eta):.17g}", f"aest_tau_H0 = {TAUH0:.17g}",
            f"want_lcmb_full_limber = {'yes' if full_limber else 'no'}"]
    return "\n".join(out)+"\n"

def run_class(class_root,label,aest,memory,eta,full_limber,kmax):
    ini=class_root/f"obs_act_r9_{label}.ini"; root=f"output/obs_act_r9_{label}_"
    ini.write_text(make_ini(BASE_INI.read_text(),root,aest,memory,eta,full_limber))
    shutil.copy2(ini,ROOT/"results"/f"act_dr6_r9_{label}.ini")
    pre=make_pre(label,kmax)
    env=os.environ.copy(); env["OMP_NUM_THREADS"]="1"
    for n in ("AEST_TANGENT_FORCE_FILE","AEST_TANGENT_LAMBDA","AEST_TANGENT_TRACE_FILE","AEST_OFFLINE_TRACE_FILE"):
        env.pop(n,None)
    log=ROOT/"results"/f"act_dr6_r9_class_{label}.log"
    with log.open("w") as fh:
        p=subprocess.run([str(class_root/"class"),ini.name,str(pre)],cwd=class_root,env=env,stdout=fh,stderr=subprocess.STDOUT)
    if p.returncode:
        raise RuntimeError(f"CLASS failed for {label}:\n"+"\n".join(log.read_text(errors="replace").splitlines()[-60:]))
    src=class_root/"output"/f"obs_act_r9_{label}__cl.dat"
    if not src.exists() or not src.stat().st_size: raise RuntimeError(f"missing _cl.dat for {label}")
    dst=ROOT/"results"/f"act_dr6_r9_{label}__cl.dat"; shutil.copy2(src,dst); return dst

def load_ckk(path,label):
    a=np.loadtxt(path)
    if a.ndim!=2 or a.shape[1]<6: raise RuntimeError(f"bad CLASS pCl shape for {label}: {a.shape}")
    er=np.asarray(a[:,0],int); dp=np.asarray(a[:,5],float)
    if not er.size or int(er[-1])<ACT_REQUIRED_LMAX: raise RuntimeError(f"{label}: insufficient L support")
    ell=np.arange(2,ACT_REQUIRED_LMAX+1,dtype=int); pos={int(L):i for i,L in enumerate(er)}
    if any(int(L) not in pos for L in ell): raise RuntimeError(f"{label}: missing multipoles")
    d=dp[np.asarray([pos[int(L)] for L in ell])]
    phys=(np.pi/2)*ell*(ell+1)*d
    if not np.all(np.isfinite(phys)): raise FloatingPointError(f"{label}: nonfinite Ckk")
    if np.any(phys<=0): raise FloatingPointError(f"{label}: non-positive Ckk first={ell[phys<=0][:20].tolist()}")
    c=np.zeros(ACT_REQUIRED_LMAX+1); c[ell]=phys
    s=dict(ell_min=2,ell_max=ACT_REQUIRED_LMAX,n_multipoles=int(ell.size),ckk_min=float(phys.min()),ckk_max=float(phys.max()))
    print(f"R9_CKK_FINITE label={label} N={ell.size} L=2..{ACT_REQUIRED_LMAX} min={s['ckk_min']:.12e} max={s['ckk_max']:.12e}",flush=True)
    return c,s

def act_eval(data,c):
    bm=np.asarray(data["binmat_act"],float); b=bm@np.asarray(c[:bm.shape[1]],float)
    obs=np.asarray(data["data_binned_clkk"],float); ci=np.asarray(data["cinv"],float); d=obs-b
    chi=float(d@ci@d)
    if not math.isfinite(chi) or not np.all(np.isfinite(b)): raise FloatingPointError("nonfinite ACT result")
    return chi,b,obs

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--class-root",required=True)
    ap.add_argument("--json-out",default="results/act_dr6_lensing_exploratory_r9_direct_los_certified_eta_scan.json")
    ap.add_argument("--npz-out",default="results/act_dr6_lensing_exploratory_r9_direct_los_certified_eta_scan.npz")
    args=ap.parse_args(); cr=Path(args.class_root).resolve(); jout=Path(args.json_out); nout=Path(args.npz_out); jout.parent.mkdir(parents=True,exist_ok=True)
    try:
        import act_dr6_lenslike as alike
        h=head(); anc={"r8_executed_base":ancestor(R8_EXECUTED_BASE),"r9_predata":ancestor(R9_PREDATA_COMMIT)}
        print("ACT_DR6_LENSING_EXPLORATORY_R9_DIRECT_LOS_START",flush=True); print("HEAD="+h,flush=True); print("ANCESTRY="+json.dumps(anc,sort_keys=True),flush=True)
        print(f"MODEL AeST Exp KB={KB} tauH0={TAUH0} memory_order={MEMORY_ORDER}",flush=True)
        print(f"DIRECT_LOS_FINAL k_max_tau0_over_l_max={KMAX_FINAL} full_limber=False",flush=True)
        print("ETA_GRID="+",".join(f"{x:.12e}" for x in ETA_GRID),flush=True)
        if not all(anc.values()): raise RuntimeError(f"missing ancestry: {anc}")
        if not (cr/"class").exists(): raise RuntimeError("CLASS executable missing")
        data=alike.load_data("act_baseline",lens_only=True,like_corrections=False,trim_lmax=TRIM_LMAX,version="v1.2")
        print(f"ACT_DR6_NBINS={len(data['data_binned_clkk'])}",flush=True)

        p=run_class(cr,"gr_full_limber",False,False,0.,True,None); gf,gfs=load_ckk(p,"gr_full_limber"); gfc,gfb,obs=act_eval(data,gf)
        p=run_class(cr,"gr_direct_k30",False,False,0.,False,KMAX_FINAL); gd,gds=load_ckk(p,"gr_direct_k30"); gdc,gdb,_=act_eval(data,gd)
        grrel=rel_l2(gdb,gfb); grp=grrel<=GR_BINNED_GATE
        print(f"R9_GR_CERT chi2_full={gfc:.12e} chi2_direct={gdc:.12e} binned_relL2={grrel:.12e} gate={GR_BINNED_GATE:.1e} pass={grp}",flush=True)

        p=run_class(cr,"aest_eta0_direct_k24",True,True,0.,False,KMAX_COMPARE); a24,a24s=load_ckk(p,"aest_eta0_direct_k24"); c24,b24,_=act_eval(data,a24)
        p=run_class(cr,"aest_eta0_direct_k30",True,True,0.,False,KMAX_FINAL); a30,a30s=load_ckk(p,"aest_eta0_direct_k30"); c30,b30,_=act_eval(data,a30)
        aerel=rel_l2(b30,b24); aep=aerel<=AEST_KMAX_BINNED_GATE
        print(f"R9_AEST_KMAX_CERT chi2_k24={c24:.12e} chi2_k30={c30:.12e} binned_relL2={aerel:.12e} gate={AEST_KMAX_BINNED_GATE:.1e} pass={aep}",flush=True)
        cert={"pass":bool(grp and aep),"gr":{"full_limber_chi2":gfc,"direct_los_chi2":gdc,"binned_rel_l2":grrel,"gate":GR_BINNED_GATE,"pass":bool(grp),"full_limber_spectrum":gfs,"direct_los_spectrum":gds},"aest_eta0_kmax":{"k24_chi2":c24,"k30_chi2":c30,"binned_rel_l2":aerel,"gate":AEST_KMAX_BINNED_GATE,"pass":bool(aep),"k24_spectrum":a24s,"k30_spectrum":a30s}}
        if not cert["pass"]:
            result={"classification":CERT_FAIL,"observational_claim_licensed":False,"exploratory":True,"head":h,"ancestry":anc,"class_upstream_sha":CLASS_SHA,"certification":cert,"eta_scan_executed":False}
            jout.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
            np.savez_compressed(nout,ell=np.arange(ACT_REQUIRED_LMAX+1),data_binned_clkk=obs,gr_full_limber=gf,gr_direct_k30=gd,aest_eta0_direct_k24=a24,aest_eta0_direct_k30=a30,gr_full_binned=gfb,gr_direct_binned=gdb,aest_k24_binned=b24,aest_k30_binned=b30)
            print("R9_CERTIFICATION=FAIL",flush=True); print("CLASSIFICATION="+CERT_FAIL,flush=True); return 2
        print("R9_CERTIFICATION=PASS",flush=True)

        rows=[]; spectra=[]; bins=[]
        for i,eta in enumerate(ETA_GRID):
            if i==0: c,s,chi,b=a30,a30s,c30,b30
            else:
                p=run_class(cr,f"aest_eta_{i:02d}_direct_k30",True,True,float(eta),False,KMAX_FINAL)
                c,s=load_ckk(p,f"aest_eta_{i:02d}_direct_k30"); chi,b,_=act_eval(data,c)
            sh=rel_l2(c[2:],a30[2:]); row={"index":int(i),"eta":float(eta),"chi2":float(chi),"spectrum_rel_l2_vs_eta0":sh,"ckk_min":s["ckk_min"],"ckk_max":s["ckk_max"]}; rows.append(row); spectra.append(c); bins.append(b)
            print(f"R9_ACT_POINT {i+1:02d}/{len(ETA_GRID):02d} eta={eta:.12e} chi2={chi:.12e} relL2={sh:.12e}",flush=True)
        chi0=rows[0]["chi2"]
        for r in rows: r["delta_chi2_vs_eta0"]=r["chi2"]-chi0
        best=min(rows,key=lambda r:r["chi2"]); bests={"grid_index":best["index"],"eta":best["eta"],"chi2":best["chi2"],"delta_chi2_vs_eta0":best["delta_chi2_vs_eta0"],"at_boundary":best["index"] in (0,len(ETA_GRID)-1)}
        result={"classification":COMPLETE,"observational_claim_licensed":False,"exploratory":True,"eta_scan_executed":True,"head":h,"ancestry":anc,"class_upstream_sha":CLASS_SHA,"model":{"aest_model":"Exp","KB":KB,"tauH0":TAUH0,"memory_order":MEMORY_ORDER,"theory":"linear"},"final_route":{"want_lcmb_full_limber":False,"k_max_tau0_over_l_max":KMAX_FINAL,"lmax_scalars":THEORY_LMAX},"act":{"variant":"act_baseline","lens_only":True,"like_corrections":False,"version":"v1.2","trim_lmax":TRIM_LMAX,"nbins":int(obs.size)},"conversion":"Ckk=(pi/2)*L*(L+1)*D_L_phiphi from CLASS-format _cl.dat","certification":cert,"eta_grid":ETA_GRID.tolist(),"rows":rows,"best_grid_point":bests,"interpretation_scope":"Exploratory linear ACT DR6 eta scan on the R9-certified direct-LOS route. No detection claim; nonlinear/Halofit AeST lensing remains unresolved."}
        jout.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
        np.savez_compressed(nout,eta=ETA_GRID,ell=np.arange(ACT_REQUIRED_LMAX+1),clkk=np.stack(spectra),binned_theory=np.stack(bins),data_binned_clkk=obs,bcents_act=np.asarray(data["bcents_act"],float),chi2=np.asarray([r["chi2"] for r in rows]),gr_full_limber=gf,gr_direct_k30=gd,gr_full_binned=gfb,gr_direct_binned=gdb,aest_eta0_direct_k24=a24,aest_eta0_direct_k30=a30,aest_k24_binned=b24,aest_k30_binned=b30)
        print(f"BEST_GRID_POINT=index:{bests['grid_index']} eta:{bests['eta']:.12e} chi2:{bests['chi2']:.12e} delta_chi2:{bests['delta_chi2_vs_eta0']:.12e} boundary:{bests['at_boundary']}",flush=True)
        print("CLASSIFICATION="+COMPLETE,flush=True); print("OBSERVATIONAL_CLAIM_LICENSED=False",flush=True); print("ACT_DR6_LENSING_EXPLORATORY_R9_DIRECT_LOS_END",flush=True); return 0
    except Exception as e:
        jout.write_text(json.dumps({"classification":INCOMPLETE,"observational_claim_licensed":False,"error":f"{type(e).__name__}: {e}"},indent=2,sort_keys=True)+"\n")
        print(f"R9_ERROR={type(e).__name__}: {e}",flush=True); print("CLASSIFICATION="+INCOMPLETE,flush=True); return 1

if __name__=="__main__": raise SystemExit(main())
