#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import numpy as np
from scipy.sparse.linalg import LinearOperator, gmres

from nl1c6 import full_j_baryonic_reclosure as base

# NL1C6R3 changes only the numerical continuation route.  The physical
# endpoint at theta=1 is exactly the original full-J baryonic equation.
THETA_SEEDS=tuple(2.0**(-p) for p in range(8,31,2))
DS_INITIAL=1.0e-2
DS_MIN=1.0e-8
DS_MAX=1.0e-1
ARC_MAX_ACCEPTED=1200
ARC_NEWTON_MAX=40
ARC_TOL=2.0e-10
THETA_BOUND=2.0
FIXED_NEWTON_MAX=80
FIXED_TOL=2.0e-10

RECOVERY_REPORTS=[]


def rms(v):
    v=np.asarray(v,float)
    return float(np.sqrt(np.mean(v*v)))


def constitutive_state(chi,a,beta,kind,theta,route,need_linear_coeff=False):
    chi=np.asarray(chi,float)
    n=len(chi)
    kk=base.kgrid(n)/a
    mask=base.dealias_mask(n)
    g=np.fft.ifft(1j*kk*np.fft.fft(chi)).real
    x=base.ACC_CONV*np.abs(g)
    jf,jp=base.j_and_prime(x,beta,kind,saturated=False)
    if route=='screened':
        j=(1.0-theta)/beta + theta*jf
        aeff=(1.0-theta)/beta + theta*(jf+x*jp)
        djdtheta=jf-1.0/beta
    elif route=='mass':
        j=theta*jf
        aeff=theta*(jf+x*jp)
        djdtheta=jf
    else:
        raise ValueError(route)
    op=np.fft.ifft(1j*kk*(np.fft.fft(j*g)*mask)).real
    if need_linear_coeff:
        return op,g,x,j,aeff,djdtheta
    return op,g,x,j


def residual_theta(chi,rhs,a,beta,kind,theta,route):
    op,g,x,j=constitutive_state(chi,a,beta,kind,theta,route)
    tilde=base.invlap_phys(op,a)
    phi=tilde+chi
    r=op+base.MU2*phi-rhs
    return r,op,tilde,phi,g,x,j


def theta_field_jvp(chi,a,beta,kind,theta,route,v):
    _,_,_,_,aeff,_=constitutive_state(
        chi,a,beta,kind,theta,route,need_linear_coeff=True
    )
    n=len(chi)
    kk=base.kgrid(n)/a
    mask=base.dealias_mask(n)
    v=np.asarray(v,float)
    vg=np.fft.ifft(1j*kk*np.fft.fft(v)).real
    dop=np.fft.ifft(1j*kk*(np.fft.fft(aeff*vg)*mask)).real
    return dop+base.MU2*(base.invlap_phys(dop,a)+v)


def theta_column(chi,a,beta,kind,theta,route):
    _,g,_,_,_,djdtheta=constitutive_state(
        chi,a,beta,kind,theta,route,need_linear_coeff=True
    )
    n=len(chi)
    kk=base.kgrid(n)/a
    mask=base.dealias_mask(n)
    dop=np.fft.ifft(1j*kk*(np.fft.fft(djdtheta*g)*mask)).real
    return dop+base.MU2*base.invlap_phys(dop,a)


def theta_preconditioner(chi,a,beta,kind,theta,route):
    n=len(chi)
    kk=base.kgrid(n)/a
    _,_,_,_,aeff,_=constitutive_state(
        chi,a,beta,kind,theta,route,need_linear_coeff=True
    )
    abar=float(np.mean(aeff))
    # The anchors permit non-negative Aeff; guard only the numerical inverse.
    if not np.isfinite(abar):
        abar=0.0
    diag=-abar*kk*kk+base.MU2*(1.0+abar)
    diag[0]=base.MU2
    scale=np.maximum(np.abs(-abar*kk*kk)+base.MU2*(1.0+abs(abar)),base.MU2)
    tiny=np.abs(diag)<1e-8*scale
    signs=np.where(diag>=0.0,1.0,-1.0)
    diag[tiny]=signs[tiny]*1e-8*scale[tiny]
    def mv(v):
        vh=np.fft.fft(np.asarray(v,float))
        return np.fft.ifft(vh/diag).real
    return LinearOperator((n,n),matvec=mv,dtype=float)


