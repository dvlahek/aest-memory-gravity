#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import roots_legendre

H0 = 67.3324639084866
h = H0/100.0
AS = 2.1308864352626987e-9
NS = 0.9666229454895277
KPIV = 0.05
A0 = 1.2e-10
C = 299792458.0
MPC_M = 3.0856775814913673e22
TAUH0 = 10.0
K_H = np.asarray([0.03,0.05,0.08,0.10,0.15,0.20],float)
K_MPC = K_H*h
PHASES = np.asarray([0.13,0.71,1.29,2.03,2.77,3.41],float)
ZMIN,ZMAX = 0.2,1.5
MODE_REL_GATE = 1e-12


def log_trap_weights(k):
    x=np.log(np.asarray(k,float))
    w=np.empty_like(x)
    w[0]=0.5*(x[1]-x[0]); w[-1]=0.5*(x[-1]-x[-2])
    w[1:-1]=0.5*(x[2:]-x[:-2])
    return w

WIDTHS=log_trap_weights(K_H)
PR=AS*(K_MPC/KPIV)**(NS-1.0)


def load_trace(path):
    df=pd.read_csv(path,sep=r'\s+')
    need={'k','tau','a','H_over_H0','chi','Q'}
    if not need.issubset(df.columns):
        raise RuntimeError(f'trace columns missing: {need-set(df.columns)}')
    modes=[]; misses=[]
    for target in K_MPC:
        rel=np.abs(df['k'].to_numpy()-target)/target
        miss=float(np.min(rel)); misses.append(miss)
        if miss>MODE_REL_GATE:
            raise RuntimeError(f'k={target} missing, best rel={miss}')
        sub=df[rel<=MODE_REL_GATE].copy()
        # Collapse repeated adaptive source calls at identical accepted tau.
        g=sub.groupby('tau',as_index=False).median(numeric_only=True).sort_values('tau')
        modes.append(g)
    n=len(modes[0])
    if any(len(m)!=n for m in modes):
        raise RuntimeError('mode history length mismatch')
    tau0=modes[0]['tau'].to_numpy(); a0=modes[0]['a'].to_numpy()
    max_trel=0.0
    for m in modes[1:]:
        t=m['tau'].to_numpy(); aa=m['a'].to_numpy()
        max_trel=max(max_trel,float(np.max(np.abs(t-tau0)/np.maximum(np.maximum(np.abs(t),np.abs(tau0)),1.0))))
        max_trel=max(max_trel,float(np.max(np.abs(aa-a0)/np.maximum(np.maximum(np.abs(aa),np.abs(a0)),1e-300))))
    if max_trel>1e-12:
        raise RuntimeError(f'common native time mismatch {max_trel}')
    chi=np.stack([m['chi'].to_numpy() for m in modes],axis=1)
    Q=np.stack([m['Q'].to_numpy() for m in modes],axis=1)
    H=np.stack([m['H_over_H0'].to_numpy() for m in modes],axis=1)
    return {
        'tau':tau0,
        'a':a0,
        'H':np.median(H,axis=1),
        'Q':np.median(Q,axis=1),
        'chi':chi,
        'mode_relative_miss_max':max(misses),
        'time_grid_relative_mismatch_max':max_trel,
    }


def synthesize(ref,nx):
    kfund=h*0.01
    box=2*np.pi/kfund
    x=np.arange(nx)*box/nx
    amp=np.sqrt(2.0*WIDTHS*PR)
    chi=np.zeros((len(ref['a']),nx),float)
    for j,k in enumerate(K_MPC):
        chi += amp[j]*ref['chi'][:,j,None]*np.cos(k*x[None,:]+PHASES[j])
    kk=2*np.pi*np.fft.fftfreq(nx,d=box/nx)
    scalar=chi/ref['a'][:,None]
    grad=np.fft.ifft(1j*kk[None,:]*np.fft.fft(scalar,axis=1),axis=1).real

    # Prior NL1C0 analytic RMS in units x=physical acceleration/a0.
    xmode=(C*C/A0)*(K_MPC[None,:]/MPC_M/ref['a'][:,None])*np.sqrt(PR)[None,:]*np.abs(ref['chi'])
    xrms_analytic=np.sqrt(np.sum(WIDTHS[None,:]*xmode*xmode,axis=1))
    xrms_real=(C*C/A0)*(np.sqrt(np.mean(grad*grad,axis=1))/MPC_M)
    rel=np.abs(xrms_real-xrms_analytic)/np.maximum(xrms_analytic,1e-300)
    return {'box':box,'x':x,'kk':kk,'scalar':scalar,'grad':grad,
            'xrms_analytic':xrms_analytic,'xrms_real':xrms_real,
            'xrms_reconstruction_rel_max':float(np.max(rel))}


def tan_nodes(n):
    z,w=roots_legendre(int(n))
    theta=0.25*np.pi*(z+1.0)
    return np.tan(theta),0.5*w


