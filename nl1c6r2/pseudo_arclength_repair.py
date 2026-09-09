#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import numpy as np
from scipy.sparse.linalg import LinearOperator, gmres

from nl1c6 import full_j_baryonic_reclosure as base

# NL1C6R2 changes only numerical continuation/globalization.
# Physical equations, sources, branches, resolutions and physical gates remain in base.
LAM0=2.0**-34
LAM1=2.0**-33
DS_INITIAL=2.0e-8
DS_MIN=1.0e-10
DS_MAX=1.0e-1
ARC_MAX_ACCEPTED=800
ARC_NEWTON_MAX=24
ARC_TOL=2.0e-10
ARC_LAMBDA_BOUND=2.0
FIXED_NEWTON_MAX=80

base.HOMOTOPY=(LAM0,LAM1)
base.NEWTON_MAX=FIXED_NEWTON_MAX


def field_jvp(chi,a,beta,kind,v,saturated=False):
    _,_,_,_,Aeff=base.full_operator(
        chi,a,beta,kind,saturated=saturated,need_linear_coeff=True
    )
    n=len(chi)
    kk=base.kgrid(n)/a
    mask=base.dealias_mask(n)
    v=np.asarray(v,float)
    vg=np.fft.ifft(1j*kk*np.fft.fft(v)).real
    dop=np.fft.ifft(1j*kk*(np.fft.fft(Aeff*vg)*mask)).real
    dtilde=base.invlap_phys(dop,a)
    return dop+base.MU2*(dtilde+v)


def fixed_newton_solve(rhs,a,beta,kind,initial,saturated=False):
    rhs=np.asarray(rhs,float).copy()
    rhs-=np.mean(rhs)
    chi=np.asarray(initial,float).copy()
    chi-=np.mean(chi)
    scale=max(float(np.linalg.norm(rhs)),1e-300)
    history=[]
    accepted_alpha=[]

    for it in range(FIXED_NEWTON_MAX+1):
        r=base.residual_state(chi,rhs,a,beta,kind,saturated=saturated)[0]
        rel=float(np.linalg.norm(r)/scale)
        history.append(rel)
        if not np.isfinite(rel):
            return {'success':False,'reason':'nonfinite_residual','chi':chi,
                    'iterations':it,'history':history,'accepted_alpha':accepted_alpha}
        if rel<=base.NEWTON_TOL:
            return {'success':True,'reason':'converged','chi':chi,
                    'iterations':it,'history':history,'accepted_alpha':accepted_alpha}
        if it==FIXED_NEWTON_MAX:
            break

        n=len(chi)
        J=LinearOperator(
            (n,n),
            matvec=lambda v: field_jvp(chi,a,beta,kind,v,saturated=saturated),
            dtype=float,
        )
        M=base.preconditioner(chi,a,beta,kind,saturated=saturated)
        delta,info=gmres(
            J,-r,M=M,rtol=1e-8,atol=0.0,
            restart=min(80,n),maxiter=240,
        )
        if info!=0 or not np.all(np.isfinite(delta)):
            return {'success':False,'reason':f'gmres_failed_{info}','chi':chi,
                    'iterations':it,'history':history,'accepted_alpha':accepted_alpha}

        norm0=float(np.linalg.norm(r))
        accepted=False
        for m in range(41):
            alpha=2.0**(-m)
            cand=chi+alpha*delta
            cand-=np.mean(cand)
            rc=base.residual_state(cand,rhs,a,beta,kind,saturated=saturated)[0]
            if np.all(np.isfinite(rc)) and float(np.linalg.norm(rc))<norm0:
                chi=cand
                accepted_alpha.append(float(alpha))
                accepted=True
                break
        if not accepted:
            return {'success':False,'reason':f'line_search_failed_gmres_{info}','chi':chi,
                    'iterations':it,'history':history,'accepted_alpha':accepted_alpha}

    return {'success':False,'reason':'max_iterations','chi':chi,
            'iterations':FIXED_NEWTON_MAX,'history':history,
            'accepted_alpha':accepted_alpha}


# Direct time continuation, high-gradient regression and alternate-root checks use
# the repaired fixed-lambda solver with unchanged physical tolerance.
base.newton_solve=fixed_newton_solve


def arc_inner(y1,l1,y2,l2):
    return float(np.mean(np.asarray(y1)*np.asarray(y2))+float(l1)*float(l2))


