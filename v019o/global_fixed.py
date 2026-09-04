import numpy as np
from scipy.optimize import nnls


def retarded_A(z,h):
    z=np.asarray(z,dtype=complex)
    A=np.sqrt(z*(z+3.0*h)+0j)
    A=np.where(A.real<0,-A,A)
    return A


def exact_kernel(z,h):
    A=retarded_A(z,h)
    return A/(1.0+A)


def oscillator_basis(z,h,omega):
    A=retarded_A(z,h)
    A2=A*A
    om=np.asarray(omega,float)
    return A2[:,None]/(A2[:,None]+om[None,:]**2)


def candidate_nodes(N,wmin=1e-9,wmax=1e9):
    return np.logspace(np.log10(wmin),np.log10(wmax),N)


def build_complex_samples(hvals,nuvals,epsvals):
    zs=[];hs=[];targets=[]
    for h in hvals:
        for nu in nuvals:
            for eps in epsvals:
                z=h*(eps+1j*nu)
                zs.append(z);hs.append(h);targets.append(exact_kernel(np.array([z]),h)[0])
    return np.asarray(zs,complex),np.asarray(hs,float),np.asarray(targets,complex)


def fit_positive(hvals,nuvals,epsvals,N,wmin=1e-9,wmax=1e9,sum_constraint_weight=30.0):
    omega=candidate_nodes(N,wmin,wmax)
    z,h,K=build_complex_samples(hvals,nuvals,epsvals)
    blocks=[]
    for zi,hi in zip(z,h):
        blocks.append(oscillator_basis(np.array([zi]),hi,omega)[0])
    B=np.asarray(blocks,complex)
    scale=np.maximum(np.abs(K),1e-12)
    M=np.vstack([B.real/scale[:,None],B.imag/scale[:,None]])
    y=np.r_[K.real/scale,K.imag/scale]
    # High-frequency exact limit K -> 1 requires sum_j w_j = 1.
    # Enforce it softly but strongly while retaining non-negative least squares.
    M=np.vstack([M,sum_constraint_weight*np.ones((1,N))])
    y=np.r_[y,sum_constraint_weight]
    w,_=nnls(M,y,maxiter=500*N)
    pred=B@w
    rel=np.abs(pred-K)/scale
    return omega,w,rel


def evaluate(omega,w,hvals,nuvals,epsvals):
    z,h,K=build_complex_samples(hvals,nuvals,epsvals)
    rows=[]
    for zi,hi in zip(z,h):
        rows.append(oscillator_basis(np.array([zi]),hi,omega)[0])
    pred=np.asarray(rows)@np.asarray(w)
    rel=np.abs(pred-K)/np.maximum(np.abs(K),1e-12)
    return rel


def metrics(rel):
    rel=np.asarray(rel,float)
    return {
      'median':float(np.median(rel)),
      'p95':float(np.quantile(rel,.95)),
      'p99':float(np.quantile(rel,.99)),
      'max':float(np.max(rel)),
    }
