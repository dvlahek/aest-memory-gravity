#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
from scipy.interpolate import CubicSpline, PchipInterpolator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from v063 import theory_response_map as v63
from nl1c6 import full_j_baryonic_reclosure as static
from nl1c6d2a import baryon_matter_sector_audit as d2a
from nl1c6d2n import corrected_class_baseline as cb
from nl1c6d2n import corrected_class_baseline_r1 as r1

A = 2.0 - static.KB
K_H = static.K_H.copy()
K_MPC = static.K_MPC.copy()
CHECK_Z = np.asarray([6.0,5.0,4.0,3.0,2.0,1.5,1.0,0.5,0.2], float)
PASS_LABEL = "NL1C6D2C6A_PHYSICAL_TIME_SCALAR_CURRENT_INTEGRATOR_PASS"
FAIL_LABEL = "NL1C6D2C6A_PHYSICAL_TIME_SCALAR_CURRENT_INTEGRATOR_FAIL"
INCOMPLETE_LABEL = "NL1C6D2C6A_PHYSICAL_TIME_SCALAR_CURRENT_INTEGRATOR_INCOMPLETE"
LINEAR_GATE = 5.0e-3
TIME_GATE = 2.0e-3
SPACE_GATE = 5.0e-3
CONSTRAINT_GATE = 1.0e-10
INITIAL_GATE = 1.0e-12


class InputIncomplete(RuntimeError):
    pass


def rel_l2(a, b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(bb),1e-300))


def norm_residual(r, *terms):
    scale=max([float(np.linalg.norm(np.asarray(x,float))) for x in terms]+[1e-300])
    return float(np.linalg.norm(np.asarray(r,float))/scale)


def git_meta():
    try:
        head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
        branch=subprocess.check_output(["git","rev-parse","--abbrev-ref","HEAD"],cwd=ROOT,text=True).strip()
    except Exception:
        head,branch="unknown","unknown"
    return head,branch


def unique_spline(x,y):
    x=np.asarray(x,float); y=np.asarray(y,float)
    order=np.argsort(x); x=x[order]; y=y[order]
    finite=np.isfinite(x)&np.isfinite(y); x=x[finite]; y=y[finite]
    keep=np.ones(x.size,dtype=bool)
    if x.size>1: keep[1:]=np.diff(x)>0
    x=x[keep]; y=y[keep]
    if x.size<8: raise InputIncomplete("insufficient unique finite dense samples")
    return CubicSpline(x,y,bc_type="not-a-knot"),x,y


def key(raw, exacts):
    for k in exacts:
        if k in raw: return k
    raise InputIncomplete(f"missing required dense field among {exacts}; available={sorted(raw.keys())}")


def build_params():
    p=dict(v63.class_params())
    p.update({
        "output":"mTk,vTk",
        "lensing":"no",
        "k_output_values":", ".join(f"{k:.17g}" for k in K_MPC),
        "P_k_max_h/Mpc":2.0,
        "z_max_pk":6.5,
        "k_per_decade_for_pk":80.0,
        "k_per_decade_for_bao":560.0,
        "aest_memory_enabled":"no",
        "aest_eta":0.0,
    })
    return p