def fixed_theta_solve(rhs,a,beta,kind,theta,route,initial):
    rhs=np.asarray(rhs,float).copy(); rhs-=np.mean(rhs)
    chi=np.asarray(initial,float).copy(); chi-=np.mean(chi)
    scale=max(float(np.linalg.norm(rhs)),1e-300)
    history=[]; accepted_alpha=[]
    for it in range(FIXED_NEWTON_MAX+1):
        r=residual_theta(chi,rhs,a,beta,kind,theta,route)[0]
        rel=float(np.linalg.norm(r)/scale)
        history.append(rel)
        if not np.isfinite(rel):
            return {'success':False,'reason':'nonfinite_residual','chi':chi,
                    'iterations':it,'history':history,'accepted_alpha':accepted_alpha}
        if rel<=FIXED_TOL:
            return {'success':True,'reason':'converged','chi':chi,
                    'iterations':it,'history':history,'accepted_alpha':accepted_alpha}
        if it==FIXED_NEWTON_MAX:
            break
        n=len(chi)
        J=LinearOperator((n,n),matvec=lambda v: theta_field_jvp(
            chi,a,beta,kind,theta,route,v),dtype=float)
        M=theta_preconditioner(chi,a,beta,kind,theta,route)
        delta,info=gmres(J,-r,M=M,rtol=1e-8,atol=0.0,
                         restart=min(80,n),maxiter=300)
        if info!=0 or not np.all(np.isfinite(delta)):
            return {'success':False,'reason':f'gmres_failed_{info}','chi':chi,
                    'iterations':it,'history':history,'accepted_alpha':accepted_alpha}
        norm0=float(np.linalg.norm(r)); accepted=False
        for m in range(41):
            alpha=2.0**(-m)
            cand=chi+alpha*delta; cand-=np.mean(cand)
            rc=residual_theta(cand,rhs,a,beta,kind,theta,route)[0]
            if np.all(np.isfinite(rc)) and float(np.linalg.norm(rc))<norm0:
                chi=cand; accepted_alpha.append(float(alpha)); accepted=True; break
        if not accepted:
            return {'success':False,'reason':f'line_search_failed_gmres_{info}','chi':chi,
                    'iterations':it,'history':history,'accepted_alpha':accepted_alpha}
    return {'success':False,'reason':'max_iterations','chi':chi,
            'iterations':FIXED_NEWTON_MAX,'history':history,
            'accepted_alpha':accepted_alpha}


def full_field_jvp(chi,a,beta,kind,v,saturated=False):
    _,_,_,_,aeff=base.full_operator(
        chi,a,beta,kind,saturated=saturated,need_linear_coeff=True)
    n=len(chi); kk=base.kgrid(n)/a; mask=base.dealias_mask(n)
    vg=np.fft.ifft(1j*kk*np.fft.fft(np.asarray(v,float))).real
    dop=np.fft.ifft(1j*kk*(np.fft.fft(aeff*vg)*mask)).real
    return dop+base.MU2*(base.invlap_phys(dop,a)+v)