def normalized_secant(chi0,lam0,chi1,lam1,chi_scale,previous=None):
    dy=(np.asarray(chi1)-np.asarray(chi0))/chi_scale
    dl=float(lam1-lam0)
    nn=float(np.sqrt(max(arc_inner(dy,dl,dy,dl),1e-300)))
    ty=dy/nn
    tl=dl/nn
    if previous is not None:
        py,pl=previous
        if arc_inner(ty,tl,py,pl)<0.0:
            ty=-ty
            tl=-tl
    return ty,float(tl)


def augmented_measure(chi,lam,rhs,a,beta,kind,chi_pred,lam_pred,ty,tl,chi_scale,saturated=False):
    rhs_scale=max(float(np.linalg.norm(rhs)),1e-300)
    r=base.residual_state(chi,lam*rhs,a,beta,kind,saturated=saturated)[0]
    frel=float(np.linalg.norm(r)/rhs_scale)
    g=float(np.mean(((chi-chi_pred)/chi_scale)*ty)+(lam-lam_pred)*tl)
    combined=float(np.sqrt(frel*frel+g*g))
    return r,frel,g,combined


def augmented_corrector(rhs,a,beta,kind,chi_pred,lam_pred,ty,tl,chi_scale,saturated=False):
    rhs=np.asarray(rhs,float)
    rhs_scale=max(float(np.linalg.norm(rhs)),1e-300)
    chi=np.asarray(chi_pred,float).copy()
    lam=float(lam_pred)
    history=[]
    accepted_alpha=[]

    n=len(chi)
    for it in range(ARC_NEWTON_MAX+1):
        r,frel,g,combined=augmented_measure(
            chi,lam,rhs,a,beta,kind,chi_pred,lam_pred,ty,tl,chi_scale,
            saturated=saturated,
        )
        history.append({'field_relative_residual':float(frel),
                        'arclength_residual':float(g),
                        'combined_residual':float(combined),
                        'lambda':float(lam)})
        if not np.isfinite(combined):
            return {'success':False,'reason':'nonfinite_augmented_residual','chi':chi,
                    'lambda':lam,'iterations':it,'history':history,
                    'accepted_alpha':accepted_alpha,'field_relative_residual':frel}
        if frel<=ARC_TOL and abs(g)<=ARC_TOL:
            return {'success':True,'reason':'converged','chi':chi,'lambda':lam,
                    'iterations':it,'history':history,'accepted_alpha':accepted_alpha,
                    'field_relative_residual':frel}
        if it==ARC_NEWTON_MAX:
            break

        Jfield_prec=base.preconditioner(chi,a,beta,kind,saturated=saturated)

        def aug_mv(q):
            q=np.asarray(q,float)
            dy=q[:n]
            dl=float(q[n])
            dchi=chi_scale*dy
            first=(field_jvp(chi,a,beta,kind,dchi,saturated=saturated)-rhs*dl)/rhs_scale
            last=float(np.mean(dy*ty)+dl*tl)
            return np.concatenate([first,np.asarray([last])])

        def prec_mv(q):
            q=np.asarray(q,float)
            dchi=Jfield_prec.matvec(rhs_scale*q[:n])
            dy=dchi/chi_scale
            return np.concatenate([dy,np.asarray([q[n]])])

        A=LinearOperator((n+1,n+1),matvec=aug_mv,dtype=float)
        P=LinearOperator((n+1,n+1),matvec=prec_mv,dtype=float)
        b=np.concatenate([-r/rhs_scale,np.asarray([-g])])
        dq,info=gmres(
            A,b,M=P,rtol=1e-9,atol=0.0,
            restart=min(100,n+1),maxiter=400,
        )
        if info!=0 or not np.all(np.isfinite(dq)):
            return {'success':False,'reason':f'augmented_gmres_failed_{info}','chi':chi,
                    'lambda':lam,'iterations':it,'history':history,
                    'accepted_alpha':accepted_alpha,'field_relative_residual':frel}

        dy=dq[:n]
        dl=float(dq[n])
        accepted=False
        for m in range(25):
            alpha=2.0**(-m)
            cand_chi=chi+alpha*chi_scale*dy
            cand_lam=lam+alpha*dl
            _,cf,cg,cc=augmented_measure(
                cand_chi,cand_lam,rhs,a,beta,kind,
                chi_pred,lam_pred,ty,tl,chi_scale,saturated=saturated,
            )
            if np.isfinite(cc) and cc<combined:
                chi=cand_chi
                lam=float(cand_lam)
                accepted_alpha.append(float(alpha))
                accepted=True
                break
        if not accepted:
            return {'success':False,'reason':'augmented_line_search_failed','chi':chi,
                    'lambda':lam,'iterations':it,'history':history,
                    'accepted_alpha':accepted_alpha,'field_relative_residual':frel}

    return {'success':False,'reason':'augmented_max_iterations','chi':chi,
            'lambda':lam,'iterations':ARC_NEWTON_MAX,'history':history,
            'accepted_alpha':accepted_alpha,
            'field_relative_residual':float(history[-1]['field_relative_residual'])}


