#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import LinearOperator, gmres

H0=67.3324639084866
h=H0/100.0
OMEGA_B=0.022377376877682164
AS=2.1308864352626987e-9
NS=0.9666229454895277
KPIV=0.05
KB=0.0665
K2=9500.0
Q0=1.0e-4
MU2=2.0*K2*Q0**2/(2.0-KB)
BETAS=(1.0,0.5,0.1)
KINDS=('simple','exponential','sharp')
K_H=np.asarray([0.03,0.05,0.08,0.10,0.15,0.20],float)
K_MPC=K_H*h
MODE_NUM=np.asarray([3,5,8,10,15,20],int)
PHASE=np.asarray([0.13,0.71,1.29,2.03,2.77,3.41],float)
C_KM=299792.458
C=299792458.0
MPC_M=3.0856775814913673e22
A0=1.2e-10
ACC_CONV=C*C/(A0*MPC_M)
ZMIN,ZMAX=0.2,1.5
NX_PRIMARY=256
NX_CONTROL=512
HOMOTOPY=(1/64,1/32,1/16,1/8,1/4,1/2,1.0)
NEWTON_MAX=40
NEWTON_TOL=2e-10
FINAL_R2_GATE=1e-8
FINAL_R1_GATE=1e-10
RES_GATE=5e-3
BRANCH_GATE=1e-4


def rel_l2(a,b):
    a=np.asarray(a); b=np.asarray(b)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(b),1e-300))


def weights_log(k):
    q=np.log(np.asarray(k,float)); w=np.empty_like(q)
    w[0]=0.5*(q[1]-q[0]); w[-1]=0.5*(q[-1]-q[-2])
    w[1:-1]=0.5*(q[2:]-q[:-2])
    return w

WIDTH=weights_log(K_H)
PR=AS*(K_MPC/KPIV)**(NS-1.0)
MODE_AMP=np.sqrt(2.0*WIDTH*PR)
BOX=2*np.pi/(0.01*h)


def kgrid(n):
    return 2*np.pi*np.fft.fftfreq(n,d=BOX/n)


def modegrid(n):
    return np.rint(np.fft.fftfreq(n)*n).astype(int)


def dealias_mask(n):
    return (np.abs(np.fft.fftfreq(n)*n)<=n/3.0+1e-12).astype(float)


def reconstruct(coeff,n):
    x=np.arange(n)*BOX/n
    out=np.zeros(n,float)
    for amp,k,p in zip(np.asarray(coeff,float),K_MPC,PHASE):
        out += amp*np.cos(k*x+p)
    out -= np.mean(out)
    return out


def spectral_resample(field,nnew):
    field=np.asarray(field,float); nold=field.size
    cold=np.fft.fft(field)/nold
    cnew=np.zeros(nnew,complex)
    mold=modegrid(nold); mnew=modegrid(nnew)
    lookup={int(m):i for i,m in enumerate(mnew)}
    for i,m in enumerate(mold):
        j=lookup.get(int(m))
        if j is not None:
            cnew[j]=cold[i]
    out=np.fft.ifft(cnew*nnew).real
    out-=np.mean(out)
    return out


def grad_phys(field,a):
    n=len(field); kk=kgrid(n)
    return np.fft.ifft((1j*kk/a)*np.fft.fft(field)).real


def lap_phys(field,a):
    n=len(field); kk=kgrid(n)
    return np.fft.ifft(-((kk/a)**2)*np.fft.fft(field)).real


def invlap_phys(src,a):
    n=len(src); kk=kgrid(n)/a; sh=np.fft.fft(src)
    out=np.zeros(n,complex); nz=np.abs(kk)>0
    out[nz]=-sh[nz]/(kk[nz]*kk[nz])
    f=np.fft.ifft(out).real; f-=np.mean(f)
    return f


def j_and_prime(x,beta,kind,saturated=False):
    x=np.asarray(x,float)
    if saturated:
        return np.full_like(x,1.0/beta),np.zeros_like(x)
    A=1.0+beta
    if kind=='simple':
        den=A+beta*x
        return x/den, A/(den*den)
    if kind=='exponential':
        c=beta/A; e=np.exp(-c*x)
        return -np.expm1(-c*x)/beta, e/A
    if kind=='sharp':
        xt=A/beta
        lo=x<=xt
        j=np.where(lo,x/A,1.0/beta)
        jp=np.where(lo,1.0/A,0.0)
        return j,jp
    raise ValueError(kind)