def fixed_full_solve(rhs,a,beta,kind,initial,saturated=False):
    rhs=np.asarray(rhs,float).copy(); rhs-=np.mean(rhs)
    chi=np.asarray(initial,float).copy(); chi-=np.mean(chi)
    scale=max(float(np.linalg.norm(rhs)),1e-300)
    history=[]; accepted_alpha=[]
    for it in range(FIXED_NEWTON_MAX+1):
        r=base.residual_state(chi,rhs,a,beta,kind,saturated=saturated)[0]
        rel=float(np.linalg.norm(r)/scale); history.append(rel)
        if not np.isfinite(rel):
            return {'success':False,'reason':'nonfinite_residual','chi':chi,
                    'iterations':it,'history':history,'accepted_alpha':accepted_alpha}
        if rel<=FIXED_TOL:
            return {'success':True,'reason':'converged','chi':chi,
                    'iterations':it,'history':history,'accepted_alpha':accepted_alpha}
        if it==FIXED_NEWTON_MAX: break
        n=len(chi)
        J=LinearOperator((n,n),matvec=lambda v: full_field_jvp(
            chi,a,beta,kind,v,saturated=saturated),dtype=float)
        M=base.preconditioner(chi,a,beta,kind,saturated=saturated)
        delta,info=gmres(J,-r,M=M,rtol=1e-8,atol=0.0,
                         restart=min(80,n),maxiter=300)
        if info!=0 or not np.all(np.isfinite(delta)):
            return {'success':False,'reason':f'gmres_failed_{info}','chi':chi,
                    'iterations':it,'history':history,'accepted_alpha':accepted_alpha}
        norm0=float(np.linalg.norm(r)); accepted=False
        for m in range(41):
            alpha=2.0**(-m)
            cand=chi+alpha*delta; cand-=np.mean(cand)
            rc=base.residual_state(cand,rhs,a,beta,kind,saturated=saturated)[0]
            if np.all(np.isfinite(rc)) and float(np.linalg.norm(rc))<norm0:
                chi=cand; accepted_alpha.append(float(alpha)); accepted=True; break
        if not accepted:
            return {'success':False,'reason':f'line_search_failed_gmres_{info}','chi':chi,
                    'iterations':it,'history':history,'accepted_alpha':accepted_alpha}
    return {'success':False,'reason':'max_iterations','chi':chi,
            'iterations':FIXED_NEWTON_MAX,'history':history,
            'accepted_alpha':accepted_alpha}


def arc_inner(y1,t1,y2,t2):
    return float(np.mean(np.asarray(y1)*np.asarray(y2))+float(t1)*float(t2))


def normalized_secant(chi0,th0,chi1,th1,chi_scale,previous=None):
    dy=(np.asarray(chi1)-np.asarray(chi0))/chi_scale
    dt=float(th1-th0)
    nn=float(np.sqrt(max(arc_inner(dy,dt,dy,dt),1e-300)))
    ty=dy/nn; tt=dt/nn
    if previous is not None and arc_inner(ty,tt,previous[0],previous[1])<0.0:
        ty=-ty; tt=-tt
    return ty,float(tt)


def augmented_measure(chi,theta,rhs,a,beta,kind,route,
                      chi_pred,theta_pred,ty,tt,chi_scale):
    rhs_scale=max(float(np.linalg.norm(rhs)),1e-300)
    r=residual_theta(chi,rhs,a,beta,kind,theta,route)[0]
    frel=float(np.linalg.norm(r)/rhs_scale)
    g=float(np.mean(((chi-chi_pred)/chi_scale)*ty)+(theta-theta_pred)*tt)
    combined=float(np.sqrt(frel*frel+g*g))
    return r,frel,g,combined