def pseudo_arclength_source_solve(rhs,a,beta,kind,n,saturated=False):
    rhs=np.asarray(rhs,float).copy()
    rhs-=np.mean(rhs)
    rhs_scale=max(float(np.linalg.norm(rhs)),1e-300)
    chi_scale=max(rhs_scale/(base.MU2*np.sqrt(float(n))),1e-300)
    steps=[]

    s0=fixed_newton_solve(LAM0*rhs,a,beta,kind,np.zeros(n),saturated=saturated)
    steps.append({'stage':'seed','lambda':float(LAM0),'success':bool(s0['success']),
                  'iterations':int(s0['iterations']),
                  'final_relative_residual':float(s0['history'][-1]),
                  'reason':s0['reason']})
    if not s0['success']:
        return s0,steps

    s1=fixed_newton_solve(LAM1*rhs,a,beta,kind,s0['chi'],saturated=saturated)
    steps.append({'stage':'seed','lambda':float(LAM1),'success':bool(s1['success']),
                  'iterations':int(s1['iterations']),
                  'final_relative_residual':float(s1['history'][-1]),
                  'reason':s1['reason']})
    if not s1['success']:
        return s1,steps

    chi_prev=np.asarray(s0['chi'],float).copy()
    lam_prev=float(LAM0)
    chi_cur=np.asarray(s1['chi'],float).copy()
    lam_cur=float(LAM1)
    tangent=normalized_secant(chi_prev,lam_prev,chi_cur,lam_cur,chi_scale)
    ds=float(DS_INITIAL)
    accepted_count=2

    while accepted_count<ARC_MAX_ACCEPTED:
        ty,tl=normalized_secant(
            chi_prev,lam_prev,chi_cur,lam_cur,chi_scale,previous=tangent
        )
        tangent=(ty,tl)
        chi_pred=chi_cur+ds*chi_scale*ty
        lam_pred=lam_cur+ds*tl

        corr=augmented_corrector(
            rhs,a,beta,kind,chi_pred,lam_pred,ty,tl,chi_scale,
            saturated=saturated,
        )
        if not corr['success']:
            steps.append({'stage':'arclength_reject','lambda':float(corr['lambda']),
                          'ds':float(ds),'success':False,
                          'iterations':int(corr['iterations']),
                          'final_relative_residual':float(corr['field_relative_residual']),
                          'reason':corr['reason']})
            next_ds=0.5*ds
            if next_ds<DS_MIN:
                fail={'success':False,'reason':'arclength_ds_below_min',
                      'chi':np.asarray(corr['chi'],float),
                      'iterations':int(corr['iterations']),
                      'history':[float(corr['field_relative_residual'])],
                      'lambda':float(corr['lambda'])}
                return fail,steps
            ds=max(next_ds,DS_MIN)
            continue

        chi_new=np.asarray(corr['chi'],float).copy()
        lam_new=float(corr['lambda'])
        accepted_count+=1
        steps.append({'stage':'arclength_accept','lambda':lam_new,'ds':float(ds),
                      'success':True,'iterations':int(corr['iterations']),
                      'final_relative_residual':float(corr['field_relative_residual']),
                      'reason':corr['reason']})

        # First positive crossing of physical lambda=1 on the oriented branch.
        if (lam_cur-1.0)*(lam_new-1.0)<=0.0 and max(lam_cur,lam_new)>=1.0:
            denom=lam_new-lam_cur
            if abs(denom)<1e-15:
                init=0.5*(chi_cur+chi_new)
            else:
                w=(1.0-lam_cur)/denom
                init=chi_cur+w*(chi_new-chi_cur)
            final=fixed_newton_solve(rhs,a,beta,kind,init,saturated=saturated)
            steps.append({'stage':'lambda1_correction','lambda':1.0,
                          'success':bool(final['success']),
                          'iterations':int(final['iterations']),
                          'final_relative_residual':float(final['history'][-1]),
                          'reason':final['reason']})
            if final['success']:
                final['arclength_steps']=steps
                final['lambda']=1.0
                return final,steps
            fail=dict(final)
            fail['reason']='lambda1_correction_'+str(final['reason'])
            fail['lambda']=1.0
            return fail,steps

        if abs(lam_new)>ARC_LAMBDA_BOUND:
            fail={'success':False,'reason':'arclength_lambda_bound','chi':chi_new,
                  'iterations':int(corr['iterations']),
                  'history':[float(corr['field_relative_residual'])],
                  'lambda':lam_new}
            return fail,steps

        chi_prev,lam_prev=chi_cur,lam_cur
        chi_cur,lam_cur=chi_new,lam_new

        if corr['iterations']<=4:
            ds=min(1.5*ds,DS_MAX)
        elif corr['iterations']<=8:
            ds=ds
        else:
            ds=max(0.7*ds,DS_MIN)

    fail={'success':False,'reason':'arclength_max_accepted_points','chi':chi_cur,
          'iterations':0,'history':[float(steps[-1]['final_relative_residual'])],
          'lambda':lam_cur}
    return fail,steps