def prepare_class_data():
    class_root=Path(os.environ.get("NL1C6D2N_CLASS_ROOT",""))
    if not class_root.exists():
        raise InputIncomplete("NL1C6D2N_CLASS_ROOT is not set to isolated corrected CLASS")
    head,branch=git_meta()
    provenance=r1.provenance_audit(class_root,head,branch)
    if not provenance.get("pass",False):
        raise InputIncomplete("corrected CLASS provenance audit did not pass")

    from classy import Class
    c=Class(); c.set(build_params()); c.compute()
    try:
        bg=c.get_background()
        pert=c.get_perturbations()
        histories,scalar_key=d2a.scalar_histories(pert)
        if len(histories)!=6:
            raise InputIncomplete(f"expected 6 dense scalar histories, got {len(histories)}")
        bg_audit,bgv=r1.background_audit_r1(bg)
        if not bg_audit.get("pass",False) or bgv is None:
            raise InputIncomplete("corrected background R1 reconstruction unavailable")
    finally:
        c.struct_cleanup(); c.empty()

    modes=[]
    for i,raw in enumerate(histories):
        ktau=key(raw,("tau [Mpc]","tau","tau[Mpc]"))
        ka=key(raw,("a","scale factor"))
        kpsi=key(raw,("psi",))
        kalpha=key(raw,("alpha_aest","alpha"))
        kE=key(raw,("E_aest","E"))
        kth=key(raw,("theta_cdm","t_cdm"))
        tau=np.asarray(raw[ktau],float); aa=np.asarray(raw[ka],float)
        if tau.shape!=aa.shape: raise InputIncomplete(f"tau/a shape mismatch in mode {i}")
        fields={}
        domains=[]
        for name,kname in (("a",ka),("psi",kpsi),("alpha",kalpha),("E",kE),("theta",kth)):
            sp,xs,ys=unique_spline(tau,np.asarray(raw[kname],float))
            fields[name]=sp; domains.append((float(xs[0]),float(xs[-1])))
        lo=max(x[0] for x in domains); hi=min(x[1] for x in domains)
        modes.append({"splines":fields,"tau_lo":lo,"tau_hi":hi,"available_keys":sorted(raw.keys())})

    # Common physical time from the first mode's monotonic a(tau).
    tau0_grid=np.asarray(histories[0][key(histories[0],("tau [Mpc]","tau","tau[Mpc]"))],float)
    a0_grid=np.asarray(histories[0][key(histories[0],("a","scale factor"))],float)
    order=np.argsort(a0_grid); aa=a0_grid[order]; tt=tau0_grid[order]
    finite=np.isfinite(aa)&np.isfinite(tt); aa=aa[finite]; tt=tt[finite]
    keep=np.ones(aa.size,dtype=bool); keep[1:]=np.diff(aa)>0; aa=aa[keep]; tt=tt[keep]
    tau_of_a=PchipInterpolator(aa,tt,extrapolate=False)
    tau_check=np.asarray([float(tau_of_a(1.0/(1.0+z))) for z in CHECK_Z])
    if not np.all(np.isfinite(tau_check)) or np.any(np.diff(tau_check)<=0):
        raise InputIncomplete("could not map frozen redshifts monotonically to conformal time")
    t0=float(tau_check[0]); t1=float(tau_check[-1])
    for i,m in enumerate(modes):
        if t0<m["tau_lo"]-1e-9 or t1>m["tau_hi"]+1e-9:
            raise InputIncomplete(f"mode {i} does not cover z=6..0.2 interval")

    # Corrected background splines from independently certified R1 reconstruction.
    ba=np.asarray(bgv["a"],float); order=np.argsort(ba); ba=ba[order]
    def bgs(name):
        yy=np.asarray(bgv[name],float)[order]
        keep=np.ones(ba.size,dtype=bool); keep[1:]=np.diff(ba)>0
        return PchipInterpolator(ba[keep],yy[keep],extrapolate=False)
    bgsp={name:bgs(name) for name in ("H","Q","KQ","KQQ","Zcoord")}

    return {"provenance":provenance,"background_audit":bg_audit,"bg":bgsp,
            "modes":modes,"tau_check":tau_check,"t0":t0,"t1":t1,
            "scalar_key":scalar_key}


def bg_eval(data,tau):
    a=float(data["modes"][0]["splines"]["a"](tau))
    H=float(data["bg"]["H"](a)); Q=float(data["bg"]["Q"](a))
    KQ=float(data["bg"]["KQ"](a)); KQQ=float(data["bg"]["KQQ"](a))
    Z=float(data["bg"]["Zcoord"](a))
    Qdot=-3.0*H*KQ/KQQ
    vals=(a,H,Q,KQ,KQQ,Z,Qdot)
    if not np.all(np.isfinite(vals)) or a<=0 or KQQ<=0:
        raise FloatingPointError("nonfinite/invalid background interpolation")
    return vals


def mode_values(data,tau,name):
    return np.asarray([float(m["splines"][name](tau)) for m in data["modes"]],float)


def cos_matrix(nx):
    x=np.arange(nx)*static.BOX/nx
    return static.MODE_AMP[:,None]*np.cos(K_MPC[:,None]*x[None,:]+static.PHASE[:,None])


def to_field(vals,C):
    return np.asarray(vals,float)@C