def augmented_corrector(rhs,a,beta,kind,route,chi_pred,theta_pred,
                        ty,tt,chi_scale):
    rhs=np.asarray(rhs,float); rhs_scale=max(float(np.linalg.norm(rhs)),1e-300)
    chi=np.asarray(chi_pred,float).copy(); theta=float(theta_pred)
    history=[]; accepted_alpha=[]; n=len(chi)
    for it in range(ARC_NEWTON_MAX+1):
        r,frel,g,combined=augmented_measure(
            chi,theta,rhs,a,beta,kind,route,
            chi_pred,theta_pred,ty,tt,chi_scale)
        history.append((frel,g,combined,theta))
        if not np.isfinite(combined):
            return {'success':False,'reason':'nonfinite_augmented_residual','chi':chi,
                    'theta':theta,'iterations':it,'field_relative_residual':frel,
                    'accepted_alpha':accepted_alpha}
        if frel<=ARC_TOL and abs(g)<=ARC_TOL:
            return {'success':True,'reason':'converged','chi':chi,'theta':theta,
                    'iterations':it,'field_relative_residual':frel,
                    'accepted_alpha':accepted_alpha}
        if it==ARC_NEWTON_MAX: break

        qtheta=theta_column(chi,a,beta,kind,theta,route)
        Mfield=theta_preconditioner(chi,a,beta,kind,theta,route)

        def aug_mv(q):
            q=np.asarray(q,float); dy=q[:n]; dt=float(q[n])
            dchi=chi_scale*dy
            first=(theta_field_jvp(chi,a,beta,kind,theta,route,dchi)+qtheta*dt)/rhs_scale
            last=float(np.mean(dy*ty)+dt*tt)
            return np.concatenate([first,np.asarray([last])])

        # Frozen bordered preconditioner.  M_A maps normalized field residuals
        # to dimensionless dy corrections.
        wchi=Mfield.matvec(qtheta)
        w=wchi/chi_scale
        den=float(tt-np.mean(ty*w))

        def prec_mv(q):
            q=np.asarray(q,float)
            zchi=Mfield.matvec(rhs_scale*q[:n])
            z=zchi/chi_scale
            gamma=float(q[n])
            if (not np.isfinite(den)) or abs(den)<1e-12:
                return np.concatenate([z,np.asarray([gamma])])
            dt=(gamma-float(np.mean(ty*z)))/den
            dy=z-w*dt
            return np.concatenate([dy,np.asarray([dt])])

        A=LinearOperator((n+1,n+1),matvec=aug_mv,dtype=float)
        P=LinearOperator((n+1,n+1),matvec=prec_mv,dtype=float)
        b=np.concatenate([-r/rhs_scale,np.asarray([-g])])
        dq,info=gmres(A,b,M=P,rtol=1e-10,atol=0.0,
                      restart=min(100,n+1),maxiter=600)
        if info!=0 or not np.all(np.isfinite(dq)):
            return {'success':False,'reason':f'augmented_gmres_failed_{info}','chi':chi,
                    'theta':theta,'iterations':it,'field_relative_residual':frel,
                    'accepted_alpha':accepted_alpha}
        dy=dq[:n]; dt=float(dq[n]); accepted=False
        for m in range(41):
            alpha=2.0**(-m)
            cchi=chi+alpha*chi_scale*dy; cchi-=np.mean(cchi)
            ctheta=theta+alpha*dt
            _,cf,cg,cc=augmented_measure(
                cchi,ctheta,rhs,a,beta,kind,route,
                chi_pred,theta_pred,ty,tt,chi_scale)
            if np.isfinite(cc) and cc<combined:
                chi=cchi; theta=float(ctheta); accepted_alpha.append(float(alpha)); accepted=True; break
        if not accepted:
            return {'success':False,'reason':'augmented_line_search_failed','chi':chi,
                    'theta':theta,'iterations':it,'field_relative_residual':frel,
                    'accepted_alpha':accepted_alpha}
    return {'success':False,'reason':'augmented_max_iterations','chi':chi,
            'theta':theta,'iterations':ARC_NEWTON_MAX,
            'field_relative_residual':float(history[-1][0]),
            'accepted_alpha':accepted_alpha}


def anchor_initial(rhs,a,beta,kind,route):
    if route=='screened':
        # base.high_gradient_analytic expects the pre-(1+beta) source.
        source=(1.0+beta)*np.asarray(rhs,float)
        chi,_=base.high_gradient_analytic(source,a,beta)
    elif route=='mass':
        chi=np.asarray(rhs,float)/base.MU2; chi-=np.mean(chi)
    else:
        raise ValueError(route)
    return np.asarray(chi,float)