def step_linear_field(q,v,omega,hubble_scaled,x0,x1,dt):
    # Vectorized exact frozen-h step for
    # z_xixi+3h z_xi+r^2 z=r^2 x(xi), with x linear over the interval.
    c=3.0*hubble_scaled; d=0.5*c
    slope=(x1-x0)/dt
    u0=q-x0; vu0=v-slope
    force=-c*slope
    om2=omega*omega
    disc=om2-d*d
    scale=np.maximum(om2+d*d,1.0)
    under=(disc[:,0] > (1e-12*scale[:,0]))
    over=(disc[:,0] < (-1e-12*scale[:,0]))
    crit=~(under|over)
    un=np.empty_like(q); vn=np.empty_like(v)

    if np.any(under):
        O=np.sqrt(disc[under]); z=O*dt; ed=np.exp(-d*dt)
        Cc=np.cos(z); Ss=np.sin(z)
        uu=u0[under]; vv=vu0[under]; oo2=om2[under]
        hu=ed*(uu*Cc+(vv+d*uu)/O*Ss)
        hv=ed*(vv*Cc-(d*vv+oo2*uu)/O*Ss)
        one=1.0-ed*(Cc+d/O*Ss)
        G=ed*Ss/O
        un[under]=hu+force/oo2*one
        vn[under]=hv+force*G
    if np.any(over):
        oo2=om2[over]; delta=np.sqrt(-disc[over])
        lam1=-oo2/(d+delta); lam2=-d-delta; den=lam1-lam2
        e1=np.exp(lam1*dt); e2=np.exp(lam2*dt)
        uu=u0[over]; vv=vu0[over]
        c1=(vv-lam2*uu)/den; c2=(lam1*uu-vv)/den
        hu=c1*e1+c2*e2; hv=lam1*c1*e1+lam2*c2*e2
        one=(-lam2*(-np.expm1(lam1*dt))+lam1*(-np.expm1(lam2*dt)))/den
        G=(e1-e2)/den
        un[over]=hu+force/oo2*one
        vn[over]=hv+force*G
    if np.any(crit):
        oo2=om2[crit]; ed=np.exp(-d*dt)
        uu=u0[crit]; vv=vu0[crit]
        hu=ed*(uu+(vv+d*uu)*dt)
        hv=ed*(vv-(d*vv+oo2*uu)*dt)
        one=-np.expm1(-d*dt)-d*dt*ed
        G=ed*dt
        un[crit]=hu+force/oo2*one
        vn[crit]=hv+force*G
    return x1+un,vn+slope


def derivative_many(field,kk):
    return np.fft.ifft(1j*kk[None,:]*np.fft.fft(field,axis=1),axis=1).real


def simulate(ref,nx,order):
    syn=synthesize(ref,nx)
    scalar=syn['scalar']; kk=syn['kk']; X=syn['grad']
    nodes,weights=tan_nodes(order)
    omega=nodes[:,None]
    q=np.zeros((order,nx),float)
    v=np.zeros((order,nx),float)
    N=np.log(ref['a'])
    rows=[]
    for i in range(len(N)):
        if i>0:
            dN=N[i]-N[i-1]
            hm=math.sqrt(ref['H'][i-1]*TAUH0*ref['H'][i]*TAUH0)
            dt=dN/hm
            if not (dt>0):
                raise RuntimeError('non-positive dimensionless time step')
            q,v=step_linear_field(q,v,omega,hm,scalar[i-1][None,:],scalar[i][None,:],dt)
        z=1.0/ref['a'][i]-1.0
        if z < ZMIN-1e-12 or z > ZMAX+1e-12:
            continue
        grad_q=derivative_many(q,kk)
        grad_v=derivative_many(v,kk)
        mean_grad_q=np.tensordot(weights,grad_q,axes=(0,0))
        B=X[i]-mean_grad_q
        # From the NL1C3B normalized action in cosmic time.  With
        # y_j=partial_x z_j and q_vec=sqrt(w)/omega_phys*y_j,
        # dot(q_vec)=sqrt(w)/r_j*partial_x z_{j,xi}.
        kin=(grad_v/omega)**2
        pot=(grad_q-X[i][None,:])**2
        rhohat=0.25*np.tensordot(weights,kin+pot,axes=(0,0))
        Xrms=float(np.sqrt(np.mean(X[i]*X[i])))
        Brms=float(np.sqrt(np.mean(B*B)))
        er=float(np.mean(rhohat))
        rows.append({
            'index':i,'tau_Mpc':float(ref['tau'][i]),'a':float(ref['a'][i]),'z':float(z),
            'x_rms_dimensionless':float(syn['xrms_real'][i]),
            'X_rms_1_per_Mpc':Xrms,'B_rms_1_per_Mpc':Brms,
            'B_over_X_rms':Brms/max(Xrms,1e-300),
            'rhohat_mem_mean_1_per_Mpc2':er,
            'rhohat_mem_over_X2':er/max(Xrms*Xrms,1e-300),
            'rhohat_mem_rms_1_per_Mpc2':float(np.sqrt(np.mean(rhohat*rhohat))),
        })
    return {'nx':nx,'order':order,'quadrature_weight_sum':float(np.sum(weights)),
            'xrms_reconstruction_rel_max':syn['xrms_reconstruction_rel_max'],'rows':rows}