# Replace only the failed source-amplitude continuation path. Base solve_branch
# still uses previous-time fixed-lambda Newton first; this function is its fallback.
base.solve_homotopy=pseudo_arclength_source_solve


def arg_value(flag):
    try:
        return sys.argv[sys.argv.index(flag)+1]
    except (ValueError,IndexError):
        raise RuntimeError(f'missing required argument {flag}')


def main():
    json_out=arg_value('--json-out')
    old_exit=0
    try:
        base.main()
    except SystemExit as exc:
        old_exit=int(exc.code or 0)

    p=Path(json_out)
    if not p.exists():
        raise RuntimeError('base solver did not produce JSON result')
    d=json.loads(p.read_text())
    old=d['classification']
    mapping={
        'NL1C6_FULL_J_BARYONIC_RECLOSURE_PASS':'NL1C6R2_FULL_J_BARYONIC_RECLOSURE_PASS',
        'NL1C6_FULL_J_MULTIBRANCH_REQUIRES_BOUNDARY_SELECTION':'NL1C6R2_FULL_J_MULTIBRANCH_REQUIRES_BOUNDARY_SELECTION',
        'NL1C6_FULL_J_BARYONIC_RECLOSURE_FAIL':'NL1C6R2_FULL_J_BARYONIC_RECLOSURE_FAIL',
    }
    if old not in mapping:
        raise RuntimeError(f'unexpected base classification {old}')

    d['classification']=mapping[old]
    d['scope']=('NL1C6R2 pseudo-arclength numerical continuation repair of the unchanged NL1C6 '
                'fixed-state periodic physical-coordinate full-J baryonic quasistatic reclosure; '
                'no matter re-evolution, finite eta, memory forcing, observational data or likelihood')
    d['repair']={
        'historical_NL1C6_classification':'NL1C6_FULL_J_BARYONIC_RECLOSURE_FAIL',
        'historical_NL1C6R_classification':'NL1C6R_FULL_J_BARYONIC_RECLOSURE_FAIL',
        'historical_NL1C6R_run':34346655008,
        'historical_NL1C6R_artifact_id':10103396065,
        'historical_NL1C6R_artifact_sha256':'6233521bf8e5f6af7a7587ba03f081159a3b725aae5dea9cdb52696fb5eefdb9',
        'physical_equations_changed':False,
        'physical_gates_changed':False,
        'branch_selection':'first lambda=1 crossing on zero-source-connected oriented pseudo-arclength branch',
        'lambda_seed':[float(LAM0),float(LAM1)],
        'chi_scaling':'||rhs||_2/(mu^2*sqrt(n))',
        'ds_initial':DS_INITIAL,'ds_min':DS_MIN,'ds_max':DS_MAX,
        'max_accepted_points':ARC_MAX_ACCEPTED,
        'augmented_newton_max_iterations':ARC_NEWTON_MAX,
        'augmented_tolerance':ARC_TOL,
        'augmented_backtracking_alpha':[float(2.0**(-m)) for m in range(25)],
        'augmented_gmres':{'rtol':1e-9,'atol':0.0,'restart_rule':'min(100,n+1)','maxiter':400},
        'fixed_lambda_newton_max_iterations':FIXED_NEWTON_MAX,
        'fixed_lambda_backtracking_alpha':[float(2.0**(-m)) for m in range(41)],
        'base_python_exit_code':old_exit,
    }
    d['continuation_rule']=('Only NL1C6R2_FULL_J_BARYONIC_RECLOSURE_PASS permits the next eta=0 '
                            'retarded-memory source/tangent test on the reclosed native-time chi trajectory.')
    p.write_text(json.dumps(d,indent=2,sort_keys=True,allow_nan=True)+'\n')
    print('NL1C6R2_FINAL_CLASSIFICATION',d['classification'])
    print(json.dumps(d['gates'],sort_keys=True))
    print(json.dumps(d['global_metrics'],sort_keys=True))


if __name__=='__main__':
    main()