def summarize_path(path):
    accepted=[p for p in path if p['accepted']]
    thetas=[p['theta'] for p in accepted]
    dss=[p['ds'] for p in accepted if p['ds'] is not None]
    folds=0
    if len(thetas)>=3:
        prev=np.sign(thetas[1]-thetas[0])
        for i in range(2,len(thetas)):
            cur=np.sign(thetas[i]-thetas[i-1])
            if cur!=0 and prev!=0 and cur!=prev: folds+=1
            if cur!=0: prev=cur
    return {
        'accepted_points':len(accepted),
        'theta_min':float(min(thetas)) if thetas else float('nan'),
        'theta_max':float(max(thetas)) if thetas else float('nan'),
        'ds_min_used':float(min(dss)) if dss else 0.0,
        'fold_count':int(folds),
        'rejected_points':int(sum(not p['accepted'] for p in path)),
    }


def anchor_route_solve(rhs,a,beta,kind,n,route):
    rhs=np.asarray(rhs,float).copy(); rhs-=np.mean(rhs)
    anchor=anchor_initial(rhs,a,beta,kind,route)
    r0=residual_theta(anchor,rhs,a,beta,kind,0.0,route)[0]
    scale=max(float(np.linalg.norm(rhs)),1e-300)
    rel0=float(np.linalg.norm(r0)/scale)
    path=[{'accepted':True,'theta':0.0,'ds':None,'iterations':0,
           'field_relative_residual':rel0,'reason':'exact_anchor'}]
    if not np.isfinite(rel0) or rel0>FIXED_TOL:
        return {'success':False,'reason':'anchor_not_residual_valid','chi':anchor,
                'iterations':0,'history':[rel0],
                'route_summary':{**summarize_path(path),'route':route,'seed_theta':None,
                                 'final_reason':'anchor_not_residual_valid'}}

    seed=None; seed_theta=None
    for th in THETA_SEEDS:
        cand=fixed_theta_solve(rhs,a,beta,kind,th,route,anchor)
        if cand['success']:
            seed=cand; seed_theta=float(th); break
    if seed is None:
        return {'success':False,'reason':'no_seed_theta_converged','chi':anchor,
                'iterations':0,'history':[rel0],
                'route_summary':{**summarize_path(path),'route':route,'seed_theta':None,
                                 'final_reason':'no_seed_theta_converged'}}

    path.append({'accepted':True,'theta':seed_theta,'ds':seed_theta,
                 'iterations':int(seed['iterations']),
                 'field_relative_residual':float(seed['history'][-1]),
                 'reason':'seed'})
    chi_scale=max(rms(anchor),scale/(base.MU2*np.sqrt(float(n))),1e-300)
    chi_prev=anchor.copy(); th_prev=0.0
    chi_cur=np.asarray(seed['chi'],float).copy(); th_cur=seed_theta
    tangent=normalized_secant(chi_prev,th_prev,chi_cur,th_cur,chi_scale)
    ds=DS_INITIAL; accepted_count=2

    while accepted_count<ARC_MAX_ACCEPTED:
        ty,tt=normalized_secant(chi_prev,th_prev,chi_cur,th_cur,chi_scale,previous=tangent)
        tangent=(ty,tt)
        chi_pred=chi_cur+ds*chi_scale*ty
        th_pred=th_cur+ds*tt
        corr=augmented_corrector(rhs,a,beta,kind,route,chi_pred,th_pred,ty,tt,chi_scale)
        if not corr['success']:
            path.append({'accepted':False,'theta':float(corr['theta']),'ds':float(ds),
                         'iterations':int(corr['iterations']),
                         'field_relative_residual':float(corr['field_relative_residual']),
                         'reason':corr['reason']})
            nxt=0.5*ds
            if nxt<DS_MIN:
                summary={**summarize_path(path),'route':route,'seed_theta':seed_theta,
                         'final_reason':'arclength_ds_below_min'}
                return {'success':False,'reason':'arclength_ds_below_min',
                        'chi':np.asarray(corr['chi'],float),'iterations':int(corr['iterations']),
                        'history':[float(corr['field_relative_residual'])],
                        'route_summary':summary}
            ds=max(nxt,DS_MIN); continue

        chi_new=np.asarray(corr['chi'],float).copy(); th_new=float(corr['theta'])
        accepted_count+=1
        path.append({'accepted':True,'theta':th_new,'ds':float(ds),
                     'iterations':int(corr['iterations']),
                     'field_relative_residual':float(corr['field_relative_residual']),
                     'reason':'converged'})

        if (th_cur-1.0)*(th_new-1.0)<=0.0 and max(th_cur,th_new)>=1.0:
            den=th_new-th_cur
            init=0.5*(chi_cur+chi_new) if abs(den)<1e-15 else chi_cur+((1.0-th_cur)/den)*(chi_new-chi_cur)
            final=fixed_theta_solve(rhs,a,beta,kind,1.0,route,init)
            summary={**summarize_path(path),'route':route,'seed_theta':seed_theta,
                     'final_reason':('theta1_'+final['reason'])}
            if final['success']:
                return {'success':True,'reason':'converged_theta1','chi':final['chi'],
                        'iterations':int(final['iterations']),
                        'history':final['history'],'route_summary':summary}
            return {'success':False,'reason':'theta1_'+final['reason'],'chi':final['chi'],
                    'iterations':int(final['iterations']),'history':final['history'],
                    'route_summary':summary}

        if abs(th_new)>THETA_BOUND:
            summary={**summarize_path(path),'route':route,'seed_theta':seed_theta,
                     'final_reason':'arclength_theta_bound'}
            return {'success':False,'reason':'arclength_theta_bound','chi':chi_new,
                    'iterations':int(corr['iterations']),
                    'history':[float(corr['field_relative_residual'])],
                    'route_summary':summary}

        chi_prev,th_prev=chi_cur,th_cur
        chi_cur,th_cur=chi_new,th_new
        if corr['iterations']<=4: ds=min(1.5*ds,DS_MAX)
        elif corr['iterations']<=8: ds=ds
        else: ds=max(0.7*ds,DS_MIN)

    summary={**summarize_path(path),'route':route,'seed_theta':seed_theta,
             'final_reason':'arclength_max_accepted_points'}
    return {'success':False,'reason':'arclength_max_accepted_points','chi':chi_cur,
            'iterations':0,'history':[float(path[-1]['field_relative_residual'])],
            'route_summary':summary}


