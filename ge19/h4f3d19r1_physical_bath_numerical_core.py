#!/usr/bin/env python3
"""D19R1 numerical bridge: original frozen bath step, D17 dense X jets, true action clock.
All threshold results are empirical numerical tests, never interval certificates.
"""
from __future__ import annotations
import numpy as np

MODES=np.asarray((3,5,8,10,15,20),int)
TINY=1.e-300

def norm(x):
    return float(np.linalg.norm(np.asarray(x)))

def rel(x,y):
    return norm(np.asarray(x)-np.asarray(y))/max(norm(x),norm(y),TINY)

def hermite_value(X,DX,x,j,theta):
    h=float(x[j+1]-x[j]);t=float(theta)
    return ((2*t**3-3*t**2+1)*X[:,j]+(t**3-2*t**2+t)*h*DX[:,j]
            +(-2*t**3+3*t**2)*X[:,j+1]+(t**3-t**2)*h*DX[:,j+1])

def physical_clock_grid(x,X,DX,evalH,tau,nsub,gauss=16):
    """Return original physical-action substep clock and D17-drive endpoint samples."""
    x=np.asarray(x,float); X=np.asarray(X,complex);DX=np.asarray(DX,complex)
    if X.shape!=DX.shape or X.shape!=(6,len(x)) or nsub not in (16,32,64):
        raise ValueError('invalid D19R1 D17 dense input or preregistered subdivision')
    if not(np.isfinite(X).all() and np.isfinite(DX).all() and np.diff(x).min()>0):
        raise ValueError('nonfinite/nonincreasing D17 physical input')
    f=np.arange(nsub,dtype=float)/nsub
    grid=np.r_[(x[:-1,None]+np.diff(x)[:,None]*f[None,:]).reshape(-1),x[-1]]
    ij=np.repeat(np.arange(len(x)-1),nsub)
    tf=np.tile(f,len(x)-1)
    drv=np.empty((6,len(grid)),complex)
    for j in range(len(x)-1):
        ii=slice(j*nsub,(j+1)*nsub)
        th=f[None,:];h=x[j+1]-x[j]
        drv[:,ii]=((2*th**3-3*th**2+1)*X[:,j,None]
          +(th**3-2*th**2+th)*h*DX[:,j,None]
          +(-2*th**3+3*th**2)*X[:,j+1,None]
          +(th**3-th**2)*h*DX[:,j+1,None])
    drv[:,-1]=X[:,-1]
    nodes,weights=np.polynomial.legendre.leggauss(gauss)
    hstep=np.diff(grid); mid=.5*(grid[:-1]+grid[1:])
    xe=mid[:,None]+.5*hstep[:,None]*nodes[None,:]
    H=np.asarray(evalH(xe)[0],float)
    if H.shape!=xe.shape or not np.isfinite(H).all() or np.any(H<=0):
        raise RuntimeError('original source-action H invalid on D19 Gauss grid')
    ds=.5*hstep*np.sum(weights[None,:]/(tau*H),axis=1)
    heff=hstep/ds
    if not(np.isfinite(ds).all() and np.all(ds>0) and np.isfinite(heff).all()):
        raise RuntimeError('original D19 action-clock increment invalid')
    return grid,drv,ds,heff

