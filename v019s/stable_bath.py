#!/usr/bin/env python3
import numpy as np
from scipy.special import roots_legendre


def waveform_metrics(test,ref,discard_fraction=.03):
    n=len(ref);i0=max(1,int(discard_fraction*n))
    a=np.asarray(test[i0:],float);b=np.asarray(ref[i0:],float)
    nr=np.linalg.norm(b);nt=np.linalg.norm(a)
    l2=float(np.linalg.norm(a-b)/max(nr,1e-300))
    cos=float(np.dot(a,b)/max(nt*nr,1e-300))
    peak=float(np.max(np.abs(a-b))/max(np.max(np.abs(b)),1e-300))
    return {'relative_L2':l2,'cosine':cos,'peak_normalized_error':peak,
            'reference_rms':float(np.sqrt(np.mean(b*b)))}


def tan_gl_nodes(n):
    z,w=roots_legendre(int(n))
    theta=0.25*np.pi*(z+1.0)
    omega=np.tan(theta)
    weights=0.5*w
    return np.asarray(omega,float),np.asarray(weights,float)


def _step_linear(q,v,omega,h,x0,x1,dt):
    # q'' + 3 h q' + omega^2 q = omega^2 x(t), with frozen h and
    # a linearly varying drive x(t). Derivatives are in t/tau units.
    c=3.0*h
    d=0.5*c
    r=(x1-x0)/dt
    u0=q-x0
    vu0=v-r
    force=-c*r
    om2=omega*omega
    disc=om2-d*d
    scale=np.maximum(om2+d*d,1.0)
    under=disc>1.e-12*scale
    over=disc<-1.e-12*scale
    crit=~(under|over)
    un=np.empty_like(q)
    vn=np.empty_like(v)

    if np.any(under):
        O=np.sqrt(disc[under])
        z=O*dt
        ed=np.exp(-d*dt)
        C=np.cos(z);S=np.sin(z)
        uu=u0[under];vv=vu0[under];oo2=om2[under]
        hu=ed*(uu*C+(vv+d*uu)/O*S)
        hv=ed*(vv*C-(d*vv+oo2*uu)/O*S)
        one=1.0-ed*(C+d/O*S)
        G=ed*S/O
        un[under]=hu+force/oo2*one
        vn[under]=hv+force*G

    if np.any(over):
        oo2=om2[over]
        delta=np.sqrt(-disc[over])
        # Slow root in cancellation-safe form.
        lam1=-oo2/(d+delta)
        lam2=-d-delta
        den=lam1-lam2
        e1=np.exp(lam1*dt);e2=np.exp(lam2*dt)
        uu=u0[over];vv=vu0[over]
        c1=(vv-lam2*uu)/den
        c2=(lam1*uu-vv)/den
        hu=c1*e1+c2*e2
        hv=lam1*c1*e1+lam2*c2*e2
        one=(-lam2*(-np.expm1(lam1*dt))+lam1*(-np.expm1(lam2*dt)))/den
        G=(e1-e2)/den
        un[over]=hu+force/oo2*one
        vn[over]=hv+force*G

    if np.any(crit):
        oo2=om2[crit]
        z=d*dt
        ed=np.exp(-z)
        uu=u0[crit];vv=vu0[crit]
        hu=ed*(uu+(vv+d*uu)*dt)
        hv=ed*(vv-(d*vv+oo2*uu)*dt)
        one=-np.expm1(-z)-z*ed
        G=ed*dt
        un[crit]=hu+force/oo2*one
        vn[crit]=hv+force*G

    return x1+un,vn+r


def simulate_modes(Ngrid,hgrid,xgrid,omega):
    omega=np.asarray(omega,float)
    q=np.zeros(len(omega));v=np.zeros(len(omega))
    out=np.empty((len(Ngrid),len(omega)))
    out[0]=xgrid[0]-q
    for i in range(len(Ngrid)-1):
        hm=np.sqrt(hgrid[i]*hgrid[i+1])
        dt=(Ngrid[i+1]-Ngrid[i])/hm
        q,v=_step_linear(q,v,omega,hm,xgrid[i],xgrid[i+1],dt)
        out[i+1]=xgrid[i+1]-q
    return out


def simulate_quadrature(Ngrid,hgrid,xgrid,n):
    omega,weights=tan_gl_nodes(int(n))
    return simulate_modes(Ngrid,hgrid,xgrid,omega)@weights