def endpoint_valid(chi,rhs,a,beta,kind):
    d,_,_=base.diagnostics(chi,rhs,a,beta,kind)
    return bool(d['finite'] and d['R1_relative_L2']<=base.FINAL_R1_GATE and
                d['R2_relative_L2']<=base.FINAL_R2_GATE),d


def dual_anchor_recover(rhs,a,beta,kind,n,return_endpoints=False):
    sols={}
    for route in ('screened','mass'):
        sols[route]=anchor_route_solve(rhs,a,beta,kind,n,route)
    valid={}; endpoints={}
    for route,sol in sols.items():
        ok=False
        if sol['success']:
            ok,_=endpoint_valid(sol['chi'],rhs,a,beta,kind)
        valid[route]=bool(ok)
        if ok: endpoints[route]=np.asarray(sol['chi'],float).copy()

    pair_diff=0.0; multi=False
    if valid['screened'] and valid['mass']:
        pair_diff=base.rel_l2(base.low_modes(endpoints['screened']),base.low_modes(endpoints['mass']))
        multi=bool(pair_diff>base.BRANCH_GATE)

    report={
        'a':float(a),'z':float(1.0/a-1.0),'beta0':float(beta),'kind':kind,'n':int(n),
        'screened':sols['screened']['route_summary'],
        'mass':sols['mass']['route_summary'],
        'screened_endpoint_valid':valid['screened'],
        'mass_endpoint_valid':valid['mass'],
        'pair_lowmode_difference':float(pair_diff),
        'pair_multibranch':bool(multi),
    }
    RECOVERY_REPORTS.append(report)

    if valid['screened']:
        chosen='screened'
    elif valid['mass']:
        chosen='mass'
    else:
        chosen=None

    steps=[{'route':'screened',**sols['screened']['route_summary']},
           {'route':'mass',**sols['mass']['route_summary']}]
    if chosen is None:
        fail=sols['screened'] if not sols['screened']['success'] else sols['mass']
        out={'success':False,'reason':'both_constitutive_anchors_failed','chi':fail['chi'],
             'iterations':int(fail['iterations']),'history':fail['history']}
    else:
        c=sols[chosen]
        out={'success':True,'reason':'converged_'+chosen+'_anchor','chi':endpoints[chosen],
             'iterations':int(c['iterations']),'history':c['history'],
             'anchor_pair_multibranch':bool(multi),'anchor_pair_difference':float(pair_diff)}
    if return_endpoints:
        out['endpoint_fields']=endpoints
        out['endpoint_valid']=valid
        out['report']=report
    return out,steps