def full_operator(chi,a,beta,kind,saturated=False,need_linear_coeff=False):
    n=len(chi); kk=kgrid(n)/a; mask=dealias_mask(n)
    gh=np.fft.fft(chi)
    g=np.fft.ifft(1j*kk*gh).real
    x=ACC_CONV*np.abs(g)
    j,jp=j_and_prime(x,beta,kind,saturated=saturated)
    flux=j*g
    op=np.fft.ifft(1j*kk*(np.fft.fft(flux)*mask)).real
    if need_linear_coeff:
        # d[j(x) g]/dg = j + x dj/dx.
        return op,g,x,j,j+x*jp
    return op,g,x,j


def residual_state(chi,rhs,a,beta,kind,saturated=False):
    op,g,x,j=full_operator(chi,a,beta,kind,saturated=saturated)
    tilde=invlap_phys(op,a)
    phi=tilde+chi
    r=op+MU2*phi-rhs
    return r,op,tilde,phi,g,x,j


def preconditioner(chi,a,beta,kind,saturated=False):
    n=len(chi); kk=kgrid(n)/a
    _,_,_,_,Aeff=full_operator(chi,a,beta,kind,saturated=saturated,need_linear_coeff=True)
    abar=max(float(np.mean(Aeff)),1e-12)
    diag=-abar*kk*kk+MU2*(1.0+abar)
    diag[0]=MU2
    scale=np.maximum(np.abs(-abar*kk*kk)+MU2*(1.0+abar),MU2)
    tiny=np.abs(diag)<1e-8*scale
    diag[tiny]=np.where(diag[tiny]>=0,1.0,-1.0)*1e-8*scale[tiny]
    def mv(v):
        vh=np.fft.fft(np.asarray(v,float))
        return np.fft.ifft(vh/diag).real
    return LinearOperator((n,n),matvec=mv,dtype=float)


def newton_solve(rhs,a,beta,kind,initial,saturated=False):
    rhs=np.asarray(rhs,float).copy(); rhs-=np.mean(rhs)
    chi=np.asarray(initial,float).copy(); chi-=np.mean(chi)
    scale=max(float(np.linalg.norm(rhs)),1e-300)
    history=[]
    for it in range(NEWTON_MAX+1):
        r,op,tilde,phi,g,x,j=residual_state(chi,rhs,a,beta,kind,saturated=saturated)
        rel=float(np.linalg.norm(r)/scale)
        history.append(rel)
        if not np.isfinite(rel):
            return {'success':False,'reason':'nonfinite_residual','chi':chi,'iterations':it,'history':history}
        if rel<=NEWTON_TOL:
            return {'success':True,'reason':'converged','chi':chi,'iterations':it,'history':history}
        if it==NEWTON_MAX:
            break
        _,_,_,_,Aeff=full_operator(chi,a,beta,kind,saturated=saturated,need_linear_coeff=True)
        n=len(chi); kk=kgrid(n)/a; mask=dealias_mask(n)
        def jmv(v):
            v=np.asarray(v,float)
            vg=np.fft.ifft(1j*kk*np.fft.fft(v)).real
            dop=np.fft.ifft(1j*kk*(np.fft.fft(Aeff*vg)*mask)).real
            dtilde=invlap_phys(dop,a)
            return dop+MU2*(dtilde+v)
        J=LinearOperator((n,n),matvec=jmv,dtype=float)
        M=preconditioner(chi,a,beta,kind,saturated=saturated)
        delta,info=gmres(J,-r,M=M,rtol=1e-8,atol=0.0,restart=min(80,n),maxiter=240)
        if not np.all(np.isfinite(delta)):
            return {'success':False,'reason':'nonfinite_newton_step','chi':chi,'iterations':it,'history':history}
        accepted=False
        base=np.linalg.norm(r)
        for alpha in (1.0,0.5,0.25,0.125,0.0625,0.03125,0.015625,0.0078125):
            cand=chi+alpha*delta; cand-=np.mean(cand)
            rc=residual_state(cand,rhs,a,beta,kind,saturated=saturated)[0]
            if np.all(np.isfinite(rc)) and np.linalg.norm(rc)<base:
                chi=cand; accepted=True; break
        if not accepted:
            return {'success':False,'reason':f'line_search_failed_gmres_{info}','chi':chi,'iterations':it,'history':history}
    return {'success':False,'reason':'max_iterations','chi':chi,'iterations':NEWTON_MAX,'history':history}