def spec_ops(nx):
    kk=2*np.pi*np.fft.fftfreq(nx,d=static.BOX/nx)
    mask=static.dealias_mask(nx)
    def grad(f): return np.fft.ifft(1j*kk*np.fft.fft(f)).real
    def lap(f): return np.fft.ifft(-(kk*kk)*np.fft.fft(f)).real
    def invlap(s):
        sh=np.fft.fft(s); out=np.zeros(nx,complex); nz=np.abs(kk)>0
        out[nz]=-sh[nz]/(kk[nz]*kk[nz])
        return np.fft.ifft(out).real
    def div_dealiased(flux): return np.fft.ifft(1j*kk*(np.fft.fft(flux)*mask)).real
    return grad,lap,invlap,div_dealiased


def class_fields(data,tau,nx,C=None):
    if C is None: C=cos_matrix(nx)
    a,H,Q,KQ,KQQ,Z,Qdot=bg_eval(data,tau)
    alpha_m=mode_values(data,tau,"alpha")
    E_m=mode_values(data,tau,"E")
    psi_m=mode_values(data,tau,"psi")
    th_m=mode_values(data,tau,"theta")
    chi_m=Q*(a*th_m/(K_MPC*K_MPC)+alpha_m)
    return {"a":a,"Q":Q,"KQ":KQ,"KQQ":KQQ,"Qdot":Qdot,
            "alpha":to_field(alpha_m,C),"E":to_field(E_m,C),
            "psi":to_field(psi_m,C),"chi":to_field(chi_m,C),"chi_modes":chi_m}


def initial_state(data,nx):
    C=cos_matrix(nx); t0=data["t0"]
    cf=class_fields(data,t0,nx,C)
    a,Q,KQQ,Qdot=cf["a"],cf["Q"],cf["KQQ"],cf["Qdot"]

    # Build independent modal chi splines, then differentiate at the physical start.
    dchi=[]
    for i,m in enumerate(data["modes"]):
        # Use the native dense tau grid implicit in the spline domain, sampled densely enough
        # to reproduce the smooth CLASS trajectory without introducing a fitted parameter.
        ts=np.linspace(m["tau_lo"],m["tau_hi"],2049)
        aa=m["splines"]["a"](ts); al=m["splines"]["alpha"](ts); th=m["splines"]["theta"](ts)
        q=np.asarray([float(data["bg"]["Q"](float(av))) for av in aa])
        ch=q*(aa*th/(K_MPC[i]*K_MPC[i])+al)
        sp=CubicSpline(ts,ch,bc_type="not-a-knot")
        dchi.append(float(sp(t0,1)))
    dchi=np.asarray(dchi,float)
    chi_tau=to_field(dchi,C)
    U=chi_tau/a-Q*cf["E"]-Qdot*cf["alpha"]
    pchi=2.0*a**3*KQQ*U
    grad,lap,invlap,div=spec_ops(nx)
    palpha=-Q*pchi-2.0*a*static.KB*lap(cf["E"])-2.0*A*a*lap(cf["chi"])
    y=np.stack([cf["alpha"],cf["chi"],pchi,palpha])

    lhs=palpha+Q*pchi
    rhs=-2.0*a*static.KB*lap(cf["E"])-2.0*A*a*lap(cf["chi"])
    ell=norm_residual(lhs-rhs,lhs,rhs)
    pdef=norm_residual(pchi-2.0*a**3*KQQ*U,pchi,2.0*a**3*KQQ*U)
    zero={k:float(abs(np.mean(cf[k]))/max(float(np.sqrt(np.mean(cf[k]**2))),1e-300)) for k in ("alpha","E","chi")}
    return y,{"elliptic_residual":ell,"pchi_definition_residual":pdef,
              "zero_mode_relative":zero,"all_finite":bool(np.all(np.isfinite(y))),"class_start":cf}


def derive_E(data,tau,y,ops):
    a,H,Q,KQ,KQQ,Z,Qdot=bg_eval(data,tau)
    alpha,chi,pchi,palpha=y
    grad,lap,invlap,div=ops
    source=-(palpha+Q*pchi)/(2.0*a)
    combo=invlap(source)
    E=(combo-A*chi)/static.KB
    return E,(a,H,Q,KQ,KQQ,Z,Qdot)