def base_homotopy_adapter(rhs,a,beta,kind,n,saturated=False):
    if saturated:
        # Saturated controls are not part of the constitutive continuation.
        chi,_=base.high_gradient_analytic((1.0+beta)*np.asarray(rhs,float),a,beta)
        sol=fixed_full_solve(rhs,a,beta,kind,chi,saturated=True)
        return sol,[{'route':'analytic_saturated_control','success':bool(sol['success'])}]
    return dual_anchor_recover(rhs,a,beta,kind,n,return_endpoints=False)


# Patch only the numerical solvers used by the immutable NL1C6 harness.
base.newton_solve=fixed_full_solve
base.solve_homotopy=base_homotopy_adapter


def arg_value(flag):
    try: return sys.argv[sys.argv.index(flag)+1]
    except (ValueError,IndexError): raise RuntimeError(f'missing required argument {flag}')


def run_independent_eval_anchor_controls(input_npz,npz_out):
    d=np.load(input_npz)
    kh=np.asarray(d['k_native_h'],float); z=np.asarray(d['z_native'],float); db=np.asarray(d['d_b'],float)
    idx,miss=base.mode_indices(kh); db6=db[idx,:]
    out=np.load(npz_out)
    if 'chi_primary' not in out or 'kind_names' not in out:
        return [],False,0.0
    prim=np.asarray(out['chi_primary'],float)
    names=[str(x) for x in np.asarray(out['kind_names'])]
    name_to_i={name:i for i,name in enumerate(names)}
    eval_idx=np.where((z>=base.ZMIN-1e-12)&(z<=base.ZMAX+1e-12))[0]
    controls=[]; multi=False; maxdiff=0.0
    for kind in base.KINDS:
        for beta in base.BETAS:
            name=f'{kind}_beta{beta:g}'
            if name not in name_to_i: continue
            pbranch=prim[name_to_i[name]]
            for it in eval_idx:
                _,source,a=base.source_for(db6[:,it],z[it],base.NX_PRIMARY)
                rhs=source/(1.0+beta)
                rec,_=dual_anchor_recover(rhs,a,beta,kind,base.NX_PRIMARY,return_endpoints=True)
                row={'kind':kind,'beta0':float(beta),'index':int(it),'z':float(z[it]),
                     'route_report':rec.get('report',{}) ,'endpoint_differences_from_primary':{}}
                for route,field in rec.get('endpoint_fields',{}).items():
                    diff=base.rel_l2(base.low_modes(field),base.low_modes(pbranch[it]))
                    row['endpoint_differences_from_primary'][route]=float(diff)
                    maxdiff=max(maxdiff,float(diff))
                    if diff>base.BRANCH_GATE: multi=True
                if rec.get('report',{}).get('pair_multibranch',False):
                    multi=True
                    maxdiff=max(maxdiff,float(rec['report']['pair_lowmode_difference']))
                controls.append(row)
    return controls,bool(multi),float(maxdiff)