def solve_homotopy(rhs,a,beta,kind,n,saturated=False):
    chi=np.zeros(n,float); steps=[]
    for lam in HOMOTOPY:
        sol=newton_solve(lam*rhs,a,beta,kind,chi,saturated=saturated)
        steps.append({'lambda':float(lam),'success':bool(sol['success']),'iterations':int(sol['iterations']),
                      'final_relative_residual':float(sol['history'][-1]),'reason':sol['reason']})
        if not sol['success']:
            return sol,steps
        chi=sol['chi']
    sol['homotopy_steps']=steps
    return sol,steps


def high_gradient_analytic(source,a,beta):
    n=len(source); kphys=kgrid(n)/a; sh=np.fft.fft(source)
    den=(1.0+beta)*MU2-kphys*kphys
    ph=np.zeros(n,complex)
    nz=np.abs(kphys)>0
    # Only sourced Fourier modes enter; denominators at unsourced modes are irrelevant.
    active=nz & (np.abs(sh)>1e-13*max(np.max(np.abs(sh)),1e-300))
    if np.any(np.abs(den[active])<1e-12*np.maximum((1.0+beta)*MU2,kphys[active]**2)):
        raise RuntimeError('high-gradient sourced Helmholtz pole approached')
    ph[active]=sh[active]/den[active]
    phi=np.fft.ifft(ph).real; phi-=np.mean(phi)
    chi=(beta/(1.0+beta))*phi
    return chi,phi


def low_modes(field,mmax=32):
    c=np.fft.fft(field)/len(field)
    return np.asarray([c[m] for m in range(1,mmax+1)])


def diagnostics(chi,rhs,a,beta,kind):
    r,op,tilde,phi,g,x,j=residual_state(chi,rhs,a,beta,kind)
    r2=float(np.linalg.norm(r)/max(np.linalg.norm(rhs),1e-300))
    r1=lap_phys(tilde,a)-op
    r1scale=max(np.linalg.norm(op),np.linalg.norm(rhs),1e-300)
    r1rel=float(np.linalg.norm(r1)/r1scale)
    gt=grad_phys(tilde,a); gp=grad_phys(phi,a)
    xrms=float(np.sqrt(np.mean(x*x)))
    return {
        'R1_relative_L2':r1rel,'R2_relative_L2':r2,
        'x_rms':xrms,'x_min':float(np.min(x)),'x_median':float(np.median(x)),'x_max':float(np.max(x)),
        'fraction_x_lt_0p1':float(np.mean(x<0.1)),
        'fraction_x_0p1_to_10':float(np.mean((x>=0.1)&(x<=10.0))),
        'fraction_x_gt_10':float(np.mean(x>10.0)),
        'j_min':float(np.min(j)),'j_mean':float(np.mean(j)),'j_max':float(np.max(j)),
        'chi_gradient_rms_1_per_Mpc':float(np.sqrt(np.mean(g*g))),
        'tildePhi_gradient_rms_1_per_Mpc':float(np.sqrt(np.mean(gt*gt))),
        'Phi_gradient_rms_1_per_Mpc':float(np.sqrt(np.mean(gp*gp))),
        'chi_rms':float(np.sqrt(np.mean(chi*chi))),
        'tildePhi_rms':float(np.sqrt(np.mean(tilde*tilde))),
        'Phi_rms':float(np.sqrt(np.mean(phi*phi))),
        'rhs_rms_1_per_Mpc2':float(np.sqrt(np.mean(rhs*rhs))),
        'finite':bool(np.all(np.isfinite(chi)) and np.all(np.isfinite(tilde)) and np.all(np.isfinite(phi)) and np.all(np.isfinite(r)))
    },tilde,phi


def mode_indices(kh_native):
    idx=[]; misses=[]
    for target in K_H:
        j=int(np.argmin(np.abs(kh_native-target)))
        miss=abs(kh_native[j]-target)/target
        idx.append(j); misses.append(miss)
    return np.asarray(idx,int),float(max(misses))


def source_for(db6_col,z,n):
    a=1.0/(1.0+z)
    delta_coeff=MODE_AMP*np.asarray(db6_col,float)
    source_pref=1.5*(100.0/C_KM)**2*OMEGA_B*a**-3
    source_coeff=source_pref*delta_coeff
    delta=reconstruct(delta_coeff,n)
    source=reconstruct(source_coeff,n)
    source-=np.mean(source)
    return delta,source,a


