#!/usr/bin/env python3
import json
import sys
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import LinearOperator, gmres

from nl1c6 import full_j_baryonic_reclosure as base

# Frozen NL1C6R-only numerical repair. Physical equations and final gates live
# in the already preregistered NL1C6 implementation and are not modified.
base.HOMOTOPY=tuple(2.0**(-p) for p in range(24,-1,-1))
base.NEWTON_MAX=60


def repaired_newton_solve(rhs,a,beta,kind,initial,saturated=False):
    rhs=np.asarray(rhs,float).copy(); rhs-=np.mean(rhs)
    chi=np.asarray(initial,float).copy(); chi-=np.mean(chi)
    scale=max(float(np.linalg.norm(rhs)),1e-300)
    history=[]
    accepted_alpha=[]
    for it in range(base.NEWTON_MAX+1):
        r,op,tilde,phi,g,x,j=base.residual_state(chi,rhs,a,beta,kind,saturated=saturated)
        rel=float(np.linalg.norm(r)/scale)
        history.append(rel)
        if not np.isfinite(rel):
            return {'success':False,'reason':'nonfinite_residual','chi':chi,'iterations':it,
                    'history':history,'accepted_alpha':accepted_alpha}
        if rel<=base.NEWTON_TOL:
            return {'success':True,'reason':'converged','chi':chi,'iterations':it,
                    'history':history,'accepted_alpha':accepted_alpha}
        if it==base.NEWTON_MAX:
            break

        _,_,_,_,Aeff=base.full_operator(chi,a,beta,kind,saturated=saturated,need_linear_coeff=True)
        n=len(chi); kk=base.kgrid(n)/a; mask=base.dealias_mask(n)

        def jmv(v):
            v=np.asarray(v,float)
            vg=np.fft.ifft(1j*kk*np.fft.fft(v)).real
            dop=np.fft.ifft(1j*kk*(np.fft.fft(Aeff*vg)*mask)).real
            dtilde=base.invlap_phys(dop,a)
            return dop+base.MU2*(dtilde+v)

        J=LinearOperator((n,n),matvec=jmv,dtype=float)
        M=base.preconditioner(chi,a,beta,kind,saturated=saturated)
        delta,info=gmres(J,-r,M=M,rtol=1e-8,atol=0.0,restart=min(80,n),maxiter=240)
        if not np.all(np.isfinite(delta)):
            return {'success':False,'reason':'nonfinite_newton_step','chi':chi,'iterations':it,
                    'history':history,'accepted_alpha':accepted_alpha}

        accepted=False
        norm0=float(np.linalg.norm(r))
        for m in range(41):
            alpha=2.0**(-m)
            cand=chi+alpha*delta; cand-=np.mean(cand)
            rc=base.residual_state(cand,rhs,a,beta,kind,saturated=saturated)[0]
            if np.all(np.isfinite(rc)) and float(np.linalg.norm(rc))<norm0:
                chi=cand
                accepted_alpha.append(float(alpha))
                accepted=True
                break
        if not accepted:
            return {'success':False,'reason':f'line_search_failed_gmres_{info}','chi':chi,'iterations':it,
                    'history':history,'accepted_alpha':accepted_alpha}

    return {'success':False,'reason':'max_iterations','chi':chi,'iterations':base.NEWTON_MAX,
            'history':history,'accepted_alpha':accepted_alpha}


base.newton_solve=repaired_newton_solve


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
        'NL1C6_FULL_J_BARYONIC_RECLOSURE_PASS':'NL1C6R_FULL_J_BARYONIC_RECLOSURE_PASS',
        'NL1C6_FULL_J_MULTIBRANCH_REQUIRES_BOUNDARY_SELECTION':'NL1C6R_FULL_J_MULTIBRANCH_REQUIRES_BOUNDARY_SELECTION',
        'NL1C6_FULL_J_BARYONIC_RECLOSURE_FAIL':'NL1C6R_FULL_J_BARYONIC_RECLOSURE_FAIL',
    }
    if old not in mapping:
        raise RuntimeError(f'unexpected base classification {old}')
    d['classification']=mapping[old]
    d['scope']=('NL1C6R deterministic numerical-globalization repair of the unchanged NL1C6 fixed-state periodic '
                'physical-coordinate full-J baryonic quasistatic reclosure; no matter re-evolution, finite eta, '
                'memory forcing, observational data or likelihood')
    d['repair']={
        'historical_NL1C6_classification':'NL1C6_FULL_J_BARYONIC_RECLOSURE_FAIL',
        'historical_NL1C6_run':34346092041,
        'physical_equations_changed':False,
        'physical_gates_changed':False,
        'source_homotopy_lambda':[float(x) for x in base.HOMOTOPY],
        'backtracking_alpha':[float(2.0**(-m)) for m in range(41)],
        'Newton_max_iterations':int(base.NEWTON_MAX),
        'base_python_exit_code':old_exit,
    }
    d['continuation_rule']=('Only NL1C6R_FULL_J_BARYONIC_RECLOSURE_PASS permits the next eta=0 retarded-memory '
                            'source/tangent test on the reclosed native-time chi trajectory.')
    p.write_text(json.dumps(d,indent=2,sort_keys=True,allow_nan=True)+'\n')
    print('NL1C6R_FINAL_CLASSIFICATION',d['classification'])
    print(json.dumps(d['gates'],sort_keys=True))
    print(json.dumps(d['global_metrics'],sort_keys=True))


if __name__=='__main__':
    main()