def rhs(data,tau,y,ops,C,nonlinear):
    E,b=derive_E(data,tau,y,ops)
    a,H,Q,KQ,KQQ,Z,Qdot=b
    alpha,chi,pchi,palpha=y
    grad,lap,invlap,div=ops
    U=pchi/(2.0*a**3*KQQ)
    psi=to_field(mode_values(data,tau,"psi"),C)
    if nonlinear:
        g=grad(chi)
        x=static.ACC_CONV*np.abs(g)/a
        j,_=static.j_and_prime(x,1.0,"simple",saturated=False)
        nl=div((1.0+j)*g)
    else:
        nl=lap(chi)
    dalpha=a*(E-psi)
    dchi=a*(U+Q*E+Qdot*alpha)
    dpchi=a*(-2.0*A*a*lap(E)+2.0*A*a*nl-2.0*a*KQ*lap(alpha))
    dpalpha=a*(-2.0*a**3*KQQ*U*Qdot-2.0*a*KQ*lap(chi)+2.0*a*KQ*Q*lap(alpha))
    out=np.stack([dalpha,dchi,dpchi,dpalpha])
    return out


def checkpoint_health(data,tau,y,ops):
    E,b=derive_E(data,tau,y,ops); a,H,Q,KQ,KQQ,Z,Qdot=b
    alpha,chi,pchi,palpha=y; grad,lap,invlap,div=ops
    lhs=palpha+Q*pchi
    rhs0=-2.0*a*static.KB*lap(E)-2.0*A*a*lap(chi)
    cr=norm_residual(lhs-rhs0,lhs,rhs0)
    g=grad(chi); x=static.ACC_CONV*np.abs(g)/a
    j,_=static.j_and_prime(x,1.0,"simple",saturated=False)
    return E,cr,x,j


def integrate(data,nx,nstep,nonlinear,collect_stats=False):
    y,init=initial_state(data,nx); C=cos_matrix(nx); ops=spec_ops(nx)
    t0,t1=data["t0"],data["t1"]; h=(t1-t0)/nstep
    tchecks=data["tau_check"]; ck=[]; ci=0
    stats_x=[]; jmax=-np.inf; onejmin=np.inf; max_constraint=0.0

    def store(t,ycur):
        nonlocal jmax,onejmin,max_constraint
        E,cr,x,j=checkpoint_health(data,t,ycur,ops)
        max_constraint=max(max_constraint,cr)
        ck.append({"tau":float(t),"y":ycur.copy(),"E":E.copy(),"constraint":cr})

    store(t0,y); ci=1
    if collect_stats:
        _,_,x,j=checkpoint_health(data,t0,y,ops); stats_x.append(x.copy()); jmax=max(jmax,float(np.max(j))); onejmin=min(onejmin,float(np.min(1+j)))

    t=t0
    finite=True; fail_reason=None
    for istep in range(nstep):
        k1=rhs(data,t,y,ops,C,nonlinear)
        k2=rhs(data,t+0.5*h,y+0.5*h*k1,ops,C,nonlinear)
        k3=rhs(data,t+0.5*h,y+0.5*h*k2,ops,C,nonlinear)
        k4=rhs(data,t+h,y+h*k3,ops,C,nonlinear)
        yn=y+(h/6.0)*(k1+2*k2+2*k3+k4)
        tn=t+h
        if not np.all(np.isfinite(yn)):
            finite=False; fail_reason=f"nonfinite_state_step_{istep+1}"; break
        while ci<len(tchecks) and tchecks[ci] <= tn+1e-10:
            frac=float((tchecks[ci]-t)/h); frac=min(1.0,max(0.0,frac))
            yc=y+frac*(yn-y)
            store(float(tchecks[ci]),yc); ci+=1
        y=yn; t=tn
        if collect_stats and (istep+1)%8==0:
            _,_,x,j=checkpoint_health(data,t,y,ops); stats_x.append(x.copy()); jmax=max(jmax,float(np.max(j))); onejmin=min(onejmin,float(np.min(1+j)))
    if finite and ci!=len(tchecks):
        finite=False; fail_reason=f"stored_only_{ci}_of_{len(tchecks)}_checkpoints"
    arr=None
    if ck:
        arr=np.stack([q["y"] for q in ck])
    stats={"finite":finite,"fail_reason":fail_reason,"max_constraint":float(max_constraint),"init":init}
    if collect_stats and stats_x:
        xx=np.concatenate(stats_x)
        stats.update({
            "x_max":float(np.max(xx)),"x_p01":float(np.percentile(xx,1)),"x_p50":float(np.percentile(xx,50)),"x_p99":float(np.percentile(xx,99)),
            "x_frac_lt1":float(np.mean(xx<1)),"x_frac_1_10":float(np.mean((xx>=1)&(xx<10))),"x_frac_ge10":float(np.mean(xx>=10)),
            "j_max":float(jmax),"one_plus_j_min":float(onejmin),"n_x_samples":int(xx.size),
        })
    return {"states":arr,"checkpoints":ck,"stats":stats}