def rel_l2(a,b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(bb),1e-300))


def extract(series,key):
    return [r[key] for r in series['rows']]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--json-out',required=True)
    args=ap.parse_args()
    ref=load_trace(args.trace)

    primary=simulate(ref,512,1024)
    control=simulate(ref,512,512)
    spatial=simulate(ref,256,1024)

    nwin=len(primary['rows'])
    qB=rel_l2(extract(control,'B_rms_1_per_Mpc'),extract(primary,'B_rms_1_per_Mpc'))
    qE=rel_l2(extract(control,'rhohat_mem_mean_1_per_Mpc2'),extract(primary,'rhohat_mem_mean_1_per_Mpc2'))
    sB=rel_l2(extract(spatial,'B_rms_1_per_Mpc'),extract(primary,'B_rms_1_per_Mpc'))
    sE=rel_l2(extract(spatial,'rhohat_mem_mean_1_per_Mpc2'),extract(primary,'rhohat_mem_mean_1_per_Mpc2'))
    finite=all(math.isfinite(float(v)) for r in primary['rows'] for v in r.values())
    positive=all(r['B_rms_1_per_Mpc']>0 and r['rhohat_mem_mean_1_per_Mpc2']>0 for r in primary['rows'])
    all_high=all(r['x_rms_dimensionless']>=10.0 for r in primary['rows'])

    gates={
        'requested_k_relative_miss_le_1e-12':ref['mode_relative_miss_max']<=1e-12,
        'minimum_8_native_times':nwin>=8,
        'xrms_realspace_closure_le_1e-10':primary['xrms_reconstruction_rel_max']<=1e-10,
        'quadrature_B_relL2_le_1e-2':qB<=1e-2,
        'quadrature_energy_relL2_le_1e-2':qE<=1e-2,
        'spatial_B_relL2_le_5e-3':sB<=5e-3,
        'spatial_energy_relL2_le_5e-3':sE<=5e-3,
        'all_finite':finite,
        'B_and_energy_positive_at_all_times':positive,
    }
    classification=('NL1C4_EXPANDING_MEMORY_SOURCE_TRAJECTORY_PASS' if all(gates.values())
                    else 'NL1C4_EXPANDING_MEMORY_SOURCE_TRAJECTORY_FAIL')
    result={
        'classification':classification,
        'scope':'action-derived expanding retarded memory-source trajectory on the certified v0.77 memory-off signal-band reference; not a self-consistent screened-resummed AeST state solution',
        'uses_observational_data':False,
        'physical_eta':0.0,
        'frozen_input':{
            'v077_run':34315590099,'artifact_id':10090367181,
            'artifact_digest':'sha256:24b97e5738eb07be4f12d433ff5f9fe22249e199e186d5617aca5dc81f748378',
            'trace_file':'v076_v077_base_trace.dat','k_h_per_Mpc':K_H.tolist(),
            'z_window':[ZMIN,ZMAX],'tauH0':TAUH0,'phases_rad':PHASES.tolist(),
            'quadrature_primary':1024,'quadrature_control':512,'spatial_resolutions':[256,512],
        },
        'input_audit':{
            'mode_relative_miss_max':ref['mode_relative_miss_max'],
            'time_grid_relative_mismatch_max':ref['time_grid_relative_mismatch_max'],
            'native_times_in_window':nwin,
        },
        'numerical_metrics':{
            'xrms_reconstruction_relative_error_max':primary['xrms_reconstruction_rel_max'],
            'quadrature_B_relative_L2':qB,
            'quadrature_energy_relative_L2':qE,
            'spatial_B_relative_L2':sB,
            'spatial_energy_relative_L2':sE,
            'primary_weight_sum':primary['quadrature_weight_sum'],
            'control_weight_sum':control['quadrature_weight_sum'],
        },
        'reference_regime':{
            'all_native_evaluation_times_high_gradient_x_ge_10':all_high,
            'x_rms_min':min(r['x_rms_dimensionless'] for r in primary['rows']),
            'x_rms_max':max(r['x_rms_dimensionless'] for r in primary['rows']),
        },
        'primary_time_results':primary['rows'],
        'summary':{
            'B_over_X_rms_min':min(r['B_over_X_rms'] for r in primary['rows']),
            'B_over_X_rms_max':max(r['B_over_X_rms'] for r in primary['rows']),
            'rhohat_mem_over_X2_min':min(r['rhohat_mem_over_X2'] for r in primary['rows']),
            'rhohat_mem_over_X2_max':max(r['rhohat_mem_over_X2'] for r in primary['rows']),
        },
        'locked_gates':gates,
        'historical_results_unchanged':True,
        'interpretation':('PASS establishes that the complete retarded NL0B memory source has a converged nonzero longitudinal backreaction and direct eta-linear metric-energy source on the certified physical-amplitude v0.77 reference. Because the reference has not yet been dynamically reclosed with the saturated AeST Y sector, this is a source-survival result only, not a screened-state survival or nonlinear-collapse result.'),
    }
    Path(args.json_out).parent.mkdir(parents=True,exist_ok=True)
    Path(args.json_out).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