def main():
    json_out=arg_value('--json-out'); npz_out=arg_value('--npz-out'); input_npz=arg_value('--input-npz')
    old_exit=0
    try:
        base.main()
    except SystemExit as exc:
        old_exit=int(exc.code or 0)

    p=Path(json_out)
    if not p.exists(): raise RuntimeError('base solver did not produce JSON result')
    result=json.loads(p.read_text())

    base_g1g4=bool(
        result['gates']['G1_input_identity'] and result['gates']['G2_high_gradient_regression'] and
        result['gates']['G3_all_primary_solutions_converged'] and result['gates']['G3_R1_le_1e-10'] and
        result['gates']['G3_R2_le_1e-8'] and result['gates']['G3_all_finite'] and
        result['gates']['G4_resolution_le_5e-3'])

    controls=[]; eval_multi=False; eval_maxdiff=0.0
    if base_g1g4:
        controls,eval_multi,eval_maxdiff=run_independent_eval_anchor_controls(input_npz,npz_out)

    recovery_multi=any(bool(r.get('pair_multibranch',False)) for r in RECOVERY_REPORTS)
    recovery_max=max([float(r.get('pair_lowmode_difference',0.0)) for r in RECOVERY_REPORTS]+[0.0])
    anchor_multi=bool(recovery_multi or eval_multi)
    anchor_max=float(max(recovery_max,eval_maxdiff))

    historical_g5=bool(result['gates']['G5_no_distinct_residual_valid_root'])
    result['gates']['G5_no_distinct_residual_valid_root']=bool(historical_g5 and not anchor_multi)
    result['global_metrics']['max_valid_alternate_branch_difference']=float(max(
        float(result['global_metrics'].get('max_valid_alternate_branch_difference',0.0)),anchor_max))

    if not base_g1g4:
        classification='NL1C6R3_FULL_J_BARYONIC_RECLOSURE_FAIL'
    elif not result['gates']['G5_no_distinct_residual_valid_root']:
        classification='NL1C6R3_FULL_J_MULTIBRANCH_REQUIRES_BOUNDARY_SELECTION'
    else:
        classification='NL1C6R3_FULL_J_BARYONIC_RECLOSURE_PASS'

    old_class=result['classification']
    result['classification']=classification
    result['historical_results_unchanged']=True
    result['repair']={
        'label':'NL1C6R3_PREDATA_FIXED_SOURCE_CONSTITUTIVE_HOMOTOPY',
        'historical_NL1C6R2_classification':'NL1C6R2_FULL_J_BARYONIC_RECLOSURE_FAIL',
        'historical_base_classification_before_R3_mapping':old_class,
        'physical_equations_changed':False,'physical_gates_changed':False,
        'source_amplitude_at_endpoint':1.0,
        'continuation_coordinate':'constitutive theta at fixed physical baryonic source',
        'anchors':['screened_high_gradient','mass_dominated'],
        'bordered_augmented_preconditioner':True,
        'theta_seed_candidates':[float(x) for x in THETA_SEEDS],
        'ds_initial':DS_INITIAL,'ds_min':DS_MIN,'ds_max':DS_MAX,
    }
    result['constitutive_recovery_reports']=RECOVERY_REPORTS
    result['independent_eval_anchor_controls']=controls
    result['anchor_multibranch_found']=bool(anchor_multi)
    result['anchor_max_lowmode_difference']=anchor_max
    result['continuation_rule']='Only NL1C6R3_FULL_J_BARYONIC_RECLOSURE_PASS permits the next eta=0 retarded-memory source/tangent test on the full reclosed native-time chi trajectory.'
    p.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=True)+'\n')
    print(json.dumps({'classification':classification,'gates':result['gates'],
                      'global_metrics':result['global_metrics'],
                      'anchor_multibranch_found':anchor_multi,
                      'anchor_max_lowmode_difference':anchor_max},indent=2,sort_keys=True))
    if classification=='NL1C6R3_FULL_J_BARYONIC_RECLOSURE_FAIL':
        raise SystemExit(2)


if __name__=='__main__':
    main()