def compare_state_runs(a,b,spatial=False):
    names=("alpha","chi","P_chi","P_alpha"); vals={}
    for q,name in enumerate(names):
        aa=a["states"][:,q,:]
        bb=b["states"][:,q,:]
        if spatial:
            bb=np.stack([static.spectral_resample(row,aa.shape[1]) for row in bb])
        vals[name]=rel_l2(aa,bb)
    return vals,max(vals.values())


def linear_class_compare(data,lin,nx):
    C=cos_matrix(nx); vals={"alpha":[],"E":[],"chi":[]}; refs={"alpha":[],"E":[],"chi":[]}
    for i,t in enumerate(data["tau_check"]):
        cf=class_fields(data,float(t),nx,C)
        vals["alpha"].append(lin["states"][i,0])
        vals["chi"].append(lin["states"][i,1])
        vals["E"].append(lin["checkpoints"][i]["E"])
        for k in refs: refs[k].append(cf[k])
    return {k:rel_l2(np.stack(vals[k]),np.stack(refs[k])) for k in vals}


def nonlinear_linear_diag(nl,lin):
    out={
        "alpha":rel_l2(nl["states"][:,0],lin["states"][:,0]),
        "chi":rel_l2(nl["states"][:,1],lin["states"][:,1]),
        "E":rel_l2(np.stack([x["E"] for x in nl["checkpoints"]),np.stack([x["E"] for x in lin["checkpoints"])),
    }
    return out


def run_main(args):
    data=prepare_class_data()
    print("NL1C6D2C6A_PHYSICAL_TIME_SCALAR_CURRENT_INTEGRATOR_START",flush=True)
    print(f"tau_interval={data['t0']:.12e}..{data['t1']:.12e}",flush=True)

    primary=integrate(data,128,4096,True,collect_stats=True)
    timectl=integrate(data,128,8192,True,collect_stats=False)
    spacectl=integrate(data,256,4096,True,collect_stats=False)
    linear=integrate(data,128,4096,False,collect_stats=False)

    init=primary["stats"]["init"]
    i2=max(init["elliptic_residual"],init["pchi_definition_residual"],max(init["zero_mode_relative"].values()))
    linear_err=linear_class_compare(data,linear,128)
    time_fields,time_max=compare_state_runs(primary,timectl,False)
    space_fields,space_max=compare_state_runs(primary,spacectl,True)
    nldiag=nonlinear_linear_diag(primary,linear)

    all_finite=all(x["stats"]["finite"] for x in (primary,timectl,spacectl,linear))
    primary_health=bool(primary["stats"]["max_constraint"]<=CONSTRAINT_GATE and primary["stats"].get("one_plus_j_min",-1)>0 and all_finite)
    gates={
        "I1_corrected_provenance_and_dense_inputs":True,
        "I2_initial_state_le_1e-12":bool(i2<=INITIAL_GATE and init["all_finite"]),
        "I3_linear_alpha_le_5e-3":bool(linear_err["alpha"]<=LINEAR_GATE),
        "I3_linear_E_le_5e-3":bool(linear_err["E"]<=LINEAR_GATE),
        "I3_linear_chi_le_5e-3":bool(linear_err["chi"]<=LINEAR_GATE),
        "I4_nonlinear_trajectory_health":primary_health,
        "I5_time_convergence_le_2e-3":bool(time_max<=TIME_GATE),
        "I6_spatial_convergence_le_5e-3":bool(space_max<=SPACE_GATE),
        "I8_scope_clean":True,
    }
    passed=all(gates.values())
    classification=PASS_LABEL if passed else FAIL_LABEL
    head,branch=git_meta()
    result={
        "classification":classification,"git":{"head":head,"branch":branch},
        "model":{"sigma":0,"interpolation":"simple","beta0":1.0,"memory":False,"eta":0.0},
        "provenance":data["provenance"],"background_audit":data["background_audit"],
        "tau_checkpoints":data["tau_check"].tolist(),"z_checkpoints":CHECK_Z.tolist(),
        "discretization":{"primary":{"Nx":128,"Nstep":4096},"time_control":{"Nx":128,"Nstep":8192},"spatial_control":{"Nx":256,"Nstep":4096},"integrator":"fixed-step classical RK4"},
        "initial_state":{"max_gate_metric":i2,"elliptic_residual":init["elliptic_residual"],"pchi_definition_residual":init["pchi_definition_residual"],"zero_mode_relative":init["zero_mode_relative"]},
        "linear_control_relative_L2":linear_err,
        "primary_health":{k:v for k,v in primary["stats"].items() if k!="init"},
        "time_convergence":{"fields":time_fields,"max":time_max},
        "spatial_convergence":{"fields":space_fields,"max":space_max},
        "nonlinear_vs_linear_descriptive":nldiag,
        "gates":gates,
        "scope":{"nonlinear_matter_evolved":False,"metric_backreaction_nonlinear":False,"memory_or_finite_eta":False,"likelihood":False,"refit":False,"static_R3_solver":False,"branch_continuation":False},
        "D2C6B_all27_licensed":bool(passed),"NL1C7_authorized":False,
    }
    Path(args.json_out).parent.mkdir(parents=True,exist_ok=True)
    Path(args.json_out).write_text(json.dumps(result,indent=2,sort_keys=True,default=str)+"\n")
    print(f"I1_INPUT pass=True",flush=True)
    print(f"I2_INITIAL max={i2:.12e} pass={gates['I2_initial_state_le_1e-12']}",flush=True)
    print(f"I3_LINEAR alpha={linear_err['alpha']:.12e} E={linear_err['E']:.12e} chi={linear_err['chi']:.12e} pass={gates['I3_linear_alpha_le_5e-3'] and gates['I3_linear_E_le_5e-3'] and gates['I3_linear_chi_le_5e-3']}",flush=True)
    print(f"I4_HEALTH constraint={primary['stats']['max_constraint']:.12e} min1pj={primary['stats'].get('one_plus_j_min',float('nan')):.12e} pass={gates['I4_nonlinear_trajectory_health']}",flush=True)
    print(f"I5_TIME max={time_max:.12e} pass={gates['I5_time_convergence_le_2e-3']}",flush=True)
    print(f"I6_SPACE max={space_max:.12e} pass={gates['I6_spatial_convergence_le_5e-3']}",flush=True)
    print(f"I7_RESPONSE alpha={nldiag['alpha']:.12e} E={nldiag['E']:.12e} chi={nldiag['chi']:.12e} x_max={primary['stats'].get('x_max',float('nan')):.12e}",flush=True)
    print(f"CLASSIFICATION={classification}",flush=True)
    print(f"D2C6B_ALL27_LICENSED={passed}",flush=True)
    print(f"JSON={args.json_out}",flush=True)
    print("NL1C6D2C6A_PHYSICAL_TIME_SCALAR_CURRENT_INTEGRATOR_END",flush=True)
    return 0 if passed else 2


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--json-out",required=True); args=ap.parse_args()
    try:
        return run_main(args)
    except InputIncomplete as exc:
        head,branch=git_meta(); result={"classification":INCOMPLETE_LABEL,"git":{"head":head,"branch":branch},"reason":str(exc),"D2C6B_all27_licensed":False,"NL1C7_authorized":False}
        Path(args.json_out).parent.mkdir(parents=True,exist_ok=True); Path(args.json_out).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
        print(f"CLASSIFICATION={INCOMPLETE_LABEL}",flush=True); print(f"REASON={exc}",flush=True); return 3

if __name__=="__main__":
    raise SystemExit(main())