def solve_branch(db6,z,beta,kind,n=NX_PRIMARY):
    nz=len(z); sols=[None]*nz; records=[None]*nz
    order=np.argsort(-z)  # largest z to smallest z
    prev=None
    for count,it in enumerate(order):
        delta,source,a=source_for(db6[:,it],z[it],n)
        rhs=source/(1.0+beta)
        if prev is None:
            sol,steps=solve_homotopy(rhs,a,beta,kind,n)
            used='first_slice_fixed_homotopy'
        else:
            sol=newton_solve(rhs,a,beta,kind,prev)
            steps=[]; used='previous_time_direct'
            if not sol['success']:
                sol,steps=solve_homotopy(rhs,a,beta,kind,n)
                used='fixed_homotopy_fallback'
        if not sol['success']:
            records[it]={'index':int(it),'z':float(z[it]),'a':float(a),'solver_success':False,
                         'solver_reason':sol['reason'],'solver_path':used,'solver_iterations':int(sol['iterations']),
                         'final_solver_relative_residual':float(sol['history'][-1]),'homotopy_steps':steps}
            return False,sols,records
        chi=sol['chi']; chi-=np.mean(chi); prev=chi.copy(); sols[it]=chi
        d,tilde,phi=diagnostics(chi,rhs,a,beta,kind)
        records[it]={'index':int(it),'z':float(z[it]),'a':float(a),'solver_success':True,
                     'solver_reason':sol['reason'],'solver_path':used,'solver_iterations':int(sol['iterations']),
                     'final_solver_relative_residual':float(sol['history'][-1]),'homotopy_steps':steps,
                     'delta_b_rms':float(np.sqrt(np.mean(delta*delta))),**d}
    return True,sols,records


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input-npz',required=True)
    ap.add_argument('--input-zip-sha256',default='')
    ap.add_argument('--json-out',required=True)
    ap.add_argument('--npz-out',required=True)
    args=ap.parse_args()

    d=np.load(args.input_npz)
    kh=np.asarray(d['k_native_h'],float); z=np.asarray(d['z_native'],float); db=np.asarray(d['d_b'],float)
    if db.shape!=(kh.size,z.size):
        raise RuntimeError(f'd_b orientation mismatch {db.shape} vs {(kh.size,z.size)}')
    idx,kmiss=mode_indices(kh); db6=db[idx,:]
    eval_idx=np.where((z>=ZMIN-1e-12)&(z<=ZMAX+1e-12))[0]
    input_gates={
        'artifact_sha256_matches':args.input_zip_sha256=='0ab60cbc32210ad3fb75c881f91a9db11148280e9223ea644680ed8cdfbaa590',
        'requested_k_match_le_1e-12':kmiss<=1e-12,
        'minimum_8_native_times':len(eval_idx)>=8,
        'finite_baryon_state':bool(np.all(np.isfinite(db6))),
    }

    # G2: constant-j high-gradient regression on all evaluation snapshots.
    regression={}; regression_pass=True; regmax=0.0
    for beta in BETAS:
        rows=[]
        for it in eval_idx:
            _,source,a=source_for(db6[:,it],z[it],NX_PRIMARY)
            rhs=source/(1.0+beta)
            chi_ref,phi_ref=high_gradient_analytic(source,a,beta)
            sol=newton_solve(rhs,a,beta,'simple',chi_ref,saturated=True)
            if sol['success']:
                chi=sol['chi']; rr,op,tilde,phi,g,x,j=residual_state(chi,rhs,a,beta,'simple',saturated=True)
                echi=rel_l2(chi,chi_ref); ephi=rel_l2(phi,phi_ref)
                err=max(echi,ephi,float(np.linalg.norm(rr)/max(np.linalg.norm(rhs),1e-300)))
            else:
                echi=ephi=err=float('inf')
            regmax=max(regmax,err); ok=bool(sol['success'] and err<=1e-10)
            regression_pass=regression_pass and ok
            rows.append({'index':int(it),'z':float(z[it]),'chi_relative_L2':float(echi),
                         'Phi_relative_L2':float(ephi),'max_regression_error':float(err),'pass':ok})
        regression[str(beta)]={'rows':rows,'pass':bool(all(r['pass'] for r in rows))}

    branches={}; primary_store=[]; primary_names=[]
    all_solve=True; all_r1=True; all_r2=True; all_finite=True; all_res=True; no_multibranch=True
    max_r1=max_r2=max_res=max_branch=0.0

    for kind in KINDS:
        branches[kind]={}
        for beta in BETAS:
            success,sols,records=solve_branch(db6,z,beta,kind,NX_PRIMARY)
            branch={'primary_success':bool(success),'primary_records':records}
            if not success:
                all_solve=False; all_r1=False; all_r2=False; all_finite=False; all_res=False
                branches[kind][str(beta)]=branch
                continue

            primary=np.asarray(sols,float)
            primary_store.append(primary); primary_names.append(f'{kind}_beta{beta:g}')
            br_r1=max(r['R1_relative_L2'] for r in records)
            br_r2=max(r['R2_relative_L2'] for r in records)
            br_fin=all(r['finite'] for r in records)
            max_r1=max(max_r1,br_r1); max_r2=max(max_r2,br_r2)
            all_r1=all_r1 and br_r1<=FINAL_R1_GATE
            all_r2=all_r2 and br_r2<=FINAL_R2_GATE
            all_finite=all_finite and br_fin

            controls=[]; branch_checks=[]; br_res=0.0; br_branch=0.0; branch_multi=False
            for it in eval_idx:
                _,source512,a=source_for(db6[:,it],z[it],NX_CONTROL); rhs512=source512/(1.0+beta)
                init512=spectral_resample(primary[it],NX_CONTROL)
                csol=newton_solve(rhs512,a,beta,kind,init512)
                if not csol['success']:
                    csol,_=solve_homotopy(rhs512,a,beta,kind,NX_CONTROL)
                if csol['success']:
                    cd,ct,cp=diagnostics(csol['chi'],rhs512,a,beta,kind)
                    pd,pt,pp=diagnostics(primary[it],source_for(db6[:,it],z[it],NX_PRIMARY)[1]/(1.0+beta),a,beta,kind)
                    chi_rel=rel_l2(low_modes(primary[it]),low_modes(csol['chi']))
                    phi_rel=rel_l2(low_modes(pp),low_modes(cp))
                    xr_rel=abs(pd['x_rms']-cd['x_rms'])/max(abs(cd['x_rms']),1e-300)
                    cres=max(chi_rel,phi_rel,xr_rel)
                else:
                    chi_rel=phi_rel=xr_rel=cres=float('inf')
                br_res=max(br_res,cres)
                controls.append({'index':int(it),'z':float(z[it]),'control_success':bool(csol['success']),
                                 'chi_lowmode_relative_L2':float(chi_rel),'Phi_lowmode_relative_L2':float(phi_rel),
                                 'x_rms_relative':float(xr_rel),'max_resolution_discrepancy':float(cres)})

                # G5 independent deterministic starts at primary resolution.
                _,source256,a256=source_for(db6[:,it],z[it],NX_PRIMARY); rhs256=source256/(1.0+beta)
                hg,_=high_gradient_analytic(source256,a256,beta)
                mass=rhs256/MU2; mass-=np.mean(mass)
                alt=[]
                for label,start in [('high_gradient',hg),('mass_dominated',mass)]:
                    ss=newton_solve(rhs256,a256,beta,kind,start)
                    if ss['success']:
                        dd,_,_=diagnostics(ss['chi'],rhs256,a256,beta,kind)
                        valid=bool(dd['R2_relative_L2']<=FINAL_R2_GATE and dd['R1_relative_L2']<=FINAL_R1_GATE and dd['finite'])
                        diff=rel_l2(low_modes(ss['chi']),low_modes(primary[it])) if valid else float('inf')
                    else:
                        valid=False; diff=float('inf')
                    if valid:
                        br_branch=max(br_branch,diff)
                        if diff>BRANCH_GATE: branch_multi=True
                    alt.append({'start':label,'solver_success':bool(ss['success']),'residual_valid':bool(valid),
                                'relative_lowmode_difference_from_continuation':float(diff)})
                branch_checks.append({'index':int(it),'z':float(z[it]),'alternate_starts':alt})

            max_res=max(max_res,br_res); max_branch=max(max_branch,br_branch)
            all_res=all_res and br_res<=RES_GATE
            no_multibranch=no_multibranch and (not branch_multi)
            branch.update({'max_R1_relative_L2':float(br_r1),'max_R2_relative_L2':float(br_r2),
                           'all_finite':bool(br_fin),'resolution_controls':controls,
                           'max_resolution_discrepancy':float(br_res),'branch_checks':branch_checks,
                           'max_valid_alternate_branch_difference':float(br_branch),
                           'distinct_residual_valid_root_found':bool(branch_multi)})
            branches[kind][str(beta)]=branch

    gates={
        'G1_input_identity':bool(all(input_gates.values())),
        'G2_high_gradient_regression':bool(regression_pass and regmax<=1e-10),
        'G3_all_primary_solutions_converged':bool(all_solve),
        'G3_R1_le_1e-10':bool(all_r1),
        'G3_R2_le_1e-8':bool(all_r2),
        'G3_all_finite':bool(all_finite),
        'G4_resolution_le_5e-3':bool(all_res),
        'G5_no_distinct_residual_valid_root':bool(no_multibranch),
    }
    g1g4=bool(gates['G1_input_identity'] and gates['G2_high_gradient_regression'] and
              gates['G3_all_primary_solutions_converged'] and gates['G3_R1_le_1e-10'] and
              gates['G3_R2_le_1e-8'] and gates['G3_all_finite'] and gates['G4_resolution_le_5e-3'])
    if not g1g4:
        classification='NL1C6_FULL_J_BARYONIC_RECLOSURE_FAIL'
    elif not gates['G5_no_distinct_residual_valid_root']:
        classification='NL1C6_FULL_J_MULTIBRANCH_REQUIRES_BOUNDARY_SELECTION'
    else:
        classification='NL1C6_FULL_J_BARYONIC_RECLOSURE_PASS'

    result={
        'classification':classification,
        'scope':'fixed-state periodic physical-coordinate quasistatic/subhorizon full-J AeST snapshot reclosure using frozen native CLASS baryon transfer; no matter re-evolution, finite eta, memory forcing, observational data or likelihood',
        'physical_eta':0.0,'memory_source_evaluated':False,'uses_observational_data':False,
        'input_artifact':{'id':10101422385,'expected_zip_sha256':'0ab60cbc32210ad3fb75c881f91a9db11148280e9223ea644680ed8cdfbaa590',
                          'observed_zip_sha256':args.input_zip_sha256},
        'frozen':{'H0_km_s_Mpc':H0,'omega_b':OMEGA_B,'As':AS,'ns':NS,'kpiv_1_per_Mpc':KPIV,
                  'KB':KB,'K2':K2,'Q0_1_per_Mpc':Q0,'mu2_1_per_Mpc2':MU2,'a0_m_s2':A0,
                  'beta0_co_primary':list(BETAS),'interpolations':list(KINDS),'k_h_per_Mpc':K_H.tolist(),
                  'phases_rad':PHASE.tolist(),'box_Mpc':BOX,'Nx_primary':NX_PRIMARY,'Nx_control':NX_CONTROL,
                  'homotopy_lambda':list(HOMOTOPY),'Newton_max_iterations':NEWTON_MAX},
        'input_audit':{'requested_k_relative_miss_max':float(kmiss),'n_native_times':int(len(z)),
                       'evaluation_indices':[int(i) for i in eval_idx],'n_evaluation_times':int(len(eval_idx)),
                       'z_native':z.tolist(),'input_gates':input_gates},
        'high_gradient_regression':regression,'max_high_gradient_regression_error':float(regmax),
        'branches':branches,
        'global_metrics':{'max_R1_relative_L2':float(max_r1),'max_R2_relative_L2':float(max_r2),
                          'max_resolution_discrepancy':float(max_res),
                          'max_valid_alternate_branch_difference':float(max_branch)},
        'gates':gates,'historical_results_unchanged':True,
        'continuation_rule':'Only a single numerically controlled full-J branch permits the next eta=0 retarded-memory source/tangent test on the reclosed native-time chi trajectory.'
    }
    Path(args.json_out).parent.mkdir(parents=True,exist_ok=True)
    Path(args.json_out).write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=True)+'\n')

    arrays={'z_native':z,'a_native':1.0/(1.0+z),'k_native_h':kh,'selected_k_indices':idx,
            'selected_d_b':db6,'mode_amp':MODE_AMP,'phase':PHASE,'box_Mpc':np.asarray([BOX]),
            'kind_names':np.asarray(primary_names,dtype='U32')}
    if primary_store:
        arrays['chi_primary']=np.asarray(primary_store,float)
    np.savez_compressed(args.npz_out,**arrays)
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=True))
    if classification=='NL1C6_FULL_J_BARYONIC_RECLOSURE_FAIL':
        raise SystemExit(2)


if __name__=='__main__':
    main()