def propagate(xfine,X,DX,evalH,z0,v0,r,tau,step,nsub,original_x,sample=True,progress=False):
    """Frozen source step with physical time and two FIXED x-samples/original interval.
    D17 fine grid must retain exactly four subintervals per original interval.
    """
    xx=np.asarray(xfine,float);xo=np.asarray(original_x,float)
    rr=np.asarray(r,float)
    q=np.asarray(z0,complex).copy();v=np.asarray(v0,complex).copy()
    if (q.shape!=(len(rr),6) or v.shape!=q.shape or len(xx)!=4*(len(xo)-1)+1
      or not np.array_equal(xx[::4],xo) or np.any(rr<=0) or not np.isfinite(q).all()):
        raise ValueError('D19R1 original input shape/fine-grid/source-parent mismatch')
    grid,drv,ds,heff=physical_clock_grid(xx,X,DX,evalH,tau,nsub)
    n_orig=len(xo);n_samples=2*(n_orig-1)
    oz=np.empty((len(rr),6,n_orig),complex);ov=np.empty_like(oz)
    oz[:,:,0]=q;ov[:,:,0]=v
    sz=np.empty((len(rr),6,n_samples),complex) if sample else None
    sv=np.empty_like(sz) if sample else None
    forcing=np.empty_like(sz) if sample else None
    samplex=np.empty(n_samples,float) if sample else None
    sampleh=np.empty(n_samples,float) if sample else None
    cursor=0;sample_count=0
    for j in range(len(ds)):
        fine=j//nsub; sub=j%nsub; original=fine//4; branch=fine%4
        if sample and branch in (1,2):
            frac_fine=.6 if branch==1 else .4
            target_sub=frac_fine*nsub
            idx=int(np.floor(target_sub))
            if idx==sub:
                f=target_sub-sub
                if not (0.0<f<1.0):
                    raise RuntimeError('D19 preregistered samples lie at step boundary')
                xa=float(grid[j]); xb=float(grid[j+1]);xq=xa+f*(xb-xa)
                xl=drv[:,j];xr=drv[:,j+1]; xm=xl+f*(xr-xl)
                zm,vm=step(q,v,rr,float(heff[j]),xl,xm,float(ds[j])*f)
                Xtrue=hermite_value(X,DX,xx,fine,(sub+f)/nsub)
                Hmid=float(np.asarray(evalH(np.asarray([xq],float))[0]).reshape(-1)[0])
                # Dimensionless original GE05 ODE residual of the numerical
                # frozen-linear-drive trajectory against D17 source-action X.
                Rs=3.*(tau*Hmid-heff[j])*vm+rr[:,None]**2*(xm[None,:]-Xtrue[None,:])
                si=2*original+(0 if branch==1 else 1)
                sz[:,:,si]=zm;sv[:,:,si]=vm;forcing[:,:,si]=Rs
                samplex[si]=xq;sampleh[si]=Hmid
                sample_count+=1
        q,v=step(q,v,rr,float(heff[j]),drv[:,j],drv[:,j+1],float(ds[j]))
        if not(np.isfinite(q).all() and np.isfinite(v).all()):
            raise RuntimeError(f'D19 nonfinite bath at step {j}')
        if (j+1)%(4*nsub)==0:
            cursor+=1;oz[:,:,cursor]=q;ov[:,:,cursor]=v
            if progress and (cursor%16==0 or cursor==n_orig-1):
                print('GE19_D19R1_PROGRESS original_sub={} intervals={}/{}'.format(
                    4*nsub,cursor,n_orig-1),flush=True)
    if cursor!=n_orig-1 or (sample and sample_count!=n_samples):
        raise RuntimeError('D19 knot/sample retention mismatch')
    return {'z':oz,'v':ov,'sample_z':sz,'sample_v':sv,'sample_Rs':forcing,
            'sample_x':samplex,'sample_H':sampleh,'clock_substep_ds':ds,
            'n_substeps':len(ds)}

def source_signed(z,v,Rs,samplex,w,r,tau,kfund,convolve,envelope):
    """Signed +4 original +/- modes: sampled source ONLY, not full H4 Ward."""
    ss=np.asarray(Rs,complex);rr=np.asarray(r,float);ww=np.asarray(w,float)
    omega=rr[:,None,None]/tau; sw=np.sqrt(ww)[:,None,None]
    a3=np.exp(3*np.asarray(samplex,float))[None,None,:]
    Eq=-sw/(2*omega)*(a3/tau**2)*ss
    qx=(sw/omega)*(1j*kfund*MODES[None,:,None])*np.asarray(z,complex)
    W=np.asarray(convolve(Eq,qx),complex)
    U=np.asarray(envelope(Eq,qx),float)
    if W.shape!=(len(samplex),41) or U.shape!=W.shape or not np.isfinite(W).all():
        raise RuntimeError('D19 original GE05 signed source shape/finite fail')
    if np.any(np.abs(W)>U*(1.+1.e-10)+1.e-24):
        raise RuntimeError('D19 original signed source exceeded unsigned envelope')
    return W,U

def high_phase_mask(r,original_action_ds,tau):
    phase=np.asarray(r,float)[:,None]*np.asarray(original_action_ds,float)[None,:]
    if phase.ndim!=2 or not np.isfinite(phase).all():
        raise RuntimeError('D19 physical high-phase mask invalid')
    return phase>=np.pi

def masked_rel(a,b,mask):
    aa=np.asarray(a);bb=np.asarray(b);mm=np.asarray(mask,bool)
    if aa.shape!=bb.shape or aa.ndim!=3 or mm.shape!=(aa.shape[0],aa.shape[2]-1):
        raise ValueError('D19 high-phase mask shape invalid')
    return rel(np.where(mm[:,None,:],aa[:,:,1:],0),np.where(mm[:,None,:],bb[:,:,1:],0))
