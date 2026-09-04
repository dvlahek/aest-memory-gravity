import json
from pathlib import Path
import numpy as np

OMEGA_R=9.2e-5
OMEGA_M=0.315
OMEGA_L=1.0-OMEGA_R-OMEGA_M


def load_rational_table(path='results/passive_table_N24.json'):
    d=json.loads(Path(path).read_text())
    return (np.asarray(d['h_anchors'],float),
            np.asarray(d['q_nodes'],float),
            np.asarray(d['weights'],float))


def interp_weights(h,anchors,W):
    h=float(h)
    if h<=anchors[0]: return W[0].copy()
    if h>=anchors[-1]: return W[-1].copy()
    j=np.searchsorted(anchors,h)-1
    la=np.log(anchors)
    t=(np.log(h)-la[j])/(la[j+1]-la[j])
    return (1.0-t)*W[j]+t*W[j+1]


def h_lcdm(a):
    a=np.asarray(a,float)
    return np.sqrt(OMEGA_R/a**4+OMEGA_M/a**3+OMEGA_L)


def find_a_for_h(target):
    lo,hi=1e-10,1.0
    for _ in range(200):
        mid=np.sqrt(lo*hi)
        if h_lcdm(mid)>target: lo=mid
        else: hi=mid
    return np.sqrt(lo*hi)


def history(kind='lcdm',nsteps=1800,hstart=1000.0,hend=1.0):
    if kind=='lcdm':
        a0=find_a_for_h(hstart)
        a1=find_a_for_h(hend)
        N=np.linspace(np.log(a0),np.log(a1),nsteps+1)
        h=h_lcdm(np.exp(N))
    elif kind in ('radiation','matter'):
        p=2.0 if kind=='radiation' else 1.5
        L=np.log(hstart/hend)/p
        N=np.linspace(0.0,L,nsteps+1)
        h=hstart*np.exp(-p*N)
    else:
        raise ValueError(kind)
    return N,np.asarray(h,float)


def smooth_drive(N,nu):
    N=np.asarray(N,float)
    u=(N-N[0])/(N[-1]-N[0])
    ramp=np.ones_like(u)
    mask=u<0.10
    ramp[mask]=np.sin(0.5*np.pi*u[mask]/0.10)**2
    return ramp*np.sin(float(nu)*(N-N[0]))


def gaussian_drive(N):
    N=np.asarray(N,float)
    u=(N-N[0])/(N[-1]-N[0])
    return np.exp(-0.5*((u-0.52)/0.11)**2)


def reference_nodes(N=1024,wmin=1e-7,wmax=1e7):
    edges=np.linspace(np.log(wmin),np.log(wmax),N+1)
    mid=0.5*(edges[:-1]+edges[1:])
    omega=np.exp(mid)
    dlog=edges[1]-edges[0]
    domega=omega*dlog
    weights=(2.0/np.pi)*domega/(1.0+omega*omega)
    return omega,weights


def _step_modes(q,v,omega,h,x,dt):
    # Exact update for Q''+3h Q'+omega^2 Q=omega^2 x with h,x frozen
    damp=1.5*h
    u=q-x
    disc=omega*omega-damp*damp
    decay=np.exp(-damp*dt)
    un=np.empty_like(u);vn=np.empty_like(v)
    under=disc>1e-14
    if np.any(under):
        Om=np.sqrt(disc[under]);C=np.cos(Om*dt);S=np.sin(Om*dt)
        uu=u[under];vv=v[under];ww=omega[under]
        un[under]=decay*(uu*C+(vv+damp*uu)/Om*S)
        vn[under]=decay*(vv*C-(damp*vv+ww*ww*uu)/Om*S)
    over=disc<-1e-14
    if np.any(over):
        d=np.sqrt(-disc[over]);C=np.cosh(d*dt);S=np.sinh(d*dt)
        uu=u[over];vv=v[over];ww=omega[over]
        un[over]=decay*(uu*C+(vv+damp*uu)/d*S)
        vn[over]=decay*(vv*C-(damp*vv+ww*ww*uu)/d*S)
    crit=~(under|over)
    if np.any(crit):
        uu=u[crit];vv=v[crit];ww=omega[crit]
        un[crit]=decay*(uu+(vv+damp*uu)*dt)
        vn[crit]=decay*(vv-(damp*vv+ww*ww*uu)*dt)
    return un+x,vn


def simulate_fixed_modes(Ngrid,hgrid,xgrid,omega):
    q=np.zeros(len(omega));v=np.zeros(len(omega))
    out=np.empty((len(Ngrid),len(omega)))
    out[0]=xgrid[0]-q
    for i in range(len(Ngrid)-1):
        Nm=0.5*(Ngrid[i]+Ngrid[i+1])
        hm=np.sqrt(hgrid[i]*hgrid[i+1])
        dt=(Ngrid[i+1]-Ngrid[i])/hm
        xm=0.5*(xgrid[i]+xgrid[i+1])
        q,v=_step_modes(q,v,omega,hm,xm,dt)
        out[i+1]=xgrid[i+1]-q
    return out


def simulate_reference(Ngrid,hgrid,xgrid,Nref=1024):
    omega,w=reference_nodes(Nref)
    B=simulate_fixed_modes(Ngrid,hgrid,xgrid,omega)
    return B@w


def simulate_rational(Ngrid,hgrid,xgrid,anchors,qnodes,W):
    m=np.zeros(len(qnodes))
    out=np.empty(len(Ngrid))
    out[0]=np.dot(interp_weights(hgrid[0],anchors,W),xgrid[0]-m)
    for i in range(len(Ngrid)-1):
        hm=np.sqrt(hgrid[i]*hgrid[i+1])
        dt=(Ngrid[i+1]-Ngrid[i])/hm
        xm=0.5*(xgrid[i]+xgrid[i+1])
        r=hm*qnodes
        er=np.exp(-r*dt)
        m=xm+(m-xm)*er
        out[i+1]=np.dot(interp_weights(hgrid[i+1],anchors,W),xgrid[i+1]-m)
    return out


def waveform_metrics(test,ref,discard_fraction=0.10):
    n=len(ref);i0=max(1,int(discard_fraction*n))
    a=np.asarray(test[i0:],float);b=np.asarray(ref[i0:],float)
    nr=np.linalg.norm(b);nt=np.linalg.norm(a)
    l2=float(np.linalg.norm(a-b)/max(nr,1e-300))
    cos=float(np.dot(a,b)/max(nt*nr,1e-300))
    peak=float(np.max(np.abs(a-b))/max(np.max(np.abs(b)),1e-300))
    return {'relative_L2':l2,'cosine':cos,'peak_normalized_error':peak,
            'reference_rms':float(np.sqrt(np.mean(b*b)))}
